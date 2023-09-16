import discord
from discord.ext import commands
import sys, os, subprocess
from scramble import gen_scramble
from cube import Cube
from cube_image import gen_cube_image
from cube_moves import is_valid_move

TOKEN = ""

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="c!", intents=intents)

active_cubes = {}

@client.event
async def on_ready():
    print("Rubik's cube bot is started")

@client.command(pass_context=True, aliases=["n"])
async def new(ctx):
    user = str(ctx.message.author)
    if user in active_cubes:
        await ctx.send(f"{ctx.message.author.mention} Cube already active, close to restart")
        return

    cube = Cube(3)
    while cube.is_solved():
        scr = gen_scramble(3)
        for move in scr.split(" "):
            cube.do_move(move)
    active_cubes[user] = cube

    gen_cube_image(active_cubes[user])
    embed = discord.Embed(title=f"{ctx.author.display_name}'s cube", description="", color=0x954535)
    with open("cube.png", "rb") as f:
        embed.set_image(url="attachment://cube.png")
        await ctx.send(file=discord.File(f), embed=embed)

@client.command(pass_context=True, aliases=["q", "c"])
async def close(ctx):
    user = str(ctx.message.author)
    if user not in active_cubes:
        await ctx.send(f"{ctx.message.author.mention} No cube currently active")
        return
    
    del active_cubes[user]
    await ctx.send(f"{ctx.message.author.mention} Closed cube")

@client.command(pass_context=True, aliases=["m"])
async def move(ctx, *, move_str):
    move_str = move_str.replace("’", "'")
    user = str(ctx.message.author)
    if user not in active_cubes:
        await ctx.send(f"{ctx.message.author.mention} No cube currently active")
        return
    
    # verify moves
    moves = move_str.split(" ")
    for i, m in enumerate(moves):
        if not is_valid_move(m):
            await ctx.send(f"{ctx.message.author.mention} Invalid move {m} at move {i+1}")
            return
    
    for m in moves:
        active_cubes[user].do_move(m)

    gen_cube_image(active_cubes[user])
    embed = discord.Embed(title=f"{ctx.author.name}'s cube", description="", color=0xffff66)
    with open("cube.png", "rb") as f:
        embed.set_image(url="attachment://cube.png")
        await ctx.send(file=discord.File(f), embed=embed)

    # if cube is solved
    if active_cubes[user].is_solved():
        await ctx.send(f"{ctx.message.author.mention} Cube is solved!")
        del active_cubes[user]

client.run(TOKEN)