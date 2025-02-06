#!/usr/bin/env python3
import os
import argparse
import configparser
import fnmatch

CBATCH_CONFIG_FILE = "cbatch.ini"
CBATCH_IGNORE_FILE = ".cbatchignore"
DEFAULT_OUTPUT_FILE = "codebatch.md"

DEFAULT_IGNORE_PATTERNS = [
    "codebatch.md",
    ".gitignore",
    ".git/",
    "*.lock",
    ".env",
    ".env.*",
    CBATCH_CONFIG_FILE,
    CBATCH_IGNORE_FILE,
    "*.pyc",
    "__pycache__/",
    "*.swp",  # Swap files (e.g., Vim)
    ".DS_Store",  # macOS specific
    "node_modules/",  # Node.js
    "venv/",  # Python virtual environments
    "env/",  # Python virtual environments
    "*.log",  # Log files
    "data/",  # Common data directories
    "temp/",  # Common temporary directories
    "tmp/",  # Common temporary directories
    "build/",  # Build directories
    "dist/",  # Distribution packages
    "dist-*/",  # Distribution variations
    ##
    # Certs, keys, dbs, and other sensitive files
    ##
    "*.pem",
    "*.key",
    "*.csr",
    "*.crt",
    "*.cer",
    "*.pfx",
    "*.p12",
    "*.sqlite",
    "*.db",
    "*.log",
    ##
    # Framework-specific build/cache directories
    ##
    ".svelte-kit/",  # SvelteKit
    ".next/",  # Next.js
    ".nuxt/",  # Nuxt.js
    ".output/",  # Nuxt.js output
    ".vitepress/",  # VitePress
    ".astro/",  # Astro
    ".cache/",  # Gatsby, general cache
    "out/",  # Next.js, general output
    ".angular/",  # Angular
    ".remix/",  # Remix
    ##
    # Bundler/Build tool outputs
    ##
    ".parcel-cache/",  # Parcel
    ".webpack/",  # Webpack
    ".rollup.cache/",  # Rollup
    ".turbo/",  # Turborepo
    ".yarn/",  # Yarn
    "yarn-error.log",  # Yarn errors
    ".pnpm-store/",  # pnpm
    ##
    # IDE and Editor files
    ##
    ".idea/",  # JetBrains IDEs
    ".vscode/",  # VS Code
    "*.sublime-*",  # Sublime Text
    ".settings/",  # Eclipse
    ".project",  # Eclipse
    ".classpath",  # Eclipse
    "*.iml",  # IntelliJ IDEA modules
]


def read_config(config_file=CBATCH_CONFIG_FILE):
    """
    Reads configuration from cbatch.ini file.

    Returns:
        configparser.ConfigParser: ConfigParser object, or None if file not found.
    """
    config = configparser.ConfigParser()
    if os.path.exists(config_file):
        config.read(config_file)
        return config
    return None


def write_config(config, config_file=CBATCH_CONFIG_FILE):
    """
    Writes configuration to cbatch.ini file.

    Args:
        config (configparser.ConfigParser): ConfigParser object to write.
        config_file (str): Path to the config file.
    """
    with open(config_file, "w") as f:
        config.write(f)


def create_default_ignore_file(
    ignore_file=CBATCH_IGNORE_FILE, patterns=DEFAULT_IGNORE_PATTERNS
):
    """
    Creates .cbatchignore file with default ignore patterns if it doesn't exist.

    Args:
        ignore_file (str): Path to the ignore file.
        patterns (list): List of default ignore patterns.
    """
    if not os.path.exists(ignore_file):
        with open(ignore_file, "w") as f:
            f.write("# Default ignore patterns for cbatch\n")
            for pattern in patterns:
                f.write(f"{pattern}\n")
        print(f"Created default ignore file: {ignore_file}")
    else:
        print(f"Ignore file already exists: {ignore_file}. Keeping existing file.")


def init_config():
    """
    Initializes cbatch.ini and .cbatchignore files through an interactive wizard.
    """
    print("Initializing cbatch configuration...")

    config = configparser.ConfigParser()
    config["General"] = {}  # Initialize General section
    config["Summary"] = {}  # Initialize Summary section - will be updated later

    set_general_info_prompt = input(
        "Would you like to set general project information to assist AI? (optional) (y/N): "
    )
    set_general_info = set_general_info_prompt.lower() in ("y", "yes")

    if set_general_info:
        codebase_type = (
            input("Enter Codebase Type (e.g., FastAPI backend, React frontend): ") or ""
        )
        deployment_location = (
            input("Enter Deployment Location (e.g., Vercel, AWS): ") or ""
        )
        general_description = (
            input("Enter General Description (e.g., AI Chatbot backend): ") or ""
        )
        execution_command = (
            input("Enter Execution Command (e.g., npm run dev, uvicorn ...): ") or ""
        )
    else:
        print("Skipping general project information setup.")
        codebase_type = ""
        deployment_location = ""
        general_description = ""
        execution_command = ""

    config["General"]["codebase_type"] = codebase_type
    config["General"]["deployment_location"] = deployment_location
    config["General"]["general_description"] = general_description
    config["General"]["execution_command"] = execution_command
    write_config(config)
    print(f"Configuration saved to {CBATCH_CONFIG_FILE}")
    # Create default .cbatchignore if it doesn't exist
    create_default_ignore_file()


def read_gitignore_patterns(ignore_file=CBATCH_IGNORE_FILE):
    """
    Reads ignore patterns from .cbatchignore file.

    Returns:
        list: List of ignore patterns, or empty list if file not found.
    """
    patterns = []
    if os.path.exists(ignore_file):
        with open(ignore_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):  # Ignore empty lines and comments
                    patterns.append(line)
    return patterns


