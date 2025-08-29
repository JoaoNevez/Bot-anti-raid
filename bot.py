import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.members = True  # Necessário para detectar entradas

bot = commands.Bot(command_prefix="!", intents=intents)

# Configurações
RAID_THRESHOLD = 5      # Quantos membros entrando em pouco tempo caracteriza raid
RAID_TIMEFRAME = 10     # Tempo em segundos para contar entradas
LOG_CHANNEL_ID = 1234567890  # Coloque aqui o ID do canal de logs

join_times = []

@bot.event
async def on_ready():
    print(f"Bot online como {bot.user}")

@bot.event
async def on_member_join(member):
    global join_times
    now = asyncio.get_event_loop().time()
    join_times = [t for t in join_times if now - t < RAID_TIMEFRAME]
    join_times.append(now)

    if len(join_times) >= RAID_THRESHOLD:
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send("🚨 Possível RAID detectado! Bloqueando novos convites.")

        # Opcional: banir automaticamente novos membros que entrarem
        try:
            await member.ban(reason="Raid detectado")
        except:
            pass

        # Resetar lista
        join_times = []

@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"🔓 {user.name} foi desbanido.")

# Iniciar bot
bot.run("SEU_TOKEN_AQUI")
