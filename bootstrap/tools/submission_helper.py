# bootstrap/tools/submission_helper.py

import os
from github import Github
from typing import Optional, List, Dict
import argparse
import yaml
import tempfile
import subprocess
from pathlib import Path

class SubmissionHelper:
    """Helper class for creating GitHub issues and pull requests"""
    
    def __init__(self, token: str):
        """Initialize with GitHub token"""
        self.g = Github(token)
        self.repo = self.g.get_repo("Quasimondo/OpenMender")
        
    def create_issue(self, 
                    title: str, 
                    body: str, 
                    labels: List[str] = None,
                    template: str = None) -> Dict:
        """
        Create a new issue
        
        Args:
            title: Issue title
            body: Issue body
            labels: List of label names
            template: Name of issue template to use
        """
        try:
            if template:
                template_content = self._get_issue_template(template)
                if template_content:
                    body = self._apply_template(template_content, body)
            
            issue = self.repo.create_issue(
                title=title,
                body=body,
                labels=labels
            )
            
            return {
                "number": issue.number,
                "url": issue.html_url,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def create_pull_request(self,
                          title: str,
                          body: str,
                          branch_name: str,
                          files: Dict[str, str],
                          base_branch: str = "main") -> Dict:
        """
        Create a new pull request
        
        Args:
            title: PR title
            body: PR description
            branch_name: Name for the new branch
            files: Dict of filepath: content pairs
            base_branch: Branch to create PR against
        """
        try:
            # Create new branch
            base = self.repo.get_branch(base_branch)
            self.repo.create_git_ref(
                ref=f"refs/heads/{branch_name}",
                sha=base.commit.sha
            )
            
            # Create/update files
            for file_path, content in files.items():
                try:
                    # Try to get existing file
                    file = self.repo.get_contents(file_path, ref=branch_name)
                    self.repo.update_file(
                        file_path,
                        f"Update {file_path}",
                        content,
                        file.sha,
                        branch=branch_name
                    )
                except:
                    # File doesn't exist, create it
                    self.repo.create_file(
                        file_path,
                        f"Add {file_path}",
                        content,
                        branch=branch_name
                    )
            
            # Create pull request
            pr = self.repo.create_pull(
                title=title,
                body=body,
                head=branch_name,
                base=base_branch
            )
            
            return {
                "number": pr.number,
                "url": pr.html_url,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _get_issue_template(self, template_name: str) -> Optional[str]:
        """Get content of an issue template"""
        try:
            template_path = f".github/ISSUE_TEMPLATE/{template_name}.md"
            content = self.repo.get_contents(template_path)
            return content.decoded_content.decode('utf-8')
        except:
            return None
    
    def _apply_template(self, template: str, content: str) -> str:
        """Apply content to a template"""
        # Simple replacement - could be made more sophisticated
        return template.replace("<!-- Add your content here -->", content)

def main():
    parser = argparse.ArgumentParser(
        description='Create GitHub issues and pull requests for OpenMender',
        epilog='Example: python submission_helper.py issue --title "Bug fix" --body "Fixed issue"'
    )
    
    parser.add_argument(
        '--token',
        required=True,
        help='GitHub personal access token'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Issue parser
    issue_parser = subparsers.add_parser('issue', help='Create an issue')
    issue_parser.add_argument('--title', required=True, help='Issue title')
    issue_parser.add_argument('--body', required=True, help='Issue body')
    issue_parser.add_argument('--labels', help='Comma-separated list of labels')
    issue_parser.add_argument('--template', help='Name of issue template to use')
    
    # PR parser
    pr_parser = subparsers.add_parser('pr', help='Create a pull request')
    pr_parser.add_argument('--title', required=True, help='PR title')
    pr_parser.add_argument('--body', required=True, help='PR description')
    pr_parser.add_argument('--branch', required=True, help='New branch name')
    pr_parser.add_argument('--files', required=True, 
                          help='YAML file containing file paths and contents')
    pr_parser.add_argument('--base', default='main', 
                          help='Base branch (default: main)')
    
    args = parser.parse_args()
    
    helper = SubmissionHelper(args.token)
    
    if args.command == 'issue':
        labels = args.labels.split(',') if args.labels else None
        result = helper.create_issue(
            title=args.title,
            body=args.body,
            labels=labels,
            template=args.template
        )
        
    elif args.command == 'pr':
        with open(args.files, 'r') as f:
            files = yaml.safe_load(f)
        
        result = helper.create_pull_request(
            title=args.title,
            body=args.body,
            branch_name=args.branch,
            files=files,
            base_branch=args.base
        )
    
    print(yaml.dump(result, sort_keys=False))

if __name__ == "__main__":
    main()
