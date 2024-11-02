import pytest
from unittest.mock import Mock, patch, MagicMock
import base64
import yaml
from bootstrap.tools.context_gatherer import OpenMenderContext

# Mock response classes
class MockContent:
    def __init__(self, path: str, type: str = "file", content: str = "", size: int = 0):
        self.path = path
        self.name = path.split("/")[-1]
        self.type = type
        self._content = base64.b64encode(content.encode()).decode()
        self.size = size
        self.sha = "mock_sha"
    
    @property
    def content(self):
        return self._content

class MockCommit:
    def __init__(self, message: str, date: str, files: list):
        from datetime import datetime
        self.commit = Mock(
            message=message,
            author=Mock(date=datetime.fromisoformat(date.replace('Z', '+00:00'))),
        )
        self.files = [Mock(filename=f) for f in files]

class MockRepo:
    def __init__(self):
        self.name = "OpenMender"
        self.description = "Test Description"
        self._topics = ["ai", "automation"]
        self._files = {
            "README.md": "# OpenMender\nTest readme",
            "CONTRIBUTING.md": "# Contributing\nTest guide",
            "CODE_OF_CONDUCT.md": "# Code of Conduct\nTest conduct",
            ".github/ISSUE_TEMPLATE/bug.yml": "name: Bug Report\nfields: []",
            "bootstrap/README.md": "# Bootstrap\nTest bootstrap readme"
        }
        self._issues = []
        self._prs = []
        
    def get_topics(self):
        return self._topics
        
    def get_contents(self, path):
        if path == "":  # Root directory
            return [
                MockContent("README.md", "file", self._files["README.md"]),
                MockContent("bootstrap", "dir"),
                MockContent("agent", "dir")
            ]
        
        if path in self._files:
            return MockContent(path, "file", self._files[path])
            
        if path == ".github/ISSUE_TEMPLATE":
            return [MockContent("bug.yml", "file", self._files[".github/ISSUE_TEMPLATE/bug.yml"])]
            
        raise Exception(f"File not found: {path}")
        
    def get_issues(self, state="open"):
        return self._issues
        
    def get_pulls(self, state="all", sort="updated", direction="desc"):
        return self._prs[:5]  # Respect the limit
        
    def get_commits(self, path=""):
        return [
            MockCommit("Test commit", "2024-01-01T00:00:00Z", ["test.py"]),
            MockCommit("Another commit", "2024-01-02T00:00:00Z", ["other.py"])
        ]

@pytest.fixture
def mock_github():
    with patch('bootstrap.tools.context_gatherer.Github') as mock_gh:
        mock_repo = MockRepo()
        mock_gh.return_value.get_repo.return_value = mock_repo
        yield mock_gh

class TestOpenMenderContext:
    
    def test_initialization(self, mock_github):
        """Test basic initialization"""
        context = OpenMenderContext("fake_token")
        assert context.repo.name == "OpenMender"
        
    def test_initialization_no_token(self, mock_github):
        """Test initialization without token"""
        context = OpenMenderContext()
        assert context.repo.name == "OpenMender"
        
    def test_get_basic_context(self, mock_github):
        """Test getting basic repository context"""
        context = OpenMenderContext("fake_token")
        basic = context.get_basic_context()
        
        assert basic["name"] == "OpenMender"
        assert basic["description"] == "Test Description"
        assert "ai" in basic["topics"]
        assert basic["readme"].startswith("# OpenMender")
        assert isinstance(basic["structure"], dict)
        
    def test_get_current_issues(self, mock_github):
        """Test getting current issues"""
        context = OpenMenderContext("fake_token")
        issues = context.get_current_issues()
        assert isinstance(issues, list)
        
    def test_get_contribution_context(self, mock_github):
        """Test getting contribution context"""
        context = OpenMenderContext("fake_token")
        contrib = context.get_contribution_context()
        
        assert contrib["contributing_guide"].startswith("# Contributing")
        assert contrib["code_of_conduct"].startswith("# Code of Conduct")
        assert isinstance(contrib["issue_templates"], dict)
        assert isinstance(contrib["recent_prs"], list)
        
    def test_get_component_context(self, mock_github):
        """Test getting component specific context"""
        context = OpenMenderContext("fake_token")
        
        # Test bootstrap component
        bootstrap = context.get_component_context("bootstrap")
        assert bootstrap["readme"].startswith("# Bootstrap")
        assert isinstance(bootstrap["structure"], dict)
        assert isinstance(bootstrap["recent_changes"], list)
        
        # Test invalid component
        with pytest.raises(ValueError):
            context.get_component_context("invalid")
            
    def test_get_file_tree(self, mock_github):
        """Test getting file tree"""
        context = OpenMenderContext("fake_token")
        tree = context.get_file_tree()
        
        assert isinstance(tree, dict)
        assert "README.md" in tree
        assert tree["README.md"]["type"] == "file"
        assert "content" in tree["README.md"]
        
    def test_get_source_files(self, mock_github):
        """Test getting source files"""
        context = OpenMenderContext("fake_token")
        files = context.get_source_files()
        
        assert isinstance(files, dict)
        for file_info in files.values():
            assert "content" in file_info
            assert "size" in file_info
            assert "sha" in file_info
            
    def test_format_for_llm(self, mock_github):
        """Test LLM formatting"""
        context = OpenMenderContext("fake_token")
        
        # Test specific context type
        basic_format = context.format_for_llm("basic")
        assert "OpenMender Context" in basic_format
        assert "Repository Information" in basic_format
        
        # Test invalid context type
        with pytest.raises(ValueError):
            context.format_for_llm("invalid")
        
        # Test all context
        all_format = context.format_for_llm("all")
        assert "OpenMender Context" in all_format
        assert "Repository Information" in all_format
        
    def test_error_handling(self, mock_github):
        """Test error handling in various scenarios"""
        context = OpenMenderContext("fake_token")
        
        # Test non-existent file
        assert context._get_file_content("nonexistent.md") is None
        
        # Test empty file structure
        empty_structure = context._get_file_structure("nonexistent")
        assert empty_structure == {}
