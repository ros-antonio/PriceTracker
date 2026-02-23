# Price Tracker

A Python-based price tracking tool for **eMAG**, **Amazon**, and **Altex**. It uses **Playwright** with stealth features to bypass anti-bot protections and monitors price drops based on your target thresholds.

## Setup and Installation

 1. Prerequisites
* Ensure you have **Python 3.8+** installed on your system.
* It is highly recommended to use a virtual environment:
  ```bash
  # Create a virtual environment
  python -m venv .venv

  # Activate it (Windows)
  .venv\Scripts\activate

  # Activate it (Mac/Linux)
  source .venv/bin/activate

2.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Playwright Browser Binaries:**
    ```bash
    playwright install
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory based on `.env.example`:
    * `EMAIL_ADDRESS`: The Gmail from which the notifications will be sent.
    * `EMAIL_PASSWORD`: Your Google App Password.

5.  **Prepare Tracking Data:**
    Create a `data.txt` file (see `data.example.txt` for format).
    The gmails from this file are the ones who want to be notified.

## Usage

Run the script manually to check current prices:
```bash
python main.py
