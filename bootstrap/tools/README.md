# OpenMender Tools

This directory contains utilities and tools that help with the development and operation of OpenMender.

## Available Tools

### Context Gatherer
`context_gatherer.py` - A utility to gather repository context for LLM interactions.

#### Purpose
Helps contributors interact with LLMs by providing structured context about the OpenMender repository, its issues, discussions, and components.

#### Installation
```bash
pip install -r requirements.txt
```

#### Usage
Basic usage:
```bash
python context_gatherer.py --context basic
```

With GitHub token (recommended):
```bash
python context_gatherer.py --token YOUR_GITHUB_TOKEN --context all
```

Available context types:
- `all`: Everything
- `basic`: Repository info and structure
- `issues`: Current open issues
- `discussions`: Active discussions
- `contribution`: Contributing guidelines and templates
- `bootstrap`: Bootstrap system context
- `agent`: Agent system context
- `files`: File structure and contents
- `tools`: Source files in tools directory

Additional options:
```bash
# Get file structure from specific directory
python context_gatherer.py --context files --directory bootstrap/tools

# Get source files with specific extensions
python context_gatherer.py --context tools --extensions .py,.md

# Control maximum file size for content inclusion
python context_gatherer.py --context files --max-file-size 10000

# Output to file instead of stdout
python context_gatherer.py --context issues --output issues.txt
```

#### Example Integration with LLMs
```python
# Example with OpenAI's GPT (you'll need the openai package installed)
import openai
from context_gatherer import OpenMenderContext

# Get context
gatherer = OpenMenderContext(github_token)
context = gatherer.format_for_llm("basic")

# Use with LLM
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant for the OpenMender project."},
        {"role": "user", "content": f"Given this context about OpenMender:\n\n{context}\n\nWhat would be a good first contribution?"}
    ]
)

# Example getting source code for analysis
source_files = gatherer.format_for_llm("tools")
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant for the OpenMender project."},
        {"role": "user", "content": f"Here are the source files:\n\n{source_files}\n\nCan you suggest improvements?"}
    ]
)
```

### Submission Helper
`submission_helper.py` - A utility for creating GitHub issues and pull requests programmatically.

#### Purpose
Helps automate the creation of issues and pull requests, particularly useful for automated improvements and updates.

#### Installation
```bash
pip install -r requirements.txt
```

#### Usage
Creating an issue:
```bash
python submission_helper.py --token YOUR_TOKEN issue \
    --title "Issue Title" \
    --body "Issue description" \
    --labels "enhancement,help wanted"
```

Creating a pull request:
```bash
# First create a files.yml with your changes:
# files.yml
"path/to/file.py": |
    # Your file content here
"another/file.md": |
    # Another file content

# Then create the PR
python submission_helper.py --token YOUR_TOKEN pr \
    --title "PR Title" \
    --body "PR description" \
    --branch feature/your-feature \
    --files files.yml
```

Options:
- Issue creation:
  - `--title`: Issue title (required)
  - `--body`: Issue description (required)
  - `--labels`: Comma-separated list of labels
  - `--template`: Name of issue template to use

- Pull request creation:
  - `--title`: PR title (required)
  - `--body`: PR description (required)
  - `--branch`: Name for the new branch (required)
  - `--files`: YAML file containing file paths and contents (required)
  - `--base`: Base branch to create PR against (default: main)

## Contributing New Tools

When adding new tools to this directory:

1. Create a dedicated Python file or subdirectory
2. Include requirements.txt if needed
3. Add documentation to this README
4. Include helpful comments in the code
5. Add error handling and useful error messages
6. Include --help documentation
7. Consider adding tests

## Tool Development Guidelines

1. **Usability**
   - Clear command-line interface
   - Helpful error messages
   - Good documentation

2. **Reliability**
   - Error handling
   - Input validation
   - Graceful degradation

3. **Integration**
   - Works with other tools
   - Follows project conventions
   - Supports automation

4. **Security**
   - Safe token handling
   - Input sanitization
   - Rate limiting awareness

## Future Tools

Planned additions:
- PR template validator
- Fix pattern analyzer
- Test generation helper
- Documentation updater

Suggest new tools by opening an issue with the `tool-proposal` label.
