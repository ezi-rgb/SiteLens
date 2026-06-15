# Contributing to SiteLens

Thanks for considering contributing! This project is beginner-friendly and
we welcome all skill levels.

## Ways to Contribute

- Report bugs or suggest features via [Issues](../../issues)
- Add a new security check (see "Adding a Check" below)
- Improve documentation
- Help review pull requests

## Development Setup

1. Fork this repository
2. Clone your fork: `git clone git@github.com:YOUR_USERNAME/SiteLens.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it and install dependencies: `pip install -r requirements.txt`
5. Run tests: `pytest`

## Adding a New Check

Each check lives in `src/sitelens/checks/` and follows this structure:

\`\`\`python
def run(domain: str) -> dict:
    """
    Returns:
        {
            "name": "Check Name",
            "severity": "info" | "low" | "medium" | "high",
            "passed": bool,
            "message": "Human-readable explanation",
            "recommendation": "How to fix this"
        }
    """
\`\`\`

Add a corresponding test in `tests/`.

## Pull Request Process

1. Create a branch: `git checkout -b feature/your-feature-name`
2. Make your changes, with tests
3. Run `pytest` to confirm everything passes
4. Push and open a Pull Request, describing what changed and why

## Code of Conduct

Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before participating.
