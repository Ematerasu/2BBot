import os
import json
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

from TeamRandomizer import generate_teams
from referee import Referee

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='%', intents=intents)
load_dotenv()

MAIN_MESSAGE_ID = ''

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

TRUSTED_USERS = ['Ematerasu', 'Furazek', 'Lufik', 'kuszy00', 'Kasta', 'Arjey', 'qtJanina', 'Taddy Mason']

EMOJIS = {
    'Top': '<:lolTop:1102992585557016667>',
    'Jungle': '<:lolJungle:1102992533765750815>',
    'Mid': '<:lolMid:1102992566040940646>',
    'Bot': '<:lolBot:1102992555475476560>',
    'Support': '<:lolSupport:1102992574924472444>',
    'Fill': '<:lolFill:1102992545006493746>',
}

def map_emoji_to_role(emoji):
    if emoji == 'lolTop':
        return 'Top'
    
    if emoji == 'lolJungle':
        return 'Jungle'
    
    if emoji == 'lolMid':
        return 'Mid'
    
    if emoji == 'lolBot':
        return 'Bot'
    
    if emoji == 'lolSupport':
        return 'Support'
    
    if emoji == 'lolFill':
        return 'Fill'

    raise ValueError('Invalid emoji')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.command(name='hej')
async def hej(ctx):
    await ctx.send(f'Siema, co tam? :)')

@bot.command(name='customs')
async def customs(ctx):
    global MAIN_MESSAGE_ID
    message = await ctx.send('Gracze chętni na scrimy wybierzcie role które chcecie grać, a ja zaraz zajme się wylosowaniem teamków. Gdy wszyscy wybiorą role, wpiszcie %assign (błagam jedna osoba...)')
    await message.add_reaction(EMOJIS['Top'])
    await message.add_reaction(EMOJIS['Jungle'])
    await message.add_reaction(EMOJIS['Mid'])
    await message.add_reaction(EMOJIS['Bot'])
    await message.add_reaction(EMOJIS['Support'])
    await message.add_reaction(EMOJIS['Fill'])
    MAIN_MESSAGE_ID = message.id

@bot.command(name='assign')
async def assign(ctx, teams_needed=2):
    ref.clear_register()
    message = await ctx.fetch_message(int('1103277254643040256'))
    reactions = message.reactions
    players = dict()
    for reaction in reactions:
        async for user in reaction.users():
            if not user.bot:
                try:
                    role = map_emoji_to_role(reaction.emoji.name)
                except ValueError:
                    await ctx.send('Nie bawcie się emotkami... Usuncie te których nie dodałam i jeszcze raz odpalcie %customs')
                    return
                if user.name in players:
                    if role == 'Fill':
                        players[user.name] = {'Top', 'Jungle', 'Mid', 'Bot', 'Support'}
                    else:
                        players[user.name].add(role)
                else:
                    if role == 'Fill':
                        players[user.name] = {'Top', 'Jungle', 'Mid', 'Bot', 'Support'}
                    else:
                        players[user.name] = {role}
    print(players)
    print(len(players))
    if len(players.keys()) < teams_needed * 5:
        await ctx.send(f"Za mało graczy! Jest was tylko {', '.join(list(players.keys()))}.")
        return
    if len(players.keys()) % 5 != 0 or len(players.keys()) / teams_needed != 5:
        await ctx.send(f'Niestety muszę kogoś wyrzucić :( Jest was {players.keys()} a potrzeba {teams_needed * 5} graczy.)')
        await ctx.send(f'Losowo wyrzucę kogoś z puli graczy.')
        toRemove = random.sample(list(players), len(players.keys()) - teams_needed * 5)
        await ctx.send(f'Wylosowalo: {toRemove}')
        for key in toRemove:
            del players[key]

    teams = generate_teams(players, teams_needed)
    if isinstance(teams, list):
        await ctx.send('Oto wylosowane teamy:')
        for team in teams:
            ref.register_teams(team)
            await ctx.send(team.print_teams())
    elif isinstance(teams, str):
        await ctx.send(teams)
    elif teams is None:
        await ctx.send('cos nie pyklo')

@bot.command(name='leaderboard')
async def leaderboard(ctx):
    with open('ranking.json', 'r') as f:
        ranking = json.load(f)
    players = list(ranking.items())
    if len(players) == 0:
        await ctx.send('Ranking na ten moment jest pusty :(')
        return
    players = sorted(players, key=lambda x: x[1]['wins']/(x[1]['wins']+x[1]['losses']), reverse=True)
    message = ''
    for i, (player, value) in enumerate(players[:10]):
        winratio = round(value['wins']/(value['wins']+value['losses']), 2)
        message += f"{i+1}. {player} - {winratio*100}% winratio\n"
    await ctx.send("Oto Top10 serwera na naszych scrimach:")
    await ctx.send(message)

@bot.command(name='win')
async def win(ctx, arg1=None, arg2=None):
    if arg1 is None or arg2 is None:
        await ctx.send("Podaj numer druzyny która wygrała i przegrała!")
        return
    if ctx.message.author.name not in TRUSTED_USERS:
        await ctx.send(f"Komende moze wykonac tylko osoba z listy: {', '.join(TRUSTED_USERS)}")
        return
    
    try:
        ref.update_leaderboard(int(arg1), int(arg2))
    except ValueError:
        await ctx.send("Któryś z teamów nie jest zarejestrowany w bazie. Sprawdz czy ID są poprawne.")
        return
    await ctx.send(f"Zapisane! Brawa dla Teamu {arg1}!")

@bot.command(name='myrank')
async def myrank(ctx):
    with open('ranking.json', 'r') as f:
        ranking = json.load(f)
    player = ctx.message.author.name
    if player not in ranking:
        await ctx.send(f'Przykro mi, ale nie mam ciebie w bazie danych :( Musisz zagrać jakąś grę najpierw żebym mogła cię wpisać.')
    else:
        players = list(ranking.items())
        players = sorted(players, key=lambda x: x[1]['wins']/(x[1]['wins']+x[1]['losses']), reverse=True)
        for i, (p, value) in enumerate(players):
            if player == p:
                winratio = round(value['wins']/(value['wins']+value['losses']), 4)
                await ctx.send(f'Zajmujesz {i+1} miejsce w rankingu z winratio równym {winratio*100}%.')
                break
    return

@bot.command(name='help')
async def help(ctx):
    message = 'Hej! Jestem 2B, bot do zarządzania 5v5 customami na serwerze Romowie Furazka :)\n'
    message += 'By mnie wywołać użyj jednej z kilku komend:\n'
    message += '.\t `%customs` - rozpoczyna proces tworzenia customów, losowania drużyn itd.\n'
    message += '.\t `%assign <liczba_druzyn=2>` - wymaga najpierw uruchomienia `customs`. Zbierze reakcje z wiadomosci wczesniej i wylosuje druzyny\n'
    message += '.\t `%win <id_druzyny_wygranej> <id_druzyny_przegranej>` - Dla drużyn wylosowanych wcześniej poprawia statystyki w bazie.\n'
    message += '.\t `%leaderboard` - Aktualny ranking serwera\n'
    message += '.\t `%myrank` - twoja pozycja w rankingu wicu\n'
    message += 'Jakby coś nie działało to piszcie do Ematerasu#0001'
    await ctx.send(message)

ref = Referee()

bot.run(TOKEN)