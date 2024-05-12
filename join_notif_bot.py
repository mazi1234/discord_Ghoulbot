import discord
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv
from settings import Environs
#get the environment variables
load_dotenv()
#declare constant values
intents = discord.Intents.all() #need this to get correct info on users.
# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)
#this is STAGING
@bot.event
async def on_ready():
    """_summary_
    Runs when the client is connected and recieves a ready signal from discord
    Returns:
        None
    """
    print(f'{bot.user} has connected to Discord!')
    print(bot.guilds)
@bot.command()
async def handleCommands(ctx, arg):
    pass
@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    """_summary_
        runs when the voice state is updated in any voice channel in any of the guilds the bot is added to.
        The bot will attempt to verify that the minimum number of members is reached before sending a notification to a text channel.
            1. The bot will attempt to send a notification to the default channel (it can be adjusted by changing DEFAULT_TEXT_CHANNEL_NAME)
            2. If the text channel is not found, it will attempt to create a text channel with the given name (visit create_correct_notif_channel docs to view how permissions are set)
            3. If the text channel cannot be created, it will attempt to use the fallback option (if set to true)
            4. Else, it will silently throw an error
        
        Args:
            member (discord.Member): The member whose voice states changed.
            before (discord.VoiceState): The voice state prior to the changes.
            after (discord.VoiceState): The voice state after the changes.
    Returns:
        None
    """
    # if before.channel is not None and after.channel is None:
    #     try:
    #         guild = client.get_channel(before.channel.id).guild
    #         textChannel = discord.utils.get(guild.text_channels, name="szechuan-sauce")
    #     except Exception as e:
    #         print(f'Error getting kick log information: {e}')
    #     await print_imposter(guild, textChannel)
    #optimization idea later change from voice state update to only join vc state update (so it doesn't )   
    if before.channel is not after.channel and after.channel is not None: #check if somebody joins any vc
        vc_id = after.channel.id
        curr_vc = bot.get_channel(vc_id)
        presentUsers = []
        for myUser in curr_vc.members:
            presentUsers.append(myUser.display_name)
        # presentUsers = [myUser.name for myUser in curr_vc.members]
        print(f'Successfully found the voice channel {curr_vc}.\n\tMembers present:{presentUsers}')
        if len(curr_vc.members) >= Environs.MIN_NUM_USERS: #find the channel, if not possible create the channel, if not possible use implemented fall-back
            print(f'Sending an invite to all server members to join {curr_vc.name}...')
            guild = curr_vc.guild
            textChannel = await send_notif_to_correct_channel(guild, curr_vc, presentUsers)
            if textChannel is None:#couldn't find the default channel. Try to create it
                textChannel = await create_and_send_to_notif_channel(guild, curr_vc, presentUsers)
                if textChannel is None:#couldn't create the default channel, use fallback option
                    textChannel = await send_notif_to_fallback_text_channel(guild, curr_vc, presentUsers)
                    if textChannel is None:
                        print(f'Failed to send notification. Quitting silently...')
                #what to do if fallback option fails? Silently throw error
        print('\t\t\tFINISHED')
async def send_notif_to_correct_channel(guild: discord.Guild, curr_vc: discord.VoiceChannel, presentUsers: list)-> discord.TextChannel: 
    """_summary_
    attempts to find a text channel in the current guild with the name given by DEFAULT_TEXT_CHANNEL_NAME. 
        Note: This can be set to your liking and adjusted using /change_default_channel_name
    
    Args:
        guild (discord.Guild): the guild where the notification will be sent to (assumes is the same as the one where the enough users joined the voice channels)
        curr_vc (discord.VoiceChannel): the voice channel object that has enough users
        presentUsers (list): list of present users in the voice channel (curr_vc)
    Returns:
        discord.TextChannel: the textChannel object (if present); None otherwise
    """
    try: #checks if the default notif channel is present
        textChannel = discord.utils.get(guild.text_channels, name=Environs.DEFAULT_TEXT_CHANNEL_NAME)
        print(f'Successfully found the: \'{Environs.DEFAULT_TEXT_CHANNEL_NAME}\' channel')
        await send_notif_to_channel(textChannel, curr_vc, presentUsers)
    except Exception as e:#if default notif channel not present checks if it can create it
        print(f'Could not find the text channel: {Environs.DEFAULT_TEXT_CHANNEL_NAME}. Error: {e}')
        textChannel = None
    return textChannel
    

