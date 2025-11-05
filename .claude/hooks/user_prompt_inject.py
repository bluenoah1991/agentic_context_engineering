#!/usr/bin/env python3
"""User Prompt Hook - Inject playbook on first message of new session"""
import json
import sys
from pathlib import Path
from common import (
    load_playbook, load_template, is_diagnostic_mode, 
    save_diagnostic, get_project_dir
)


def is_first_message(session_id: str) -> bool:
    """Check if this is the first message of a new session"""
    session_file = get_project_dir() / ".claude" / "last_session.txt"
    
    if session_file.exists():
        last_session_id = session_file.read_text().strip()
        return session_id != last_session_id
    
    return True


def mark_session(session_id: str):
    """Mark current session as seen"""
    session_file = get_project_dir() / ".claude" / "last_session.txt"
    session_file.parent.mkdir(parents=True, exist_ok=True)
    session_file.write_text(session_id)


def format_playbook(playbook: dict) -> str:
    """Format playbook for injection"""
    key_points = playbook.get('key_points', [])
    if not key_points:
        return ""
    
    key_points_text = "\n".join(
        f"- {kp['text'] if isinstance(kp, dict) else kp}"
        for kp in key_points
    )
    
    template = load_template("playbook.txt")
    return template.format(key_points=key_points_text)


def main():
    input_data = json.load(sys.stdin)
    session_id = input_data.get('session_id', 'unknown')
    
    if not is_first_message(session_id):
        print(json.dumps({}), flush=True)
        sys.exit(0)
    
    playbook = load_playbook()
    context = format_playbook(playbook)
    
    if not context:
        print(json.dumps({}), flush=True)
        sys.exit(0)
    
    if is_diagnostic_mode():
        save_diagnostic(context, "user_prompt_inject")
    
    response = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context
        }
    }
    
    sys.stdout.reconfigure(encoding='utf-8')
    print(json.dumps(response), flush=True)
    
    mark_session(session_id)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        print(json.dumps({}), flush=True)
        sys.exit(1)
