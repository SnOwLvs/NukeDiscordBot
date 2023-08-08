import os
import discord
from discord.ext import commands
from colorama import Fore, Style

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

header = r'''
  .-')        .-') _                (`\ .-') /`                 .-') _             .-. .-')     ('-.   
 ( OO ).     ( OO ) )                `.( OO ),'                ( OO ) )            \  ( OO )  _(  OO)  
(_)---\_),--./ ,--,'  .-'),-----. ,--./  .--.              ,--./ ,--,' ,--. ,--.   ,--. ,--. (,------. 
/    _ | |   \ |  |\ ( OO'  .-.  '|      |  |              |   \ |  |\ |  | |  |   |  .'   /  |  .---' 
\  :` `. |    \|  | )/   |  | |  ||  |   |  |,             |    \|  | )|  | | .-') |      /,  |  |     
 '..`''.)|  .     |/ \_) |  |\|  ||  |.'.|  |_)            |  .     |/ |  |_|( OO )|     ' _)(|  '--.  
.-._)   \|  |\    |    \ |  | |  ||         |              |  |\    |  |  | | `-' /|  .   \   |  .--'  
\       /|  | \   |     `'  '-'  '|   ,'.   |              |  | \   | ('  '-'(_.-' |  |\   \  |  `---. 
 `-----' `--'  `--'       `-----' '--'   '--'              `--'  `--'   `-----'    `--' '--'  `------'  
'''

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    clear_console()
    print(Fore.RED + header + Style.RESET_ALL)

def ask_for_confirmation():
    print("\n" + Fore.YELLOW + "WARNING: The following instructions will lead to potentially destructive actions. Use this tool responsibly and only on authorized servers. Proceed at your own risk." + Style.RESET_ALL)
    print(Fore.YELLOW + "To proceed, type 'proceed'. To exit, type 'exit':" + Style.RESET_ALL)
    response = input().lower()
    return response

def display_questions():
    print(Fore.YELLOW + "Choose an option:" + Style.RESET_ALL)
    print("1. Delete all existing channels")
    print("2. Create new channels")
    print("3. Modify server name")
    print("4. Create roles")

def ask_choice():
    print(Fore.YELLOW + "\nEnter the number of your choice:" + Style.RESET_ALL)
    return input()

@bot.event
async def on_ready():
    display_header()
    
    response = ask_for_confirmation()

    if response == 'exit':
        return

    if response == 'proceed':
        display_header()
        while True:
            display_questions()
            choice = ask_choice()

            if choice == '1':
                await delete_all_channels(bot.guilds[0])
            elif choice == '2':
                await proceed_with_create_new_channels()
            elif choice == '3':
                await modify_server_name(bot.guilds[0])
            elif choice == '4':
                await create_roles(bot.guilds[0])
            else:
                print(Fore.YELLOW + "Invalid choice. Please enter a valid number." + Style.RESET_ALL)

            print(Fore.YELLOW + "Do you want to continue? (yes/no):" + Style.RESET_ALL)
            continue_response = input().lower()
            if continue_response == 'no':
                break

async def delete_all_channels(guild):
    for channel in guild.channels:
        await channel.delete()

async def proceed_with_create_new_channels():
    print(Fore.YELLOW + "Enter the base name for the new channels:" + Style.RESET_ALL)
    base_name = input()

    print(Fore.YELLOW + "\nType the number of channels you want to create:" + Style.RESET_ALL)
    num_channels = input()

    try:
        num_channels = int(num_channels)
    except ValueError:
        print(Fore.YELLOW + "Invalid input. Please provide a valid number." + Style.RESET_ALL)
        return

    guild = bot.guilds[0]  # Assumes the bot is only in one guild

    for i in range(num_channels):
        channel_name = f"{base_name}_{i + 1}"
        new_channel = await guild.create_text_channel(channel_name)
        print(f"Created channel: {channel_name}")

role_name = ""

async def modify_server_name(guild):
    global role_name

    print(Fore.YELLOW + "Do you want to modify the server name? (yes/no):" + Style.RESET_ALL)
    response = input().lower()

    if response == 'yes':
        print(Fore.YELLOW + "Enter the new server name:" + Style.RESET_ALL)
        new_name = input()
        if 2 <= len(new_name) <= 100:
            await guild.edit(name=new_name)
            print(Fore.GREEN + f"Server name has been changed to: {new_name}" + Style.RESET_ALL)
            role_name = new_name
        else:
            print(Fore.YELLOW + "Invalid name length. Server name remains unchanged." + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "Server name remains unchanged." + Style.RESET_ALL)
        role_name = ""

async def create_roles(guild):
    global role_name

    print(Fore.YELLOW + "Enter the number of roles you want to create:" + Style.RESET_ALL)
    num_roles = input()

    try:
        num_roles = int(num_roles)
    except ValueError:
        print(Fore.YELLOW + "Invalid input. Please provide a valid number." + Style.RESET_ALL)
        return

    if not role_name:
        print(Fore.YELLOW + "Enter the name for the roles:" + Style.RESET_ALL)
        role_name = input()

    for i in range(num_roles):
        await guild.create_role(name=role_name)
        print(Fore.GREEN + f"Created role: {role_name}" + Style.RESET_ALL)

bot.run("YOUR TOKEN BOT")
