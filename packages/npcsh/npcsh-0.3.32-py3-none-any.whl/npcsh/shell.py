import os
import sys
import readline
import atexit
import re
import pty
import select
import termios
import tty
import shlex
import json

from datetime import datetime
from inspect import isgenerator


# Third-party imports
import pandas as pd
import sqlite3
import numpy as np
from termcolor import colored
from dotenv import load_dotenv
import subprocess
from typing import Dict, Any, List, Optional


try:
    from sentence_transformers import SentenceTransformer
except:
    print("Could not load the sentence-transformers package.")
# Local imports

from npcsh.npc_sysenv import (
    get_system_message,
    lookup_provider,
    NPCSH_STREAM_OUTPUT,
    NPCSH_CHAT_MODEL,
    NPCSH_CHAT_PROVIDER,
    NPCSH_API_URL,
)

from npcsh.command_history import (
    CommandHistory,
    start_new_conversation,
    save_conversation_message,
    save_attachment_to_message,
)
from npcsh.llm_funcs import (
    execute_llm_command,
    execute_llm_question,
    generate_image,
    check_llm_command,
    get_conversation,
    get_system_message,
)
from npcsh.search import rag_search, search_web
from npcsh.helpers import (
    load_all_files,
    setup_npcsh_config,
    is_npcsh_initialized,
    initialize_base_npcs_if_needed,
)
from npcsh.shell_helpers import (
    complete,  # For command completion
    readline_safe_prompt,
    get_multiline_input,
    setup_readline,
    execute_command,
    render_markdown,
    render_code_block,
    orange,  # For colored prompt
)
from npcsh.npc_compiler import (
    NPCCompiler,
    load_tools_from_directory,
    NPC,
    initialize_npc_project,
)

import argparse
from npcsh.serve import (
    start_flask_server,
)
import importlib.metadata  # Python 3.8+

# Fetch the version from the package metadata
try:
    VERSION = importlib.metadata.version(
        "npcsh"
    )  # Replace "npcsh" with your package name
except importlib.metadata.PackageNotFoundError:
    VERSION = "unknown"  # Fallback if the package is not installed


