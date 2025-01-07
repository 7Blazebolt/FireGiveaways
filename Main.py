import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Store ongoing games
coinflip_games = {}
rps_games = {}

@bot.event
async def on_ready():
    print(f"{bot.user} is online and ready!")

# Coinflip command
@bot.command()
async def coinflip(ctx, member: discord.Member, bet: int):
    if ctx.author == member:
        await ctx.send("You can't challenge yourself!")
        return
    
    if ctx.author.id in coinflip_games or member.id in coinflip_games:
        await ctx.send("One of the players is already in a coinflip game!")
        return

    coinflip_games[ctx.author.id] = {
        "challenger": ctx.author,
        "opponent": member,
        "bet": bet
    }

    await ctx.send(f"{member.mention}, {ctx.author.name} has challenged you to a coinflip for {bet} coins! Use `!accept` or `!decline`.")

# Accept or Decline CF
@bot.command()
async def accept(ctx):
    game = next((game for game in coinflip_games.values() if game["opponent"].id == ctx.author.id), None)
    if not game:
        await ctx.send("You have no pending challenges!")
        return

    result = "heads" if random.randint(0, 1) == 0 else "tails"
    winner = game["challenger"] if result == "heads" else game["opponent"]

    await ctx.send(f"The coin landed on **{result}**! 🎉 {winner.mention} wins {game['bet']} coins!")
    del coinflip_games[game["challenger"].id]

@bot.command()
async def decline(ctx):
    game = next((game for game in coinflip_games.values() if game["opponent"].id == ctx.author.id), None)
    if not game:
        await ctx.send("You have no pending challenges!")
        return

    await ctx.send(f"{ctx.author.name} declined the coinflip challenge from {game['challenger'].mention}.")
    del coinflip_games[game["challenger"].id]

# Rock-Paper-Scissors command
@bot.command()
async def rps(ctx, member: discord.Member):
    if ctx.author == member:
        await ctx.send("You can't challenge yourself!")
        return

    if ctx.author.id in rps_games or member.id in rps_games:
        await ctx.send("One of the players is already in a rock-paper-scissors game!")
        return

    rps_games[ctx.author.id] = {
        "challenger": ctx.author,
        "opponent": member,
        "choices": {}
    }

    await ctx.send(f"{member.mention}, {ctx.author.name} has challenged you to Rock-Paper-Scissors! Both players should DM me their choices (`rock`, `paper`, or `scissors`).")

@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.guild:
        return

    # Handle RPS choices
    for game in rps_games.values():
        if message.author.id in [game["challenger"].id, game["opponent"].id]:
            if message.content.lower() in ["rock", "paper", "scissors"]:
                game["choices"][message.author.id] = message.content.lower()
                await message.author.send("Your choice has been recorded!")
                
                # Check if both players have chosen
                if len(game["choices"]) == 2:
                    challenger_choice = game["choices"][game["challenger"].id]
                    opponent_choice = game["choices"][game["opponent"].id]
                    
                    result = determine_rps_winner(challenger_choice, opponent_choice)
                    if result == "draw":
                        result_message = "It's a draw! Both players chose the same."
                    elif result == "challenger":
                        result_message = f"{game['challenger'].mention} wins! 🎉 {challenger_choice} beats {opponent_choice}."
                    else:
                        result_message = f"{game['opponent'].mention} wins! 🎉 {opponent_choice} beats {challenger_choice}."
                    
                    await message.channel.send(result_message)
                    del rps_games[game["challenger"].id]

def determine_rps_winner(choice1, choice2):
    if choice1 == choice2:
        return "draw"
    if (choice1 == "rock" and choice2 == "scissors") or \
       (choice1 == "paper" and choice2 == "rock") or \
       (choice1 == "scissors" and choice2 == "paper"):
        return "challenger"
    return "opponent"

# Replace with your bot's token
bot.run("MTMxNzEyNjI3Mzc1OTE4NzExNg.GEyRfd.jHfBj91sHRFle-BgYQ_jwyS4hSaE-sLmDanbyc")
