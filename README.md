# OpenMender

## TL;DR
OpenMender is building a distributed system that autonomously improves open source software. Want to help? Check out our [Getting Started Guide](GETTING_STARTED.md) to learn how to use our development tools with your preferred LLM to contribute improvements.


## Manifesto

Software is the invisible fabric that shapes our modern world. Open source software, built through the collaborative effort of countless individuals, forms the foundation of this digital infrastructure. Yet, across millions of repositories, there are countless small imperfections: bugs waiting to be fixed, optimizations waiting to be made, security vulnerabilities waiting to be patched.

We envision a future where artificial intelligence doesn't replace human developers but augments them - working tirelessly in the background to improve the quality of our shared digital commons. Like a careful gardener tending to a vast garden, OpenMender observes, analyzes, and thoughtfully improves the digital commons we all share.

### Our Mission
To create an autonomous, distributed system that continuously improves open source software through careful observation, intelligent analysis, and measured intervention. We believe that by combining human creativity with machine persistence, we can elevate the quality of the entire open source ecosystem.

### Our Principles
1. **Collaborative Intelligence**: We're not building a replacement for human developers, but a helper that handles the routine so humans can focus on the creative.

2. **Democratic Participation**: Anyone can contribute computing power, code, or knowledge to make the system better. The project itself grows through collective intelligence.

3. **Verifiable Improvement**: Every change must be provably beneficial, tested, and safe. We believe in progress through small, confident steps rather than large, risky leaps.

4. **Open Process**: The system that builds the system is as important as the end result. We're creating a framework that grows from a simple README to a sophisticated AI agent through transparent, collaborative evolution.

5. **Distributed Ownership**: No single entity should control this system. Like the open source projects it aims to improve, it belongs to the community.

6. **Preserve Community Growth**: We recognize that easily fixable issues often serve as valuable entry points for new contributors. OpenMender will:
   - Respect issues tagged as "good first issue", "first-timers-only", "beginner friendly" etc.
   - Focus on issues that have remained unaddressed for extended periods
   - Prioritize fixes for issues that might deter rather than encourage new contributors
   - Work alongside human contributors, not replace them6. 

### Why Now?
We stand at a unique moment in technological history. The tools for automated code analysis, generation, and verification have reached a level of sophistication that makes this vision possible. Yet we're also seeing the limitations of centralized AI systems. By creating a distributed, community-driven approach to code improvement, we can harness the power of AI while maintaining the open, collaborative spirit that makes open source software great.

## Project Structure

OpenMender consists of two distinct but related systems:

1. **The Bootstrap System** - A self-improving framework that helps build the agent
2. **The Mender Agent** - The final autonomous system that will improve open source projects

### The Bootstrap System
Located in `/bootstrap`, this is our starting point. It's a framework that:
- Evaluates and merges pull requests
- Gradually automates its own processes
- Helps coordinate the collaborative development
- Eventually becomes capable of building the agent itself

The bootstrap system starts simple (mainly manual) and grows more sophisticated through community contributions, eventually becoming capable of autonomous operation.

### The Mender Agent
Located in `/agent`, this is our end goal. Once built, it will:
- Explore GitHub repositories
- Identify fixable issues
- Generate and verify fixes
- Submit improvements
- Operate in a distributed manner

The agent itself will be built gradually through the bootstrap system, ensuring quality and safety at each step.

## Current Phase
We are at the very beginning, focusing on building the bootstrap system. The current priorities are:

1. Setting up basic PR evaluation criteria
2. Creating initial contribution guidelines
3. Establishing quality control mechanisms
4. Building the first automated components

## How to Contribute
You can contribute to either system:

### Bootstrap System Contributions
- Improve PR evaluation logic
- Add automation capabilities
- Enhance quality checks
- Document patterns and processes

### Agent System Contributions
- Design architecture
- Define fix patterns
- Create analysis tools
- Develop distribution mechanisms

## Getting Started
1. Star this repository to show interest
2. Check the issues for current tasks
3. Read CONTRIBUTING.md for contribution guidelines
4. Join discussions in the Discussions tab

## Future Vision
As the project evolves, we aim to:
- Create a self-improving system
- Build a distributed computing network
- Develop AI-assisted code improvement capabilities
- Create a reputation system for contributors

## License
[![License: CC0-1.0](https://img.shields.io/github/license/Quasimondo/OpenMender)](LICENSE)

## Contact
- Create an issue for questions
- Join our [Discord/Matrix] channel (coming soon)
- Follow project updates

## Related Projects

### AI-Assisted Development
- [Claudine](https://github.com/xemantic/claudine) - An AI agent using Claude to interact with local systems and assist developers through command-line tools. Focuses on general-purpose assistance and local system interaction.


---

> "Small improvements, consistently made, create extraordinary results."
