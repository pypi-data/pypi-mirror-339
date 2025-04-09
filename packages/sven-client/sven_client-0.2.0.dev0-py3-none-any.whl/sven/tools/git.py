import os
from pathlib import Path
from typing import List, Optional, Dict, Any, Union

from agno.tools import Toolkit
from agno.utils.log import log_debug, log_info, logger
import json

class GitTools(Toolkit):
    """
    A toolkit for interacting with git repositories.
    """
    name: str = "git"
    description: str = "A toolkit for interacting with git repositories."

    def __init__(
        self,
        base_dir: Optional[Path] = None,
        **kwargs,
    ):
        """
        Initialize GitTools with a base directory.
        
        :param base_dir: Base directory where git commands will be executed, defaults to current working directory
        """
        super().__init__(name="git_tools", **kwargs)
        
        self.base_dir: Path = base_dir or Path.cwd()
        
        # Register all tools
        self.register(self.diff)
        self.register(self.status)
        self.register(self.stage)
        self.register(self.unstage)
        self.register(self.commit)
        
        # Import GitPython here to avoid import errors if it's not installed
        try:
            import git
            self.git_module = git
            self._repo = None
        except ImportError:
            logger.error("GitPython not installed. Please install with: pip install gitpython")
            raise
    
    @property
    def repo(self):
        """
        Retrieve the git repository object for the current working directory. 
        If the repository is not already initialized, this method will initialize it.
        
        Usage:
        - Call this property to get the git.Repo object for performing git operations.
        - Example: `repo = self.repo`
        
        Returns:
        - git.Repo: The repository object for the current working directory.
        
        Raises:
        - Exception: If there is an error accessing the git repository.
        
        :return: git.Repo object for the current repository
        """
        if self._repo is None:
            try:
                self._repo = self.git_module.Repo(self.base_dir, search_parent_directories=True)
            except Exception as e:
                logger.error(f"Error accessing git repository: {e}")
                raise
        return self._repo
    
    def diff(
        self, 
        source: str = "HEAD", 
        target: str = "origin/main", 
        line_start: int = 0, 
        line_end: int = 2000,
        paths: Optional[List[str]] = None
    ) -> str:
        """
        - Use this tool to get the diff between two branches or commits.
        - Specify the source and target branches or commits to compare.
        - Optionally, provide a list of file paths to limit the diff to specific files.
        - You can also specify the range of lines to return from the diff output.
        
        Example usage:
        - `diff(source="HEAD", target="origin/main")` to get the diff between the current HEAD and the main branch.
        - `diff(source="commit1", target="commit2", paths=["file1.py", "file2.py"])` to get the diff for specific files between two commits.
        - `diff(source="HEAD", target="origin/main", line_start=0, line_end=100)` to get the first 100 lines of the diff.
        
        :param source: Source branch or commit (default: "HEAD")
        :param target: Target branch or commit (default: "origin/main")
        :param line_start: First line of the diff to be returned (default: 0)
        :param line_end: Last line of the diff to be returned (default: 2000)
        :param paths: List of file paths to get diff for (default: None, all files)
        :return: String containing the unified diff
        """
        try:
            log_info(f"Getting diff between {source} and {target}")
            
            # Make sure source and target are valid
            try:
                self.repo.git.rev_parse('--verify', source)
            except Exception:
                return f"Error: Source '{source}' does not exist or is not a valid reference"
                
            try:
                self.repo.git.rev_parse('--verify', target)
            except Exception:
                return f"Error: Target '{target}' does not exist or is not a valid reference"
            
            # Get the diff - we use git.diff directly to get a string result
            diff_command = ['--no-color', source, target]
            if paths:
                diff_command.extend(['--'] + paths)
                
            diff_output = self.repo.git.diff(*diff_command)
            diff_lines = diff_output.splitlines()
            total_lines = len(diff_lines)
            
            # Apply line limits
            if line_start > 0 or total_lines > line_end:
                # Calculate effective line start/end, ensuring they're in valid range
                effective_start = max(0, min(line_start, total_lines))
                effective_end = max(effective_start, min(line_end, total_lines))
                
                # Get the slice of lines we want
                result_lines = diff_lines[effective_start:effective_end]
                
                # Add a note if the diff was clipped
                if total_lines > effective_end:
                    lines_returned = effective_end - effective_start
                    lines_clipped = total_lines - lines_returned
                    result_lines.append(
                        f"\nDiff was clipped: {lines_clipped} lines out of {total_lines} in total were omitted. "
                        f"{lines_returned} lines returned."
                    )
                
                return "\n".join(result_lines)
            else:
                return diff_output
                
        except Exception as e:
            logger.error(f"Error getting diff: {e}")
            return f"Error getting diff: {e}"
    
    def status(self, return_untracked: bool = False) -> Dict[str, List[str]]:
        """
        Use this tool to retrieve the current state of the git repository. 
        It provides information on staged, unstaged, added, modified, and deleted files.
        
        :param return_untracked: Whether to include untracked files in the result (default: False)
        :return: Dictionary containing lists of files in different states
        """
        try:
            log_info(f"Getting git status, return_untracked={return_untracked}")
            
            result = {
                "staged": [],
                "unstaged": [],
                "added": [],
                "modified": [],
                "deleted": [],
                "untracked": [] if return_untracked else None
            }
            
            # Get status
            status = self.repo.git.status('--porcelain')
            
            if not status:
                return result
                
            for line in status.splitlines():
                if not line or len(line) < 2:
                    continue
                    
                status_code = line[:2]
                file_path = line[3:].strip()
                
                # Check staged changes (index)
                if status_code[0] != ' ' and status_code[0] != '?':
                    result["staged"].append(file_path)
                    
                    if status_code[0] == 'A':
                        result["added"].append(file_path)
                    elif status_code[0] == 'M':
                        result["modified"].append(file_path)
                    elif status_code[0] == 'D':
                        result["deleted"].append(file_path)
                
                # Check unstaged changes (working tree)
                if status_code[1] != ' ' and status_code[1] != '?':
                    result["unstaged"].append(file_path)
                    
                    if status_code[1] == 'A':  # This shouldn't happen normally
                        result["added"].append(file_path)
                    elif status_code[1] == 'M':
                        result["modified"].append(file_path)
                    elif status_code[1] == 'D':
                        result["deleted"].append(file_path)
                
                # Check untracked files
                if status_code == '??' and return_untracked:
                    result["untracked"].append(file_path)
            
            return json.dumps(result)
            
        except Exception as e:
            logger.error(f"Error getting git status: {e}")
            return json.dumps({"error": str(e)})
    
    def stage(self, files: List[str]) -> str:
        """
        Use this tool to stage files for commit in a Git repository.
        Provide a list of file paths to be staged. The tool will check if the files exist
        and then add them to the Git index, preparing them for the next commit.
        
        :param files: List of files to stage
        :return: Result message
        """
        if not files:
            return "No files specified for staging"
            
        try:
            log_info(f"Staging files: {files}")
            
            # Check if any of the files exist before trying to stage them
            non_existent = []
            for file_path in files:
                full_path = self.base_dir / file_path
                if not os.path.exists(full_path):
                    non_existent.append(file_path)
            
            if non_existent:
                return f"Error: The following files don't exist: {', '.join(non_existent)}"
            
            # Add the files to the index
            self.repo.git.add(*files)
            
            return f"Successfully staged {len(files)} files for commit"
            
        except Exception as e:
            logger.error(f"Error staging files: {e}")
            return f"Error staging files: {e}"
    
    def unstage(self, files: List[str]) -> str:
        """
        Use this tool to unstage files from a commit in a Git repository.
        Provide a list of file paths to be unstaged. The tool will remove these files
        from the Git index, effectively undoing their staging.

        :param files: List of files to unstage
        :return: Result message
        """
        if not files:
            return "No files specified for unstaging"
            
        try:
            log_info(f"Unstaging files: {files}")
            
            # Reset the files from the index
            self.repo.git.reset("HEAD", "--", *files)
            
            return f"Successfully unstaged {len(files)} files"
            
        except Exception as e:
            logger.error(f"Error unstaging files: {e}")
            return f"Error unstaging files: {e}"
    
    def commit(self, message: str, no_verify: bool = True) -> str:
        """
        Use this tool to commit staged changes to a Git repository.
        Provide a commit message to describe the changes being committed.
        Optionally, you can skip pre-commit hooks by setting no_verify to True.
        
        :param message: Commit message
        :param no_verify: Skip pre-commit hooks (default: True)
        :return: Result message including commit hash
        """
        if not message:
            return "Error: Commit message cannot be empty"
            
        try:
            log_info(f"Committing changes with message: {message}")
            
            # Check if there are changes to commit
            if not self.repo.git.diff("--cached"):
                return "Error: No changes staged for commit"
            
            # Build command arguments
            args = []
            if no_verify:
                args.append("--no-verify")
            args.append(message)
            
            # Perform the commit
            result = self.repo.git.commit("-m", *args)
            
            # Extract the commit hash from the result
            commit_hash = None
            for line in result.splitlines():
                if line.startswith("[") and "]" in line and "commit" in line.lower():
                    parts = line.split()
                    for part in parts:
                        if len(part) >= 7 and all(c in "0123456789abcdef" for c in part.lower()):
                            commit_hash = part
                            break
            
            if commit_hash:
                return f"Successfully committed changes with hash: {commit_hash}\n\n{result}"
            else:
                return f"Successfully committed changes:\n{result}"
            
        except Exception as e:
            logger.error(f"Error committing changes: {e}")
            return f"Error committing changes: {e}" 