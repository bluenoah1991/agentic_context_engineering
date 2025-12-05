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
- [anthropic](https://github.com/anthropics/anthropic-sdk-python) Python SDK
- Node.js and npm

### Setup

1. Clone and install:
```bash
git clone https://github.com/bluenoah1991/agentic_context_engineering.git
cd agentic_context_engineering
npm install
```

2. Install required Python package:
```bash
pip3 install anthropic
```

3. Set environment variables for the LLM API:

| Environment Variable | Description | Required |
|---------------------|-------------|----------|
| `AGENTIC_CONTEXT_MODEL` | Model name for key point extraction (fallback: `ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `claude-sonnet-4-5-20250929`) | Optional |
| `AGENTIC_CONTEXT_API_KEY` | API key (fallback: `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_API_KEY`) | Optional |
| `AGENTIC_CONTEXT_BASE_URL` | API base URL (fallback: `ANTHROPIC_BASE_URL`) | Optional |

4. Restart Claude Code - hooks will be active across all your projects

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

### `/exit` Command Behavior

By default, the system does **not** update the playbook when using `/exit`. You can enable this behavior by setting `playbook_update_on_exit` to `true` in your `~/.claude/settings.json`:

```json
{
  "playbook_update_on_exit": true
}
```

### `/clear` Command Behavior

By default, the system does **not** update the playbook when using `/clear`. You can enable this behavior by setting `playbook_update_on_clear` to `true` in your `~/.claude/settings.json`:

```json
{
  "playbook_update_on_clear": true
}
```

### Customizing Prompts

Prompts are located in `~/.claude/prompts/`:

- `reflection.txt`: Template for key point extraction from reasoning trajectories
- `playbook.txt`: Template for injecting key points into sessions

## File Structure

```
.
├── install.js                 # Installation script
├── package.json               # npm package configuration
├── src/
│   ├── hooks/
│   │   ├── common.py           # Shared utilities
│   │   ├── session_end.py      # SessionEnd hook
│   │   ├── precompact.py       # PreCompact hook
│   │   └── user_prompt_inject.py  # UserPromptSubmit hook
│   ├── prompts/
│   │   ├── reflection.txt      # Key point extraction template
│   │   └── playbook.txt        # Injection template
│   └── settings.json           # Hook configuration template
└── README.md
```

## License

MIT
