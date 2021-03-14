import discord
from discord.ext import commands
import json
import datetime
import time, threading
import asyncio
import os

fetch_path = os.getcwd()
path = fetch_path.replace("\\", "/")

with open(path + '/config.json') as data:
    config = json.load(data)

bot = commands.Bot(command_prefix=config['prefix'], description=f" {config["description"]} ")

async def my_background_task():
    while True:

        index = 0
        
        with open(path + '/recall.json') as data:
            json_file = json.load(data)
        
        for content in json_file['recall']:
            json_time = content['time'].split('/', 2)
            
            if json_time[0] == time.strftime(r"%d"):
                if json_time[1] == time.strftime(r"%H"):
                    if json_time[2] == time.strftime(r"%M"):
                        user = bot.get_user(content['user_id'])
                        await user.send(content['message'])

                        del json_file['recall'][index]
                        y = json.dumps(json_file)

                        f = open(path + "/recall.json", "w")
                        f.write(y)
                        f.close()

            index += 1


        await asyncio.sleep(30) # task runs every 60 seconds

@bot.event 
async def on_ready():
    print('bot est prêt')
    await my_background_task()

@bot.command()
async def recall(ctx, *,args):

    with open(path + '/recall.json') as data:
        json_file = json.load(data)

    await ctx.send('donnez moi un : `jour/heure/minute`')

    def check(m):
        return m.channel == ctx.message.channel and m.author == ctx.message.author

    msg = await bot.wait_for('message', check=check)

    times = msg.content.split('/', 2)

    if int(times[0]) > 31:
        times[0] = 31
    if int(times[1]) > 23:
        times[1] = 24
    if int(times[2]) > 59:
        times[2] = 60

    json_file['recall'].append({"user_id": ctx.message.author.id, "message": "".join(args), "time": f"{times[0]}/{times[1]}/{times[2]}"})

    y = json.dumps(json_file)

    f = open(path + "/recall.json", "w")
    f.write(y)
    f.close()

    embed = discord.Embed(title="Rappel", description="Le rappel a été enregistrer.")
    embed.add_field(name="Temps", value=f"{times[0]}/{times[1]}/{times[2]}")
    embed.add_field(name="Rappel", value="".join(args))

    await ctx.send(embed=embed)

bot.run(f' {config['token']} ')