async def create_and_send_to_notif_channel(guild: discord.Guild, curr_vc: discord.VoiceChannel, presentUsers: list) -> discord.TextChannel:
    """_summary_
        attempts to create a text channel in the current guild with the name given by DEFAULT_TEXT_CHANNEL_NAME. 
            Note: This can be set to your liking and adjusted using /change_default_channel_name
            Note: the channel created will become the top channel in the server. Server Owner can adjust this by dragging the server to whatever position they like
        The created text channel will give the following permissions:
            bot: @everyone, and all text permissions only.
            Server owner: all permissions
            Everyone else: only view permissions
        
    Args:
        guild (discord.Guild): the guild where the notification will be sent to (assumes is the same as the one where the enough users joined the voice channels)
        curr_vc (discord.VoiceChannel): the voice channel object that has enough users
        presentUsers (list): list of present users in the voice channel (curr_vc)
    Returns:
        discord.TextChannel: the textChannel object (if present); None otherwise
    """ 
    try:  
        textChannel = await guild.create_text_channel(
            name=Environs.DEFAULT_TEXT_CHANNEL_NAME, 
            position=0,
            news=True,
            reason=f'To send a notification offline users when {Environs.MIN_NUM_USERS} join the same voice channel.')
        print(f'Successfully created text channel: {Environs.DEFAULT_TEXT_CHANNEL_NAME}')
    except Exception as e:
        print(f'Could not create the text channel: {Environs.DEFAULT_TEXT_CHANNEL_NAME}. Error: {e}')
    try:
        #await textChannel.set_permissions(client.user, discord.Permissions.text)
        # view_channel=True,
        #     manage_channels=False,
        #     manage_permissions=True,
        #     manage_webhooks=False,
        #     create_instant_invite=False,
        #     send_messages=True,
        #     embed_links=False,
        #     attach_files=False,
        #     use_external_emoji=False,
        #     mention_everyone=True,
        #     manage_messages=True,
        #     read_message_history=True,
        #     send_tts_messages=True,
        #     use_application_commands=True
       # await textChannel.set_permissions(guild.owner, discord.Permissions.all)
        await textChannel.set_permissions(guild.default_role, view_channel=True, send_messages=False)
        print(f'\tSuccessfully given bot @everyone and text permissions.\n\tServer owner has all permissions.\n\teveryone else only has view permissions.')
        await send_notif_to_channel(textChannel, curr_vc, presentUsers)
    except Exception as e: 
        print(f'Could not create the text channel: {Environs.DEFAULT_TEXT_CHANNEL_NAME}. Error: {e}')
        textChannel = None
    return textChannel
  
async def send_notif_to_fallback_text_channel(guild: discord.Guild, curr_vc: discord.VoiceChannel, presentUsers: list)-> discord.TextChannel:
    """_summary_
    attempts to find the first text channel it can send the notification to
        Note: This option can be turned off using /disable_fallback_notif
        
    Args:
        guild (discord.Guild): the guild where the notification will be sent to (assumes is the same as the one where the enough users joined the voice channels)
        curr_vc (discord.VoiceChannel): the voice channel object that has enough users
        presentUsers (list): list of present users in the voice channel (curr_vc)
    Returns:
        discord.TextChannel: the textChannel object (if present); None otherwise
    """  
    try:#text to first channel if possible
        print(f'Trying to send the notification to any text channel it can')
        for channel in guild.text_channels:
            #check if channel permission allows the bot to text to the channel
            try:
                textChannel = channel
                print(f'Successfully found a suitable text channel to send the notification in: {textChannel.name}')
                await send_notif_to_channel(textChannel, curr_vc, presentUsers)
                break
            except Exception as e:
                print(f'Failed to send the notification to {textChannel.name} text channel because error: {e}. Moving on to find a suitable textChannel')
    except Exception as e:
        print(f'Failed to send the notification to all text channel. Error {e}. Quitting now')
        textChannel = None
    return textChannel
def verifySlowMode() -> bool:
    """_summary_
    verifies if the request is valid or too soon (according to the DEFAULT_SLOWMODE_DELAY)
    Returns:
        bool: whether the request to send valid or not
    """
    if Environs.LAST_SENT_TIMESTAMP == 0:
        return True
    #timestamp must be positive
    now = datetime.now()
    try:
        previous = datetime.fromisoformat(Environs.LAST_SENT_TIMESTAMP)
    except:
        raise ValueError(f'Error: Invalid timestamp. Last sent timestamp: {Environs.LAST_SENT_TIMESTAMP} contains an invalid value')
    if previous > now:
        raise(f'Error: Invalid date. last sent message date: {previous} is after current date: {now}')
    timed = (now - previous).seconds
    if (now - previous).seconds >= Environs.DEFAULT_SLOWMODE_DELAY:
        print(f'This message is sent too soon. Current time: {now}, last sent message: {previous}. Current text_cooldown (slowmode_delay) is set to: {Environs.DEFAULT_SLOWMODE_DELAY}.')
        return False
    
async def send_notif_to_channel(textChannel: discord.TextChannel, voiceChannel: discord.VoiceChannel, curr_users: list):
    """_summary_
        uses discord API to send a notifcation to send a notification to textChannel asking @everyone to join
        
    Args:
        textChannel (discord.TextChannel): the text channel where the notification will be sent to (assumes is the same as the one where the enough users joined the voice channels)
        voiceChannel (discord.VoiceChannel): the voice channel object that has enough users
        curr_users (list): list of present users in the voice channel (voiceChannel)
    Returns:
        None
    """
    try:
        if not verifySlowMode(): #don't send the message if cannot verify the message is valid to send and is
            return
        print("\n".join([u for u in curr_users]))
        newlineChar = '\n- ' #can't just keep this literally in an f string but using a variable works.
        await textChannel.send(f"{len(curr_users)} {Environs.DEFAULT_GREETING} have joined {voiceChannel.name}:\n- {newlineChar.join([u for u in curr_users])}")
        Environs.LAST_SENT_TIMESTAMP = datetime.now().isoformat()
        print(f'Succefully sent the notification to {textChannel.name}')
    except Exception as e:
        print(f'Error: Failed to send the notification to text channel {textChannel.name}. Error message: {e}')
            
async def print_imposter(guild: discord.guild, textChannel: discord.TextChannel):
    """_summary_
    Args:
        guild (discord.guild): _description_
        textChannel (discord.TextChannel): _description_
    """
    async for entry in guild.audit_logs(action=discord.AuditLogAction.member_disconnect):
        print(f'{entry.user} {entry.action} {entry.target}')
#CODE EXECUTION STARTS HERE!!!!
# client.run(Environs.TOKEN)
bot.run(Environs.TOKEN)
