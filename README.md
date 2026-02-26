# Price Tracker

A Python-based price tracking tool for **eMAG**, **Amazon**, and **Altex**. It uses **Playwright** with stealth features to bypass anti-bot protections and monitors price drops based on your target thresholds.

## Setup and Installation

### Prerequisites

- Ensure you have **Python 3.8+** installed on your system.
- It is highly recommended to use a virtual environment:

  ```bash
  # Create a virtual environment
  python -m venv .venv

  # Activate it (Windows)
  .venv\Scripts\activate

  # Activate it (Mac/Linux)
  source .venv/bin/activate
  ```

1. **Install Python Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Install Playwright Browser Binaries:**

   ```bash
   playwright install
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the root directory based on `.env.example`:
   - `EMAIL_ADDRESS`: The Gmail from which the notifications will be sent.
   - `EMAIL_PASSWORD`: Your Google App Password.
   - Tip: You cannot use your regular Gmail password here. You must generate a 16-character App Password from your Google Account security settings for the script to bypass Google's security blocks.

4. **Prepare Tracking Data:**
   Create a `data.txt` file (see `data.example.txt` for format).
   The gmails from this file are the ones who want to be notified.

## Usage

Run the script manually to check current prices:

```bash
python main.py
```
