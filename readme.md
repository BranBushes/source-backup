# Source Code to Markdown Backup Tool

A simple command-line tool to archive a project's directory structure and source code into a single, well-organized Markdown file.

This tool creates a backup in two parts: first, it displays a clean tree of the folder structure, and second, it lists the contents of each file, making it easy to review and share your code.

## Features

-   **Two-Part Format**: Generates a clean folder structure tree and a separate section for file contents.
-   **Portable Archive**: Saves the entire project's text-based source code in one Markdown file.
-   **Smart Exclusions**: Easily ignore files and directories you don't need (like `node_modules` or `__pycache__`).
-   **Binary File Handling**: Detects and skips the content of binary files (e.g., images, executables), noting their presence in the file tree.
-   **Simple CLI**: A straightforward command-line interface for easy use.

## Requirements

-   Python 3.x
-   No external libraries needed.

## How to Use

1.  **Save the Script**: Save the Python code as `backup_tool.py`.
2.  **Open a Terminal**: Navigate to the directory where you saved the script.
3.  **Run the Command**: Execute the script with the following structure.

### Command Syntax

```bash
python backup_tool.py <source_directory> <output_markdown_file> [options]
```

#### **Arguments:**

-   `source_directory`: The path to the project you want to back up.
-   `output_markdown_file`: The name of the Markdown file to create (e.g., `project_backup.md`).

#### **Options:**

-   `-e, --exclude [PATTERN_1] [PATTERN_2] ...`: (Optional) A space-separated list of file or directory patterns to exclude.

---

## Examples

### 1. Basic Backup

To back up a project in the `my-app` folder to a file named `my-app-backup.md`:

```bash
python backup_tool.py ./my-app my-app-backup.md
```

### 2. Backup with Exclusions

To back up a project while ignoring the `dist` folder, all `.log` files, and any `.env` files:

```bash
python backup_tool.py ./my-project backup.md --exclude "dist" "*.log" ".env"
```

## Output Format

The generated Markdown file is structured for maximum clarity:

1.  **Folder Structure**: A visual tree representing the hierarchy of your directories and files.
    ```
    ## Folder Structure

    my-project/
      - index.html
      - assets/
          - style.css
          - logo.png
      - js/
          - app.js
    ```

2.  **File Contents**: Each file's content is then listed, preceded by a clear header. Binary files are noted and their content is skipped.
    ```
    -- index.html --
    ```html
    <!DOCTYPE html>
    <html>
    ...
    </html>
    ```

    -- assets/style.css --
    ```css
    body { ... }
    ```

    -- assets/logo.png --
    [Binary file, content not included]
    ```
