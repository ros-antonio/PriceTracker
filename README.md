# Price Tracker

A Python-based price tracking tool for **eMAG**, **Amazon**, **Altex**. It uses **Playwright** with stealth features to bypass anti-bot protections and monitors price drops based on your target thresholds. The program also writes a .md tabelar file with current prices.

## Setup and Installation

### Prerequisites

- **Python 3.8+** on your system.
- Use a virtual environment:

  ```bash
  # Create a virtual environment
  python -m venv .venv

  # Activate it (Windows)
  .venv\Scripts\activate
  ```

1. Install Python Dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Install Playwright Browser Binaries:

   ```bash
   playwright install
   ```

3. Configure Environment Variables:
   Create a `.env` file in the root directory based on `.env.example`:
   - `OUTPUT_FILEPATH` : Where u want to save your results. (File should be md)
   - `EMAIL_ADDRESS`: The Gmail from which the notifications will be sent.
   - `EMAIL_PASSWORD`: Your Google App Password.
   - Tip: You cannot use your regular Gmail password here. You must generate a 16-character App Password from your Google Account security settings for the script to bypass Google's security blocks.

4. Prepare Tracking Data:
   Create a `data.json` file (see `data.example.json` for format).
   The gmails from this file are the ones who want to be notified.

## Usage

Run the script manually to check current prices:

```bash
python main.py
```

(Windows) Set task to run when any user logs on device
Create `setup_startup.ps1` and `toggle_startup.ps1` files
Run ps as administrator

```powershell
powershell -ExecutionPolicy Bypass -File .\setup_startup.ps1
```

Disable/Enable the task at startup

```powershell
.\toggle_startup.ps1 enable
```
