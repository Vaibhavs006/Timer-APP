# Timer

A lightweight, native macOS menu bar productivity timer built with Swift and SwiftUI. Timer brings powerful time-tracking capabilities to your macOS environment with an elegant, minimalist design.

## Core Features

- **Smart Single-Line Text Parsing**: Type natural time expressions like `1h 25m` or `30m 45s` for instant timer setup
- **Precise Input Controls**: Separate dedicated input boxes for hours, minutes, and seconds when you need exact timing
- **Native System Sound Alerts**: Get notified with a crisp system sound alert when your countdown reaches zero
- **Menu Bar Integration**: Runs entirely in the menu bar (look for the ⏰ emoji) with zero desktop clutter—no dock icon, no floating windows

---

## How to Install and Run (for Mac Users)

### Prerequisites
- macOS 12.0 or later
- Xcode 13.0 or later

### Installation Steps

1. **Open the Project in Xcode**
   - Navigate to the project directory on your Mac
   - Double-click `Timer.xcodeproj` to open it in Xcode
   - Alternatively, open Xcode and select **File > Open**, then browse to the project folder

2. **Build and Run**
   - Press **Cmd + R** to build and run the application
   - Xcode will compile the project and launch Custom Horo Timer automatically

3. **Locate the Timer in Your Menu Bar**
   - Look at the **top-right corner of your screen** in the menu bar
   - You'll see a **⏰ emoji icon**—this is your timer
   - Click on it to open the timer interface and start setting your countdown

### How the App Runs
Custom Horo Timer runs entirely as a background menu bar application. There is **no standard desktop window** and **no dock icon**. All functionality is accessed through the menu bar icon in the top-right corner of your screen.

---

## How to Install and Run on Windows

### Prerequisites

- **Python 3.7 or later** (download from [python.org](https://www.python.org/downloads/))
- **Windows 7 or later**

### Quick Setup (30 seconds)

Custom Horo Timer now has a **native Windows system tray version** built with Python! No Mac environment needed.

#### Step 1: Install Python Dependencies

Open **Command Prompt** or **PowerShell** and run:

```bash
pip install pystray pillow
```

This installs the system tray library and image processing toolkit.

#### Step 2: Run the Timer

From the project root directory, run:

```bash
python timer_windows.py
```

The timer will launch as a **system tray icon** (look for ⏰ in your taskbar's notification area at the bottom-right corner of your screen).

### Using the Windows Version

- **Click the tray icon** to open the timer window
- Use **Smart Input** (type `1h 25m`, `30m 45s`, etc.) or **Custom Input** (separate hours/minutes/seconds boxes)
- **Press Enter** or click **Start** to begin the countdown
- The tray icon updates in real-time with remaining time
- When the timer hits zero, you'll hear a **system alert sound**
- **Right-click the tray icon** and select **Quit** to exit

---

## Important Note: Native macOS Version

The original **Swift/SwiftUI version** is a native macOS application built exclusively with Apple-specific frameworks:

- **SwiftUI**: Apple's modern UI framework (macOS/iOS only)
- **MenuBarExtra**: Apple's menu bar integration API (macOS only)
- **AudioToolbox**: Apple's native audio framework (macOS/iOS only)

**Why we created the Python version for Windows**: These frameworks do not exist on Windows, and the Swift code cannot be compiled to a Windows `.exe`. Instead of complex workarounds, we built a lightweight Python-based Windows version that delivers the same timer experience in your system tray.

---

## How to Use

### Getting Started

Once the timer is running, click the **⏰ emoji** in your menu bar to open the timer interface.

### Method 1: Smart Text Parsing (Quick Mode)

The "Smart Box" allows you to type natural time expressions in a single field:

- **Examples of valid input:**
  - `1h 25m` → 1 hour, 25 minutes
  - `30m` → 30 minutes
  - `45s` → 45 seconds
  - `2h 15m 30s` → 2 hours, 15 minutes, 30 seconds
  - `90m` → 1 hour, 30 minutes

Simply type your time expression and press Enter to start the countdown. This is perfect for quick, everyday timing needs.

### Method 2: Precise Input Controls (Detailed Mode)

The **Custom Split boxes** provide three separate input fields for granular control:

- **Hours field**: Enter hours (0–23)
- **Minutes field**: Enter minutes (0–59)
- **Seconds field**: Enter seconds (0–59)

Use this mode when you need exact precision or prefer a structured interface.

### Starting and Managing Your Timer

- **Start Countdown**: After entering your time (either method), press Enter or click the Start button
- **Pause/Resume**: Click the timer display to toggle between paused and running states
- **Reset**: Press the Reset button to clear the timer and return to input mode
- **Quit the App**: Press **Cmd + Q** or click the Quit button in the menu to safely terminate Custom Horo Timer

### Audio Alert

When your timer reaches zero, Custom Horo Timer will play a **native system sound alert** to notify you. The timer interface will also display a completion message.

---

## Support & Contributing

For issues, feature requests, or contributions, feel free to reach out or submit a pull request.

---

**Timer** — Timeless productivity for your macOS menu bar.
