import os
import discord
from discord.ext import commands
from colorama import Fore, Style

intents = discord.Intents.default()
intents.message_content = True
# by SnowFish
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
'''.format(Fore.RED)
# by SnowFish
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
# by SnowFish
def display_header():
    clear_console()
    print(Fore.RED + header + Style.RESET_ALL)
# by SnowFish
def ask_for_confirmation():
    print("\n" + Fore.YELLOW + "WARNING: The following instructions will lead to potentially destructive actions. Use this tool responsibly and only on authorized servers. Proceed at your own risk." + Style.RESET_ALL)
    print(Fore.YELLOW + "To proceed, type 'proceed'. To exit, type 'exit':" + Style.RESET_ALL)
    response = input().lower()
    return response
# by SnowFish
def display_questions():
    print(Fore.YELLOW + "Choose an option:" + Style.RESET_ALL)
    print("1. Delete all existing channels")
    print("2. Create new channels")
    print("3. Modify server name")
    print("4. Create roles")
# by SnowFish
def ask_choice():
    print(Fore.YELLOW + "\nEnter the number of your choice:" + Style.RESET_ALL)
    return input()
# by SnowFish
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
# by SnowFish
            print(Fore.GREEN + "Action completed successfully." + Style.RESET_ALL)
            print(Fore.YELLOW + "Do you want to continue? (yes/no):" + Style.RESET_ALL)
            continue_response = input().lower()
            if continue_response == 'no':
                break

async def delete_all_channels(guild):
    for channel in guild.channels:
        await channel.delete()
    # by SnowFish
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

    print(Fore.YELLOW + "\nDo you want to send a message in the new channels? (yes/no):" + Style.RESET_ALL)
    send_message = input().lower()
# by SnowFish
    if send_message == 'yes':
        print(Fore.YELLOW + "\nEnter the message to be sent in the new channels:" + Style.RESET_ALL)
        message = input()
    else:
        message = None
# by SnowFish
    for i in range(1, num_channels + 1):
        channel_name = f"{base_name}-{i}"
        new_channel = await guild.create_text_channel(channel_name)

        if message:
            await new_channel.send(message)
# by SnowFish
    print(Fore.GREEN + "\nChannels created successfully." + Style.RESET_ALL)
# by SnowFish
async def modify_server_name(guild):
    print(Fore.YELLOW + "\nDo you want to modify the server name? (yes/no):" + Style.RESET_ALL)
    modify_name = input().lower()
# by SnowFish
    if modify_name == 'yes':
        print(Fore.YELLOW + "Enter the new server name:" + Style.RESET_ALL)
        new_name = input()
# by SnowFish
        try:
            await guild.edit(name=new_name)
            print(Fore.GREEN + "\nServer name modified successfully." + Style.RESET_ALL)
        except discord.errors.HTTPException:
            print(Fore.YELLOW + "Invalid server name. Please provide a name between 2 and 100 characters." + Style.RESET_ALL)
    elif modify_name == 'no':
        return
# by SnowFish
async def create_roles(guild):
    print(Fore.YELLOW + "\nEnter the name for the roles:" + Style.RESET_ALL)
    role_name = input()

    print(Fore.YELLOW + "Enter the number of roles to create:" + Style.RESET_ALL)
    num_roles = input()
# by SnowFish
    try:
        num_roles = int(num_roles)
    except ValueError:
        print(Fore.YELLOW + "Invalid input. Please provide a valid number." + Style.RESET_ALL)
        return
# by SnowFish
    for _ in range(num_roles):
        await guild.create_role(name=role_name)
# by SnowFish
bot.run('YOUR BOT TOKEN')
