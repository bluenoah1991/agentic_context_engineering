# Agentic Context Engineering

A simplified implementation of Agentic Context Engineering (ACE) for Claude Code that automatically learns and accumulates key points from reasoning trajectories.

## Features

- **Automatic Key Point Extraction**: Learns from reasoning trajectories and extracts valuable insights
- **Score-Based Filtering**: Evaluates key points across trajectories and removes unhelpful ones
- **Context Injection**: Automatically injects accumulated knowledge at the start of new sessions
- **Multiple Triggers**: Works on session end, manual clear (`/clear`), and context compaction

## Installation

### Prerequisites

- Python 3.8+
- Claude Code
- [claude-agent-sdk](https://github.com/anthropics/claude-agent-sdk-python)

### Setup

1. Clone this repository:
```bash
git clone https://github.com/PaodingSoftware/agentic_context_engineering.git
cd agentic_context_engineering
```

2. Install required Python package:
```bash
pip install claude-agent-sdk
```

3. Enable hooks in Claude Code:
   - The `.claude/settings.json` file is already configured with the necessary hooks
   - Hooks will activate automatically when you start Claude Code in this directory

## How It Works

### Hooks

The system uses three types of hooks:

1. **UserPromptSubmit**: Injects accumulated key points at the start of each new session
2. **SessionEnd**: Extracts key points when a session ends
3. **PreCompact**: Extracts key points before context compaction

### Key Point Lifecycle

1. **Extraction**: At the end of each session, the system analyzes the reasoning trajectories and extracts new key points
2. **Evaluation**: Existing key points are evaluated based on the reasoning trajectories and rated as helpful/harmful/neutral
3. **Scoring**: 
   - Helpful: +1 point
   - Harmful: -3 points
   - Neutral: -1 point
4. **Pruning**: Key points with score ≤ -5 are automatically removed
5. **Injection**: Surviving key points are injected into new sessions

## Configuration

### Diagnostic Mode

To enable detailed logging of LLM interactions:

```bash
touch .claude/diagnostic_mode
```

Diagnostic logs will be saved to `.claude/diagnostic/` with timestamped filenames.

To disable:
```bash
rm .claude/diagnostic_mode
```

### Customizing Prompts

Prompts are located in `.claude/prompts/`:

- `reflection.txt`: Template for key point extraction from reasoning trajectories
- `playbook.txt`: Template for injecting key points into sessions

## File Structure

```
.
├── .claude/
│   ├── hooks/
│   │   ├── common.py           # Shared utilities
│   │   ├── session_end.py      # SessionEnd hook
│   │   ├── precompact.py       # PreCompact hook
│   │   └── user_prompt_inject.py  # UserPromptSubmit hook
│   ├── prompts/
│   │   ├── reflection.txt      # Key point extraction template
│   │   └── playbook.txt        # Injection template
│   ├── settings.json           # Hook configuration
│   ├── playbook.json          # Generated: accumulated key points
│   ├── last_session.txt       # Generated: session tracking
│   └── diagnostic/            # Generated: debug logs (if enabled)
├── .gitignore
└── README.md
```

## License

MIT
