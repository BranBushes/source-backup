import argparse
import os
import shutil
from pathlib import Path

def is_binary(file_path):
    """
    Checks if a file is likely binary by reading a chunk and looking for null bytes.
    """
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            return b'\x00' in chunk
    except IOError:
        return True

def create_markdown_backup(source_dir, output_file, exclude_patterns):
    """
    Creates a backup with a directory structure overview followed by file contents.

    Args:
        source_dir (str): The path to the source directory to back up.
        output_file (str): The path to the output Markdown file.
        exclude_patterns (list): A list of glob patterns to exclude.
    """
    source_path = Path(source_dir).resolve()
    output_path = Path(output_file).resolve()

    if not source_path.is_dir():
        print(f"Error: Source directory '{source_dir}' not found.")
        return

    temp_dir = output_path.parent / "temp_backup_dir"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)

    try:
        # Create a temporary, clean copy of the source directory
        shutil.copytree(
            source_path,
            temp_dir,
            ignore=shutil.ignore_patterns(*exclude_patterns) if exclude_patterns else None,
            dirs_exist_ok=True
        )

        structure_lines = []
        file_paths_to_process = []

        # First pass: Build the directory structure and collect file paths
        for root, dirs, files in os.walk(temp_dir):
            current_dir = Path(root)
            relative_dir = current_dir.relative_to(temp_dir)
            depth = len(relative_dir.parts)

            # Indent based on directory depth
            indent = "    " * depth

            if str(relative_dir) != ".":
                structure_lines.append(f"{indent}- {relative_dir.name}/")
                indent += "    "

            # Sort directories and files for consistent ordering
            dirs.sort()
            files.sort()

            for file in files:
                relative_file_path = relative_dir / file
                structure_lines.append(f"{indent}- {file}")
                file_paths_to_process.append(current_dir / file)

        # Second pass: Write everything to the Markdown file
        with open(output_path, 'w', encoding='utf-8') as md_file:
            md_file.write(f"# Backup of `{source_path.name}`\n\n")

            # Write the folder structure section
            md_file.write("## Folder Structure\n\n")
            md_file.write("```\n")
            md_file.write(f"{source_path.name}/\n")
            # Adjusting the structure lines to match the requested format
            for line in structure_lines[1:]: # Skip the first entry which is the root
                 md_file.write(line.replace("-", "  -", 1) + "\n")
            md_file.write("```\n\n")
            md_file.write("---\n\n") # Separator

            # Write the file contents section
            for file_path in file_paths_to_process:
                relative_path = file_path.relative_to(temp_dir)
                md_file.write(f"-- {relative_path} --\n")

                if is_binary(file_path):
                    md_file.write("[Binary file, content not included]\n\n")
                else:
                    language = file_path.suffix.lstrip('.') or 'text'
                    md_file.write(f"```{language}\n")
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            md_file.write(f.read())
                    except Exception as e:
                        md_file.write(f"Error reading file: {e}")
                    md_file.write("\n```\n\n")

        print(f"Backup successfully created at: {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

def main():
    """
    Main function to parse command-line arguments and run the backup tool.
    """
    parser = argparse.ArgumentParser(
        description="A source-code backup tool that creates a structured Markdown file."
    )
    parser.add_argument("source_directory", help="The source directory to back up.")
    parser.add_argument("output_markdown_file", help="The path for the output Markdown file.")
    parser.add_argument(
        "-e", "--exclude",
        nargs='*',
        help="A list of file or directory patterns to exclude (e.g., '*.pyc', 'node_modules').",
        default=[]
    )
    args = parser.parse_args()
    create_markdown_backup(args.source_directory, args.output_markdown_file, args.exclude)

if __name__ == "__main__":
    main()
