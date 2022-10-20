import discord
import random
import json
import re
from function import *
from datetime import *
from program import Program
from discord.ext import commands, tasks
from collections import OrderedDict
from discord_slash import ButtonStyle, SlashCommand
from discord_slash.utils.manage_components import *
from dotenv import load_dotenv
import os

load_dotenv()
intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents)
slash = SlashCommand(bot, sync_commands=True)
discordMember = Program()
#-------------------------------------------------------------------------------
@bot.event
async def on_ready():
    print("RoBot est prêt")
    vocal_time.start()
    check_time.start()

@bot.event
async def on_message(message):
    channel = bot.get_channel(906948757805998090)
    if message.author != bot.user and message.channel != channel:
        member = message.author
        discordMember.add_msg(member)
        await bot.process_commands(message)
    else:
        await bot.process_commands(message)
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(504678332965584907)
    roleChannel = bot.get_channel(908780839482064978)
    guild = bot.get_guild(504673619214073857)
    discordMember.init_mbr(member)
    role = discord.utils.get(guild.roles, name="ROTURIER")
    await member.add_roles(role)

    await channel.send(f"Bienvenue chez les **LORDS** {member.mention},\
 te voilà maintenant **ROTURIER**. Si tu souhaites \
obtenir des **titres(rôle)** et en obtenir leurs privilèges, tu dois \
simplement **participer** en écrivant sur la **PLACE PUBLIQUE** \
ou en t'asseyant à une des tables de **LA TAVERNE** pour venir discuter. \
Pour avoir accès aux salons qui t'intéressent ça se passe ici : {roleChannel.mention}")

@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(504673619214073857)
    if payload.message_id == 908781115983167518:
        if payload.emoji.name == 'rl':
            Role = discord.utils.get(guild.roles, name="ROCKET LEAGUE")
            await payload.member.add_roles(Role)
        elif payload.emoji.name == 'pkm':
            Role = discord.utils.get(guild.roles, name="POKEMON GO")
            await payload.member.add_roles(Role)
        elif payload.emoji.name == 'teso':
            Role = discord.utils.get(guild.roles, name="TESO")
            await payload.member.add_roles(Role)
        elif payload.emoji.name == 'warh':
            Role = discord.utils.get(guild.roles, name="WARGAMER")
            await payload.member.add_roles(Role)
        elif payload.emoji.name == 'warf':
            Role = discord.utils.get(guild.roles, name="WARFRAME")
            await payload.member.add_roles(Role)
        elif payload.emoji.name == '⚔️':
            Role = discord.utils.get(guild.roles, name="ELYON")
            await payload.member.add_roles(Role)

    elif payload.message_id == 931376041887428718:
        if payload.emoji.name == '✅':
            Role = discord.utils.get(guild.roles, name="ANIME-MANGA")
            await payload.member.add_roles(Role)

@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(504673619214073857)
    member = discord.utils.get(guild.members, id = payload.user_id)
    if payload.message_id == 908781115983167518:
        if payload.emoji.name == 'rl':
            role = discord.utils.get(guild.roles, name="ROCKET LEAGUE")
            await member.remove_roles(role)
        elif payload.emoji.name == 'pkm':
            role = discord.utils.get(guild.roles, name="POKEMON GO")
            await member.remove_roles(role)
        elif payload.emoji.name == 'teso':
            role = discord.utils.get(guild.roles, name="TESO")
            await member.remove_roles(role)
        elif payload.emoji.name == 'warh':
            role = discord.utils.get(guild.roles, name="WARGAMER")
            await member.remove_roles(role)
        elif payload.emoji.name == 'warf':
            role = discord.utils.get(guild.roles, name="WARFRAME")
            await member.remove_roles(role)
        elif payload.emoji.name == '⚔️':
            role = discord.utils.get(guild.roles, name="ELYON")
            await member.remove_roles(role)

    elif payload.message_id == 931376041887428718:
        if payload.emoji.name == '✅':
            role = discord.utils.get(guild.roles, name="ANIME-MANGA")
            await member.remove_roles(role)

@bot.event
async def on_member_remove(member):
    discordMember.del_mbr(member)
#-------------------------------------------------------------------------------
@tasks.loop(seconds = 1)
async def vocal_time():
    channels = vocal_channels()
    x = 0
    for channel in channels:
        channel = bot.get_channel(channel)
        members = channel.members
        for member in members:
            discordMember.add_vocal_time(member, x)
            x += 1

