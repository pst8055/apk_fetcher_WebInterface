# APK Puller (Legacy)

A Python/Flask application to extract and download APK files from your connected Android device using ADB.

![How it works](instructions.png)

## Features
*   **Connect via ADB**: Automatically detects connected Android devices.
*   **List Apps**: Fetches a list of all 3rd-party installed applications.
*   **Download**: One-click download of the APK file to your computer.
*   **Dockerized**: Easy to run without manual dependency management.

## Prerequisites
*   **Android Device** with **USB Debugging enabled**:
    1. Go to **Settings** → **About Phone**
    2. Tap **Build Number** 7 times to enable Developer Options
    3. Go to **Settings** → **Developer Options**
    4. Enable **USB Debugging**
*   **ADB installed** (if running without Docker)

## How to Run

### Option 1: Using Docker (Recommended)
1.  Build and run:
    ```bash
    docker-compose up --build
    ```

### Option 2: Running Locally (Python)
1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the app:
    ```bash
    python app.py
    ```
3.  Open `http://localhost:5000`.
