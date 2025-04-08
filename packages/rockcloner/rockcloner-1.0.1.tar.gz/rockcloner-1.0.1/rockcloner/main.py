from os import system
import os
import sys
import time
import platform
import psutil
import traceback
import asyncio
import discord
import inquirer
import aiohttp
from pathlib import Path
from colorama import Fore, init, Style
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
from pyfiglet import Figlet
from .replicator import Clone  
sys.path.insert(0, str(Path(__file__).parent.parent))
init()
console = Console()

version = '1'
versao_python = sys.version.split()[0]
client = discord.Client()

SUPPORT_LINK = "https://d3vr.vercel.app/"

def clear_screen():
    system('cls' if platform.system() == 'Windows' else 'clear')

def ascii_banner(text, font='bloody'):
    f = Figlet(font=font)
    return f.renderText(text)

def print_logo():
    banner = ascii_banner("ROCK V!", font="bloody")
    styled_banner = f"[bold yellow]{banner}[/bold yellow]"
    console.print(Panel.fit(styled_banner, title="[bold blue]Rock V1[/bold blue]", border_style="blue"))

def print_status(text, color="cyan"):
    console.print(f"[bold {color}]• {text}[/bold {color}]")

def loading_spinner(task_message, duration=3):
    with Progress(
        SpinnerColumn(spinner_name="dots", style="yellow"),
        "[progress.description]{task.description}",
        TimeElapsedColumn(),
        transient=True
    ) as progress:
        task = progress.add_task(f"[cyan]{task_message}", total=None)
        time.sleep(duration)
        progress.stop()

def restart():
    python = sys.executable
    os.execv(python, [python] + sys.argv)

def show_documentation():
    doc_text = f"""[yellow]
[bold blue]Welcome to Rock V1 - Discord Server Cloner[/bold blue]

This tool allows you to clone a Discord server's:
• Roles
• Categories
• Channels
• Emojis (optional)
• Server icon and name

Instructions:
1. Provide a valid user token
2. Enter Source and Destination Server IDs
3. Configure what to clone
4. Let Rock V1 do its magic ✨

[bold cyan]Need help? Join our support server:[/bold cyan]
[blue]{SUPPORT_LINK}[/blue]
[/yellow]"""
    console.print(Panel.fit(doc_text, title="📘 Documentation", border_style="blue"))
    input(f"\n{Fore.CYAN}Press ENTER to return to menu...{Style.RESET_ALL}")

def show_tips():
    tips = """[bold cyan]
Shortcuts:
- [Y] to confirm inputs
- [N] to re-enter info
- [Ctrl+C] to exit

Make sure:
- You’re in both servers
- Bot has required permissions
- Server IDs are correct
[/bold cyan]"""
    console.print(Panel(tips, title="💡 Tips & Shortcuts", border_style="yellow"))
    input(f"\n{Fore.CYAN}Press ENTER to return to menu...{Style.RESET_ALL}")

def get_user_preferences():
    preferences = {
        'guild_edit': True,
        'channels_delete': True,
        'roles_delete': True,
        'roles_create': True,
        'categories_create': True,
        'channels_create': True,
        'emojis_create': False
    }

    panel_content = "\n".join([f"[bold blue]•[/bold blue] {key.replace('_', ' ').capitalize()}: [yellow]{value}[/yellow]" for key, value in preferences.items()])
    console.print(Panel(panel_content, title="Preferences Summary", style="bold blue"))

    answers = inquirer.prompt([inquirer.List('reconfigure', message='Reconfigure settings?', choices=['Yes', 'No'], default='No')])
    if answers['reconfigure'] == 'Yes':
        questions = [
            inquirer.Confirm('guild_edit', message='Edit server icon/name?', default=True),
            inquirer.Confirm('channels_delete', message='Delete channels?', default=True),
            inquirer.Confirm('roles_delete', message='Delete roles?', default=True),
            inquirer.Confirm('roles_create', message='Clone roles?', default=True),
            inquirer.Confirm('categories_create', message='Clone categories?', default=True),
            inquirer.Confirm('channels_create', message='Clone channels?', default=True),
            inquirer.Confirm('emojis_create', message='Clone emojis?', default=False)
        ]
        answers = inquirer.prompt(questions)
        preferences.update(answers)

    clear_screen()
    print_logo()
    return preferences

def show_main_menu():
    while True:
        clear_screen()
        print_logo()
        print_status("1. Run Rock V1", "green")
        print_status("2. Show Documentation", "blue")
        print_status("3. Show Tips & Shortcuts", "yellow")
        print_status("4. Exit", "red")

        choice = input(f"\n{Fore.CYAN}Choose an option (1/2/3/4): {Style.RESET_ALL}")
        if choice == '1':
            return
        elif choice == '2':
            clear_screen()
            print_logo()
            show_documentation()
        elif choice == '3':
            clear_screen()
            print_logo()
            show_tips()
        elif choice == '4':
            print_status("Exiting... Goodbye!", "red")
            sys.exit()
        else:
            print_status("Invalid choice, try again!", "red")
            time.sleep(2)

# Main Entry Point
show_main_menu()

clear_screen()
print_logo()

