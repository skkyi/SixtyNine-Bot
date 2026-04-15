import discord
from discord.ext import commands, tasks
import itertools

# إعدادات الصلاحيات - تأكد من تفعيلها في صفحة المطورين (Intents)
intents = discord.Intents.default()
intents.members = True 
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# التوكن حقك حطيته لك هنا عشان يشتغل فوراً
TOKEN = "MTQ5Mzc2ODY2NTA3MjY2ODY5Mg.G89xen.YIoQY12dE3org2so9s-K3ezhEvxTkIOX__-dUo"

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
    change_status.start() # تشغيل الحالة المتغيرة

@bot.event
async def on_member_join(member):
    # ملاحظة مهمة: لازم يكون عندك روم اسمها welcome في السيرفر
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if channel:
        # رسالة الترحيب اللي طلبتها بالمنشن
        await channel.send(f"Welcome {member.mention} to Sixty Nine")

# تشغيل البوت
bot.run(TOKEN)