@tasks.loop(seconds = 30)
async def check_time():
    channel = bot.get_channel(907356683691491359)
    admin = bot.get_user(383080378501431309)
    time = datetime.now()
    stats = discordMember.stats_auto_update(time)
    if stats[0] == "day":
        embed = discord.Embed(title = "Rapport quotidien")
        embed.add_field(name = "Messages publiés", value = f"`{stats[1]}`")
        embed.add_field(name = "Temps passé en vocal", value = f"`{calc_time(stats[2])}`")
        await channel.send(embed = embed)
    elif stats[0] == "month":
        embed = discord.Embed(title = "Rapport mensuel")
        embed.add_field(name = "Messages publiés", value = f"`{stats[1]}`")
        embed.add_field(name = "Temps passé en vocal", value = f"`{calc_time(stats[2])}`")
        await channel.send(embed = embed)

        #choix kick inactifs
        await admin.send("Membres inactifs du mois dernier :")
        for inactif in stats[3]:
            user = bot.get_user(inactif)
            await admin.send(f"- {user.name}", components=[action_row])

            button_ctx = await wait_for_component(bot, components=action_row)

            if button_ctx.custom_id == "noKick":
                await button_ctx.edit_origin(content=f"- {user.name} n'a pas été kick")
            else:
                await ctx.guild.kick(user, reason = "inactif")
                await button_ctx.edit_origin(content=f"- {user.name} a été kick")
    elif stats[0] == "year":
        embed = discord.Embed(title = "Rapport annuel")
        embed.add_field(name = "Messages publiés", value = f"`{stats[1]}`")
        embed.add_field(name = "Temps passé en vocal", value = f"`{calc_time(stats[2])}`")
        await channel.send(embed = embed)
    else:
        pass
#-------------------------------------------------------------------------------


@bot.command()
async def reactrole(ctx):
    embed = discord.Embed(title = "Pour avoir accès au salon #animé-manga cliquez sur ✅")
    message = await ctx.channel.send(embed = embed)
    await message.add_reaction("✅")

@bot.command()
async def dm_all_member(ctx):
    guild = bot.get_guild(504673619214073857)
    channel = bot.get_channel(910619115725668364)
    members = ctx.guild.members
    for member in members:
        await member.send(f"Un nouveau jeu est disponible sur le discord des \
**LORD**, tu pourras l'essayer ici : {channel.mention}. Viens tenter ta chance \
pour essayer d'obtenir la créature la plus **RARE**. Pour jouer il te suffit de \
taper la commande **!open**. 3 essai max par jour !!")


@bot.command()
async def inactifs(ctx):
    channel = bot.get_channel(906948757805998090)
    admin = bot.get_user(383080378501431309)
    inactifs = discordMember.testing()
    buttons = [
        create_button(
            style=ButtonStyle.success,
            label="Garder",
            custom_id="noKick"
        ),
        create_button(
            style=ButtonStyle.danger,
            label="Expulser",
            custom_id="kick"
        )
    ]
    action_row = create_actionrow(*buttons)
    await channel.send("Voici la liste des membres inactifs le mois dernier :")
    for inactif in inactifs:
        user = bot.get_user(inactif)
        await channel.send(f"- {user.name}", components=[action_row])

        button_ctx = await wait_for_component(bot, components=action_row)

        if button_ctx.custom_id == "noKick":
            await button_ctx.edit_origin(content=f"- {user.name} n'a pas été kick")
        else:
            await ctx.guild.kick(user, reason = "inactif")
            await button_ctx.edit_origin(content=f"- {user.name} a été kick")

@bot.command()
async def cmd(ctx):

    embed = discord.Embed(title = "Commandes")
    embed.add_field(name = "-----COMMANDES-GENERAL-----", value = "#1",inline = False)
    embed.add_field(name = "!stats", value = "`Afficher ses stats personnels du serveur`",inline = False)
    embed.add_field(name = "!clear X", value = "`Supprime un ou plusieurs messages. \
'X' = nombre de message à supprimer`",inline = False)
    embed.add_field(name = "!top (X : optionnel)", value = "`Affiche par default le Top 10 des membres actifs. \
Modifiez 'X' pour changer la valeur du Top`",inline = False)

    embed.add_field(name = "-----COMMANDES-DU-JEU------", value = "#2",inline = False)
    embed.add_field(name = "!play", value = "`Faire deviner une image`",inline = False)
    embed.add_field(name = "!rank (X : optionnel)", value = "`Affiche par default le Top 10 des joueurs. \
Modifiez 'X' pour changer la valeur du Top`",inline = False)

    await ctx.channel.send(embed = embed)


