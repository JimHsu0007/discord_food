import discord
from discord.ext import commands
from dotenv import load_dotenv
import os, json

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)

orders = {}  # 用戶點餐紀錄

@bot.event
async def on_ready():
    print(f"Bot 已上線：{bot.user}")

@bot.command()
async def menu(ctx):
    with open("menu.json", "r", encoding="utf-8") as f:
        menu = json.load(f)
    msg = "**今日菜單：**\n" + "\n".join([f"{k}：${v}" for k, v in menu.items()])
    await ctx.send(msg)

@bot.command()
async def order(ctx, *, item):
    user = ctx.author.name
    with open("menu.json", "r", encoding="utf-8") as f:
        menu = json.load(f)
    if item not in menu:
        await ctx.send(f"{item} 不在菜單上喔")
    else:
        orders[user] = item
        await ctx.send(f"{user} 已點餐：{item}")

@bot.command()
async def checkout(ctx):
    if not orders:
        await ctx.send("還沒有人點餐喔")
        return

    total = 0
    summary = "**點餐清單：**\n"
    with open("menu.json", "r", encoding="utf-8") as f:
        menu = json.load(f)
    
    for user, item in orders.items():
        price = menu.get(item, 0)
        total += price
        summary += f"{user}：{item} ${price}\n"

    summary += f"\n總金額：${total}"
    await ctx.send(summary)

bot.run(TOKEN)
