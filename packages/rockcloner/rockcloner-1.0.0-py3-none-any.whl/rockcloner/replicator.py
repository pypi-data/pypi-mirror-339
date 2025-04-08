# replicator.py
import discord
import asyncio
import random
import requests
import aiohttp
from colorama import Fore, init, Style

init()

# Colored log helpers
def print_bar():
    print(Fore.CYAN + "+------------------------------------------------------+" + Style.RESET_ALL)

def print_add(message):
    print_bar()
    print(Fore.GREEN + f"[+] {message}" + Style.RESET_ALL)

def print_delete(message):
    print_bar()
    print(Fore.RED + f"[-] {message}" + Style.RESET_ALL)

def print_warning(message):
    print_bar()
    print(Fore.YELLOW + f"[!] {message}" + Style.RESET_ALL)

def print_error(message):
    print_bar()
    print(Fore.MAGENTA + f"[x] {message}" + Style.RESET_ALL)

def print_info(message):
    print_bar()
    print(Fore.BLUE + f"{message}" + Style.RESET_ALL)

class Clone:
    @staticmethod
    async def roles_delete(guild_to: discord.Guild):
        if not guild_to.me.guild_permissions.manage_roles:
            print_warning("Skipping role deletion: Requires 'Manage Roles' permission")
            return
        for role in guild_to.roles:
            try:
                if role.name != "@everyone":
                    await role.delete()
                    print_delete(f"Deleted role {role.name}")
                    await asyncio.sleep(random.uniform(0.1, 0.3))
            except discord.Forbidden:
                print_error(f"Cannot delete role {role.name}: Insufficient permissions")
            except discord.HTTPException as e:
                print_error(f"HTTP error deleting role {role.name}: {str(e)}")

    @staticmethod
    async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
        if not guild_to.me.guild_permissions.manage_roles:
            print_warning("Skipping role creation: Requires 'Manage Roles' permission")
            return
        roles = [role for role in guild_from.roles if role.name != "@everyone"][::-1]
        for role in roles:
            try:
                await guild_to.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    colour=role.colour,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                print_add(f"The role {role.name} was created")
                await asyncio.sleep(random.uniform(0.1, 0.3))
            except discord.Forbidden:
                print_error(f"Cannot create role {role.name}: Insufficient permissions")
            except discord.HTTPException as e:
                print_error(f"HTTP error creating role {role.name}: {str(e)}")

    @staticmethod
    async def channels_delete(guild_to: discord.Guild):
        if not guild_to.me.guild_permissions.manage_channels:
            print_warning("Skipping channel deletion: Requires 'Manage Channels' permission")
            return
        for channel in guild_to.channels:
            try:
                await channel.delete()
                print_delete(f"Deleted channel {channel.name}")
                await asyncio.sleep(random.uniform(0.1, 0.3))
            except discord.Forbidden:
                print_error(f"Cannot delete channel {channel.name}: Insufficient permissions")
            except discord.HTTPException as e:
                print_error(f"HTTP error deleting channel {channel.name}: {str(e)}")

    @staticmethod
    async def categories_create(guild_to: discord.Guild, guild_from: discord.Guild):
        if not guild_to.me.guild_permissions.manage_channels:
            print_warning("Skipping category creation: Requires 'Manage Channels' permission")
            return
        for channel in guild_from.categories:
            try:
                overwrites_to = {}
                for key, value in channel.overwrites.items():
                    if isinstance(key, discord.Role):
                        role = discord.utils.get(guild_to.roles, name=key.name)
                        if role:
                            overwrites_to[role] = value
                    elif isinstance(key, discord.Member):
                        member = guild_to.get_member(key.id)
                        if member:
                            overwrites_to[member] = value

                await guild_to.create_category(
                    name=channel.name,
                    overwrites=overwrites_to,
                    position=channel.position
                )
                print_add(f"The category {channel.name} was created")
                await asyncio.sleep(random.uniform(0.1, 0.3))
            except discord.Forbidden:
                print_error(f"Cannot create category {channel.name}: Insufficient permissions")
            except discord.HTTPException as e:
                print_error(f"HTTP error creating category {channel.name}: {str(e)}")

    @staticmethod
    async def channels_create(guild_to: discord.Guild, guild_from: discord.Guild):
        if not guild_to.me.guild_permissions.manage_channels:
            print_warning("Skipping channel creation: Requires 'Manage Channels' permission")
            return
        text_channels = [c for c in guild_from.channels if isinstance(c, discord.TextChannel)]
        for channel in text_channels:
            try:
                category = discord.utils.get(guild_to.categories, name=channel.category.name) if channel.category else None
                overwrites_to = {}
                for key, value in channel.overwrites.items():
                    if isinstance(key, discord.Role):
                        role = discord.utils.get(guild_to.roles, name=key.name)
                        if role:
                            overwrites_to[role] = value
                    elif isinstance(key, discord.Member):
                        member = guild_to.get_member(key.id)
                        if member:
                            overwrites_to[member] = value
                await guild_to.create_text_channel(
                    name=channel.name,
                    overwrites=overwrites_to,
                    position=channel.position,
                    topic=channel.topic,
                    slowmode_delay=channel.slowmode_delay,
                    nsfw=channel.nsfw,
                    category=category
                )
                print_add(f"The text channel {channel.name} was created")
                await asyncio.sleep(random.uniform(0.1, 0.3))
            except discord.Forbidden:
                print_error(f"Cannot create text channel {channel.name}: Insufficient permissions")
            except discord.HTTPException as e:
                print_error(f"HTTP error creating text channel {channel.name}: {str(e)}")

        voice_channels = [c for c in guild_from.channels if isinstance(c, discord.VoiceChannel)]
        for channel in voice_channels:
            try:
                category = discord.utils.get(guild_to.categories, name=channel.category.name) if channel.category else None
                overwrites_to = {}
                for key, value in channel.overwrites.items():
                    if isinstance(key, discord.Role):
                        role = discord.utils.get(guild_to.roles, name=key.name)
                        if role:
                            overwrites_to[role] = value
                    elif isinstance(key, discord.Member):
                        member = guild_to.get_member(key.id)
                        if member:
                            overwrites_to[member] = value
                await guild_to.create_voice_channel(
                    name=channel.name,
                    overwrites=overwrites_to,
                    position=channel.position,
                    bitrate=channel.bitrate,
                    user_limit=channel.user_limit,
                    category=category
                )
                print_add(f"The voice channel {channel.name} was created")
                await asyncio.sleep(random.uniform(0.1, 0.3))
            except discord.Forbidden:
                print_error(f"Cannot create voice channel {channel.name}: Insufficient permissions")
            except discord.HTTPException as e:
                print_error(f"HTTP error creating voice channel {channel.name}: {str(e)}")

    @staticmethod
    async def emojis_create(guild_to: discord.Guild, guild_from: discord.Guild):
        if not guild_to.me.guild_permissions.manage_emojis:
            print_warning("Skipping emoji creation: Requires 'Manage Emojis' permission")
            return
        if not guild_from.emojis:
            print_warning("No emojis found in the source server")
            return
        for emoji in guild_from.emojis:
            try:
                if not discord.utils.get(guild_to.emojis, name=emoji.name):
                    async with aiohttp.ClientSession() as session:
                        async with session.get(str(emoji.url)) as resp:
                            if resp.status == 200:
                                image_data = await resp.read()
                                await guild_to.create_custom_emoji(name=emoji.name, image=image_data)
                                print_add(f"The emoji {emoji.name} was created")
                                await asyncio.sleep(0.5)
                else:
                    print_add(f"Emoji {emoji.name} already exists")
            except discord.Forbidden:
                print_error(f"Cannot create emoji {emoji.name}: Insufficient permissions")
            except (discord.HTTPException, Exception) as e:
                print_error(f"Error creating emoji {emoji.name}: {str(e)}")

    @staticmethod
    async def guild_edit(guild_to: discord.Guild, guild_from: discord.Guild):
        if not guild_to.me.guild_permissions.manage_guild:
            print_warning("Skipping server edit: Requires 'Manage Server' permission")
            return
        try:
            icon_content = None
            if guild_from.icon:
                async with aiohttp.ClientSession() as session:
                    async with session.get(guild_from.icon.url) as resp:
                        if resp.status == 200:
                            icon_content = await resp.read()
            else:
                print_warning(f"The server {guild_from.name} has no icon")
            await guild_to.edit(name=guild_from.name, icon=icon_content)
            print_add(f"Server edited: {guild_to.name} (name and icon updated)")
        except discord.Forbidden:
            print_error("Cannot edit server: Insufficient permissions")
        except Exception as e:
            print_error(f"Error editing server: {str(e)}")

    @staticmethod
    def log_server_structure(guild_from: discord.Guild):
        print_add(f"Logging structure of source server: {guild_from.name}")
        print_add("Roles:")
        for role in guild_from.roles:
            if role.name != "@everyone":
                print(f"  - {Fore.YELLOW}{role.name}{Fore.RESET} (Color: {role.colour}, Hoist: {role.hoist}, Mentionable: {role.mentionable})")
        print_add("Categories and Channels:")
        for category in guild_from.categories:
            print(f"  - Category: {Fore.YELLOW}{category.name}{Fore.RESET}")
            for channel in category.channels:
                print(f"    - {Fore.YELLOW}{channel.name}{Fore.RESET} ({'Text' if isinstance(channel, discord.TextChannel) else 'Voice'})")
        print_add("Emojis:")
        for emoji in guild_from.emojis:
            print(f"  - {Fore.YELLOW}{emoji.name}{Fore.RESET} (URL: {emoji.url})")