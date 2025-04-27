import requests
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("results_monitor.log"),
        logging.StreamHandler()
    ]
)

# Replace this with your actual Discord webhook URL
webhook_url = ""

api_url = "https://result.doenets.lk/result/service/examDetails"

def check_for_results(last_seen_year):
    try:
        response = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        data = response.json()
        print("API response:", data)  # Print the API response to the console
        year_al_result = data.get("yearAlResult", "")
        logging.info(f"Current yearAlResult: {year_al_result}")

        if year_al_result != last_seen_year:
            # Remove emoji from all log messages to avoid UnicodeEncodeError on Windows console
            log_message = f"ALERT: The A/L exam results year has changed! New value: {year_al_result}\nCheck: {api_url}"
            discord_message = f"🎉 ALERT: The A/L exam results year has changed! New value: {year_al_result}\nCheck: {api_url}"
            logging.info(log_message)
            payload = {"content": discord_message}
            webhook_response = requests.post(webhook_url, json=payload)
            webhook_response.raise_for_status()
            logging.info(f"Notification sent to Discord! Status code: {webhook_response.status_code}")
            return year_al_result  # Return the new value

        logging.info("No change in yearAlResult yet.")
        return last_seen_year

    except requests.RequestException as e:
        logging.error(f"Error fetching the API: {e}")
        return last_seen_year
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)
        return last_seen_year

if __name__ == "__main__":
    logging.info("Starting to monitor the API for A/L exam result changes...")
    last_seen_year = None

    # Get the initial value
    try:
        response = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        data = response.json()
        last_seen_year = data.get("yearAlResult", "")
        logging.info(f"Initial yearAlResult: {last_seen_year}")
    except Exception as e:
        logging.error(f"Could not fetch initial yearAlResult: {e}")
        last_seen_year = ""

    check_count = 0
    while True:
        check_count += 1
        logging.info(f"Check #{check_count} - Checking for result changes...")
        new_year = check_for_results(last_seen_year)
        if new_year != last_seen_year:
            logging.info("Result year changed! Stopping monitoring.")
            break
        next_check = time.localtime(time.time() + 30)
        logging.info(f"Next check scheduled at {time.strftime('%H:%M:%S', next_check)}")
        time.sleep(30)  # Wait 30 seconds before next check