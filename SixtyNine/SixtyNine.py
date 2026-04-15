import discord
from discord.ext import commands, tasks
import itertools
import os

# إعدادات الصلاحيات
intents = discord.Intents.default()
intents.members = True 
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# هنا الكود بيسحب التوكن من إعدادات الموقع اللي بنضيفها
TOKEN = os.environ.get('BOT_TOKEN')

# قائمة الكلمات للحالة المتغيرة (الستاتس)
status_list = itertools.cycle([
    "طلال مداح",
    "Div By : @.skyi",
    "Sixty Nine"
])

# وظيفة تغيير الحالة كل 4 ثواني
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

# تشغيل البوت
if TOKEN:
    bot.run(TOKEN)
else:
    print("خطأ: لم يتم العثور على BOT_TOKEN في إعدادات Render!")

# تشغيل البوت
bot.run(TOKEN)

