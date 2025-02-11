import discord
import validators
import gspread
import random
import time
import asyncio
import typing
import json
from typing import List
from discord.ext import commands
from discord import app_commands
from discord import Interaction
from oauth2client.service_account import ServiceAccountCredentials

# Enable necessary intents
intents = discord.Intents.default()
intents.message_content = True  # REQUIRED for reading messages
intents.members = True  # REQUIRED for mentions



# Initialize bot with command prefix
bot = commands.Bot(command_prefix="?", intents=intents, help_command=None)

#tokens and sheet link in super special secret json
with open('tokens.json') as f:
    data = json.load(f)
    token=data["TOKEN"]
    prefix = data["PREFIX"]
    db = data["DB"]

# Google Sheets API Setup
SHEET_URL = db  # sheeturl
CREDENTIALS_FILE = "credentials.json"  # sheets credentials

# Authenticate Google Sheets i copied this tbh
scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scopes)
client = gspread.authorize(creds)

# sheet var will be used to access the sheet
sheet = client.open_by_url(SHEET_URL).get_worksheet(0)  # 0 is workbook index

#this is testing to get buttons to work
class artview(discord.ui.View):
    def __init__(self, pages):
        super().__init__()
        self.page = 0
        self.pages = pages

        self.add_item(Button(label="<", style=discord.ButtonStyle.green, custom_id="prev"))
        self.add_item(Button(label=">", style=discord.ButtonStyle.green, custom_id="next"))

    @discord.ui.button(custom_id="prev")
    async def prev_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.page > 0:
            self.page -= 1
            await interaction.response.edit_message(content=self.pages[self.page])

    @discord.ui.button(custom_id="next")
    async def next_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.page < len(self.pages) - 1:
            self.page += 1
            await interaction.response.edit_message(content=self.pages[self.page])


#this is also button testing
@bot.command()
async def button(ctx):
    pages = ["page1","page2","page3","page4"]
    await ctx.send(pages[0], view=PaginationView(pages))




def get_card_stats(input):
    """Fetches user stats from Google Sheets by looking up the Discord ID in Column C."""
    sheet = client.open_by_url(SHEET_URL).get_worksheet(3)  
    try:
        data = sheet.get_all_values()  # Get all sheet values
        for row in data:  # Loop through each row
            if str.lower(row[1]) == str.lower(input):  # Column B, str.lower to account for case issues
                if (row[2]) == 'Trainer':   #Different Variables if Trainer Card
                  category = (row[4])  
                  effect = (row[5])         #Column 5 stores the effect etc etc
                  art = (row[7])
                  test = True               #test is true if trainer, false if pokemon
                  typist = 0                #i have to return these for the pokemon so they are just 0 now
                  hp = 0  
                  stage = 0  
                  attack = 0  
                  weak = 0  
                  retreat = 0
                  ability = 0
                  
                  return typist, hp, stage, attack, attack_eff, weak, retreat, ability, art, category, effect, test
                else:                          #pokemon else
                    typist = str(row[2])       # i think this is self explanetory
                    hp = str(row[3])  
                    stage = row[4]  
                    attack = row[5]  
                    attack_eff = row[6]  
                    weak = row[7]  
                    retreat = row[8]
                    ability = row[9]
                    art = row[10]
                    category = 0                #have to return these for trainer
                    effect = 0
                    test = False                #test is true if trainer, false if pokemon
                    return typist, hp, stage, attack, attack_eff, weak, retreat, ability, art, category, effect, test
        return None  # Return None if the card isnt found
    except Exception as e:      #something blew up if this happens
        print(f"❌ Error accessing Google Sheets: {e}")
        return None

def get_arts(input):
    '''This gets the arts of a card'''
    sheet = client.open_by_url(SHEET_URL).get_worksheet(3)  
    try:
        data = sheet.get_all_values()  # Get all sheet values
        for row in data:  # Loop through each row
            if str.lower(row[1]) == str.lower(input):   #str.lower to account for case issues
                art1=row[11]
                art2=row[12]
                art3=row[13]
                art4=row[14]
                art5=row[15]
                art6=row[16]
                art7=row[17]         #store up to 7 arts, no cards have more than 7. should make this an array tho
                
                return art1, art2, art3, art4, art5, art6, art7
        return None         #return none if not found
    except Exception as e:
        print(f"❌ Error accessing Google Sheets: {e}")
        return None

