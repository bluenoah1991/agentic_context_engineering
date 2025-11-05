#!/usr/bin/env python3
"""PreCompact Hook - Extract key points before context compaction"""
import json
import sys
import asyncio
from common import (
    load_playbook, save_playbook, load_transcript,
    extract_keypoints, update_playbook_data
)


async def main():
    input_data = json.load(sys.stdin)
    
    transcript_path = input_data.get("transcript_path")
    messages = load_transcript(transcript_path)
    
    if not messages:
        sys.exit(0)
    
    playbook = load_playbook()
    extraction_result = await extract_keypoints(messages, playbook, "precompact_reflection")
    playbook = update_playbook_data(playbook, extraction_result)
    save_playbook(playbook)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
