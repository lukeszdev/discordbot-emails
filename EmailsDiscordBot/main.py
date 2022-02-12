import discord
from imap_tools import MailBox, AND
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("TOKEN")
prefix = os.getenv("PREFIX")

client = commands.Bot(command_prefix=prefix)

user = os.getenv("USER")
password = os.getenv("PASSWORD")
imap = os.getenv("IMAP")

@client.event
async def on_ready():
    print("Bot iniciado!")


@client.command()
async def ajuda(ctx):
    helpEmbed = discord.Embed(title="Emails ajuda",
                              description="Olá, sou um simples bot que liga o seu email com o discord\n"
                                          "\nOu seja, ao invés de você precisar todo dia verificar o seu email,"
                                          "\nbasta vir aqui no discord e digitar um simples comando que eu faço o trabalho para você!"
                                          "\n\n**Lista de comandos:**"
                                          f"\n``Todos os comandos são executados com o prefix {prefix}``"
                                          f"\n\n``{prefix}getemail`` Mostra todos os seus novos emails no chat do discord.")
    helpEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/933788941499396226/7849e871a35ae3453c3a1267a625a92b.png?size=2048")

    await ctx.send(embed=helpEmbed)

@client.command()
@commands.has_role("Admin")
async def getemail(ctx):
    await ctx.message.delete()
    myEmail = MailBox(imap).login(user, password)
    emailsList = myEmail.fetch(AND(seen=False))
    for email in emailsList:
        msg = await ctx.send(f"**Enviado por:** {email.from_} \n"
                       f"**Assunto:** {email.subject}\n"
                       f"**Texto:** {email.text}")
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        await ctx.send("``` ```")
client.run(token)