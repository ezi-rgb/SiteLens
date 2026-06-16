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

Checks are automatically discovered — you don't need to register them anywhere!

1. Create a new file in `src/sitelens/checks/`, e.g. `cookie_check.py`
2. Define a `run(domain: str) -> dict` function following this contract:

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

3. Add a corresponding test in `tests/test_your_check.py`
4. That's it — your check will run automatically as part of every scan.

## Pull Request Process

1. Create a branch: `git checkout -b feature/your-feature-name`
2. Make your changes, with tests
3. Run `pytest` to confirm everything passes
4. Push and open a Pull Request, describing what changed and why

## Code of Conduct

Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before participating.
