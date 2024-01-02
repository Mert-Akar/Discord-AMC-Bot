import discord
from discord.ext import commands
import pathlib
from random import choice

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='^', intents=intents)

amc10_problem_list, amc12_problem_list = list(), list()

def add_to_list(cur_list : list, cur_item):
    if cur_item.is_dir():
        for item in cur_item.iterdir():
            add_to_list(cur_list, item)
    elif cur_item.is_file():
        cur_list.append(cur_item)

add_to_list(amc10_problem_list, pathlib.Path("amc/10"))
add_to_list(amc12_problem_list, pathlib.Path("amc/12")) ## prepares problem lists

@bot.command(description='Recommends random problem from past AMC10/AMC12 contests')
async def gimme(ctx, contest_type : int = commands.parameter(default=37, description="AMC contest choice from {10,12}")):
    if contest_type == 10:
        chosen_problem = choice(amc10_problem_list)
    elif contest_type == 12:
        chosen_problem = choice(amc12_problem_list)
    else:
        await ctx.send("AMC contest type must be 10 or 12")
        return

    text = str(chosen_problem)[0:-4].upper().split('/') ## last 4 chars were .png so I discarded them
    text = ' '.join(text)
    await ctx.send(content = text, file=discord.File( chosen_problem ) )

TOKEN = [line.strip() for line in open('TOKEN.txt')][0]
bot.run(TOKEN)