def allcards():
    '''Used to nab a random card'''
    sheet = client.open_by_url(SHEET_URL).get_worksheet(3)  # Index 1 = second tab
    try:
        data = sheet.get_all_values()
        choices=[]   # Get all sheet values
        for row in data:  # Loop through each row
            if row[1]=="":  #stop counting once we are out of cards
                break       #yes theres a better way dont worry
            choices.append(row[1])
        choices = [x for x in choices if x.strip()]     #strip blanks
       #choices = ["pika","mewtwo","charizard","alexa","nibleton","testttttt","moltres","zard x and y"]
                
        return choices
    except Exception as e:
        print(f"❌ Error accessing Google Sheets: {e}")
        return None

async def card_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    '''mmmm card but a slash command'''
    choices = allcards()
    choices = [app_commands.Choice(name=choice, value=choice) for choice in choices if current.lower() in choice.lower()][:24]
    return choices

def randomcard():
    sheet = client.open_by_url(SHEET_URL).get_worksheet(1)
    try:
        data = sheet.get_all_values()
        x=0
        for row in data:
            if str.lower(row[0]) == str.lower(""):
                break
            x +=1
        print(x)
        i = random.randint(0,x)
        j = "A" + str(i)
        final = sheet.cell(i,1).value
        return final

        
    except Exception as e:
        print(f"❌ Error accessing Google Sheets: {e}")
        return None



@bot.event
async def on_ready():
    """Runs when the bot is online"""
    print(f"✅ Logged in as {bot.user}")

    # Send bot status message in the general channel
    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels, name="general")
        #if channel:
           # await channel.send("Yooo im online!")


@bot.command(name="sync")
@commands.is_owner()
async def syncing(ctx):

    print(f"hi im here lets go")
    try:
        synced = await bot.tree.sync()
        await ctx.send(f"Suynced {len(synced)} commands")
    except Exception as e:
        await ctx.send("wow i botched it {e}")

@bot.tree.command(name="testtttttt")
async def hello(interaction: discord.Interaction):
    
    view = discord.ui.View()
    style = discord.ButtonStyle.gray
    item = discord.ui.Button(style=style, label="I know what im doing")
    async def function_name(self, int: discord.Interaction):
        await int.response.send_message("button clicked")
    view.add_item(item=item)
    await interaction.response.send_message(f"Hey {interaction.user.mention} wassssup", ephemeral=True, view=view)
    async def butt(self, interaction):
        await interaction.channel.send("wow we are goin to the left")
    

@bot.event
async def on_message(message):
    print(f"Received message: {message.content}")  # Debug: Logs all messages the bot sees
    await bot.process_commands(message)  # Ensures bot processes commands

@bot.command(name="pack")
async def stats(ctx, *lmao):
    """Fetches Wins, Losses, WPG, Win %, WPG+, Win Rate+ from Google Sheets."""
   

    card=(" ".join(lmao))
    user_stats = get_user_stats(card)
    card=card.title
    if user_stats:
        pack, rarity = user_stats

        # Create a Discord embed
        embed = discord.Embed(
            title=f"Pack stats for {card}",
            color=discord.Color.orange()
        )
        #embed.set_thumbnail(url=member.avatar.url)  # Set user avatar as thumbnail
        
        # Add fields for stats
        embed.add_field(name="Pack", value=f"{pack}", inline=True)
        embed.add_field(name="Rarity", value=f"{rarity}", inline=True)
        #embed.add_field(name="WPG", value=f"📊 {wpg}", inline=True)
        #embed.add_field(name="Win %", value=f"📈 {win_rate}", inline=True)
        #embed.add_field(name="WPG+", value=f"🔥 {wpg_plus}", inline=True)
        #embed.add_field(name="Win Rate+", value=f"🚀 {win_rate_plus}", inline=True)

        # Send the embed
        await ctx.send(embed=embed)

    else:
        await ctx.send(f"case sensitve")
