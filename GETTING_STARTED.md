# Getting Started with OpenMender

Welcome to OpenMender! This guide will help you get started with contributing to the project using our development tools.

## Initial Setup

1. Clone the repository:
```bash
git clone https://github.com/Quasimondo/OpenMender.git
cd OpenMender
```

2. Install dependencies:
```bash
pip install -r bootstrap/tools/requirements.txt
```

3. Get a GitHub token:
- Go to GitHub.com → Settings → Developer settings → Personal access tokens
- Create a new token with 'repo' scope
- Save this token securely

## Development Tools

OpenMender provides tools to help you interact with the project effectively:

### 1. Context Gatherer
The context gatherer helps you understand the project by collecting relevant information that you can feed into your preferred LLM (like ChatGPT).

```bash
# Get basic project information
python bootstrap/tools/context_gatherer.py --token YOUR_TOKEN --context basic

# Get source code of tools
python bootstrap/tools/context_gatherer.py --token YOUR_TOKEN --context tools

# Get current issues
python bootstrap/tools/context_gatherer.py --token YOUR_TOKEN --context issues
```

Use this tool to:
- Understand project structure and components
- Get context about current issues and discussions
- Analyze source code for improvements
- Generate LLM prompts with accurate project context

### 2. Submission Helper
The submission helper allows you to programmatically create issues and pull requests.

```bash
# Create an issue
python bootstrap/tools/submission_helper.py --token YOUR_TOKEN issue \
    --title "Your Issue Title" \
    --body "Issue description" \
    --labels "enhancement"

# Create a pull request (requires a files.yml)
python bootstrap/tools/submission_helper.py --token YOUR_TOKEN pr \
    --title "Your PR Title" \
    --body "PR description" \
    --branch feature/your-feature \
    --files your-changes.yml
```

Use this tool to:
- Report issues you've discovered
- Submit improvements automatically
- Propose changes programmatically
- Automate repetitive tasks

## Typical Workflow

1. **Understand the Context**
```bash
# Get project overview
python bootstrap/tools/context_gatherer.py --token YOUR_TOKEN --context basic > context.txt

# Feed this into your preferred LLM:
"Given this OpenMender context: [content of context.txt], what would be a good first contribution?"
```

2. **Analyze Specific Areas**
```bash
# Get source code for analysis
python bootstrap/tools/context_gatherer.py --token YOUR_TOKEN --context tools > tools.txt

# Ask your LLM:
"Looking at this code: [content of tools.txt], what improvements could be made?"
```

3. **Submit Contributions**
```bash
# Create an issue for discussion
python bootstrap/tools/submission_helper.py --token YOUR_TOKEN issue \
    --title "Proposal: Improve error handling" \
    --body "Based on analysis, we should..."

# After discussion, submit changes
python bootstrap/tools/submission_helper.py --token YOUR_TOKEN pr \
    --title "Add improved error handling" \
    --body "Implements improvements discussed in #123" \
    --branch feature/error-handling \
    --files changes.yml
```

## Best Practices

1. **Using with LLMs**
- Always provide relevant context using the context gatherer
- Break down large changes into smaller, focused improvements
- Use LLMs to analyze code but verify their suggestions

2. **Making Contributions**
- Start with small, well-defined changes
- Create an issue for discussion before major changes
- Use clear, descriptive titles and descriptions
- Reference related issues in your PRs

3. **Tool Usage**
- Keep your GitHub token secure
- Use appropriate labels for issues
- Follow the branch naming convention (feature/, fix/, docs/, etc.)
- Test changes locally before submitting

## Next Steps

- Review the [main README](README.md) for project overview
- Check [open issues](https://github.com/Quasimondo/OpenMender/issues) for tasks
- Join project [discussions](https://github.com/Quasimondo/OpenMender/discussions)
- Read the [contributing guidelines](CONTRIBUTING.md)

## Getting Help

- Create an issue with the 'question' label
- Join the project discussions
- Check the tool-specific documentation in bootstrap/tools/

Remember: OpenMender is about improving open source software collaboratively. Start small, learn from the community, and help make the ecosystem better!
