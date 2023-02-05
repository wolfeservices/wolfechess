# made with care by wolfe
# version 0.1

#this is a discord bot that plays chess with you, or facilitates a game between two people

import discord
import asyncio
import chess
import chess.svg
import chess.pgn
import chess.engine
from config import *

#initialize the bot
client = discord.Client()

#initialize the chess engine
engine = chess.engine.SimpleEngine.popen_uci(enginePath)