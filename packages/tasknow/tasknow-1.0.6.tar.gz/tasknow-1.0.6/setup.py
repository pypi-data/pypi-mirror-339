from setuptools import setup, find_packages

setup(
    name="tasknow",
    version="1.0.6",
    description="A terminal to-do app that helps you focus on one task at a time.",
    long_description="""# TaskNow

A terminal to-do app that helps you focus on one task at a time.

## Why use TaskNow?

- Stay focused by seeing just your current task
- Add, complete, and manage tasks easily from the terminal
- No accounts, no clutter — just your tasks

## Installation

You can install TaskNow directly from PyPI:

```bash
pip install tasknow
```

## Commands

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
tasknow remove <id>
```

Show completed tasks:
```bash
tasknow completed
```

Un-complete a task:
```bash
tasknow undone <id>
```

Edit a task:
```bash
tasknow edit <id> "New description"
```

---

MIT License
""",
    long_description_content_type="text/markdown",
    author="Decoding Chris",
    license="MIT",
    py_modules=["main"],
    python_requires=">=3.10",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "tasknow=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: End Users/Desktop",
        "Environment :: Console",
        "Topic :: Utilities",
    ],
)