@bot.command(name="card")
async def stats(ctx, *lmao):
    """Fetches Wins, Losses, WPG, Win %, WPG+, Win Rate+ from Google Sheets."""
   

    card=(" ".join(lmao))
    card_stats = get_card_stats(card)
    card=str.title(card)

    if card_stats:
        typist, hp, stage, attack, attack_eff, weak, retreat, ability, art, category, effect, test = card_stats

        # Create a Discord embed
        
        #if validators.url(art):
        #  print('valid')
        #else:
        #  print('booo')
        if test:
          embed = discord.Embed(
            title=f"Card Stats for {card}",
            color=discord.Color.blue()
          )
          embed.set_thumbnail(url=art)  # Set user avatar as thumbnail
          embed.set_author(name="WooperBot",url="https://x.com/radlup",icon_url=bot.user.avatar.url)

          # Add fields for stats
          embed.add_field(name="Category", value=f"{category}", inline=True)
          embed.add_field(name="Effect", value=f"{effect}", inline=False)

          embed.set_footer(text="Thank you for using WooperBot!")

          # Send the embed
          await ctx.send(embed=embed)
        else:
          embed = discord.Embed(
            title=f"Card Stats for {card}",
            color=discord.Color.red()
          )
          embed.set_thumbnail(url=art)  # Set user avatar as thumbnail
          embed.set_author(name="WooperBot",url="https://x.com/radlup",icon_url=bot.user.avatar.url)
          # Add fields for stats
          embed.add_field(name="Type", value=f"{typist}", inline=True)
          embed.add_field(name="HP", value=f"{hp}", inline=True)
          embed.add_field(name="Stage", value=f"{stage}", inline=True)
          embed.add_field(name="Attack", value=f"{attack}", inline=True)
          if attack_eff != "":
            embed.add_field(name="Attack Effect", value=f"{attack_eff}", inline=False)
            
          embed.add_field(name="Ability", value=f"{ability}", inline=False)
          embed.add_field(name="Weakness", value=f"{weak}", inline=True)
          embed.add_field(name="Retreat", value=f"{retreat}", inline=True)

          embed.set_footer(text="Thank you for using WooperBot!")
         

          # Send the embed
          await ctx.send(embed=embed)

    else:
        await ctx.send(f"I couldnt find that card, <:sadwoop:1335481337678790758> maybe check your spelling")

@bot.tree.command(name="card",description="Info about a PTCGP card!")
@app_commands.autocomplete(card=card_autocomplete)
async def cardian(interaction: discord.Interaction, card: str):
    card_stats = get_card_stats(card)
    card=str.title(card)

    if card_stats:
        typist, hp, stage, attack, attack_eff, weak, retreat, ability, art, category, effect, test = card_stats

        # Create a Discord embed
        
        #if validators.url(art):
        #  print('valid')
        #else:
        #  print('booo')
        if test:
          embed = discord.Embed(
            title=f"Card Stats for {card}",
            color=discord.Color.blue()
          )
          embed.set_thumbnail(url=art)  # Set user avatar as thumbnail
          embed.set_author(name="WooperBot",url="https://x.com/radlup",icon_url=bot.user.avatar.url)

          # Add fields for stats
          embed.add_field(name="Category", value=f"{category}", inline=True)
          embed.add_field(name="Effect", value=f"{effect}", inline=False)

          embed.set_footer(text="Thank you for using WooperBot!")

          # Send the embed
          await interaction.response.send_message(embed=embed)
        else:
          embed = discord.Embed(
            title=f"Card Stats for {card}",
            color=discord.Color.red()
          )
          embed.set_thumbnail(url=art)  # Set user avatar as thumbnail
          embed.set_author(name="WooperBot",url="https://x.com/radlup",icon_url=bot.user.avatar.url)
          # Add fields for stats
          embed.add_field(name="Type", value=f"{typist}", inline=True)
          embed.add_field(name="HP", value=f"{hp}", inline=True)
          embed.add_field(name="Stage", value=f"{stage}", inline=True)
          embed.add_field(name="Attack", value=f"{attack}", inline=True)
          if attack_eff != "":
            embed.add_field(name="Attack Effect", value=f"{attack_eff}", inline=False)
            
          embed.add_field(name="Ability", value=f"{ability}", inline=False)
          embed.add_field(name="Weakness", value=f"{weak}", inline=True)
          embed.add_field(name="Retreat", value=f"{retreat}", inline=True)

          embed.set_footer(text="Thank you for using WooperBot!")
         

          # Send the embed
          await interaction.response.send_message(embed=embed)

    else:
        await interaction.response.send_message(f"I couldnt find that card, <:sadwoop:1335481337678790758> maybe check your spelling")