while True:
    clear_screen()
    print_logo()

    print(f"{Fore.BLUE}{'-' * 60}")
    print(f"{Fore.YELLOW}{'ROCK CLONER V1':^60}")
    print(f"{Fore.BLUE}{'-' * 60}{Style.RESET_ALL}")

    token = input(f"{Fore.YELLOW} [1] Your Token\n   {Fore.BLUE}> {Style.RESET_ALL}")
    guild_s = input(f"{Fore.YELLOW} [2] Source Server ID\n   {Fore.BLUE}> {Style.RESET_ALL}")
    guild = input(f"{Fore.YELLOW} [3] Destination Server ID\n   {Fore.BLUE}> {Style.RESET_ALL}")

    clear_screen()
    print_logo()

    print(f"{Fore.BLUE}{'-' * 60}")
    print(f"{Fore.YELLOW}{'PLEASE CONFIRM YOUR DETAILS':^60}")
    print(f"{Fore.BLUE}{'-' * 60}{Style.RESET_ALL}")

    print(f"{Fore.YELLOW} Token:              {Style.RESET_ALL}{'*' * len(token)}")
    print(f"{Fore.YELLOW} Source Server ID:   {Style.RESET_ALL}{guild_s}")
    print(f"{Fore.YELLOW} Destination Server ID: {Style.RESET_ALL}{guild}")

    print(f"\n{Fore.BLUE}{'-' * 60}{Style.RESET_ALL}")
    confirm = input(f"{Fore.YELLOW} Is the above information correct? (Y/N)\n   {Fore.BLUE}> {Style.RESET_ALL}")

    if confirm.strip().upper() == 'Y':
        if not (guild_s.isnumeric() and guild.isnumeric()):
            print_status("Server IDs must be numbers!", "red")
            input(f"{Fore.BLUE}Press Enter to try again...{Style.RESET_ALL}")
            continue
        if not all([token.strip(), guild_s.strip(), guild.strip()]):
            print_status("Fields cannot be blank!", "red")
            input(f"{Fore.BLUE}Press Enter to try again...{Style.RESET_ALL}")
            continue
        break
    else:
        print(f"\n{Fore.YELLOW} Let's try again...{Style.RESET_ALL}")
        input(f"{Fore.BLUE}Press Enter to restart setup...{Style.RESET_ALL}")



input_guild_id, output_guild_id = guild_s, guild

@client.event
async def on_ready():
    try:
        start_time = time.time()
        clear_screen()
        print_logo()

        table = Table(title="Rock V1 Environment", style="bold blue")
        table.add_column("Component", style="bold cyan")
        table.add_column("Version", style="yellow")
        table.add_row("Rock V1", version)
        table.add_row("discord.py-self", discord.__version__)
        table.add_row("Python", versao_python)
        console.print(table)

        loading_spinner("Authenticating...", 3)

        guild_from = client.get_guild(int(input_guild_id))
        guild_to = client.get_guild(int(output_guild_id))
        if not guild_from or not guild_to:
            raise ValueError("Invalid guilds! Check server IDs and access.")

        preferences = get_user_preferences()
        if not any(preferences.values()):
            preferences = {k: True for k in preferences}

        permissions = guild_to.me.guild_permissions
        if not (permissions.manage_guild and permissions.manage_roles and permissions.manage_channels):
            print_status("Permissions insufficient, switching to log-only.", "red")
            Clone.log_server_structure(guild_from)
        else:
            tasks = []
            if preferences['channels_delete']:
                tasks.append(Clone.channels_delete(guild_to))
            if preferences['roles_delete']:
                tasks.append(Clone.roles_delete(guild_to))
            if preferences['roles_create']:
                tasks.append(Clone.roles_create(guild_to, guild_from))
            if preferences['categories_create']:
                tasks.append(Clone.categories_create(guild_to, guild_from))
            if preferences['channels_create']:
                tasks.append(Clone.channels_create(guild_to, guild_from))
            if preferences['emojis_create']:
                tasks.append(Clone.emojis_create(guild_to, guild_from))
            if preferences['guild_edit']:
                tasks.append(Clone.guild_edit(guild_to, guild_from))

            for task in tasks:
                try:
                    await task
                except discord.HTTPException as e:
                    if e.status == 429:
                        retry_after = e.retry_after
                        print_status(f"Rate limited for {retry_after}s", "yellow")
                        await asyncio.sleep(retry_after)
                        await task
                    else:
                        raise

        duration = time.strftime("%M:%S", time.gmtime(time.time() - start_time))
        print_status(f"Operation completed in {duration}", "blue")
        print_status(f"Thank you for using Rock V1 💙", "cyan")
        console.print(Panel.fit(f"[bold green]Join our support Discord server:[/bold green]\n[blue]{SUPPORT_LINK}[/blue]", title="💬 Support", border_style="green"))
        await asyncio.sleep(10)
        await client.close()

    except Exception as e:
        print_status(f"Error: {str(e)}", "red")
        traceback.print_exc()
        console.print(Panel(
            f"[red]• Check server IDs\n• Ensure you're in both servers\n• Token must be valid\n[/red]\n\n[bold cyan]Need help? Join our support server:[/bold cyan]\n[blue]{SUPPORT_LINK}[/blue]",
            title="❌ Troubleshooting", border_style="red"
        ))
        loading_spinner("Restarting in 15 seconds...", 15)
        restart()

try:
    client.run(token)
except discord.LoginFailure:
    print_status("Invalid token.", "red")
    loading_spinner("Restarting in 10 seconds...", 10)
    restart()