def main() -> None:
    """
    Main function for the npcsh shell and server.
    Starts either the Flask server or the interactive shell based on the argument provided.
    """
    # Set up argument parsing to handle 'serve' and regular commands

    check_old_par_name = os.environ.get("NPCSH_MODEL", None)
    if check_old_par_name is not None:
        # raise a deprecation warning
        print(
            """Deprecation Warning: NPCSH_MODEL and NPCSH_PROVIDER were deprecated in v0.3.5 in favor of NPCSH_CHAT_MODEL and NPCSH_CHAT_PROVIDER instead.\
                Please update your environment variables to use the new names.
                """
        )

    parser = argparse.ArgumentParser(description="npcsh CLI")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"npcsh version {VERSION}",  # Use the dynamically fetched version
    )
    args = parser.parse_args()

    setup_npcsh_config()
    if "NPCSH_DB_PATH" in os.environ:
        db_path = os.path.expanduser(os.environ["NPCSH_DB_PATH"])
    else:
        db_path = os.path.expanduser("~/npcsh_history.db")

    command_history = CommandHistory(db_path)
    valid_commands = [
        "/compile",
        "/com",
        "/whisper",
        "/notes",
        "/data",
        "/cmd",
        "/command",
        "/set",
        "/sample",
        "/spool",
        "/sp",
        "/help",
        "/exit",
        "/quit",
    ]

    readline.set_completer_delims(" \t\n")
    readline.set_completer(complete)
    if sys.platform == "darwin":
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")

    # check if ./npc_team exists
    if os.path.exists("./npc_team"):

        npc_directory = os.path.abspath("./npc_team/")
    else:
        npc_directory = os.path.expanduser("~/.npcsh/npc_team/")

    npc_compiler = NPCCompiler(npc_directory, db_path)

    os.makedirs(npc_directory, exist_ok=True)

    # Compile all NPCs in the user's npc_team directory
    for filename in os.listdir(npc_directory):
        if filename.endswith(".npc"):
            npc_file_path = os.path.join(npc_directory, filename)
            npc_compiler.compile(npc_file_path)

    # Compile NPCs from project-specific npc_team directory
    if os.path.exists(npc_directory):
        for filename in os.listdir(npc_directory):
            if filename.endswith(".npc"):
                npc_file_path = os.path.join(npc_directory, filename)
                npc_compiler.compile(npc_file_path)

    if not is_npcsh_initialized():
        print("Initializing NPCSH...")
        initialize_base_npcs_if_needed(db_path)
        print(
            "NPCSH initialization complete. Please restart your terminal or run 'source ~/.npcshrc' for the changes to take effect."
        )

    history_file = setup_readline()
    atexit.register(readline.write_history_file, history_file)
    atexit.register(command_history.close)
    # make npcsh into ascii art
    from colorama import init

    init()  # Initialize colorama for ANSI code support
    if sys.stdin.isatty():

        print(
            """
    Welcome to \033[1;94mnpc\033[0m\033[1;38;5;202msh\033[0m!
    \033[1;94m                    \033[0m\033[1;38;5;202m               \\\\
    \033[1;94m _ __   _ __    ___ \033[0m\033[1;38;5;202m ___  | |___    \\\\
    \033[1;94m| '_ \ | '_ \  / __|\033[0m\033[1;38;5;202m/ __/ | |_ _|    \\\\
    \033[1;94m| | | || |_) |( |__ \033[0m\033[1;38;5;202m\_  \ | | | |    //
    \033[1;94m|_| |_|| .__/  \___|\033[0m\033[1;38;5;202m|___/ |_| |_|   //
            \033[1;94m| |          \033[0m\033[1;38;5;202m              //
            \033[1;94m| |
            \033[1;94m|_|

    Begin by asking a question, issuing a bash command, or typing '/help' for more information.
            """
        )

    current_npc = None
    messages = None
    current_conversation_id = start_new_conversation()

    # --- Minimal Piped Input Handling ---
    if not sys.stdin.isatty():
        for line in sys.stdin:
            user_input = line.strip()
            if not user_input:
                continue  # Skip empty lines
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                sys.exit(0)
            result = execute_command(
                user_input,
                db_path,
                npc_compiler,
                current_npc,
                model=NPCSH_CHAT_MODEL,
                provider=NPCSH_CHAT_PROVIDER,
                messages=messages,
                conversation_id=current_conversation_id,
                stream=NPCSH_STREAM_OUTPUT,
                api_url=NPCSH_API_URL,
            )
            messages = result.get("messages", messages)
            if "current_npc" in result:
                current_npc = result["current_npc"]
            output = result.get("output")
            conversation_id = result.get("conversation_id")
            model = result.get("model")
            provider = result.get("provider")
            npc = result.get("npc")
            messages = result.get("messages")
            current_path = result.get("current_path")
            attachments = result.get("attachments")
            npc_name = (
                npc.name
                if isinstance(npc, NPC)
                else npc if isinstance(npc, str) else None
            )

            save_conversation_message(
                command_history,
                conversation_id,
                "user",
                user_input,
                wd=current_path,
                model=model,
                provider=provider,
                npc=npc_name,
                attachments=attachments,
            )
            if NPCSH_STREAM_OUTPUT and (
                isgenerator(output)
                or (hasattr(output, "__iter__") and hasattr(output, "__next__"))
            ):
                str_output = ""
                in_code = False
                code_buffer = ""
                text_buffer = ""

                for chunk in output:
                    # Get chunk content based on provider
                    if provider == "anthropic":
                        chunk_content = (
                            chunk.delta.text
                            if chunk.type == "content_block_delta"
                            else None
                        )
                    elif provider in ["openai", "deepseek", "openai-like"]:
                        chunk_content = "".join(
                            c.delta.content for c in chunk.choices if c.delta.content
                        )
                    elif provider == "ollama":
                        chunk_content = chunk["message"]["content"]
                    else:
                        continue

                    if not chunk_content:
                        continue

                    str_output += chunk_content

                    # Process chunk
                    if "```" in chunk_content:
                        parts = chunk_content.split("```")

                        for i, part in enumerate(parts):
                            if i == 0:  # First part (before any backticks)
                                if in_code:
                                    code_buffer += part
                                else:
                                    print(part, end="")
                            elif i % 2 == 1:  # Inside a code block
                                if not in_code:  # Starting a new code block
                                    in_code = True
                                    code_buffer = part
                                else:  # Shouldn't happen but handle anyway
                                    code_buffer += part
                            else:  # Outside a code block
                                if in_code:  # Just finished a code block
                                    in_code = False
                                    # Render the code block
                                    render_code_block(code_buffer)
                                    code_buffer = ""
                                print(part, end="")
                    else:
                        if in_code:
                            code_buffer += chunk_content
                        else:
                            print(chunk_content, end="")

                # Handle any remaining code buffer
                if in_code and code_buffer:
                    render_code_block(code_buffer)

                if str_output:
                    output = str_output
        save_conversation_message(
            command_history,
            conversation_id,
            "assistant",
            output,
            wd=current_path,
            model=model,
            provider=provider,
            npc=npc_name,
        )
        sys.exit(0)

    while True:
        try:
            if current_npc:
                prompt = f"{colored(os.getcwd(), 'blue')}:{orange(current_npc.name)}> "
            else:
                prompt = f"{colored(os.getcwd(), 'blue')}:\033[1;94mnpc\033[0m\033[1;38;5;202msh\033[0m!> "

            prompt = readline_safe_prompt(prompt)
            user_input = get_multiline_input(prompt).strip()

            if user_input.lower() in ["exit", "quit"]:
                if current_npc:
                    print(f"Exiting {current_npc.name} mode.")
                    current_npc = None
                    continue
                else:
                    print("Goodbye!")
                    break
            # print(current_npc, "current npc fore command execution")
            # Execute the command and capture the result
            result = execute_command(
                user_input,
                db_path,
                npc_compiler,
                current_npc=current_npc,
                model=NPCSH_CHAT_MODEL,
                provider=NPCSH_CHAT_PROVIDER,
                messages=messages,
                conversation_id=current_conversation_id,
                stream=NPCSH_STREAM_OUTPUT,
                api_url=NPCSH_API_URL,
            )

            messages = result.get("messages", messages)

            # need to adjust the output for the messages to all have
            # model, provider, npc, timestamp, role, content
            # also messages

            if "current_npc" in result:

                current_npc = result["current_npc"]
            output = result.get("output")

            conversation_id = result.get("conversation_id")
            model = result.get("model")
            provider = result.get("provider")

            messages = result.get("messages")
            current_path = result.get("current_path")
            attachments = result.get("attachments")

            if current_npc is not None:
                if isinstance(current_npc, NPC):
                    npc_name = current_npc.name
                elif isinstance(current_npc, str):
                    npc_name = current_npc
            else:
                npc_name = None
            message_id = save_conversation_message(
                command_history,
                conversation_id,
                "user",
                user_input,
                wd=current_path,
                model=model,
                provider=provider,
                npc=npc_name,
                attachments=attachments,
            )

            str_output = ""
            try:
                if NPCSH_STREAM_OUTPUT and hasattr(output, "__iter__"):

                    buffer = ""
                    in_code = False
                    code_buffer = ""

                    for chunk in output:

                        chunk_content = "".join(
                            c.delta.content for c in chunk.choices if c.delta.content
                        )
                        if not chunk_content:
                            continue

                        str_output += chunk_content
                        # print(str_output, "str_output")
                        # Process the content character by character
                        for char in chunk_content:
                            buffer += char

                            # Check for triple backticks
                            if buffer.endswith("```"):
                                if not in_code:
                                    # Start of code block
                                    in_code = True
                                    # Print everything before the backticks
                                    print(buffer[:-3], end="")
                                    buffer = ""
                                    code_buffer = ""
                                else:
                                    # End of code block
                                    in_code = False
                                    # Remove the backticks from the end of the buffer
                                    buffer = buffer[:-3]
                                    # Add buffer to code content and render
                                    code_buffer += buffer

                                    # Check for and strip language tag
                                    if (
                                        "\n" in code_buffer
                                        and code_buffer.index("\n") < 15
                                    ):
                                        first_line, rest = code_buffer.split("\n", 1)
                                        if (
                                            first_line.strip()
                                            and not "```" in first_line
                                        ):
                                            code_buffer = rest

                                    # Render the code block
                                    render_code_block(code_buffer)

                                    # Reset buffers
                                    buffer = ""
                                    code_buffer = ""
                            elif in_code:
                                # Just add to code buffer
                                code_buffer += char
                                if len(buffer) >= 3:  # Keep buffer small while in code
                                    buffer = buffer[-3:]
                            else:
                                # Regular text - print if buffer gets too large
                                if len(buffer) > 100:
                                    print(buffer[:-3], end="")
                                    buffer = buffer[
                                        -3:
                                    ]  # Keep last 3 chars to check for backticks

                    # Handle any remaining content
                    if in_code:
                        render_code_block(code_buffer)
                    else:
                        print(buffer, end="")

                    if str_output:
                        output = str_output
            except:
                output = None

            print("\n")

            if isinstance(output, str):
                save_conversation_message(
                    command_history,
                    conversation_id,
                    "assistant",
                    output,
                    wd=current_path,
                    model=model,
                    provider=provider,
                    npc=npc_name,
                )

            # if there are attachments in most recent user sent message, save them
            # save_attachment_to_message(command_history, message_id, # file_path, attachment_name, attachment_type)

            if (
                result["output"] is not None
                and not user_input.startswith("/")
                and not isinstance(result, dict)
            ):
                print("final", result)

        except (KeyboardInterrupt, EOFError):
            if current_npc:
                print(f"\nExiting {current_npc.name} mode.")
                current_npc = None
            else:
                print("\nGoodbye!")
                break


if __name__ == "__main__":
    main()
