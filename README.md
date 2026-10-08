# Smart Quick Timer

A lightweight, native macOS timer that lives in your Dock and menu bar. Type a duration like `1h 25m` or `1:30:00`, press Enter, and it counts down with a live Dock badge, a menu bar readout, and a notification when it finishes.

## Features

- **Smart text input**: Type `1h 25m 10s`, `1h25m`, `1.5h`, `90` (minutes), `1:30` (m:ss), or `1:30:00` (h:mm:ss)
- **Live countdown everywhere**: The Dock badge and menu bar both show the remaining time
- **Pause, resume, and +1 min**: Adjust a running timer without restarting it
- **Presets**: Save durations you use often (Pomodoro, tea, and so on). They persist between launches
- **Clear error messages**: Invalid input explains what formats work instead of failing silently
- **Notifications and sound**: A banner and a system sound when the timer reaches zero
- **Launch at login**: Optional, from the main window
- **Accurate timing**: The timer tracks an end time rather than counting ticks, so it stays correct after sleep or a busy system

## Requirements

- macOS 13.0 or later
- Xcode 14 or later

## Installation (macOS)

1. **Open the project**
   - In Finder, open the `Timer` folder and double-click `Timer.xcodeproj`
   - Or open Xcode, choose **File > Open**, and select `Timer.xcodeproj`

2. **Build and run**
   - Press **Cmd + R**
   - Grant notification permission when macOS asks. Timers still work without it, but you won't get the banner

3. **Find the app**
   - The app appears in your **Dock** and as a **⏱** icon in the menu bar (top-right of the screen)
   - Click the Dock icon to open the main window, or click the menu bar icon for a compact version

## How to Use

### Starting a Timer

Type a duration in the input field and press **Enter** or click **Start**:

| Input | Duration |
|---|---|
| `1h 25m` | 1 hour 25 minutes |
| `30m 45s` | 30 minutes 45 seconds |
| `90` | 90 minutes |
| `1.5h` | 1 hour 30 minutes |
| `1:30` | 1 minute 30 seconds |
| `1:30:00` | 1 hour 30 minutes |

### While a Timer Runs

- **Pause / Resume**: Pauses the countdown. Time spent paused doesn't count
- **+1 min**: Adds a minute to the timer
- **Stop**: Cancels the timer and returns to input mode

### Presets

- Enter a duration, then click **Save current** to store it as a preset. You can name it or let the app use the time as the name
- Click a preset to start it immediately
- Click the **−** button next to a preset to remove it

### Launch at Login

Turn on **Launch at login** in the main window. The app starts automatically when you log in.

## Project Structure

```text
Timer App/
├── README.md
├── timer_windows.py
└── Timer/
    ├── Timer.xcodeproj
    └── Timer/
        ├── Assets.xcassets/
        ├── TimerApp.swift
        └── TimerManager.swift
```

## Windows Version

A Python system tray version is included for Windows users.

**Requirements:** Python 3.7 or later, Windows 7 or later

```bash
pip install pystray pillow
python timer_windows.py
```

The timer appears as a ⏰ icon in the system tray (bottom-right of the taskbar). Right-click the icon and choose **Quit** to exit.

## Support & Contributing

For issues, feature requests, or contributions, open an issue or submit a pull request.

---

**Smart Quick Timer**: Timeless productivity for your Mac.
