import discord
from discord.ext import commands
import yfinance as yf
from dotenv import load_dotenv
import os
import pandas as pd
from boto.s3.connection import S3Connection
import requests

# load_dotenv('.env')
# client = discord.Client()
bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(name = "52weeklow")
async def fifty_two_wlow(ctx):

    url = "https://nse-data1.p.rapidapi.com/near_fifty_two_week_low"

    headers = {
        'x-rapidapi-host': os.environ['X-RAPIDAPI-HOST'],
        'x-rapidapi-key': os.environ['X-RAPIDAPI-KEY']
        }
    
    response = requests.request("GET", url, headers=headers)

    try:
        dataLtpLess20 = pd.json_normalize(response.json()['body']['dataLtpLess20'])
    except:
        dataLtpLess20 = pd.DataFrame()
    
    try:
        dataLtpGreater20 = pd.json_normalize(response.json()['body']['dataLtpGreater20'])
    except:
        dataLtpGreater20 = pd.DataFrame()
    
    if (len(dataLtpLess20) > 0) | (len(dataLtpGreater20) > 0):
        df_52w_low = pd.concat([dataLtpLess20, dataLtpGreater20])
        df_52w_low.to_excel("52w Low.xlsx")
        file = discord.File("52w Low.xlsx")
        await ctx.send(file=file, content="Here is your excel file")
    else:
        await ctx.send(f"No Stocks found")

@bot.command()
async def price(ctx, symbol):
    current_price = yf.Ticker(f"{symbol}.NS").info['regularMarketPrice']
    print(current_price)
    if current_price:
        await ctx.send(f"The price of {symbol} is {current_price}")
    else:
        await ctx.send(f"{symbol} not found")

@bot.command()
async def info(ctx, symbol):
    info_json = yf.Ticker(f"{symbol}.NS").info
    if info_json['regularMarketPrice']:
        info_df = pd.json_normalize(info_json).T.reset_index()
        info_df.columns = ['Info', 'Details']
        info_df.to_excel(f"{symbol}_info.xlsx")
        file = discord.File(f"{symbol}_info.xlsx")
        await ctx.send(file=file, content="Here is your excel file")
    else:
        await ctx.send(f"{symbol} not found")

bot.run(os.environ['TOKEN'])
