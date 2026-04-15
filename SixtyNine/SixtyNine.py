import discord
from discord.ext import commands, tasks
import itertools
from flask import Flask
from threading import Thread
import os

# --- كود خادم وهمي عشان Render ما يطفي البوت ---
app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run_flask():
    # Render يستخدم بورت 10000 
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()
# ---------------------------------------------

# إعدادات الصلاحيات
intents = discord.Intents.default()
intents.members = True 
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# سحب التوكن من إعدادات الموقع (Environment Variables)
TOKEN = os.environ.get('BOT_TOKEN')

# قائمة الحالة المتغيرة
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

# --- وظيفة الترحيب في روم hye ---
@bot.event
async def on_member_join(member):
    # يبحث عن الروم اللي اسمها hye
    channel = discord.utils.get(member.guild.text_channels, name="hye")
    
    if channel:
        # رسالة الترحيب بالمنشن داخل الروم
        await channel.send(f"Welcome {member.mention} to Sixty Nine")
    else:
        # إذا ما لقى الروم بيطبع لك تنبيه في اللوقز
        print(f"تنبيه: لم أجد روم باسم hye للترحيب بـ {member.name}")

# --- تشغيل البوت ---
if TOKEN:
    print("جاري محاولة تشغيل البوت...")
    keep_alive()
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"خطأ أثناء تشغيل البوت: {e}")
else:
    print("خطأ: لم يتم العثور على BOT_TOKEN في إعدادات Render! تأكد من إضافته في Environment Variables باسم BOT_TOKEN")