@bot.command()
async def stats(ctx):
    if ctx.channel == bot.get_channel(504685159547797525):
        stats = discordMember.get_stats(ctx.author)

        embed = discord.Embed(title = f"Level {stats[4][0]}")
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        embed.add_field(name = "Messages", value = f"`{stats[0]}`")
        embed.add_field(name = "Vocal*", value = f"`{stats[2]}`")
        embed.add_field(name = "Experiences", value = f"`{stats[3]}/{stats[4][1]} XP`", inline = False)
        embed.add_field(name = "Points", value = f"`{stats[1]} pts`")
        embed.set_footer(text = "*depuis le 07/11/21")
        await ctx.channel.send(embed = embed)
    else:
        stats_channel = bot.get_channel(504685159547797525)
        await ctx.message.delete()
        await ctx.channel.send(f"Utilisez cette commande dans {stats_channel.mention}", delete_after = 5)

@bot.command()
async def top(ctx, top=10):
    if ctx.channel == bot.get_channel(504685159547797525):
        rang = discordMember.get_leaderboard()[0]
        ldb = discordMember.get_leaderboard()[1]
        index = 0
        position = 0
        embed = discord.Embed(title = f"Top {top} actifs", color = 0xffd966)
        embed.set_thumbnail(url = "https://emoji.gg/assets/emoji/1238_Trophy.png")

        for k, v in sorted(ldb.items(), key=lambda x: x[1] ,reverse=True):
            embed.add_field(name = f"{rang[position]} # {k}", value = f"`Lvl {calc_lvl(v)[0]} : {v} XP`", inline = False)
            position += 1
            index += 1
            if index == top:
                break

        await ctx.channel.send(embed = embed)
    else:
        stats_channel = bot.get_channel(504685159547797525)
        await ctx.message.delete()
        await ctx.channel.send(f"Utilisez cette commande dans {stats_channel.mention}", delete_after = 5)

@bot.command()
async def rank(ctx, top=10):
    if ctx.channel == bot.get_channel(882078878150037575):
        rang = discordMember.get_leaderboard_game()[0]
        ldb = discordMember.get_leaderboard_game()[1]
        index = 0
        position = 0
        embed = discord.Embed(title = f"Classement Top {top}", color = 0xffd966)
        embed.set_thumbnail(url = "https://emoji.gg/assets/emoji/1238_Trophy.png")

        for k, v in sorted(ldb.items(), key=lambda x: x[1] ,reverse=True):
            embed.add_field(name = f"{rang[position]} # {k}", value = f"`{v} points`", inline = False)
            position += 1
            index += 1
            if index == top:
                break

        await ctx.channel.send(embed = embed)
    else:
        ldb_channel = bot.get_channel(882078878150037575)
        await ctx.message.delete()
        await ctx.channel.send(f"Utilisez cette commande dans {ldb_channel.mention}", delete_after = 5)

@bot.command()
async def clear(ctx, nombre : int):
    if ctx.author.id == 383080378501431309:
        messages = await ctx.channel.history(limit = nombre + 1).flatten()
        for message in messages:
            await message.delete()
        if nombre <= 1:
            await ctx.channel.send(f"{nombre} message supprimé", delete_after = 2)
        else:
            await ctx.channel.send(f"{nombre} messages supprimés", delete_after = 2)
    else:
        await ctx.send("Tu n'est pas autorisé à utilisé cette commande")