@bot.command(name="arts")
async def stats(ctx, *lmao):       

    card=(" ".join(lmao))
    arties = get_arts(card)
    card=str.title(card)

    if(arties):
        art1, art2, art3, art4, art5, art6, art7 = arties
        j = [art1, art2, art3, art4, art5, art6, art7]
        j = [x for x in j if x.strip()]
        l = len(j)
        x=0
        await ctx.send(f"**Viewing {l} card arts for {card}:**")
      
        print(f"hi {art1}")
        react = await ctx.send(art1)

        msg = react.id    
        left = "⬅️"
        right = "➡️"
        
        await react.add_reaction(left)    
        await react.add_reaction(right)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in [left,right]

        member = ctx.author

        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=20.0, check=check)

                if str(reaction.emoji) == left:
                    x = x-1
                    if x == -1:
                        x = l-1
                   
                    await reaction.message.edit(content=j[x])
                    await react.add_reaction(left)    
                    await react.add_reaction(right)


                if str(reaction.emoji) == right:
                    x=x+1
                    if x == l:
                        x = 0
                    await reaction.message.edit(content=j[x])
                    await react.add_reaction(left)    
                    await react.add_reaction(right)
            except asyncio.TimeoutError:
                return

    else:
        await ctx.send("I couldnt find that card <:sadwoop:1335481337678790758>")
 
@bot.tree.command(name="arts",description="All arts for a card! This is extra handy if a pokemon has multiple cards (Ex. Magneton/Eevee)")
@app_commands.autocomplete(card=card_autocomplete)
async def cardian(interaction: discord.Interaction, card: str):        
    arties = get_arts(card)
    card=str.title(card)

    if(arties):
        art1, art2, art3, art4, art5, art6, art7 = arties
        j = [art1, art2, art3, art4, art5, art6, art7]
        j = [x for x in j if x.strip()]
        l = len(j)
        x=0
        await interaction.response.send_message(j[0],view=artview(j))
      
        print(f"hi {art1}")
        #await interaction.channel.send(j[0],view=artview(j))

        #msg = react.id    
        '''left = "⬅️"
        right = "➡️"
        
        await react.add_reaction(left)    
        await react.add_reaction(right)

        def check(reaction, user):
            return user == interaction.author and str(reaction.emoji) in [left,right]

        member = interaction.author

        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=20.0, check=check)

                if str(reaction.emoji) == left:
                    x = x-1
                    if x == -1:
                        x = l-1
                   
                    await reaction.message.edit(content=j[x])
                    await react.add_reaction(left)    
                    await react.add_reaction(right)


                if str(reaction.emoji) == right:
                    x=x+1
                    if x == l:
                        x = 0
                    await reaction.message.edit(content=j[x])
                    await react.add_reaction(left)    
                    await react.add_reaction(right)
            except asyncio.TimeoutError:
                return'''

    else:
        await ctx.send("I couldnt find that card <:sadwoop:1335481337678790758>")    


@bot.command(name="winter")
async def stats(ctx):       
    await ctx.send("hate that guy")

