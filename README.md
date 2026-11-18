# triage-mcp

> LLM-powered log triage CLI for endpoint and cloud operations.

![CI](https://github.com/AK-Sw/triage-mcp/actions/workflows/ci.yml/badge.svg)

## What it does

Point it at any endpoint operations log — Intune IME, PSAppDeployToolkit, or macOS
install logs — and get back a structured triage in seconds: severity, error type,
root cause, and a suggested fix. Powered by the Google Gemini API (free tier).

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| LLM | Google Gemini (`gemini-1.5-flash`) via `google-generativeai` |
| CLI | `argparse` (stdlib) |
| CI | GitHub Actions — lint (flake8) + test (pytest) on every push |

## How it works

1. You point the CLI at a log file.
2. The script reads the file and sends the content to Gemini with a structured prompt.
3. Gemini returns: severity, error type, root cause, and suggested fix.
4. The result prints to your terminal.

The prompt is intentionally narrow — it frames Gemini as an endpoint operations
engineer so the output stays relevant to real-world triage work.

## Project structure

```
triage-mcp/
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions: lint + test on every push
├── sample_logs/
│   ├── ime_sample.log      # Intune Management Extension example
│   ├── psadt_sample.log    # PSAppDeployToolkit example
│   └── macos_sample.log    # macOS installd / MDM example
├── tests/
│   └── test_triage.py      # pytest unit tests (no API key needed)
├── triage.py               # main CLI entry point
├── requirements.txt
├── requirements-dev.txt
└── .gitignore
```

## How to run

### 1. Clone the repo

```bash
git clone https://github.com/AK-Sw/triage-mcp.git
cd triage-mcp
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your Gemini API key

Get a free key at [aistudio.google.com](https://aistudio.google.com)

```bash
# Windows
set GEMINI_API_KEY=your-key-here

# macOS / Linux
export GEMINI_API_KEY=your-key-here
```

### 4. Run

```bash
python triage.py sample_logs/ime_sample.log
```

## Sample output

```
Triaging: sample_logs/ime_sample.log

--- Triage Result ---
Severity: Warning
Error type: IME install-context error
Root cause: The Win32 application installer ran under the wrong execution
context (SYSTEM vs. user), triggering error 0x80070001.
Suggested fix:
1. Confirm the Intune app deployment is set to "System" context in the assignment.
2. Check the PSAppDeployToolkit log for the matching timestamp.
3. Re-deploy the package after correcting the install context.
```

## Running the tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

Tests mock the Gemini API so no key is needed to run them locally or in CI.

## Author

Aksh Swanni 
