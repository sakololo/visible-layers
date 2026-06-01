# Contributing to Visible Layers

Thank you for your interest in Visible Layers.

Visible Layers is an early-stage, human-in-the-loop OSS project for inspecting, organizing, and repairing layered character assets before 2D rigging workflows.

## Project Scope

Good contributions include:

- metadata improvements
- layer import and export helpers
- preview and comparison tools
- gap and overdraw detection
- documentation and examples
- tests for CLI behavior
- issue triage and small bug fixes

Please avoid framing the project as a complete replacement for artists, riggers, or existing layer-decomposition research. The project focuses on the bridge between automatic decomposition and production preparation.

## Development Setup

Install locally:

```bash
python -m pip install -e .
```

Run tests:

```bash
python -m unittest discover -s tests
```

Try the synthetic demo:

```bash
python -m visible_layers.cli demo --output demo-output
```

## Working On Issues

For new contributors:

1. Pick a small issue or open one describing the change.
2. Keep changes focused.
3. Add or update tests when behavior changes.
4. Update README or docs when the CLI surface changes.

## Pull Request Checklist

Before opening a pull request:

- [ ] Tests pass with `python -m unittest discover -s tests`
- [ ] CLI help is still accurate
- [ ] Documentation is updated if behavior changed
- [ ] Generated outputs are not committed
- [ ] The change keeps the workflow inspectable and human-in-the-loop

## Generated Files

Do not commit generated folders such as:

- `output/`
- `outputs/`
- `demo-output/`
- `work-demo-output/`
- `work-import-output/`
- `.test-tmp/`

These are ignored by `.gitignore`.

## Reporting Problems

When filing an issue, include:

- command used
- input shape or layer folder structure
- expected output
- actual output or error message
- operating system and Python version if relevant
