# made with care by wolfe
# version 0.1

#this is a discord bot that plays chess with you, or facilitates a game between two people

import discord
import asyncio
import chess
import chess.svg
import chess.pgn
import chess.engine
from config import dToken as TOKEN

#bot setup
client = discord.Client()
PREFIX = '!'
listening_rooms = []
playing = []
challenge_list = []

#defining static utility functions
def get_board_image(board):
    return chess.svg.board(board=board)

def help(message):
    return message.channel.send('''
    Commands:
    !help - displays this message
    !newroom - creates a new chess room
    !challenge <user> - challenges a user to a game
    !accept <user> - accepts a challenge from a user
    !decline <user> - declines a challenge from a user
    !resign - resigns from a game
    !draw - offers a draw
    !acceptdraw - accepts a draw offer
    !declinedraw - declines a draw offer
    !playbot <engine> - plays a game against the bot with a specific engine
    !listengines - lists the available engines
    !close - closes the current room, if the room is inactive for 10 minutes, it will close automatically.
    !move <move> - makes a move (e.g. !move e2e4)
    !board - displays the current board
    ''')

def newroom(message):
  #make room name
    roomname = message.author.name + "'s chess room"
    #make room and set permissions, bot can read and write, user can read and write, everyone else can read
    room = message.guild.create_text_channel(roomname, overwrites={message.guild.default_role: discord.PermissionOverwrite(read_messages=True), message.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True), message.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)})
    #send a message to the room to let the user know it was created, mention the user
    room.send('Room created, ' + message.author.mention)
    #add the user to the playing list
    playing.append(message.author)
    #send room management instructions
    room.send('''
    To manage the room, use the following commands:
    !challenge <user> - challenges a user to a game
    !playbot <engine> - plays a game against the bot with a specific engine
    !listengines - lists the available engines
    !close - closes the current room, if the room is inactive for 10 minutes, it will close automatically.''')
    #save the room to the list of listening rooms
    listening_rooms.append(room)
    return

def start_match(user1, user2, message):
    #initate a new game
    board = chess.Board()
    #send the board image to the room
    message.channel.send(get_board_image(board))
    #start the game loop
    while not board.is_game_over():
        #if it is user1's turn, then wait for their move
        if board.turn == chess.WHITE:
            #wait for a move from user1
            move = await client.wait_for('message', check=lambda message: message.author == user1)
            #if the move is valid, then make it
            if board.is_legal(chess.Move.from_uci(move)):
                board.push(chess.Move.from_uci(move))
                #send the board image to the room
                message.channel.send(get_board_image(board))
            #if the move is not valid, then tell the user and wait for another move
            else:
                message.channel.send('Invalid move, please try again.')
        #if it is user2's turn, then wait for their move
        elif board.turn == chess.BLACK:
            #wait for a move from user2
            move = await client.wait_for('message', check=lambda message: message.author == user2)
            #if the move is valid, then make it
            if board.is_legal(chess.Move.from_uci(move)):
                board.push(chess.Move.from_uci(move))
                #send the board image to the room
                message.channel.send(get_board_image(board))
            #if the move is not valid, then tell the user and wait for another move
            else:
                message.channel.send('Invalid move, please try again.')
    #if the game is over, then send the result to the room
    message.channel.send(board.result())
    #remove the users from the playing list
    playing.remove(user1)
    playing.remove(user2)
    



    

def challenge(message):

def accept(message):

    
    




        



#start the bot
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

#start listening for messages
@client.event
async def on_message(message):
    #we do not want the bot to reply to itself
    if message.author == client.user:
        return
        #if the message starts with the assigned prefix, then we will process it
    if message.content.startswith(PREFIX):
        #pass the message to the command processor
        await process_command(message)

#process commands
async def process_command(message):
    #strip the prefix from the message
    command = message.content[len(PREFIX):]
    #split the command into a list of arguments
    args = command.split()
    #if command is help, then print the help message
    if args[0] == 'help':
        await help(message)
    #if command is newroom, then create a new room
    elif args[0] == 'newroom':
        await newroom(message)
    #if command is challenge, then challenge a user
    elif args[0] == 'challenge':
        await challenge(message)
    #if command is accept, then accept a challenge
    elif args[0] == 'accept':
        await accept(message)
    #if command is decline, then decline a challenge
    elif args[0] == 'decline':
        await decline(message)
    #if command is resign, then resign from a game
    elif args[0] == 'resign':
        await resign(message)
    #if command is draw, then offer a draw
    elif args[0] == 'draw':
        await draw(message)
    #if command is acceptdraw, then accept a draw offer
    elif args[0] == 'acceptdraw':
        await acceptdraw(message)
    #if command is declinedraw, then decline a draw offer
    elif args[0] == 'declinedraw':
        await declinedraw(message)
    #if command is playbot, then play a game against the bot with a specific engine
    elif args[0] == 'playbot':
        engine = args[1]
        await playbot(message engine)
    #if command is listengines, then list the available engines
    elif args[0] == 'listengines':
        await listengines(message)
    #if command is close, then close the current room
    elif args[0] == 'close':
        await close(message)
    #if command is move, then make a move
    elif args[0] == 'move':
        await move(message)
    #if command is board, then display the current board
    elif args[0] == 'board':
        await board(message)
    
    #check if the room is inactive for 10 minutes, if so, close it
    if message.channel in listening_rooms:
        if time.time() - message.channel.last_message_at > 600:
            await close(message)
        
#run the bot
client.run(TOKEN)


