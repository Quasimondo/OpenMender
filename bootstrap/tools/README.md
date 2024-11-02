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

Output to file:
```bash
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
```

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
