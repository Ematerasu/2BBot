import os
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv

from TeamRandomizer import generate_teams

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='%', intents=intents)
load_dotenv()

LIGA_LEGENDS_CHANNEL_ID = '1001856140486901850'
MAIN_MESSAGE_ID = ''

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

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

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    await bot.process_commands(message)

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
    message = await ctx.fetch_message(int(MAIN_MESSAGE_ID))
    reactions = message.reactions
    players = dict()
    for reaction in reactions:
        async for user in reaction.users():
            if not user.bot:
                try:
                    role = map_emoji_to_role(reaction.emoji.name)
                except ValueError:
                    await ctx.send('Co za zjeb sie bawi emotkami i dodaje nowe? Jeszcze raz odpalcie %customs')
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
    if len(players.keys()) % 5 != 0 or len(players.keys()) / teams_needed != 5:
        await ctx.send(f'Nie da sie was podzielic na {teams_needed} teamy 5-cio osobowe')
        return
    teams = generate_teams(players, teams_needed)
    if isinstance(teams, list):
        await ctx.send('Oto wylosowane teamy:')
        for i, team in enumerate(teams):
            message = ''
            await ctx.send(f'Team {i+1}:')
            for position, player in team.items():
                message += f'.\t{position} - {player}\n'
            await ctx.send(message)
    elif isinstance(teams, str):
        await ctx.send(teams)
    elif teams is None:
        await ctx.send('cos nie pyklo')

bot.run(TOKEN)