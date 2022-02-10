import discord
from discord.ext import commands
import yfinance as yf
from dotenv import load_dotenv
import os

load_dotenv('.env')
# client = discord.Client()
bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')

# @bot.command()
# async def ping(ctx):
#     file = discord.File("businesstimes.xlsx")
#     await ctx.send(file=file, content="Here is your excel file")

@bot.command()
async def price(ctx, symbol):
    current_price = yf.Ticker(f"{symbol}.NS").info['regularMarketPrice']
    if current_price:
        await ctx.send(f"The price of {symbol} is {current_price}")
    else:
        await ctx.send(f"{symbol} not found")

# @bot.command()
# async def info(ctx, symbol):
#     current_price = yf.Ticker(f"{symbol}.NS").info['regularMarketPrice']
#     if current_price:
#         await ctx.send(f"The price of {symbol} is {current_price}")
#     else:
#         await ctx.send(f"{symbol} not found")
print(os.getenv('TOKEN'))
bot.run(os.getenv("TOKEN"))

