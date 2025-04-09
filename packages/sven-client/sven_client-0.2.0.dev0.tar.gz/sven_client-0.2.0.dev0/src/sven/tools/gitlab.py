import os
from pathlib import Path
from typing import List, Optional, Dict, Any, Union, Tuple, bool

from agno.tools import Toolkit
from agno.utils.log import log_debug, log_info, logger


class GitLabTools(Toolkit):
    """
    A toolkit for interacting with GitLab repositories and resources.
    """
    name: str = "gitlab"
    description: str = "A toolkit for interacting with GitLab repositories and resources."

    def __init__(
        self,
        base_url: Optional[str] = None,
        private_token: Optional[str] = None,
        **kwargs,
    ):
        """
        Initialize GitLabTools with GitLab server information.
        
        :param base_url: Base URL of the GitLab instance, defaults to value from environment variable GITLAB_URL
        :param private_token: Private token for authentication, defaults to value from environment variable GITLAB_TOKEN
        """
        super().__init__(name="gitlab_tools", **kwargs)
        
        self.base_url = base_url or os.environ.get("GITLAB_URL")
        self.private_token = private_token or os.environ.get("GITLAB_TOKEN")
        
        if not self.base_url:
            logger.warning("GitLab URL not provided. Set GITLAB_URL environment variable or pass base_url parameter.")
        
        if not self.private_token:
            logger.warning("GitLab token not provided. Set GITLAB_TOKEN environment variable or pass private_token parameter.")
        
        # Register all tools
        self.register(self.get_projects)
        self.register(self.get_merge_requests)
        self.register(self.get_merge_request)
        self.register(self.update_merge_request)
        self.register(self.get_issues)
        self.register(self.get_issue)
        self.register(self.create_issue)
        
        # Import gitlab module here to avoid import errors if it's not installed
        try:
            import gitlab
            self.gitlab_module = gitlab
            self._gitlab = None
        except ImportError:
            logger.error("python-gitlab not installed. Please install with: pip install python-gitlab")
            raise
    
    @property
    def gitlab(self):
        """
        Retrieve the GitLab client connection.
        If not already initialized, this method will initialize it.
        
        :return: gitlab.Gitlab object for the current connection
        """
        if self._gitlab is None:
            if not self.base_url or not self.private_token:
                raise ValueError("GitLab URL and private token are required")
            
            try:
                self._gitlab = self.gitlab_module.Gitlab(
                    url=self.base_url,
                    private_token=self.private_token
                )
            except Exception as e:
                logger.error(f"Error connecting to GitLab: {e}")
                raise
        return self._gitlab
    
    def get_projects(self, details: bool = False) -> List[Dict[str, Any]]:
        """
        Use this tool to retrieve a list of accessible projects from GitLab.
        
        By default, it returns minimal information about each project.
        When details is set to True, more comprehensive information is provided.
        
        :param details: Whether to include detailed project information (default: False)
        :return: List of projects with their information
        """
        try:
            log_info("Retrieving GitLab projects")
            
            # Get projects
            projects = self.gitlab.projects.list(all=True)
            
            # Prepare the response based on the details parameter
            if details:
                return [
                    {
                        'id': project.id,
                        'path_with_namespace': project.path_with_namespace,
                        'name': project.name,
                        'description': project.description,
                        'web_url': project.web_url,
                        'visibility': project.visibility,
                        'star_count': project.star_count,
                        'created_at': project.created_at,
                        'last_activity_at': project.last_activity_at
                    }
                    for project in projects
                ]
            else:
                return [
                    {
                        'id': project.id,
                        'path_with_namespace': project.path_with_namespace,
                        'name': project.name,
                        'description': project.description
                    }
                    for project in projects
                ]
            
        except Exception as e:
            logger.error(f"Error retrieving GitLab projects: {e}")
            return [{"error": str(e)}]
    
    def get_merge_requests(self, project_id: Union[int, str], state: str = 'all') -> List[Dict[str, Any]]:
        """
        Use this tool to list merge requests for a specific project.
        
        By default, it returns basic information about each merge request,
        including title, ID, and labels (tags).
        
        :param project_id: ID or URL-encoded path of the project
        :param state: State of merge requests to list (opened, closed, locked, merged, or all). Default: all
        :return: List of merge requests with their information
        """
        try:
            log_info(f"Retrieving merge requests for project {project_id}")
            
            # Get project
            project = self.gitlab.projects.get(project_id)
            
            # Get merge requests
            merge_requests = project.mergerequests.list(state=state, all=True)
            
            return [
                {
                    'id': mr.iid,  # Note: iid is the project-specific MR ID
                    'title': mr.title,
                    'labels': mr.labels,
                    'state': mr.state,
                    'created_at': mr.created_at,
                    'web_url': mr.web_url
                }
                for mr in merge_requests
            ]
            
        except Exception as e:
            logger.error(f"Error retrieving merge requests: {e}")
            return [{"error": str(e)}]
    
    def get_merge_request(
        self, 
        project_id: Union[int, str], 
        mr_id: int,
        include_threads: bool = False,
        include_changes: bool = False
    ) -> Dict[str, Any]:
        """
        Use this tool to get detailed information about a specific merge request.
        
        By default, it returns basic information. Additional data like discussion threads
        and code changes can be included using the optional parameters.
        
        :param project_id: ID or URL-encoded path of the project
        :param mr_id: ID of the merge request
        :param include_threads: Whether to include discussion threads (default: False)
        :param include_changes: Whether to include code changes/diff (default: False)
        :return: Dictionary with merge request information
        """
        try:
            log_info(f"Retrieving merge request {mr_id} for project {project_id}")
            
            # Get project
            project = self.gitlab.projects.get(project_id)
            
            # Get merge request
            mr = project.mergerequests.get(mr_id)
            
            # Build response
            response = {
                'id': mr.iid,
                'title': mr.title,
                'description': mr.description,
                'state': mr.state,
                'created_at': mr.created_at,
                'updated_at': mr.updated_at,
                'author': {
                    'id': mr.author['id'],
                    'name': mr.author['name'],
                    'username': mr.author['username']
                },
                'web_url': mr.web_url,
                'labels': mr.labels
            }
            
            # Include discussion threads if requested
            if include_threads:
                discussions = mr.discussions.list(all=True)
                response['discussions'] = [
                    {
                        'id': discussion.id,
                        'notes': [
                            {
                                'author': note['author']['name'],
                                'body': note['body'],
                                'created_at': note['created_at']
                            }
                            for note in discussion.attributes['notes']
                        ]
                    }
                    for discussion in discussions
                    if discussion.attributes.get('notes')
                ]
            
            # Include changes if requested
            if include_changes:
                changes = mr.changes()
                response['changes'] = [
                    {
                        'old_path': change['old_path'],
                        'new_path': change['new_path'],
                        'diff': change['diff']
                    }
                    for change in changes['changes']
                ]
            
            return response
            
        except Exception as e:
            logger.error(f"Error retrieving merge request: {e}")
            return {"error": str(e)}
    
    def update_merge_request(
        self, 
        project_id: Union[int, str], 
        mr_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Use this tool to update a merge request's title and/or description.
        
        If title or description is not provided, the existing value will be kept.
        
        :param project_id: ID or URL-encoded path of the project
        :param mr_id: ID of the merge request
        :param title: New title for the merge request (optional)
        :param description: New description for the merge request (optional)
        :return: Dictionary with updated merge request information
        """
        try:
            log_info(f"Updating merge request {mr_id} for project {project_id}")
            
            if title is None and description is None:
                return {"error": "At least one of title or description must be provided"}
            
            # Get project
            project = self.gitlab.projects.get(project_id)
            
            # Get merge request
            mr = project.mergerequests.get(mr_id)
            
            # Prepare update data
            update_data = {}
            if title is not None:
                update_data['title'] = title
            if description is not None:
                update_data['description'] = description
            
            # Update the merge request
            mr.save(update_data)
            
            # Return updated merge request
            return {
                'id': mr.iid,
                'title': mr.title,
                'description': mr.description,
                'web_url': mr.web_url,
                'message': 'Merge request updated successfully'
            }
            
        except Exception as e:
            logger.error(f"Error updating merge request: {e}")
            return {"error": str(e)}
    
    def get_issues(
        self, 
        project_id: Union[int, str],
        state: str = 'opened'
    ) -> List[Dict[str, Any]]:
        """
        Use this tool to get a list of issues for a specific project.
        
        :param project_id: ID or URL-encoded path of the project
        :param state: State of issues to retrieve (opened, closed, or all). Default: opened
        :return: List of issues with their information
        """
        try:
            log_info(f"Retrieving issues for project {project_id}")
            
            # Get project
            project = self.gitlab.projects.get(project_id)
            
            # Get issues
            issues = project.issues.list(state=state, all=True)
            
            return [
                {
                    'id': issue.iid,  # Note: iid is the project-specific issue ID
                    'title': issue.title,
                    'description': issue.description,
                    'state': issue.state,
                    'created_at': issue.created_at,
                    'labels': issue.labels,
                    'web_url': issue.web_url
                }
                for issue in issues
            ]
            
        except Exception as e:
            logger.error(f"Error retrieving issues: {e}")
            return [{"error": str(e)}]
    
    def get_issue(
        self, 
        project_id: Union[int, str], 
        issue_id: int
    ) -> Dict[str, Any]:
        """
        Use this tool to get detailed information about a specific issue.
        
        :param project_id: ID or URL-encoded path of the project
        :param issue_id: ID of the issue
        :return: Dictionary with issue information
        """
        try:
            log_info(f"Retrieving issue {issue_id} for project {project_id}")
            
            # Get project
            project = self.gitlab.projects.get(project_id)
            
            # Get issue
            issue = project.issues.get(issue_id)
            
            return {
                'id': issue.iid,
                'title': issue.title,
                'description': issue.description,
                'state': issue.state,
                'created_at': issue.created_at,
                'updated_at': issue.updated_at,
                'labels': issue.labels,
                'author': {
                    'id': issue.author['id'],
                    'name': issue.author['name'],
                    'username': issue.author['username']
                },
                'assignees': [
                    {
                        'id': assignee['id'],
                        'name': assignee['name'],
                        'username': assignee['username']
                    }
                    for assignee in issue.attributes.get('assignees', [])
                ],
                'web_url': issue.web_url
            }
            
        except Exception as e:
            logger.error(f"Error retrieving issue: {e}")
            return {"error": str(e)}
    
    def create_issue(
        self,
        project_id: Union[int, str],
        title: str,
        description: str,
        labels: Optional[List[str]] = None,
        assignee_ids: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Use this tool to create a new issue in a project.
        
        :param project_id: ID or URL-encoded path of the project
        :param title: Title of the issue
        :param description: Description of the issue
        :param labels: List of labels to apply to the issue (optional)
        :param assignee_ids: List of user IDs to assign to the issue (optional)
        :return: Dictionary with created issue information
        """
        try:
            log_info(f"Creating new issue in project {project_id}")
            
            if not title:
                return {"error": "Issue title is required"}
            
            # Get project
            project = self.gitlab.projects.get(project_id)
            
            # Prepare issue data
            issue_data = {
                'title': title,
                'description': description
            }
            
            if labels:
                issue_data['labels'] = labels
            
            if assignee_ids:
                issue_data['assignee_ids'] = assignee_ids
            
            # Create the issue
            issue = project.issues.create(issue_data)
            
            return {
                'id': issue.iid,
                'title': issue.title,
                'description': issue.description,
                'state': issue.state,
                'created_at': issue.created_at,
                'labels': issue.labels,
                'web_url': issue.web_url,
                'message': 'Issue created successfully'
            }
            
        except Exception as e:
            logger.error(f"Error creating issue: {e}")
            return {"error": str(e)} 