# TaskNow

A terminal to-do app that helps you focus on one task at a time.

[![PyPI version](https://img.shields.io/pypi/v/tasknow.svg)](https://pypi.org/project/tasknow/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Why use TaskNow?

- **Stay focused:** See just your current task by default
- **Minimalist & distraction-free:** No accounts, no clutter — just your tasks
- **Full control:** Add, complete, edit, and manage tasks easily from the terminal
- **Simple commands:** Intuitive CLI interface
- **Lightweight:** Python-based with JSON storage, works seamlessly on Linux

---

## Requirements

- **Python 3.10 or higher**
- Compatible with Ubuntu/Linux systems

---

## Installation

Install TaskNow directly from PyPI:

```bash
pip install tasknow
```

---

## Quick Start

Add a task:

```bash
tasknow add "Write report"
```

See your current task:

```bash
tasknow
```

Mark it done:

```bash
tasknow done
```

List all tasks:

```bash
tasknow list
```

Remove a task:

```bash
tasknow remove 3
```

Show completed tasks:

```bash
tasknow completed
```

Un-complete a task:

```bash
tasknow undone 3
```

Edit a task:

```bash
tasknow edit 2 "New task description"
```

---

For more commands and details, see the full documentation or run:

```bash
tasknow --help
```

---

## Links

- **PyPI:** [https://pypi.org/project/tasknow/](https://pypi.org/project/tasknow/)
- **Source Code:** [https://github.com/decodingchris/tasknow](https://github.com/decodingchris/tasknow)
- **Issue Tracker:** [https://github.com/decodingchris/tasknow/issues](https://github.com/decodingchris/tasknow/issues)

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](https://opensource.org/licenses/MIT) file for details.

---

MIT License © Decoding Chris
