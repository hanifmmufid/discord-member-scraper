import discord
import asyncio
import pandas as pd
import openpyxl
import datetime
import schedule
import time
from discord.ext import commands
from aiohttp import ClientConnectorError

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = 'XXXX'
# RANGE_NAME = 'Class Data!A2:E'

intents = discord.Intents.all()
client = discord.Client(intents=intents)
token = "XXXX"
GUILD_ID = 'XXXX'

def pull_user_server():
    name = []
    member_id = []
    roles = []
    joined_at = []
    for guild in client.guilds:
        if guild.id == GUILD_ID:
            print(guild.name)
            print(guild.id)
            for member in guild.members:
                name.append(member.name)
                member_id.append(member.id)
                roles.append(member.roles)
                joined_at.append(member.joined_at)

    df = pd.DataFrame({'Member Username':name, 'Member ID':member_id, 'Roles':roles,'Joined At':joined_at})
    return df

def input_sheet(user_data_input):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('tstoken.json'):
        creds = Credentials.from_authorized_user_file('tstoken.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('tscredentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('tstoken.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        user_data = user_data_input
        n_row = user_data.shape[0]
        print(f"{n_row} user's data collected")
        print("Inputing Data to Spreadsheet..")
        user_data = user_data.astype(str)
        user_data_list = user_data.values.tolist()
        
        data = [
            {
                'range': f'discord_active_members!A2:D{n_row+1}',
                'values': user_data_list
            }
        ]
        body = {
            'valueInputOption': "USER_ENTERED",
            'data': data
        }

        clear_body = {
            'ranges':["A2:Z1000"]
        }

        # sheet.values().batchClear(spreadsheetId=SPREADSHEET_ID, body=clear_body).execute()
        sheet.values().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()

        return user_data

    except HttpError as err:
        print(err)

def testing_def():
    print('Pengulangan')

@client.event
async def on_ready():
    print('Bot is Ready')
    # while True:
    user_data_input = pull_user_server()
    print(user_data_input)
    # user_data_input.to_csv('membership_discord.csv', index = False)
    # print(input_sheet(user_data_input))
    # user_input_old = user_data_input.copy()
    # print('Done')
    # while True:
    #     user_data_input = pull_user_server()
    #     if  user_data_input != user_input_old:
    #         print("Tidak sama, update")
    #         # print(input_sheet(user_data_input))
    #         # user_input_old = user_data_input.copy()
    #     else:
    #         print("Masih sama")
    #         user_input_old = user_data_input.copy()
    #     print("Done")
    # time.sleep(5)
    await client.close()


try:
    if token == "":
        raise Exception("Please add your token to the Secrets pane.")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.start(token))
except ClientConnectorError:
    print("Discord connection error try again")