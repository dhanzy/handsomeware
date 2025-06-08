# Handsomeware File Organizer

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Issues](https://img.shields.io/github/issues/dhanzy/handsomeware)](https://github.com/dhanzy/handsomeware/issues)

> A secure, intelligent, and interactive file organization utility with passcode protection, time-limited access, and real-time folder monitoring.

---

## Features

- 📁 **Auto-organizes files** in watched directories by type.
- 🔐 **Passcode protected access** — secure your files behind a randomly generated code.
- ⏰ **Time-limited usage** — scrambled after expiration unless unlocked.
- 🖥️ **Interactive desktop UI** built with `Tkinter`.
- 🧼 **Cleans and scrambles** sensitive files after a timeout.
- 🕵️ **Monitors folders** in real-time using `watchdog`.
- 🔁 **Persistent state** across restarts (`state.json`).
- 🪵 **Customizable logging** and debugging.

---

## Installation

### 1. Clone this repo

```bash
git clone https://github.com/dhanzy/handsomeware.git
cd handsomeware
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python main.py
```

## Command Line Options

| Flag      | Description                   |
| --------- | ----------------------------- |
| `--debug` | Enable debug logging          |
| `--reset` | Reset stored state completely |

## How It Works

- First run: A random passcode is generated and stored.
- Timer starts: Files remain accessible until the time expires.
- Scramble phase: Files are scrambled when time runs out.
- Unlock: Entering the correct passcode stops the scrambling.
- Reset: Removes all state and starts fresh.

### Inspired by kalle Hallden on a previous work

> Download Categorizer

[https://github.com/dhanzy/DownloadCategorizer](https://github.com/dhanzy/DownloadCategorizer)
