# bootstrap/tools/context_gatherer.py

import os
import base64
from github import Github
from typing import Dict, List, Optional
import yaml
import markdown
import re

class OpenMenderContext:
    """
    Gathers relevant context from the OpenMender repository to help
    contributors interact with LLMs more effectively.
    """
    
    def __init__(self, token: Optional[str] = None):
        """Initialize with optional GitHub token for higher rate limits"""
        try:
            self.g = Github(token) if token else Github()
            self.repo = self.g.get_repo("Quasimondo/OpenMender")
        except Exception as e:
            print(f"Warning: Could not initialize GitHub connection: {str(e)}")
            raise
        
    def get_basic_context(self) -> Dict:
        """Get basic repository information and structure"""
        return {
            "name": self.repo.name,
            "description": self.repo.description,
            "topics": self.repo.get_topics(),
            "structure": self._get_file_structure(),
            "readme": self._get_file_content("README.md"),
        }
    
    def get_current_issues(self) -> List[Dict]:
        """Get open issues with their labels and discussions"""
        issues = []
        for issue in self.repo.get_issues(state="open"):
            issues.append({
                "title": issue.title,
                "body": issue.body,
                "labels": [l.name for l in issue.labels],
                "comments": [c.body for c in issue.get_comments()],
                "number": issue.number
            })
        return issues
    
    def get_discussions(self) -> List[Dict]:
        """Get active discussions"""
        try:
            # Note: This is a workaround as PyGithub doesn't directly support discussions yet
            # We'll use the GraphQL API instead
            query = """
            {
              repository(owner: "Quasimondo", name: "OpenMender") {
                discussions(first: 10) {
                  nodes {
                    title
                    body
                    category {
                      name
                    }
                    comments(first: 10) {
                      nodes {
                        body
                      }
                    }
                  }
                }
              }
            }
            """
            
            if not hasattr(self.g, '_Github__requester'):
                return []  # Return empty list if no token provided
                
            result = self.g._Github__requester.requestJsonAndCheck(
                "POST",
                "https://api.github.com/graphql",
                input={'query': query}
            )
            
            discussions = []
            try:
                for discussion in result[0]['data']['repository']['discussions']['nodes']:
                    discussions.append({
                        "title": discussion['title'],
                        "body": discussion['body'],
                        "category": discussion['category']['name'],
                        "comments": [c['body'] for c in discussion['comments']['nodes']]
                    })
            except (KeyError, TypeError):
                pass
                
            return discussions
        except Exception as e:
            print(f"Warning: Could not fetch discussions: {str(e)}")
            return []
    
    def get_contribution_context(self) -> Dict:
        """Get context relevant for contributors"""
        return {
            "contributing_guide": self._get_file_content("CONTRIBUTING.md"),
            "code_of_conduct": self._get_file_content("CODE_OF_CONDUCT.md"),
            "issue_templates": self._get_issue_templates(),
            "recent_prs": self._get_recent_prs()
        }
    
    def get_component_context(self, component: str) -> Dict:
        """Get context for a specific component (bootstrap or agent)"""
        if component not in ["bootstrap", "agent"]:
            raise ValueError("Component must be 'bootstrap' or 'agent'")
            
        return {
            "readme": self._get_file_content(f"{component}/README.md"),
            "structure": self._get_file_structure(component),
            "recent_changes": self._get_recent_changes(component)
        }
    
    def format_for_llm(self, context_type: str = "all") -> str:
        """
        Format gathered context in a way that's optimal for LLM consumption
        """
        contexts = {
            "basic": self.get_basic_context,
            "issues": self.get_current_issues,
            "discussions": self.get_discussions,
            "contribution": self.get_contribution_context,
            "bootstrap": lambda: self.get_component_context("bootstrap"),
            "agent": lambda: self.get_component_context("agent")
        }
        
        if context_type not in contexts and context_type != "all":
            raise ValueError(f"Invalid context type. Must be one of: {', '.join(contexts.keys())} or 'all'")
        
        if context_type == "all":
            result = {}
            for k, v in contexts.items():
                result[k] = v()
        else:
            result = contexts[context_type]()
            
        return self._format_context(result)
    
    def _get_file_content(self, path: str) -> Optional[str]:
        """Get content of a file from the repository"""
        try:
            content = self.repo.get_contents(path)
            return base64.b64decode(content.content).decode('utf-8')
        except:
            return None
    
    def _get_file_structure(self, path: str = "") -> Dict:
        """Get repository structure starting from path"""
        structure = {}
        try:
            contents = self.repo.get_contents(path)
            for content in contents:
                if content.type == "dir":
                    structure[content.name] = self._get_file_structure(content.path)
                else:
                    structure[content.name] = content.type
        except:
            pass
        return structure
    
    def _get_issue_templates(self) -> Dict:
        """Get issue templates configuration"""
        templates = {}
        template_path = ".github/ISSUE_TEMPLATE"
        try:
            for template in self.repo.get_contents(template_path):
                if template.name.endswith(('.yml', '.yaml')):
                    content = base64.b64decode(template.content).decode('utf-8')
                    templates[template.name] = yaml.safe_load(content)
        except:
            pass
        return templates
    
    def _get_recent_prs(self, limit: int = 5) -> List[Dict]:
        """Get recent pull requests"""
        prs = []
        for pr in self.repo.get_pulls(state="all", sort="updated", direction="desc")[:limit]:
            prs.append({
                "title": pr.title,
                "body": pr.body,
                "state": pr.state,
                "labels": [l.name for l in pr.labels]
            })
        return prs
    
    def _get_recent_changes(self, path: str, limit: int = 5) -> List[Dict]:
        """Get recent commits affecting a specific path"""
        commits = []
        for commit in self.repo.get_commits(path=path)[:limit]:
            commits.append({
                "message": commit.commit.message,
                "date": commit.commit.author.date.isoformat(),
                "files": [f.filename for f in commit.files]
            })
        return commits
    
    def _format_context(self, context: Dict) -> str:
        """Format context in a way that's optimal for LLM consumption"""
        # This could be customized based on what works best with different LLMs
        return f"""
# OpenMender Context

## Repository Information
{yaml.dump(context, sort_keys=False, width=80, indent=2)}
        """

def main():
    """CLI interface for the context gatherer"""
    import argparse
    parser = argparse.ArgumentParser(
        description='Gather context from OpenMender repository for LLM interactions',
        epilog='Example: python context_gatherer.py --context issues --output issues.txt'
    )
    
    parser.add_argument(
        '--token', 
        help='GitHub personal access token for authentication (increases rate limits)'
    )
    
    parser.add_argument(
        '--context', 
        choices=['all', 'basic', 'issues', 'discussions', 'contribution', 'bootstrap', 'agent'],
        default='all', 
        help='''Type of context to gather:
                all: Everything
                basic: Repository info and structure
                issues: Current open issues
                discussions: Active discussions
                contribution: Contributing guidelines and templates
                bootstrap: Bootstrap system context
                agent: Agent system context'''
    )
    parser.add_argument(
        '--output', 
        help='Output file path (if not specified, prints to stdout)'
    )
    
    args = parser.parse_args()
    
    gatherer = OpenMenderContext(args.token)
    result = gatherer.format_for_llm(args.context)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
    else:
        print(result)

if __name__ == "__main__":
    main()
