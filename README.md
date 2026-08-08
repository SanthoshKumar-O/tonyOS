# Tony

A local-first AI system administrator for Fedora Linux.

Tony is being developed as a local-first system administration assistant with a modular architecture for configuration, execution, permissions, AI providers, and native Linux tools.

## Current Status

**Milestone 4.6 completed.**

Tony currently includes:

* Application bootstrap and lifecycle
* Configuration management
* Logging system
* Session and conversation management
* Execution context
* Planning and execution infrastructure
* Permission engine
* Tool discovery, validation, registration, and dispatch
* Ollama provider integration
* Filesystem tools
* Git tools
* Package management tools
* Systemctl tools
* Python tools
* Docker tools
* Terminal and system information tools

### Native Tool Modules

Tony currently provides tools for:

* **Filesystem**: `pwd`, `ls`, `mkdir`, `touch`, `cat`, `cp`, `mv`, `rm`
* **Git**: repository initialization and common Git operations
* **Package management**: package installation, removal, search, listing, and updates
* **Systemctl**: service start, stop, restart, enable, disable, and status
* **Python**: Python execution, environments, package management, and dependency freezing
* **Docker**: containers, images, build, pull, run, stop, and remove operations
* **Terminal**: command execution, process management, system information, networking, environment inspection, and other basic Linux operations

All implemented tool modules follow Tony's centralized tool architecture with shared metadata, validation, permissions, registration, and dispatch.

## Development Roadmap

### Milestone 4

Native Fedora/Linux capabilities.

* [x] M4.1 Filesystem
* [x] M4.2 Git
* [x] M4.3 Package
* [x] M4.4 Systemctl
* [x] M4.5 Docker
* [x] M4.6 Terminal
* [ ] M4.7 Workspace
* [ ] M4.8 Search
* [ ] M4.9 Archive
* [ ] M4.10 Media

### Milestone 5

Agent-oriented capabilities and higher-level system interaction.

### Milestone 6

Complete CLI-oriented Tony system with refined permissions, planning, execution, and autonomous capabilities.

## Architecture

Tony is organized into modular components:

```text
src/tony/
├── audit/
├── clarification/
├── configuration/
├── container/
├── context/
├── context_builder/
├── conversation/
├── core/
├── execution/
├── llm/
├── logging_system/
├── pipeline/
├── planner/
├── prompts/
├── providers/
├── recovery/
├── response/
├── session/
├── streaming/
└── tools/
```

The tool system provides:

```text
Tool
  ↓
Tool Metadata
  ↓
Tool Registry
  ↓
Tool Discovery
  ↓
Argument Validation
  ↓
Permission Engine
  ↓
Tool Dispatcher
  ↓
Execution
```

Security and authorization remain centralized in the **PermissionEngine** rather than being duplicated inside individual tools.

## Requirements

* Fedora Linux
* Python 3.14+
* `uv`
* Ollama for local AI functionality

## Run

```bash
uv run tony
```

Press `Ctrl+C` to stop.

## Development

Run the test suite:

```bash
uv run pytest
```

Run linting:

```bash
uv run ruff check .
```

Run formatting:

```bash
uv run ruff format .
```

Run type checking:

```bash
uv run basedpyright
```

## Project Philosophy

Tony is designed around a **local-first** approach.

The long-term goal is to provide a capable Linux system administrator that can reason about the user's environment, select appropriate tools, request permission when necessary, execute operations safely, and eventually become capable of extending its own capabilities.

Development is milestone-driven, with each milestone building on the previous architecture rather than replacing it.
