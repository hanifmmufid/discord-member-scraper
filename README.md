# Discord Member Scraper

This repository contains a Python script (`discord_member_scraper.py`) for scraping member data from a Discord server using the discord.py module. The script retrieves usernames, member IDs, roles, and join dates, and stores them in a pandas DataFrame. It then uploads this data to a Google Sheets spreadsheet using Google Cloud credentials.

## Usage

1. Install the required Python packages listed in `requirements.txt`.
2. Set up your Google Cloud credentials and replace `tscredentials.json` with your credentials file.
3. Replace the `SPREADSHEET_ID` variable in the script with your Google Sheets spreadsheet ID.
4. Run the script `discord_member_scraper.py`.
