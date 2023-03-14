import discord, argparse, colorama, os, threading, asyncio, requests, time
from colorama import Fore

tokens = [
    ""
]

ids = [
    ""
]
guild_count = 0
banner = ""

def counting_guild(guild_count):
    for token in tokens:
        header = {"Authorization": token, "Content-Type": 'application/json'}
        requests_guild = requests.get('https://discord.com/api/users/@me/guilds', headers=header).json()
        guild_count = len(requests_guild) + guild_count
    os.system("clear")
    banner = (f"""
                             ██████╗ ██████╗       Just a little spyware for discord
                            ██╔═████╗╚════██╗      02 Know everything 
                            ██║██╔██║ █████╔╝
                            ████╔╝██║██╔═══╝       Tokens load : {Fore.LIGHTRED_EX}{len(tokens)}{Fore.WHITE}
                            ╚██████╔╝███████╗      IDs    load : {Fore.LIGHTRED_EX}{len(ids)}{Fore.WHITE}
                             ╚═════╝ ╚══════╝      Guilds load : {Fore.LIGHTRED_EX}{int(guild_count)}{Fore.WHITE}
            """)
    return banner



async def spy_02(token, id):
    client = discord.Client()

    @client.event
    async def on_ready():
        pass

    @client.event
    async def on_voice_state_update(member, before, after):
        if member.id == int(id):
            if before.channel is None and after.channel is not None:
                print(f'[{Fore.GREEN}+{Fore.WHITE}] {Fore.LIGHTMAGENTA_EX}{member}{Fore.WHITE} Joined voice channel {Fore.LIGHTMAGENTA_EX}{after.channel.name}{Fore.WHITE} in {Fore.LIGHTMAGENTA_EX}{after.channel.guild.name} ({after.channel.guild.id}){Fore.WHITE}')

            elif before.channel is not None and after.channel is None:
                print(f'[{Fore.RED}-{Fore.WHITE}] {Fore.LIGHTMAGENTA_EX}{member}{Fore.WHITE} Left voice channel {Fore.LIGHTMAGENTA_EX}{before.channel.name}{Fore.WHITE} in {Fore.LIGHTMAGENTA_EX}{before.channel.guild.name} \t ({before.channel.guild.id}){Fore.WHITE}')
        

    @client.event
    async def on_message(message):
        if message.author.id == int(id):
            print(f"[{Fore.GREEN}+{Fore.WHITE}] {Fore.LIGHTMAGENTA_EX}{message.author}{Fore.WHITE} Send this message : {Fore.LIGHTMAGENTA_EX}{message.content} \t {message.channel.guild} ({message.guild.id}){Fore.WHITE}")

 
    @client.event
    async def on_message_delete(message):
        if message.author.id == int(id):
            print(f"[{Fore.RED}-{Fore.WHITE}] {Fore.LIGHTMAGENTA_EX}{message.author}{Fore.WHITE} Delete this message : {Fore.LIGHTMAGENTA_EX}{message.content} \t {message.channel.guild} ({message.channel.guild.id}){Fore.WHITE}")



    await client.start(token)


async def main(id):
    tasks = [asyncio.ensure_future(spy_02(token, id)) for token in tokens]
    await asyncio.gather(*tasks)


def start_threads():
    banner = counting_guild(guild_count)
    print(banner)
    time.sleep(2)

    threads = []
    for id in ids:
        t = threading.Thread(target=asyncio.run, args=(main(id),))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

start_threads()
