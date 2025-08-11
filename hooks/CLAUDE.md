# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Claude Code hooks system that provides lifecycle hooks for Claude Code sessions. The hooks enable security checks, notifications, logging, and text-to-speech (TTS) announcements for various events during a Claude Code session.

## Architecture

### Core Hook Scripts
The hooks system consists of Python scripts that are triggered at different lifecycle events:

- **pre_tool_use.py**: Validates tool usage before execution, blocks dangerous commands (rm -rf, env exposure)
- **post_tool_use.py**: Logs tool usage after execution
- **notification.py**: Announces when Claude needs user input via TTS
- **stop.py**: Announces task completion with random friendly messages via TTS
- **subagent_stop.py**: Announces when subagent tasks complete
- **user_prompt_submit.py**: Logs user prompts for audit trails

### Supporting Infrastructure

- **utils/tts/**: TTS implementations (ElevenLabs, OpenAI, pyttsx3)
- **utils/llm/**: LLM helpers for Anthropic and OpenAI
- **logs/**: JSON log files for each hook type
- **smart-lint.sh**: Multi-language linting and code quality checks
- **common-helpers.sh**: Shared bash utilities

## Development Commands

### Running Hook Scripts
All Python scripts use `uv` for dependency management and execution:
```bash
# Scripts are executable with uv shebang
./pre_tool_use.py
./notification.py
./stop.py
```

### Code Quality Checks
```bash
# Run comprehensive linting for detected project type
./smart-lint.sh

# Fast mode (skip slow checks like security scans)
./smart-lint.sh --fast

# Debug mode for verbose output
./smart-lint.sh --debug
```

### Testing Hooks
```bash
# Test pre-tool-use hook with dangerous command detection
echo '{"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}}' | ./pre_tool_use.py

# Test notification with TTS
./notification.py --test
```

## Key Features

### Security Protection
- **pre_tool_use.py** blocks:
  - Dangerous rm commands (rm -rf /, rm -rf ~, etc.)
  - Environment variable exposure (env | grep, printenv)
  - Provides detailed security violation messages

### TTS Integration
Priority order for TTS providers:
1. ElevenLabs (if ELEVENLABS_API_KEY set)
2. pyttsx3 (fallback, no API key required)
3. OpenAI TTS currently disabled in code

### Logging System
All hooks log to `logs/` directory:
- Structured JSON format
- Includes session ID, transcript path, working directory
- Tool inputs and outputs captured

## Environment Variables

Optional API keys for enhanced functionality:
- `ELEVENLABS_API_KEY`: Enable ElevenLabs TTS
- `OPENAI_API_KEY`: OpenAI integration (TTS currently disabled)
- `ENGINEER_NAME`: Personalized TTS announcements

## Script Patterns

### Python Scripts
- Use `#!/usr/bin/env -S uv run --script` shebang
- Inline dependencies via PEP 723 script metadata
- Structured argparse for CLI options
- JSON input/output for hook communication

### Bash Scripts
- Comprehensive error handling without `set -e`
- Project type detection (Go, Python, JS/TS, Ruby, etc.)
- Colored output with status indicators
- Exit codes: 0 (success), 1 (error), 2 (issues found)

## Important Implementation Details

### Hook Event Flow
1. Claude Code triggers hook event
2. Hook script receives JSON on stdin
3. Script processes event (validate, log, notify)
4. Script may block execution (pre_tool_use)
5. Exit code determines continuation

### Cache Files
- `.users_cache.json`: Cached user data
- `.channels_cache_v2.json`: Cached channel data
- Used by notification system for context

### Smart Linting
The `smart-lint.sh` script auto-detects project type and runs appropriate linters:
- Python: ruff, mypy, bandit
- JavaScript/TypeScript: prettier, eslint
- Go: gofmt, govet, golangci-lint
- Ruby: rubocop, reek