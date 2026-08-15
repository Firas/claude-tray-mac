# claude-tray-mac

> Written by [Claude](https://claude.com/claude-code) (Anthropic's AI, in
> conversation with the repo owner) — not hand-coded by a human.
>
> Note: retired from active use on the owner's Mac in favor of the
> [ClaudeTokenMonitor](https://github.com/Firas/ClaudeTokenMonitor)
> companion project (native Swift, was already running) — kept here as a
> working alternative using a different data source (Keychain / Claude
> Code CLI instead of Claude Desktop cookies).

Claude usage (5-hour + weekly token budget remaining) in the macOS menu
bar. Python, built on [rumps](https://github.com/jaredks/rumps)
(BSD-3-Clause) for the status-bar UI.

```
h 80% · w 89%
```

Click for a dropdown: exact %, reset countdowns, current model, session
cost, burn rate (tok/min), and data source.

## How it's different from ClaudeTokenMonitor

Companion project: [ClaudeTokenMonitor](https://github.com/Firas/ClaudeTokenMonitor)
does the same job in native Swift, but reads its session from **Claude
Desktop**'s cookie store and hits the claude.ai web API.

This one instead reads the OAuth token from **macOS Keychain**
(`Claude Code-credentials`, the same place the `claude` CLI itself stores
it) and calls Anthropic's official `/api/oauth/usage` endpoint — the same
data source the `/usage` slash command in Claude Code uses. Falls back to
a rough estimate from local `~/.claude/projects/*.jsonl` logs if neither
the API nor the Keychain entry is available.

`claude_stats.py` (the stats/API logic) is shared with the
[Экранчик](https://github.com/Firas/screenchik) project (Claude usage on a
physical USB LCD) — same data source, different display.

## Requirements

- Claude Code CLI installed and logged in.

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install rumps
```

## Run

```bash
.venv/bin/python app.py
```
