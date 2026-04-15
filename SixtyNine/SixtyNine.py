import discord
from discord.ext import commands, tasks
import itertools
from flask import Flask
from threading import Thread
import os

# --- خادم وهمي لاستمرار التشغيل ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Online and Dev By @.skyi !"

def run_flask():
    # المنصات تعطي المنفذ تلقائياً عبر PORT، وإذا لم يوجد نستخدم 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# --- إعدادات البوت ---
intents = discord.Intents.default()
intents.members = True 
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# جلب التوكن من "Secrets" في Replit
TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

# قائمة الحالة المتغيرة (تم تعديل الغلط هنا ✅)
status_list = itertools.cycle([
    "طلال مداح",
    "Dev By : @.skyi",
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
    # يبحث عن روم باسم hye للترحيب
    channel = discord.utils.get(member.guild.text_channels, name="hye")
    if channel:
        await channel.send(f"Welcome {member.mention} to Sixty Nine")

if __name__ == "__main__":
    keep_alive()
    if TOKEN:
        try:
            bot.run(TOKEN)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("خطأ: لم يتم العثور على التوكن!")
