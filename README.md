# A/L Result Monitor

Python script that polls the Sri Lankan Department of Examinations result metadata endpoint and sends a Discord webhook notification when the published A/L result year changes.

## What It Does

- Polls `https://result.doenets.lk/result/service/examDetails`
- Watches the `yearAlResult` value
- Sends a Discord notification when that value changes
- Logs checks to both console output and `results_monitor.log`

## Setup

Install dependencies:

```bash
pip install requests
```

Set your Discord webhook URL in the environment:

```bash
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
python main.py
```

PowerShell:

```powershell
$env:DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/..."
python main.py
```

## Configuration

By default the script checks every 30 seconds. You can change that with:

```bash
CHECK_INTERVAL_SECONDS=60 python main.py
```

## Notes

This is a lightweight notification script, not an official government service. Keep polling intervals reasonable and verify results through the official website.