def is_file_ignored(file_path, ignore_patterns):
    """
    Checks if a file path is ignored based on the provided patterns.
    Handles both file and directory patterns.

    Args:
        file_path (str): Path to the file.
        ignore_patterns (list): List of ignore patterns.

    Returns:
        bool: True if the file is ignored, False otherwise.
    """
    for pattern in ignore_patterns:
        # Handle directory patterns (ending with /)
        if pattern.endswith("/"):
            # Remove trailing slash for matching
            dir_pattern = pattern[:-1]
            # Check if this directory pattern appears anywhere in the path
            path_parts = file_path.split(os.sep)
            if any(fnmatch.fnmatch(part, dir_pattern) for part in path_parts):
                return True
        # Handle regular file patterns
        elif fnmatch.fnmatch(file_path, pattern):
            return True
    return False


def estimate_tokens(text):
    """
    Estimates the number of input tokens for a given text (simple word count approximation).

    Args:
        text (str): The text content.

    Returns:
        int: Estimated number of tokens.
    """
    words = text.split()
    return len(words)  # Simple word count as token estimate


def output_codebase_to_structured_file(
    codebase_path, output_file, general_info, ignore_patterns
):
    """
    Outputs the codebase content to a structured file in Markdown format and updates token estimate in config.

    Args:
        codebase_path (str): Path to the root directory of the codebase.
        output_file (str): Path to the output file (.md).
        general_info (dict): Dictionary containing general info about the codebase.
        ignore_patterns (list): List of file ignore patterns.
    """

    output_content = ""  # Accumulate content in memory first for token estimation

    # Instructions Section
    output_content += "# Instructions #\n\n"
    output_content += "This file represents the entire codebase I am working on, it is structured in markdown syntax for readability and to explore codes and my routes relatively easily.\n\n"

    # General Info Section
    output_content += "## General Info ##\n\n"
    for key, value in general_info.items():
        output_content += f"**{key.replace('_', ' ').title()}**: {value}\n"
    output_content += "\n"

    # Files Section
    output_content += "## Files ##\n\n"

    for root, _, files in os.walk(codebase_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, codebase_path)

            if is_file_ignored(relative_path, ignore_patterns):
                continue

            try:
                with open(file_path, "r") as infile:
                    content = infile.read()
                    output_content += f"### `{relative_path}` ###\n"
                    output_content += "```\n"
                    output_content += content
                    output_content += "\n```\n\n"
            except Exception as e:
                print(f"Error reading file: {file_path} - {e}")

    try:
        with open(output_file, "w") as outfile:
            outfile.write(output_content)  # Write accumulated content to file

        token_estimate = estimate_tokens(output_content)

        config = read_config()  # Read existing config
        if config:
            config["Summary"]["input_token_estimate"] = str(
                token_estimate
            )  # Update token estimate
            write_config(config)  # Write back updated config
            print(f"Codebase structured output written to: {output_file}")
            print(
                f"Estimated input tokens: {token_estimate} (updated in {CBATCH_CONFIG_FILE})"
            )
        else:
            print(f"Codebase structured output written to: {output_file}")
            print(f"Estimated input tokens: {token_estimate}")
            print(
                f"Warning: Could not update {CBATCH_CONFIG_FILE} - run 'cbatch init' first if you want to track token estimates."
            )

    except Exception as e:
        print(f"An error occurred: {e}")


def tokens_command():
    """
    Displays the input token estimate from cbatch.ini.
    """
    config = read_config()
    if config and "Summary" in config and "input_token_estimate" in config["Summary"]:
        token_estimate = config["Summary"]["input_token_estimate"]
        print(f"Estimated input tokens (from {CBATCH_CONFIG_FILE}): {token_estimate}")
    else:
        print(
            f"Token estimate not found in {CBATCH_CONFIG_FILE}. Run 'cbatch update' first to generate the output and estimate tokens."
        )


def main():  # Define the main function
    parser = argparse.ArgumentParser(
        description="Codebatcher (cbatch) - CLI tool to output codebase to structured file for AI context."
    )
    subparsers = parser.add_subparsers(
        title="commands", dest="command", help="Available commands"
    )

    # 'init' command
    init_parser = subparsers.add_parser(
        "init", help="Initialize cbatch configuration (cbatch.ini and .cbatchignore)"
    )

    # 'update' command
    update_parser = subparsers.add_parser(
        "update", help="Update codebase output file and token estimate"
    )
    update_parser.add_argument(
        "codebase_path",
        nargs="?",
        default=".",
        help="Path to the root directory of your codebase (default: current directory).",
    )
    update_parser.add_argument(
        "output_file",
        nargs="?",
        default=DEFAULT_OUTPUT_FILE,
        help=f"Path to the output structured file (default: {DEFAULT_OUTPUT_FILE} in current directory).",
    )

    # 'tokens' command
    tokens_parser = subparsers.add_parser(
        "tokens", help="Check estimated input tokens from cbatch.ini"
    )

    args = parser.parse_args()

    if args.command == "init":
        init_config()
    elif args.command == "update":
        config = read_config()  # Read config to get general info
        if not config or "General" not in config:
            print(
                f"Error: {CBATCH_CONFIG_FILE} not found or [General] section is missing. Run 'cbatch init' to set up configuration."
            )
        else:
            general_info = dict(config["General"])  # Extract General section as dict
            ignore_patterns = read_gitignore_patterns()
            output_codebase_to_structured_file(
                args.codebase_path, args.output_file, general_info, ignore_patterns
            )
    elif args.command == "tokens":
        tokens_command()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()  # Call the main function when cbatch.py is run directly or via 'cbatch' command