@bot.command(name="misty")
async def stats(ctx, member: discord.Member = None):

    member = ctx.author

    j = random.randint(1,11)

    cont = True
    
    x=0
    while cont:
        flip = random.choice([0,1])
        if flip == 1:
            if j == 1:
                await ctx.send(file=discord.File('heads-blast.png'))
            elif j== 2:
                await ctx.send(file=discord.File('heads-cynthia.png'))
            elif j== 3:
                await ctx.send(file=discord.File('heads-eevee.png'))
            elif j== 4:
                await ctx.send(file=discord.File('heads-erika.png'))
            elif j== 5:
                await ctx.send(file=discord.File('heads-garde.png'))
            elif j== 6:
                await ctx.send(file=discord.File('heads-lux.png'))
            elif j== 7:
                await ctx.send(file=discord.File('heads-m2.png'))
            elif j== 8:
                await ctx.send(file=discord.File('heads-meow.png'))
            elif j== 9:
                await ctx.send(file=discord.File('heads-mew.png'))
            elif j== 10:
                await ctx.send(file=discord.File('heads-pika.png'))
            elif j== 11:
                await ctx.send(file=discord.File('heads-zard.png'))
            #elif j== 12:
            #    await ctx.send(file=discord.File('heads-dark.png'))
            x+=1
        else:
            await ctx.send(file=discord.File('tails.png'))
            cont = False
        time.sleep(1.5)
    if x == 0:
        await ctx.send(f"**{member.display_name}** flipped **0 heads**..... Maybe switch to Darkrai today champ.")
    elif x == 1:
         await ctx.send(f"**{member.display_name}** flipped **1 head!** Go out there and test your luck!")
    else :
        await ctx.send(f"**{member.display_name}** flipped **{x} Heads!** Go out there and win some battles!")

@bot.tree.command(name="misty")
async def hello(interaction: discord.Interaction):
    member = interaction.user

    j = random.randint(1,11)

    cont = True
    
    x=0
    while cont:
        flip = random.choice([0,1])
        if flip == 1:
            if j == 1:
                if x==0:
                    await interaction.response.send_message(file=discord.File('heads-blast.png'))
                else:
                    await interaction.channel.send(file=discord.File('heads-blast.png'))
            elif j== 2:
                if x==0:
                    await interaction.response.send_message(file=discord.File('heads-cynthia.png'))
                else:
                    await interaction.channel.send(file=discord.File('heads-cynthia.png'))
            elif j== 3:
                if x==0:
                    await interaction.response.send_message(file=discord.File('heads-eevee.png'))
                else:
                    await interaction.channel.send(file=discord.File('heads-eevee.png'))
            elif j== 4:
                if x==0:
                    await interaction.response.send_message(file=discord.File('heads-erika.png'))
                else:
                    await interaction.channel.send(file=discord.File('heads-erika.png'))
            elif j== 5:
                if x==0:
                    await interaction.response.send_message(file=discord.File('heads-garde.png'))
                else:
                    await interaction.channel.send(file=discord.File('heads-garde.png'))
            elif j== 6:
                if x==0:
                    await interaction.response.send_message(file=discord.File('heads-lux.png'))
                else:
                    await interaction.channel.send(file=discord.File('heads-lux.png'))
            elif j== 7:
                if x==0:
                    await interaction.response.send_message(file=discord.File('heads-m2.png'))
                else:
                    await interaction.channel.send(file=discord.File('heads-m2.png'))
            elif j== 8:
                if x==0:
                    await interaction.response.send_message(file=discord.File('heads-meow.png'))
                else:
                    await interaction.channel.send(file=discord.File('heads-meow.png'))
            elif j== 9:
                if x==0:
                    await interaction.response.send_message(file=discord.File('heads-mew.png'))
                else:
                    await interaction.channel.send(file=discord.File('heads-mew.png'))
            elif j== 10:
                if x==0:
                    await interaction.response.send_message(file=discord.File('heads-pika.png'))
                else:
                    await interaction.channel.send(file=discord.File('heads-pika.png'))
            elif j== 11:
                if x==0:
                    await interaction.response.send_message(file=discord.File('heads-zard.png'))
                else:
                    await interaction.channel.send(file=discord.File('heads-zard.png'))
            #elif j== 12:
            #    if x==0:
            #        await interaction.response.send_message(file=discord.File('heads-dark.png'))
            #    else:
            #        await interaction.channel.send(file=discord.File('heads-dark.png'))

            x+=1
        else:
            if x==0:
                await interaction.channel.send(file=discord.File('tails.png'))
            else:
                await interaction.response.send_message(file=discord.File('tails.png'))
            cont = False
        time.sleep(1.5)
    if x == 0:
        await interaction.channel.send(f"**{member.display_name}** flipped **0 heads**..... Maybe switch to Darkrai today champ.")
    elif x == 1:
         await interaction.channel.send(f"**{member.display_name}** flipped **1 head!** Go out there and test your luck!")
    else :
        await interaction.channel.send(f"**{member.display_name}** flipped **{x} Heads!** Go out there and win some battles!")

