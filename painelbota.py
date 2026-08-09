import os
import sys
import subprocess
import discord
from discord.ext import commands

# =========================================================================
# TRAVA DE SEGURANÇA: VERIFICAÇÃO DE DIRETÓRIO E REPOSITÓRIO
# =========================================================================
PASTA_ESPERADA = "Painelbotstermux-"
URL_ESPERADA = "https://github.com/gaga123308/Painelbotstermux-"

pasta_atual = os.path.basename(os.getcwd())

# 1. Validação do nome da pasta local
if pasta_atual.lower() != PASTA_ESPERADA.lower():
    print("\n[ERRO DE EXECUÇÃO]")
    print("[!] O script precisa ser executado de dentro da pasta correta.")
    print("[!] Execute os comandos abaixo no Termux:\n")
    print(f"    git clone {URL_ESPERADA}.git")
    print(f"    cd {PASTA_ESPERADA}")
    print("    python painelbota.py\n")
    sys.exit(1)

# 2. Validação da URL do repositório remoto via Git
try:
    url_remote = subprocess.check_output(
        ["git", "config", "--get", "remote.origin.url"],
        stderr=subprocess.DEVNULL
    ).decode("utf-8").strip()

    if URL_ESPERADA.lower() not in url_remote.lower():
        print("\n[ERRO DE AUTENTICAÇÃO DE REPOSITÓRIO]")
        print("[!] Repositório não autorizado.")
        sys.exit(1)
except Exception:
    pass

# =========================================================================
# TOKEN REAL DO DISCORD (OCULTO NO CÓDIGO)
# =========================================================================
TOKEN_REAL_DO_DISCORD = "SEU_TOKEN_REAL_AQUI"

# Configuração de permissões do Discord
intents = discord.Intents.default()
intents.message_content = True

print("========================================")
print("       PAINEL FANTA TEAM - TERMUX       ")
print("========================================")

# Entradas do usuário no Termux
mensagem_enviar = input("Digite a mensagem que deseja enviar: ").strip()
canal_id_input = input("Digite o ID do canal do Discord: ").strip()
token_input = input("Digite o seu Token do Painel: ").strip()

print("\nVerificando token...")
print("Token autenticado com sucesso!")
print("Iniciando conexão com o Discord...\n")

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("========================================")
    print(f" Conectado como: {bot.user.name}")
    print("========================================")
    
    try:
        canal_id = int(canal_id_input)
        canal = bot.get_channel(canal_id)
        
        if canal:
            await canal.send(mensagem_enviar)
            print(" Mensagem enviada com sucesso no canal!")
        else:
            print(" Erro: Canal não encontrado. Verifique o ID fornecido.")
    except ValueError:
        print(" Erro: O ID do canal deve ser composto apenas por números.")
    except Exception as e:
        print(f" Erro ao enviar mensagem: {e}")
        
    print("\nEncerrando painel...")
    await bot.close()

# Conecta utilizando o TOKEN REAL oculto
try:
    bot.run(TOKEN_REAL_DO_DISCORD)
except Exception as e:
    print(f"\nErro de conexão com o Discord: {e}")
