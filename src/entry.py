import os
import discord
from discord.ext import commands
from gemini import Gemini

from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!",intents=intents)
gemini = Gemini()

chunkLen = 1985

@bot.command(name="ask",help="Talk to the bot")
async def query(ctx, *, arg):
  messageObj = ctx.message
  await messageObj.add_reaction('\N{THUMBS UP SIGN}')  
  response = gemini.query_gemini(arg)
  
  if len(response) >= chunkLen:
    response_chunks = [response[i: i + chunkLen] for i in range(0, len(response), chunkLen)]
    for i, chunk in enumerate(response_chunks):
      if i != len(response_chunks) - 1:
        await ctx.send(f"(Part {i+1}): {chunk}...\n")
      else:
        await ctx.send(f"(Part {i+1}): {chunk}")
  else: 
    await ctx.send(response)
  
@bot.command(name="chat", help="Chat with context")
async def query_with_context(ctx, *, arg):
  messageObj = ctx.message
  await messageObj.add_reaction('\N{THUMBS UP SIGN}')
  response = gemini.chat_with_context(arg)

  if len(response) >= chunkLen:
    response_chunks = [response[i: i + chunkLen] for i in range(0, len(response), chunkLen)]
    for i, chunk in enumerate(response_chunks):
      if i != len(response_chunks) - 1:
        await ctx.send(f"(Part {i+1}): {chunk}...\n")
      else:
        await ctx.send(f"(Part {i+1}): {chunk}")
  else: 
    await ctx.send(response)

bot.run(DISCORD_TOKEN)




