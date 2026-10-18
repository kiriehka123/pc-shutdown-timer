# PC Shutdown Timer

A lightweight Windows app for scheduling your computer to shut down, without typing a `shutdown` command in the command prompt.

Choose a delay in hours and minutes, then click **Start timer**. The app displays a countdown, and you can cancel the scheduled shutdown at any time.

## Features

- Set a shutdown delay in hours and minutes.
- Quick presets for 30 minutes, 1 hour, and 2 hours.
- Live countdown to shutdown.
- Cancel a scheduled shutdown.
- The shutdown timer keeps running after you close the app window.
- No third-party Python packages required.

## Requirements

- Windows 10 or Windows 11.
- Python 3 with Tkinter.

## Run

Download `shutdown_timer.pyw` and double-click it.

If it does not open on double-click, run it from PowerShell:

```powershell
python shutdown_timer.pyw
```

## Usage

1. Enter the number of hours and minutes, or choose a preset.
2. Click **Start timer**.
3. Click **Cancel** to cancel the scheduled shutdown.

The app uses the built-in Windows `shutdown.exe` command to schedule and cancel shutdowns.
