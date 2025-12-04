#!/usr/bin/env python3
import json
import sys
import asyncio
from common import (
    load_playbook, save_playbook, load_transcript,
    extract_keypoints, update_playbook_data, clear_session,
    load_settings
)


async def main():
    input_data = json.load(sys.stdin)

    transcript_path = input_data.get("transcript_path")
    messages = load_transcript(transcript_path)

    if not messages:
        sys.exit(0)

    settings = load_settings()
    update_on_exit = settings.get("playbook_update_on_exit", False)
    update_on_clear = settings.get("playbook_update_on_clear", False)

    reason = input_data.get("reason", "")
    
    # Skip playbook update for /exit command when setting is disabled
    if not update_on_exit and reason == "prompt_input_exit":
        sys.exit(0)
    
    # Skip playbook update for /clear command when setting is disabled
    if not update_on_clear and reason == "clear":
        sys.exit(0)

    playbook = load_playbook()
    extraction_result = await extract_keypoints(messages, playbook, "session_end_reflection")
    playbook = update_playbook_data(playbook, extraction_result)
    save_playbook(playbook)

    clear_session()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
