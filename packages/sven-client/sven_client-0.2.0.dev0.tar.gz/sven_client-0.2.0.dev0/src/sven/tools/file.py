import difflib
from datetime import datetime
from pathlib import Path
from typing import Optional

from agno.tools import Toolkit
from agno.utils.log import log_debug, log_info, logger
from rich.panel import Panel
from rich.text import Text


class FileTools(Toolkit):
    def __init__(
        self,
        base_dir: Optional[Path] = None,
        write_files: bool = True,
        read_files: bool = True,
        edit_files: bool = True,
        glob: bool = True,
        grep: bool = True,
        ls: bool = True,
        insert_files: bool = True,
        **kwargs,
    ):
        super().__init__(name="file_tools", **kwargs)

        self.base_dir: Path = base_dir or Path.cwd()
        if write_files:
            self.register(self.write_file, sanitize_arguments=False)
        if read_files:
            self.register(self.read_file)
        if edit_files:
            self.register(self.edit_file)
        if glob:
            self.register(self.glob)
        if grep:
            self.register(self.grep)
        if ls:
            self.register(self.ls)
        if insert_files:
            self.register(self.insert)

    def glob(
        self, pattern: str, sort_by_modified: bool = True, max_results: int = 100
    ) -> str:
        """
        - Fast file pattern matching tool that works with any codebase size
        - Supports glob patterns like "**/*.js" or "src/**/*.ts"
        - Returns matching file paths sorted by modification time
        - Use this tool when you need to find files by name patterns
        - When you are doing an open ended search that may require multiple
        rounds of globbing and grepping, use the Agent tool instead

        :param pattern: The glob pattern to match files (e.g., '**/*.js', 'src/**/*.py').
        :param sort_by_modified: Whether to sort results by modification time (newest first).
        :param max_results: Maximum number of results to return.
        :return: A list of file paths that match the pattern.
        """
        try:
            log_info(f"Globbing files with pattern: {pattern}")

            # Ensure we're working with a Path object
            base_path = self.base_dir

            # Handle absolute patterns
            if pattern.startswith("/"):
                # Remove the leading slash for Path compatibility
                pattern = pattern[1:]
                base_path = Path("/")

            # Use pathlib's .glob() to find matching files
            matching_files = list(base_path.glob(pattern))

            # Filter out directories, only keep files
            matching_files = [f for f in matching_files if f.is_file()]

            # Sort results if requested
            if sort_by_modified:
                try:
                    matching_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                except Exception as sort_error:
                    log_debug(f"Error sorting files by modification time: {sort_error}")

            # Limit the number of results
            matching_files = matching_files[:max_results]

            # Format the results
            if not matching_files:
                return "No files found matching the pattern."

            # If sorting by modified time, include the modification time in the output
            if sort_by_modified:
                results = []
                for file_path in matching_files:
                    try:
                        mod_time = file_path.stat().st_mtime
                        mod_time_str = datetime.fromtimestamp(mod_time).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        results.append(f"{file_path} (modified: {mod_time_str})")
                    except Exception:
                        results.append(str(file_path))

                result_str = "\n".join(results)
            else:
                result_str = "\n".join(str(f) for f in matching_files)

            if len(matching_files) == max_results:
                result_str += f"\n\n[Note: Results limited to {max_results} files. Use a more specific pattern to narrow down results.]"

            return result_str

        except Exception as e:
            logger.error(f"Error in glob operation: {e}")
            return f"Error searching for files: {e}"

    def grep(
        self,
        pattern: str,
        include: str = "**/*",
        case_sensitive: bool = False,
        max_results: int = 50,
        max_matches_per_file: int = 5,
        respect_gitignore: bool = True,
    ) -> str:
        """
        Purpose: Searches file contents using regular expressions.

        How it works:
        - Searches through file contents using regular expression patterns.
        - Can be filtered to specific file types using the include parameter.
        - Returns matching files sorted by modification time.
        - Respects .gitignore patterns to exclude files from search.

        Example use case:
        When the agent needs to find where a specific function is defined, or where a
        particular string or pattern appears in the codebase.

        Tool description for the model:
        - Fast content search tool that works with any codebase size
        - Searches file contents using regular expressions
        - Supports full regex syntax (eg. "log.*Error", "function\\s+\\w+", etc.)
        - Filter files by pattern with the include parameter (eg. "*.js", "*.{ts,tsx}")
        - Returns matching file paths sorted by modification time
        - Respects .gitignore patterns to exclude files from search
        - Use this tool when you need to find files containing specific patterns
        - When you are doing an open ended search that may require multiple rounds of globbing and grepping, use the Agent tool instead

        :param pattern: The regex pattern to search for in file contents.
        :param include: Glob pattern to filter which files to search (e.g., '**/*.js', 'src/**/*.py').
        :param case_sensitive: Whether the search should be case sensitive.
        :param max_results: Maximum number of results to return.
        :param max_matches_per_file: Maximum number of matches to show per file.
        :param respect_gitignore: Whether to respect .gitignore patterns to exclude files from search.
        """
        try:
            import re

            log_info(
                f"Searching for pattern: '{pattern}' in files matching: '{include}'"
            )

            # Get files to search using the glob method
            base_path = self.base_dir

            # Handle absolute patterns for include
            if include.startswith("/"):
                include = include[1:]
                base_path = Path("/")

            # Get all files matching the include pattern
            all_files = list(base_path.glob(include))

            # Filter out directories, only keep files
            all_files = [f for f in all_files if f.is_file()]

            # Sort by modification time (newest first)
            try:
                all_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            except Exception as sort_error:
                log_debug(f"Error sorting files by modification time: {sort_error}")

            # If respecting .gitignore, find and apply those patterns
            if respect_gitignore:
                try:
                    import fnmatch

                    gitignore_patterns = []
                    gitignore_path = base_path / ".gitignore"

                    if gitignore_path.exists():
                        with gitignore_path.open("r") as gitignore_file:
                            for line in gitignore_file:
                                line = line.strip()
                                if line and not line.startswith("#"):
                                    gitignore_patterns.append(line)

                    if gitignore_patterns:
                        # Use fnmatch to apply gitignore patterns
                        filtered_files = []
                        for file_path in all_files:
                            rel_path = file_path.relative_to(base_path)
                            str_path = str(rel_path)

                            # Check if file matches any gitignore pattern
                            should_ignore = False
                            for pattern in gitignore_patterns:
                                # Handle pattern syntax
                                if pattern.endswith("/"):
                                    # Directory pattern
                                    if fnmatch.fnmatch(
                                        str_path + "/", pattern
                                    ) or fnmatch.fnmatch(str_path, pattern + "*"):
                                        should_ignore = True
                                        break
                                else:
                                    if fnmatch.fnmatch(str_path, pattern):
                                        should_ignore = True
                                        break

                            if not should_ignore:
                                filtered_files.append(file_path)

                        all_files = filtered_files

                except Exception as gitignore_error:
                    log_debug(f"Error handling .gitignore patterns: {gitignore_error}")

            # Compile regex pattern
            try:
                flags = 0 if case_sensitive else re.IGNORECASE
                regex = re.compile(pattern, flags)
            except re.error as regex_error:
                return f"Error in regex pattern: {regex_error}"

            # Search each file for the pattern
            results = []
            files_with_matches = 0
            total_matches = 0

            for file_path in all_files:
                if files_with_matches >= max_results:
                    break

                try:
                    # Skip very large files
                    if file_path.stat().st_size > 10_000_000:  # 10MB limit
                        continue

                    file_content = file_path.read_text(errors="replace")
                    matches = list(regex.finditer(file_content))

                    if matches:
                        files_with_matches += 1
                        file_results = [f"File: {file_path}"]

                        # Get file modification time
                        try:
                            mod_time = file_path.stat().st_mtime
                            mod_time_str = datetime.fromtimestamp(mod_time).strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                            file_results[0] += f" (modified: {mod_time_str})"
                        except Exception:
                            pass

                        # Add the matches with context
                        lines = file_content.splitlines()
                        match_count = 0

                        for match in matches[:max_matches_per_file]:
                            match_count += 1
                            total_matches += 1

                            # Get line number of the match
                            match_pos = match.start()
                            line_num = file_content.count("\n", 0, match_pos) + 1

                            # Extract the line with the match
                            try:
                                line_index = line_num - 1
                                line = (
                                    lines[line_index]
                                    if 0 <= line_index < len(lines)
                                    else ""
                                )

                                # Get context (a few lines before and after)
                                context_lines = []
                                context_start = max(0, line_index - 2)
                                context_end = min(len(lines), line_index + 3)

                                for i in range(context_start, context_end):
                                    prefix = "-> " if i == line_index else "   "
                                    context_lines.append(f"{prefix}{i+1}: {lines[i]}")

                                context_text = "\n".join(context_lines)
                                file_results.append(
                                    f"Match {match_count} at line {line_num}:\n{context_text}"
                                )

                            except Exception:
                                file_results.append(
                                    f"Match {match_count} at line {line_num}"
                                )

                        # Show if there are more matches than displayed
                        if len(matches) > max_matches_per_file:
                            file_results.append(
                                f"... {len(matches) - max_matches_per_file} more matches in this file"
                            )

                        results.append("\n".join(file_results))

                except Exception as file_error:
                    log_debug(f"Error searching in {file_path}: {file_error}")

            # Format final results
            if not results:
                return "No matching files found."

            result_str = "\n\n".join(results)

            # Add summary and notes
            summary = (
                f"Found {total_matches} matches across {files_with_matches} files. "
                f"Displaying up to {max_matches_per_file} matches per file."
            )

            if files_with_matches == max_results:
                summary += f"\n[Note: Results limited to {max_results} files. Use a more specific pattern to narrow down results.]"

            result_str = summary + "\n\n" + result_str

            return result_str

        except Exception as e:
            logger.error(f"Error in grep operation: {e}")
            return f"Error searching for pattern: {e}"

    def write_file(self, contents: str, file_name: str, overwrite: bool = True) -> str:
        """
        Write a file to the local filesystem. Overwrites the existing file if there is
        one.

        Before using this tool:

        1. Use the file_read tool to understand the file's contents and context

        2. Directory Verification (only applicable when creating new files):
            - Use the LS tool to verify the parent directory exists and is the correct location
            - Use the mkdir -p command to create the directory if it doesn't exist

        :param contents: The contents to save.
        :param file_name: The name of the file to save to.
        :param overwrite: Overwrite the file if it already exists.
        :return: The file name if successful, otherwise returns an error message.
        """
        try:
            # Convert to Path object
            path_obj = Path(file_name)

            log_debug(f"Writing contents to {path_obj}")

            # Check if file exists and handle overwrite flag
            if path_obj.exists() and not overwrite:
                return f"Error: File {file_name} already exists and overwrite is set to False"

            # Create parent directories if they don't exist
            if not path_obj.parent.exists():
                path_obj.parent.mkdir(parents=True, exist_ok=True)
                log_info(f"Created directory structure for {path_obj.parent}")

            # Write the file
            path_obj.write_text(contents)
            log_info(f"Successfully wrote to file: {path_obj}")

            return f"Successfully wrote to file: {file_name}"

        except Exception as e:
            logger.error(f"Error writing to file: {e}")
            return f"Error writing to file: {e}"

    def read_file(
        self, file_path: str, line_offset: int = 0, line_limit: int = 2000
    ) -> str:
        """
        Reads a file from the local filesystem. The file_path parameter must be an
        absolute path, not a relative path. By default, it reads up to 2000 lines
        starting from the beginning of the file. You can optionally specify a line
        offset and limit (especially handy for long files), but it's recommended to read
        the whole file by not providing these parameters. Any lines longer than 2000
        characters will be truncated.

        :param file_path: The path to the file to read.
        :param line_offset: The number of lines to skip from the beginning of the file.
        :param line_limit: The maximum number of lines to read.
        :return: The contents of the file if successful, otherwise returns an error message.
        """
        try:
            # Convert to Path object
            path_obj = Path(file_path)

            # Check if file exists
            if not path_obj.exists():
                return f"Error: File {file_path} does not exist"

            # Check if path is a file and not a directory
            if not path_obj.is_file():
                return f"Error: {file_path} is not a file"

            log_info(
                f"Reading file: {file_path} (offset={line_offset}, limit={line_limit})"
            )

            # Read file with line offset and limit
            with path_obj.open("r") as file:
                # Skip offset lines
                for _ in range(line_offset):
                    if not file.readline():
                        # Reached end of file during offset
                        return f"Error: Line offset {line_offset} exceeds file length"

                # Read specified number of lines with truncation
                MAX_CHAR_PER_LINE = 2000
                lines = []
                for _ in range(line_limit):
                    line = file.readline()
                    if not line:  # End of file
                        break
                    # Truncate long lines if needed
                    if len(line) > MAX_CHAR_PER_LINE:
                        line = line[:MAX_CHAR_PER_LINE] + "... [truncated]\n"
                    lines.append(line)

                # Provide info about truncation if needed
                if file.readline():  # Check if there are more lines
                    total_lines = (
                        line_offset + len(lines) + 1
                    )  # +1 for the line we just read
                    while file.readline():
                        total_lines += 1

                    footer = (
                        f"\n\n[Note: Displayed {len(lines)} of {total_lines} total lines. "
                        f"Use line_offset and line_limit parameters to see more.]"
                    )
                    lines.append(footer)

            return "".join(lines)

        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return f"Error reading file: {e}"

    def edit_file(self, file_path: str, old_string: str, new_string: str) -> str:
        """
        This is a tool for editing files. For moving or renaming files, you should
        generally use the Bash tool with the 'mv' command instead. For larger edits, use
        the Write tool to overwrite files. For Jupyter notebooks (.ipynb files), use the
        NotebookEditCell instead.

        Before using this tool:

        1. Use the View tool to understand the file's contents and context

        2. Verify the directory path is correct (only applicable when creating new files):
        - Use the LS tool to verify the parent directory exists and is the correct location

        To make a file edit, provide the following:
        1. file_name: The name of the file to modify (must be absolute, not relative)
        2. old_string: The text to replace (must be unique within the file, and must match the file contents exactly, including all whitespace and indentation)
        3. new_string: The edited text to replace the old_string

        The tool will replace ONE occurrence of old_string with new_string in the specified file.

        CRITICAL REQUIREMENTS FOR USING THIS TOOL:

        1. UNIQUENESS: The old_string MUST uniquely identify the specific instance you want to change. This means:
        - Include AT LEAST 3-5 lines of context BEFORE the change point
        - Include AT LEAST 3-5 lines of context AFTER the change point
        - Include all whitespace, indentation, and surrounding code exactly as it appears in the file

        2. SINGLE INSTANCE: This tool can only change ONE instance at a time. If you need to change multiple instances:
        - Make separate calls to this tool for each instance
        - Each call must uniquely identify its specific instance using extensive context

        3. VERIFICATION: Before using this tool:
        - Check how many instances of the target text exist in the file
        - If multiple instances exist, gather enough context to uniquely identify each one
        - Plan separate tool calls for each instance

        WARNING: If you do not follow these requirements:
        - The tool will fail if old_string matches multiple locations
        - The tool will fail if old_string doesn't match exactly (including whitespace)
        - You may change the wrong instance if you don't include enough context

        When making edits:
        - Ensure the edit results in idiomatic, correct code
        - Do not leave the code in a broken state
        - Always use absolute file paths (starting with /)

        If you want to create a new file, use:
        - A new file path, including dir name if needed
        - An empty old_string
        - The new file's contents as new_string

        :param file_name: The name of the file to edit.
        :param old_string: The string to replace.
        :param new_string: The new string to replace the old string with.
        """
        try:
            # Handle file path - ensure it's a Path object
            path_obj = Path(file_path)

            # Check if we're creating a new file (old_string is empty)
            if not old_string:
                # Check if the parent directory exists
                if not path_obj.parent.exists():
                    path_obj.parent.mkdir(parents=True, exist_ok=True)
                    log_info(f"Created directory structure for {path_obj.parent}")

                # Write the new file
                path_obj.write_text(new_string)
                log_info(f"Created new file: {path_obj}")
                return f"Successfully created new file: {file_path}"

            # For existing files, ensure the file exists
            if not path_obj.exists():
                return f"Error: File {file_path} does not exist"

            # Read the current file contents
            file_contents = path_obj.read_text()

            # Check for uniqueness of the old_string
            occurrences = file_contents.count(old_string)

            if occurrences == 0:
                return (
                    f"Error: The specified text to replace was not found in {file_path}"
                )

            if occurrences > 1:
                return f"Error: Found {occurrences} instances of the specified text in {file_path}. The replacement text must uniquely identify a single instance."

            # Perform the replacement
            new_contents = file_contents.replace(old_string, new_string, 1)

            # Write the modified contents
            path_obj.write_text(new_contents)
            log_info(f"Successfully edited file: {file_path}")

            return f"Successfully edited file: {file_path}"

        except Exception as e:
            logger.error(f"Error editing file: {e}")
            return f"Error editing file: {e}"

    def ls(self, path: str = ".") -> str:
        """
        Purpose: Lists files and directories in a given path.

        How it works:
        - Takes an absolute path and returns a list of files and directories.
        - Helps the agent explore the codebase structure.
        - Particularly useful when the agent needs to understand what files are available.

        Example use case:
        When agent needs to verify that a directory exists before creating a file in it,
        or to understand the overall structure of a project.

        Tool description for the model:
        Lists files and directories in a given path. The path parameter must be an
        absolute path, not a relative path. You should generally prefer the Glob and
        Grep tools, if you know which directories to search.

        :param path: The path to list files and directories from.
        """
        try:
            # Handle path
            if path == ".":
                # Use base directory if no path provided
                dir_path = self.base_dir
            else:
                # Convert to Path object
                dir_path = Path(path)

            log_info(f"Listing contents of directory: {dir_path}")

            # Check if path exists
            if not dir_path.exists():
                return f"Error: Path {path} does not exist"

            # Check if path is a directory
            if not dir_path.is_dir():
                return f"Error: Path {path} is not a directory"

            # Get all entries in the directory
            entries = list(dir_path.iterdir())

            # Separate files and directories
            directories = []
            files = []

            for entry in entries:
                try:
                    # Get basic file information
                    stats = entry.stat()
                    size = stats.st_size
                    mod_time = datetime.fromtimestamp(stats.st_mtime).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

                    # Format size in a human-readable way
                    if size < 1024:
                        size_str = f"{size} B"
                    elif size < 1024 * 1024:
                        size_str = f"{size / 1024:.1f} KB"
                    elif size < 1024 * 1024 * 1024:
                        size_str = f"{size / (1024 * 1024):.1f} MB"
                    else:
                        size_str = f"{size / (1024 * 1024 * 1024):.1f} GB"

                    entry_info = {
                        "name": entry.name,
                        "full_path": str(entry),
                        "size": size_str,
                        "modified": mod_time,
                    }

                    if entry.is_dir():
                        entry_info["type"] = "directory"
                        directories.append(entry_info)
                    else:
                        entry_info["type"] = "file"
                        files.append(entry_info)

                except Exception as entry_error:
                    log_debug(f"Error getting info for {entry}: {entry_error}")
                    if entry.is_dir():
                        directories.append(
                            {
                                "name": entry.name,
                                "full_path": str(entry),
                                "type": "directory",
                            }
                        )
                    else:
                        files.append(
                            {
                                "name": entry.name,
                                "full_path": str(entry),
                                "type": "file",
                            }
                        )

            # Sort directories and files alphabetically by name
            directories.sort(key=lambda x: x["name"].lower())
            files.sort(key=lambda x: x["name"].lower())

            # Format the output
            output = [f"Contents of {dir_path}:"]
            output.append(
                f"\nTotal: {len(directories)} directories, {len(files)} files\n"
            )

            if directories:
                output.append("Directories:")
                for d in directories:
                    if "modified" in d:
                        output.append(f"  📁 {d['name']} (modified: {d['modified']})")
                    else:
                        output.append(f"  📁 {d['name']}")

            if files:
                output.append("\nFiles:")
                for f in files:
                    if "size" in f and "modified" in f:
                        output.append(
                            f"  📄 {f['name']} ({f['size']}, modified: {f['modified']})"
                        )
                    else:
                        output.append(f"  📄 {f['name']}")

            if not directories and not files:
                output.append("(Empty directory)")

            return "\n".join(output)

        except Exception as e:
            logger.error(f"Error listing directory: {e}")
            return f"Error listing directory: {e}"

    def _create_diff_display(
        self, old_content: str, new_content: str, start_line: int = 1
    ) -> Panel:
        """
        Create a rich panel displaying the diff between old and new content with line numbers.

        Args:
            old_content: The original content
            new_content: The new content
            start_line: The starting line number for the diff (default: 1)

        Returns:
            A rich Panel containing the diff with color highlighting and line numbers
        """
        # Split content into lines if they aren't already lists
        if isinstance(old_content, str):
            old_lines = old_content.splitlines()
        else:
            old_lines = old_content

        if isinstance(new_content, str):
            new_lines = new_content.splitlines()
        else:
            new_lines = new_content

        # Generate the diff
        diff = difflib.SequenceMatcher(None, old_lines, new_lines)

        # Create a text object with colored diff lines and line numbers
        diff_text = Text()

        line_num = start_line

        # Process each diff block
        for tag, i1, i2, j1, j2 in diff.get_opcodes():
            if tag == "equal":
                # Lines are the same - regular display with line numbers
                for line_idx in range(i1, i2):
                    line_txt = f"{line_num:4d} | {old_lines[line_idx]}\n"
                    diff_text.append(line_txt)
                    line_num += 1

            elif tag == "replace":
                # Lines were replaced - show old lines (red) and new lines (green)
                for line_idx in range(i1, i2):
                    line_txt = f"{line_num:4d} | {old_lines[line_idx]}\n"
                    diff_text.append(line_txt, style="black on red")
                    line_num += 1

                # Reset line number for new lines (they're at the same position)
                temp_line_num = start_line + i1
                for line_idx in range(j1, j2):
                    line_txt = f"{temp_line_num:4d} | {new_lines[line_idx]}\n"
                    diff_text.append(line_txt, style="black on green")
                    temp_line_num += 1

            elif tag == "delete":
                # Lines were deleted - red background
                for line_idx in range(i1, i2):
                    line_txt = f"{line_num:4d} | {old_lines[line_idx]}\n"
                    diff_text.append(line_txt, style="black on red")
                    line_num += 1

            elif tag == "insert":
                # Lines were inserted - green background
                for line_idx in range(j1, j2):
                    line_txt = f"{line_num:4d} | {new_lines[line_idx]}\n"
                    diff_text.append(line_txt, style="black on green")
                    line_num += 1

        # Return a panel containing the styled diff
        return Panel(diff_text, title="File Changes", border_style="yellow")

    def insert(self, file_path: str, line: int, content: str) -> str:
        """
        Insert new text into a file at a specific line. If line is -1, the content will be 
        appended to the end of the file.
        
        This tool is useful when you want to:
        - Append text to the end of a file
        - Insert lines at the beginning of a file
        - Add content at a specific line number
        
        Before using this tool:
        1. Use the read_file tool to understand the file's contents and context
        2. Make sure the line number exists in the file (unless appending)
        
        :param file_path: The path to the file where the content will be inserted.
        :param line: The line number where the content should be inserted (1-indexed).
                    Use -1 to append to the end of the file.
        :param content: The text to insert at the specified line.
        :return: A success message if the operation was successful, otherwise an error message.
        """
        try:
            # Convert to Path object
            path_obj = Path(file_path)
            
            # Check if file exists
            if not path_obj.exists():
                return f"Error: File {file_path} does not exist"
                
            # Check if it's a file
            if not path_obj.is_file():
                return f"Error: {file_path} is not a file"
                
            log_info(f"Inserting content at line {line} in file: {file_path}")
            
            # Read the current file contents
            with path_obj.open("r") as file:
                lines = file.readlines()
                
            # Insert content at the specified line
            if line == -1:
                # Append to the end of the file
                if lines and not lines[-1].endswith('\n'):
                    # Ensure there's a newline before appending if the last line doesn't have one
                    content = '\n' + content
                lines.append(content)
                log_debug(f"Appended content to end of file: {file_path}")
            elif line < 1:
                return f"Error: Line number must be >= 1 or -1 for append"
            elif line > len(lines) + 1:
                return f"Error: Line number {line} is out of range. File has {len(lines)} lines."
            else:
                # Convert from 1-indexed to 0-indexed
                zero_idx_line = line - 1
                lines.insert(zero_idx_line, content)
                log_debug(f"Inserted content at line {line} in file: {file_path}")
                
            # Write the modified contents back to the file
            with path_obj.open("w") as file:
                file.writelines(lines)
                
            log_info(f"Successfully inserted content at line {line} in file: {file_path}")
            
            return f"Successfully inserted content at line {line} in file: {file_path}"
            
        except Exception as e:
            logger.error(f"Error inserting into file: {e}")
            return f"Error inserting into file: {e}"