@bot.command(name="commands")
async def stats(ctx, *lmao):

    embed = discord.Embed(
        title=f"Here are all my commands!",
        color=discord.Color.teal()
    )
    embed.set_author(name="WooperBot",url="https://x.com/radlup",icon_url=bot.user.avatar.url)
          # Add fields for stats
    embed.add_field(name="?Slash Commands", value=f"All the commands also work with slash commands!", inline=False)
    embed.add_field(name="?about/?wooper", value=f"Basic info about the bot and how to add me!", inline=False)
    embed.add_field(name="?commands", value=f"You're lookin at it", inline=False)
    embed.add_field(name="?card <Card Name>", value=f"Info about a PTCGP Card!", inline=False)
    embed.add_field(name="?arts <Card Name>", value=f"All arts for a given card, including those with multiple variants", inline=False)
    embed.add_field(name="?misty", value=f"Practice flipping your Mistys before battle!", inline=False)
    embed.add_field(name="?randcard/?random", value=f"Get a random Card!", inline=False)
    embed.add_field(name="?help", value=f"Link to the support server", inline=False)
    embed.set_footer(text="Thank you for using WooperBot!")

    await ctx.send(embed=embed)

@bot.command(name="about")
async def stats(ctx, *lmao):
    
    embed = discord.Embed(
        title=f"WooperBot Info",
        color=discord.Color.teal()
    )
    embed.set_author(name="WooperBot",url="https://x.com/radlup",icon_url=bot.user.avatar.url)
          # Add fields for stats
    embed.add_field(name="What do you do?", value=f"I can give you info and arts for all PTCG cards! I also flip coins sometimes. Use ?commands to see more!", inline=False)
    embed.add_field(name="Who made you?", value=f"@radlup on discord and twitter, feel free to message him with any questions/suggestions or bug reports!", inline=False)
    embed.add_field(name="How do I add you to my server?", value=f"Click this link to add me to your server! [Add Me!](https://discord.com/oauth2/authorize?client_id=1306086328601153547&permissions=689342597184&integration_type=0&scope=bot)", inline=False)

    await ctx.send(embed=embed)

@bot.command(name="wooper")
async def stats(ctx, *lmao):
    
    await ctx.send(f"Hey thats me!")
    embed = discord.Embed(
        title=f"WooperBot Info",
        color=discord.Color.teal()
    )
    embed.set_author(name="WooperBot",url="https://x.com/radlup",icon_url=bot.user.avatar.url)
          # Add fields for stats
    embed.add_field(name="What do you do?", value=f"I can give you info and arts for all PTCG cards! I also flip coins sometimes. Use ?commands to see more!", inline=False)
    embed.add_field(name="Who made you?", value=f"@radlup on discord and twitter, feel free to message him with any questions/suggestions or bug reports!", inline=False)
    embed.add_field(name="How do I add you to my server?", value=f"Click this link to add me to your server! [Add Me!](https://discord.com/oauth2/authorize?client_id=1306086328601153547&permissions=689342597184&integration_type=0&scope=bot)", inline=False)

    await ctx.send(embed=embed)



@bot.command(name="random")
async def stats(ctx, *lmao):
    
    await ctx.send(f"Here's you're random card! Now do it 19 more times for a very fun and competitive deck.")
    card = randomcard()

    if card:
        final = card
        await ctx.send(final)
    else:
        await ctx.send("weird error happened :(")

@bot.command(name="randcard")
async def stats(ctx, *lmao):
    
    await ctx.send(f"Here's you're random card! Now do it 19 more times for a very fun and competitive deck.")
    card = randomcard()

    if card:
        final = card
        await ctx.send(final)
    else:
        await ctx.send("weird error happened :(")

@bot.command(name="help")
async def stats(ctx, *lmao):
    
    await ctx.send(f"[Click here](https://discord.gg/TgytjBRevv) to join the support server!")

@bot .command("faint")
@commands.is_owner()
async def shutdown(ctx):
    exit()

bot.run(token)