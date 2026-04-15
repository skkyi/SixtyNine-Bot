import discord
from discord.ext import commands, tasks
import itertools
from flask import Flask
from threading import Thread
import os

# خادم وهمي عشان يخلي Render يعطينا Live
app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# إعدادات الصلاحيات
intents = discord.Intents.default()
intents.members = True 
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# الأمر السري: هنا الكود يسحب التوكن من إعدادات الموقع مو من الكود
TOKEN = os.environ.get('BOT_TOKEN')

status_list = itertools.cycle([
    "طلال مداح",
    "Div By : @.skyi",
    "Sixty Nine"
])

@tasks.loop(seconds=4)
async def change_status():
    await bot.change_presence(activity=discord.Game(name=next(status_list)))

@bot.event
async def on_ready():
    print(f'Done! {bot.user.name} is now online.')
    if not change_status.is_running():
        change_status.start()

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if channel:
        await channel.send(f"Welcome {member.mention} to Sixty Nine")

if TOKEN:
    keep_alive()
    bot.run(TOKEN)
else:
    print("خطأ: لم يتم العثور على BOT_TOKEN في إعدادات Render!")
