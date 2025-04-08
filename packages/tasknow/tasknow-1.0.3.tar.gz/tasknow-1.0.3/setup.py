from setuptools import setup, find_packages

setup(
    name="tasknow",
    version="1.0.3",
    description="A super simple terminal to-do app that helps you focus on one task at a time.",
    long_description="""# TaskNow

A super simple terminal to-do app that helps you focus on one task at a time.

## Why use TaskNow?

- Stay focused by seeing just your current task
- Add, complete, and manage tasks easily from the terminal
- No accounts, no clutter — just your tasks

## Quick start

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

For more commands and details, see the full documentation.

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