#-----------------------------------JEU-----------------------------------------
@bot.command()
async def play(ctx):
    game_channel: discord.TextChannel = bot.get_channel(882078878150037575)
    if ctx.channel == game_channel:
        attente = await ctx.channel.send(":hourglass:Une image est en cours d'envoi...")

        await ctx.author.send("Ajoute une IMAGE !",delete_after=60) #le bot demande à l'utilisateur une image et une réponse dans le channel temporaire

        def check(message):
            return message.author == ctx.message.author and message.attachments
        try:
            screenshot = await bot.wait_for("message", timeout = 60, check = check)

            await ctx.author.send("Ajoute une la REPONSE !",delete_after=60)

            def checkS(message):
                return message.author == ctx.message.author and message.content

            contenu = await bot.wait_for("message", timeout = 60, check = checkS)

            await ctx.author.send("Ajoute une CATEGORIE !",delete_after=60)

            def checkC(message):
                return message.author == ctx.message.author and message.content

            category = await bot.wait_for("message", timeout = 60, check = checkC)

            await ctx.author.send(content=f"L'image a bien été envoyé dans {game_channel.mention} !",delete_after=20)

            channel = bot.get_channel(882078878150037575)
            guild = bot.get_guild(504673619214073857)

            sans_espace = ""
            separe_mot_reponse = re.split(" |'|’|-", contenu.content) #place dans une liste tous les mots de la réponse
            for i in separe_mot_reponse: #enlève les espaces de la réponse
                sans_espace += i

            nbr_lettres_reponse = len(sans_espace) #stock le nombre de charactère de la réponse
            reponse = del_accent(sans_espace).lower() #transforme toutes les lettres de la réponse en minuscule
            image = screenshot.attachments[0].url# stocker l'url de l'image

            embed = discord.Embed(title = "Qu'est ce que c'est ?") #crée un embed et definit le titre
            embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            embed.set_image(url = image) #ajoute l'image a trouver dans l'embed
            embed.add_field(name = "Nombre de lettres", value = nbr_lettres_reponse)
            embed.add_field(name = "Catégorie", value = category.content)
            embed.set_footer(text = "Version 1.4.3")

            await attente.delete()
            await channel.send(embed = embed) #envoi l'embed dans le channel jeu

            essai = ''
            tentatives = 0

            while essai != reponse:
                sans_espace_essai = ""
                resultat = await bot.wait_for("message")
                separe_mot_essai = re.split(" |'|’|-", resultat.content)
                for i in separe_mot_essai: #enlève les espaces de l'essai
                    sans_espace_essai += i

                essai = del_accent(sans_espace_essai).lower()
                tentatives += 1

                if tentatives == 12 or resultat.content == "#indice":
                    mot = contenu.content
                    indice = random.choice(mot)
                    while indice == " " or indice == "-" or indice == "'" or indice == "’" or indice == ".":
                        indice = random.choice(mot)

                    for lettre in mot:
                        if lettre != indice and lettre != " " and lettre != "-" and lettre != "'" and lettre != "’" and lettre != ".":
                            mot = mot.replace(lettre, "#")
                    await ctx.channel.send(f"**Indice :** {mot}")


            gagnant = resultat.author
                                        #----***POINT***---
            discordMember.add_point(gagnant.id)

            await game_channel.send(content=f'✅ Bonne reponse de {gagnant.mention} || `+1 point`')
        except:
            await ctx.author.send(content=f"IMAGE et/ou REPONSE manquante ! Retape la commande !dm dans {game_channel.mention} pour recommencer", delete_after=15)
            await attente.delete()
    else:
        await ctx.message.delete()
        await ctx.channel.send(content=f"Cette commande s'utilise dans le channel {game_channel.mention}", delete_after=15)
#-------------------------------------------------------------------------------
#@bot.command()
#async def init_mbr_file(ctx):
#    if ctx.channel == bot.get_channel(906948757805998090):
#        members = ctx.guild.members
#        for member in members:
#            if not member.bot:
#                discordMember.init_mbr(member)
#@bot.command()
#async def init_mbr_xp(ctx):
#    if ctx.channel == bot.get_channel(906948757805998090):
#        members = ctx.guild.members
#        for member in members:
#            if not member.bot:
#                discordMember.init_mbr_xp(member)

#@bot.command()
#async def init_msg(ctx):
#    members = ctx.guild.members
#    messages = await ctx.channel.history(limit = None).flatten()
#    for message in messages:
#        for member in members:
#            if not member.bot:
#                x = 0
#                if message.author.id == member.id:
#                    x += 1
#                    discordMember.add_msg(member)
#
#                print(member.name, ":", x)
#    print("-------FIN---------")
#-------------------------------------------------------------------------------
bot.run(os.getenv("TOKEN"))
