import argparse
import os
import sys

import google.generativeai as genai


def load_log(path: str) -> str:
    """Read a log file and return its contents as a string."""
    with open(path, "r", errors="replace") as f:
        return f.read()


def triage_log(log_content: str, api_key: str) -> str:
    """Send log content to Gemini and return a structured triage result."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""You are an endpoint operations engineer. Analyze the log below and respond with:
1. Severity: (Critical / Warning / Info)
2. Error type: (brief label)
3. Root cause: (1-2 sentences)
4. Suggested fix: (1-3 actionable steps)

Log:
{log_content[:4000]}
"""
    response = model.generate_content(prompt)
    return response.text


def main():
    parser = argparse.ArgumentParser(
        description="triage-mcp: LLM-powered log triage for endpoint and cloud operations"
    )
    parser.add_argument("log_file", help="Path to the log file to triage")
    parser.add_argument(
        "--api-key",
        help="Gemini API key (or set GEMINI_API_KEY env var)",
    )
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print(
            "Error: Gemini API key required. Set GEMINI_API_KEY or use --api-key.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not os.path.exists(args.log_file):
        print(f"Error: File not found: {args.log_file}", file=sys.stderr)
        sys.exit(1)

    print(f"Triaging: {args.log_file}")
    log_content = load_log(args.log_file)
    result = triage_log(log_content, api_key)
    print("
--- Triage Result ---")
    print(result)


if __name__ == "__main__":
    main()
