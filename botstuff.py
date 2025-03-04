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
from discord import Color as c
from discord import Interaction
from discord import interactions
from oauth2client.service_account import ServiceAccountCredentials

"""WooperBot Version 1.12"""


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
sheet = client.open_by_url(SHEET_URL).get_worksheet(3)  # 0 is workbook index





def get_card_stats(input,set):
    """Fetches user stats from Google Sheets by looking up the Discord ID in Column C."""
    sheet = client.open_by_url(SHEET_URL).get_worksheet(3)  
    try:
        data = sheet.get_all_values()  # Get all sheet values
        
        if set != "":
            for row in data:  # Loop through each row
                if row[1] == set:
                    if str.lower(row[2]) == str.lower(input):  # Column B, str.lower to account for case issues
                        if (row[3]) == 'Supporter' or (row[3]) == 'Item' or (row[3]) == 'Tool':   #Different Variables if Trainer Card
                            category = (row[3])  
                            effect = (row[4])         #Column 5 stores the effect etc etc
                            art = (row[13])
                            test = True               #test is true if trainer, false if pokemon
                            typist = 0                #i have to return these for the pokemon so they are just 0 now
                            hp = 0  
                            stage = 0  
                            attack = 0  
                            attack_eff = 0
                            atk2 = 0
                            atk2_eff=0
                            weak = 0  
                            retreat = 0
                            ability = 0
                            if (row[3]) == 'Supporter':
                                newcolor= discord.Color.orange()
                            elif (row[2]) == 'Tool':
                                newcolor= discord.Color.purple()
                            else:
                                newcolor = discord.Color.blue()
                  
                            return typist, hp, stage, attack, attack_eff, weak, retreat, ability, art, category, effect, test, atk2, atk2_eff, newcolor
                        else:                          #pokemon else
                            typist = str(row[3])       # i think this is self explanetory
                            hp = str(row[4])  
                            stage = row[5]  
                            attack = row[6]  
                            attack_eff = row[7] 
                            atk2 = row[8] 
                            atk2_eff = row[9]
                            weak = row[10]  
                            retreat = row[11]
                            ability = row[12]
                            art = row[13]
                            category = 0                #have to return these for trainer
                            effect = 0
                            newcolor=0
                            test = False                #test is true if trainer, false if pokemon
                            return typist, hp, stage, attack, attack_eff, weak, retreat, ability, art, category, effect, test, atk2, atk2_eff, newcolor
            
        else:
            for row in data:  # Loop through each row
                if str.lower(row[2]) == str.lower(input):  # Column B, str.lower to account for case issues
                    if (row[3]) == 'Supporter' or (row[3]) == 'Item' or (row[3]) == 'Tool':   #Different Variables if Trainer Card
                        category = (row[3])  
                        effect = (row[4])         #Column 5 stores the effect etc etc
                        art = (row[13])
                        test = True               #test is true if trainer, false if pokemon
                        typist = 0                #i have to return these for the pokemon so they are just 0 now
                        hp = 0  
                        stage = 0  
                        attack = 0  
                        attack_eff = 0
                        atk2 = 0
                        atk2_eff=0
                        weak = 0  
                        retreat = 0
                        ability = 0
                        if (row[3]) == 'Supporter':
                            newcolor= discord.Color.orange()
                        elif (row[2]) == 'Tool':
                            newcolor= discord.Color.purple()
                        else:
                            newcolor = discord.Color.blue()
                  
                        return typist, hp, stage, attack, attack_eff, weak, retreat, ability, art, category, effect, test, atk2, atk2_eff, newcolor
                    else:                          #pokemon else
                        typist = str(row[3])       # i think this is self explanetory
                        hp = str(row[4])  
                        stage = row[5]  
                        attack = row[6]  
                        attack_eff = row[7] 
                        atk2 = row[8] 
                        atk2_eff = row[9]
                        weak = row[10]  
                        retreat = row[11]
                        ability = row[12]
                        art = row[13]
                        category = 0                #have to return these for trainer
                        effect = 0
                        newcolor=0
                        test = False                #test is true if trainer, false if pokemon
                        return typist, hp, stage, attack, attack_eff, weak, retreat, ability, art, category, effect, test, atk2, atk2_eff, newcolor
        return None  # Return None if the card isnt found
    except Exception as e:      #something blew up if this happens
        print(f"❌ Error accessing Google Sheets: {e}")
        return None

def filter_for(type,stage,hp_min,hp_max,atk_dmg_min,atk_dmg_max,retreat_cost,ability,ex):
    sheet = client.open_by_url(SHEET_URL).get_worksheet(3)
    try:
        data = sheet.get_all_values()  # Get all sheet values
        a = []
        t = False
        s = False
        r = False
        hp = False
        atk = False
        ab = False
        e = False
        '''pokemon gets added to the list iff all the variables are true'''
        for row in data:  # Loop through each row
            x = row[4]
            if(x==""):
                break
            if x != "HP":
                x = int(x.replace(" HP","")) #HP to integer from sheet
            else:
                x =-1000
            #print(x)
            y = row[6]
            y= y.replace("+","")
            y= y.replace("x","")
            if(y == ""):
                break
            if (y == "Attack" or not y.endswith("0") or y == ""):
                y=0
            else:
                y= y.split(" ")
                y= int(y[len(y)-1]) #Attack Damage to integer
            z = row[8]
            z= z.replace("+","")
            z= z.replace("x","")
            if (z== "Attack2" or not z.endswith("0") or z == ""):
                z=0
            else:
                z= z.split(" ")
                z= int(z[len(z)-1]) #Attack2 Damage to integer
            if(type == "" or type == row[3]):
                t = True
            if(stage == "" or stage in row[5]):
                s = True
            if(retreat_cost ==-1 or retreat_cost == row[11]):
                r = True
            if(x >= hp_min and x <= hp_max):
                hp = True
            if((y >= atk_dmg_min and y <= atk_dmg_max) or (z >= atk_dmg_min and z <= atk_dmg_max)):
                atk = True
            if ability == None:
                ab = True
            elif ability:    
                if(row[12] != ""):
                    ab = True
            else: 
                if(row[12] == ""):
                    ab = True
            if ex == None:
                e = True
            elif ex:    
                if(" ex" in row[2]):
                    e = True
            else:
                if(" ex" not in row[2]):
                    e = False
            if(t and s and r and hp and atk and ab and e):
                dupe = True
                for i in a:
                    if row[2] == i:
                        dupe = False
                        break
                if dupe:
                    a.append(row[2])
            t = False
            s = False
            r = False
            hp = False
            atk = False
            ab = False
            e = False

        if(len(a) == 0):
            return None
        return a
            
    except Exception as e:
        print(f"❌ Error accessing Google Sheets: {e}")
        return None


def get_arts(input):
    """This gets the arts of a card"""
    sheet = client.open_by_url(SHEET_URL).get_worksheet(3)  
    try:
        data = sheet.get_all_values()  # Get all sheet values
        for row in data:  # Loop through each row
            if str.lower(row[2]) == str.lower(input):   #str.lower to account for case issues
                art1=row[13]
                art2=row[14]
                art3=row[15]
                art4=row[16]
                art5=row[17]
                art6=row[18]
                art7=row[19]
                #art8=row[20]         #store up to 7 arts, no cards have more than 7. should make this an array tho
                
                return art1, art2, art3, art4, art5, art6, art7
        return None         #return none if not found
    except Exception as e:
        print(f"❌ Error accessing Google Sheets: {e}")
        return None

def allcards():
    """Used to nab a random card"""
    sheet = client.open_by_url(SHEET_URL).get_worksheet(5)  
    try:
        data = sheet.get_all_values()
        choices=[]   # Get all sheet values
        for row in data:  # Loop through each row
            if row[0]=="":  #stop counting once we are out of cards
                break       #yes theres a better way dont worry i am just kinda dumb?
            choices.append(row[0])
        choices = [x for x in choices if x.strip()]     #strip blanks
       #choices = ["pika","mewtwo","charizard","alexa","nibleton","testttttt","moltres","zard x and y"]
                
        return choices
    except Exception as e:
        print(f"❌ Error accessing Google Sheets: {e}")
        return None


def randdeck():
    sheet=client.open_by_url(SHEET_URL).get_worksheet(3) 
    sheet2 = client.open_by_url(SHEET_URL).get_worksheet(3) 
    #try:
     #   data = sheet.get_values()
    

async def card_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    """This allows us to have a bi list of cards in the drop down"""
    choices = allcards()
    choices = [app_commands.Choice(name=choice, value=choice) for choice in choices if current.lower() in choice.lower()][:24] #slice into many 24 length arrays
    return choices

def randomcard():
    """random card im not even gonna explain this one"""
    sheet = client.open_by_url(SHEET_URL).get_worksheet(1)
    try:
        data = sheet.get_all_values()
        x=len(data)
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
    """syncs all my slash commands with diiscord's, only i can use it"""
    print(f"hi im here lets go")
    try:
        synced = await bot.tree.sync()
        await ctx.send(f"Suynced {len(synced)} commands")
    except Exception as e:
        await ctx.send("wow i botched it {e}")


class LeftRight(discord.ui.View):
    def __init__(self,pages,author):
            super().__init__(timeout=15)
            self.author = author
            self.page=0
            self.pages=pages
    foo : bool = None
    
    async def count_press(self):
        for item in self.children:
            item.disabled = True
    async def on_timeout(self) -> None:
        await self.count_press()
    @discord.ui.button(label="Previous",
                       style=discord.ButtonStyle.blurple, emoji="⬅️")
    async def left(self, interaction: discord.Interaction, button: discord.ui.Button,):
        if self.page > 0:
            self.page -= 1
        else:
            self.page = len(self.pages) - 1
        await interaction.response.edit_message(content=self.pages[self.page])
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.author:
            await interaction.response.send_message("Not your button buddy <:sadwoop:1339496999258558464>",ephemeral = True)
        return interaction.user.id == self.author
    @discord.ui.button(label="Next",
                       style=discord.ButtonStyle.blurple, emoji="➡️")
    async def right(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page < len(self.pages) - 1:
            self.page += 1
        else:
            self.page = 0
        await interaction.response.edit_message(content=self.pages[self.page])
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.author:
            await interaction.response.send_message("Not your button buddy <:sadwoop:1339496999258558464>",ephemeral = True)
        return interaction.user.id == self.author


@bot.command(name="asd")
async def button(ctx):
    pages = ["page", "2", "3", "4"]
    auth = ctx.author
    view=LeftRight(pages,auth)
    await ctx.send("Viewing x Card Arts for:")
    message = await ctx.send(pages[0], view=view)
    view.message=message
    await view.wait()

    if view.foo is None:
        print("Timeout")
    elif view.foo is True:
        print("pressed left")
    else:
        print("pressed right")

    

@bot.event
async def on_message(message):
    print(f"Received message: {message.content}")  # Debug: Logs all messages the bot sees
    await bot.process_commands(message)  # Ensures bot processes commands

g="<:grass:1334617925461741799>"
r="<:fire:1334618516904476702>"
w="<:water:1334618527209885747>"
l="<:lightning:1334618537183936563>"
d="<:darkness:1334618567370604635>"
p="<:psychic:1334618547262849045>"
f="<:fighting:1334618556985376809>"
m="<:metal:1334618578175131708>"
dr="<:dragon:1334620515108655104>"
c="<:colorless:1334620662240776212>"


@bot.command(name="card")
async def stats(ctx, *lmao):
    """Get Card stats!"""
   
    
    card=(" ".join(lmao))
    card_stats = get_card_stats(card)
    card=str.title(card)

    if card_stats:
        typist, hp, stage, attack, attack_eff, weak, retreat, ability, art, category, effect, test, atk2, atk2_eff, newcolor = card_stats

        """different colors for types"""
        
        if typist == g:
            color=discord.Color.green()
        elif typist == r:
            color=discord.Color.red()
        elif typist == w:
            color=discord.Color.blue()
        elif typist == l:
            color=discord.Color.gold()
        elif typist == d:
            color=discord.Color.dark_purple()
        elif typist == p:
            color=discord.Color.magenta()
        elif typist == f:
            color=discord.Color.dark_orange()
        elif typist == m:
            color=discord.Color.dark_grey()
        elif typist == dr:
            color=discord.Color.dark_gold()
        else:
            color=discord.Color.lighter_grey()
        # Create a Discord embed

        if test:
          """Trainers have a different embed than pokemon"""
          embed = discord.Embed(
            title=f"Card Stats for {card}",
            color=newcolor
          )
          embed.set_thumbnail(url=art)  # Set card art as thumbnail
          embed.set_author(name="WooperBot",url="https://x.com/radlup",icon_url=bot.user.avatar.url)

          # Add fields
          embed.add_field(name="Category", value=f"{category}", inline=True)
          embed.add_field(name="Effect", value=f"{effect}", inline=False)

          embed.set_footer(text="Thank you for using WooperBot!")

          # Send the embed
          await ctx.send(embed=embed)
        else:
          embed = discord.Embed(
            title=f"Card Stats for {card}",
            color=color
          )
          embed.set_thumbnail(url=art)  # Set card art as thumbnail
          embed.set_author(name="WooperBot",url="https://x.com/radlup",icon_url=bot.user.avatar.url)
          # Add fields
          embed.add_field(name="Type", value=f"{typist}", inline=True)
          embed.add_field(name="HP", value=f"{hp}", inline=True)
          embed.add_field(name="Stage", value=f"{stage}", inline=True)
          embed.add_field(name="Attack", value=f"{attack}", inline=False)
          if attack_eff != "":
            embed.add_field(name="Attack Effect", value=f"{attack_eff}", inline=False)
          if atk2 != "":
            embed.add_field(name="Second Attack", value=f"{atk2}", inline=False)
            if atk2_eff != "":
                embed.add_field(name= "Second Attack Effect", value=f"{atk2_eff}", inline=False)
          if ability !="":
            embed.add_field(name="Ability", value=f"{ability}", inline=False)
          embed.add_field(name="Weakness", value=f"{weak}", inline=True)
          embed.add_field(name="Retreat", value=f"{retreat}", inline=True)

          embed.set_footer(text="Thank you for using WooperBot!")
         

          # Send the embed
          await ctx.send(embed=embed)

    else:
        await ctx.send(f"I couldnt find that card, <:sadwoop:1339496999258558464> maybe check your spelling")


        
@bot.tree.command(name="card",description="Info about a PTCGP card!")
@app_commands.autocomplete(card=card_autocomplete)
@app_commands.choices(set=[app_commands.Choice(name="Space-Time Smackdown",value="A2"),
        app_commands.Choice(name="Mythical Island",value="A1a"),
        app_commands.Choice(name="Genetic Apex",value="A1"),
        app_commands.Choice(name="Promo A",value="P-A"),
        app_commands.Choice(name="Triumphant Light",value="A2a")
        ])
async def cardian(interaction: discord.Interaction, card: str, set: str=""):
    """?card but now its a slash command"""
    card_stats = get_card_stats(card,set)
    card=str.title(card)
    if card_stats:
        typist, hp, stage, attack, attack_eff, weak, retreat, ability, art, category, effect, test, atk2, atk2_eff, newcolor = card_stats

        if typist == g:
            color=discord.Color.green()
        elif typist == r:
            color=discord.Color.red()
        elif typist == w:
            color=discord.Color.blue()
        elif typist == l:
            color=discord.Color.gold()
        elif typist == d:
            color=discord.Color.dark_purple()
        elif typist == p:
            color=discord.Color.magenta()
        elif typist == f:
            color=discord.Color.dark_orange()
        elif typist == m:
            color=discord.Color.dark_grey()
        elif typist == dr:
            color=discord.Color.dark_gold()
        else:
            color=discord.Color.lighter_grey()

        # w=Create a Discord embed

        if test:
          embed = discord.Embed(
            title=f"Card Stats for {card}",
            color=newcolor
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
            color=color
          )
          embed.set_thumbnail(url=art)  # Set user avatar as thumbnail
          embed.set_author(name="WooperBot",url="https://x.com/radlup",icon_url=bot.user.avatar.url)
          # Add fields for stats
          embed.add_field(name="Type", value=f"{typist}", inline=True)
          embed.add_field(name="HP", value=f"{hp}", inline=True)
          embed.add_field(name="Stage", value=f"{stage}", inline=True)
          embed.add_field(name="Attack", value=f"{attack}", inline=False)
          if attack_eff != "":
            embed.add_field(name="Attack Effect", value=f"{attack_eff}", inline=False)
          if atk2 != "":
            embed.add_field(name="Second Attack", value=f"{atk2}", inline=False)
            if atk2_eff != "":
                embed.add_field(name= "Second Attack Effect", value=f"{atk2_eff}", inline=False)
          if ability !="":
            embed.add_field(name="Ability", value=f"{ability}", inline=False)
          embed.add_field(name="Weakness", value=f"{weak}", inline=True)
          embed.add_field(name="Retreat", value=f"{retreat}", inline=True)

          embed.set_footer(text="Thank you for using WooperBot!")
         

          # Send the embed
          await interaction.response.send_message(embed=embed)

    else:
        await interaction.response.send_message(f"I couldnt find that card, <:sadwoop:1339496999258558464> maybe it isnt in that set?")


@bot.tree.command(name="filter",description="Filter Pokemon Cards by HP, Type, Damage, Retreat cost, etc")
@app_commands.choices(type=[app_commands.Choice(name="Colorless",value="<:colorless:1334620662240776212>"),
                            app_commands.Choice(name="Fighting",value="<:fighting:1334618556985376809>"),
                            app_commands.Choice(name="Fire",value="<:fire:1334618516904476702>"),
                            app_commands.Choice(name="Water",value="<:water:1334618527209885747>"),
                            app_commands.Choice(name="Psychic",value="<:psychic:1334618547262849045>"),
                            app_commands.Choice(name="Lightning",value="<:lightning:1334618537183936563>"),
                            app_commands.Choice(name="Darkness",value="<:darkness:1334618567370604635>"),
                            app_commands.Choice(name="Metal",value="<:metal:1334618578175131708>"),
                            app_commands.Choice(name="Grass",value="<:grass:1334617925461741799>"),
                            app_commands.Choice(name="Dragon",value="<:dragon:1334620515108655104>")])
@app_commands.choices(stage=[app_commands.Choice(name="Basic",value="Basic"),
                            app_commands.Choice(name="Stage 1",value="Stage 1"),
                            app_commands.Choice(name="Stage 2",value="Stage 2")])
async def filter(interaction: discord.Interaction, type: str ="", stage: str="",hp_min: int=0, hp_max: int=500, atk_dmg_min: int=0, atk_dmg_max: int=500, retreat_cost: int=-1, ability: bool=None,ex: bool=None):
    print(hp_min)
    print(ability)
    print(atk_dmg_max)
    print(type)
    atk_dmg_max=int(atk_dmg_max)
    results=filter_for(type,stage,hp_min,hp_max,atk_dmg_min,atk_dmg_max,retreat_cost,ability,ex)
    txt =""
    if type != "":
        txt += "**Type: **" + type +", "
    if stage != "":
        txt += "**Stage: **" + stage.replace("Stage ","")+", "
    if hp_min > 0:
        txt += "**Min HP: **" + str(hp_min) + ", "
    if hp_max < 500:
        txt += "**Max HP: **" + str(hp_max) + ", "
    if atk_dmg_min > 0:
        txt += "**Min Atk Damage: **" + str(atk_dmg_min) + ", "
    if int(atk_dmg_max) < 500:
        txt += "**Max Atk Damage: **" + str(atk_dmg_max) + ", "
    if retreat_cost != -1:
        txt += "**Retreat: **" + str(retreat_cost) + ", "
    if ability != None:
        txt += "**Ability: " + str(ability) + ", "
    if ex != None:
        txt += "**Is Ex: **" + str(ex) + ", "



    if results:
        pokemons = results
        embed = discord.Embed(
            title=f"Filter Results for; {txt} ",
            color=discord.Color.teal()
          )
        embed.set_author(name="WooperBot",url="https://x.com/radlup",icon_url=bot.user.avatar.url)
          # Add fields
        embed.add_field(name="Pokemon", value=f"{pokemons}", inline=True)
        await interaction.response.send_message(embed=embed)

    else:
        await interaction.response.send_message(f"<:sadwoop:1339496999258558464> No cards matched that search.")





@bot.command(name="arts")
async def stats(ctx, *lmao):       
    """get all arts for a given card"""
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
      
        react = await ctx.send(art1)

        msg = react.id    #add reactions so the user can click on em
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
                #check for reactions

                if str(reaction.emoji) == left:
                    #move left in the array, loop to the right end if you are at 0
                    x = x-1
                    if x == -1:
                        x = l-1
                   
                    await reaction.message.edit(content=j[x])
                    await react.add_reaction(left)    
                    await react.add_reaction(right)


                if str(reaction.emoji) == right:
                    #move right in the array, loop back to start
                    x=x+1
                    if x == l:
                        x = 0
                    await reaction.message.edit(content=j[x])
                    await react.add_reaction(left)    
                    await react.add_reaction(right)
            except asyncio.TimeoutError:
                return

    else:
        await ctx.send("I couldnt find that card <:sadwoop:1339496999258558464>")
 
@bot.tree.command(name="arts",description="All arts for a card! This is extra handy if a pokemon has multiple cards (Ex. Magneton/Eevee)")
@app_commands.autocomplete(card=card_autocomplete)
async def cardian(interaction: discord.Interaction, card: str):        
    """Arts but a slash command, uses buttons"""
    arties = get_arts(card)
    card=str.title(card)

    if(arties):
        art1, art2, art3, art4, art5, art6, art7 = arties
        j = [art1, art2, art3, art4, art5, art6, art7]
        j = [x for x in j if x.strip()]
        l = len(j)
        x=0
        auth = interaction.user.id
        view=LeftRight(j,auth)
        await interaction.response.send_message(f"Viewing **{l}** card arts for **{card}**")
        message = await interaction.channel.send(j[0], view=view)
        view.message=message
        await view.wait()
      

    else:
        await interaction.channel.send("I couldnt find that card <:sadwoop:1339496999258558464>")    


@bot.command(name="winter")
async def stats(ctx):
    """hate that guy"""       
    await ctx.send("hate that guy")

@bot.command(name="misty")
async def stats(ctx, member: discord.Member = None):

    """flip flip flip!!!"""

    member = ctx.author
    coins=["heads-blast.png","heads-cynthia.png","heads-eevee.png","heads-erika.png","heads-garde.png","heads-lux.png","heads-m2.png","heads-meow.png","heads-mew.png",
           "heads-pika.png","heads-zard.png","heads-darkrai.png"]
    j = random.randint(0,len(coins)-1)


    cont = True

    x=0
    while cont:
        flip = random.choice([0,1])
        #50/50 flip
        if flip == 1:
            await ctx.send(file=discord.File(coins[j]))
            x+=1
        else:
            await ctx.send(file=discord.File('tails.png'))
            cont = False
        time.sleep(1.5) #suspense
    if x == 0:
        await ctx.send(f"**{member.display_name}** flipped **0 heads**..... Maybe switch to Darkrai today champ.")
    elif x == 1:
         await ctx.send(f"**{member.display_name}** flipped **1 head!** Go out there and test your luck!")
    else :
        await ctx.send(f"**{member.display_name}** flipped **{x} Heads!** Go out there and win some battles!")

@bot.tree.command(name="misty")
async def hello(interaction: discord.Interaction):
    """misty but slash"""
    member = interaction.user
    coins=["heads-blast.png","heads-cynthia.png","heads-eevee.png","heads-erika.png","heads-garde.png","heads-lux.png","heads-m2.png","heads-meow.png","heads-mew.png",
           "heads-pika.png","heads-zard.png","heads-darkrai.png"]
    j = random.randint(0,len(coins)-1)

    cont = True
    
    x=0
    while cont:
        flip = random.choice([0,1])
        if flip == 1:
            if x==0:
                await interaction.response.send_message(file=discord.File(coins[j]))
            else:
                await interaction.channel.send(file=discord.File(coins[j]))
            x+=1
        else:
            if x==0:
                await interaction.response.send_message(file=discord.File('tails.png'))
            else:
                await interaction.channel.send(file=discord.File('tails.png'))
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
    """my commands"""
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
    embed.add_field(name="?filter", value=f"Search through all pokemon with a handful of different filters!", inline=False)
    embed.add_field(name="?misty", value=f"Practice flipping your Mistys before battle!", inline=False)
    embed.add_field(name="?randcard/?random", value=f"Get a random Card!", inline=False)
    embed.add_field(name="?help", value=f"Link to the support server", inline=False)
    embed.set_footer(text="Thank you for using WooperBot!")

    await ctx.send(embed=embed)

@bot.tree.command(name="commands")
async def hello(interaction: discord.Interaction):
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
    embed.add_field(name="?filter", value=f"Search through all pokemon with a handful of different filters!", inline=False)
    embed.add_field(name="?misty", value=f"Practice flipping your Mistys before battle!", inline=False)
    embed.add_field(name="?randcard/?random", value=f"Get a random Card!", inline=False)
    embed.add_field(name="?help", value=f"Link to the support server", inline=False)
    embed.set_footer(text="Thank you for using WooperBot!")

    await interaction.response.send_message(embed=embed)

@bot.command(name="about")
async def stats(ctx, *lmao):
    """about"""
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

@bot.tree.command(name="about")
async def hello(interaction: discord.Interaction):
    embed = discord.Embed(
        title=f"WooperBot Info",
        color=discord.Color.teal()
    )
    embed.set_author(name="WooperBot",url="https://x.com/radlup",icon_url=bot.user.avatar.url)
          # Add fields for stats
    embed.add_field(name="What do you do?", value=f"I can give you info and arts for all PTCG cards! I also flip coins sometimes. Use ?commands to see more!", inline=False)
    embed.add_field(name="Who made you?", value=f"@radlup on discord and twitter, feel free to message him with any questions/suggestions or bug reports!", inline=False)
    embed.add_field(name="How do I add you to my server?", value=f"Click this link to add me to your server! [Add Me!](https://discord.com/oauth2/authorize?client_id=1306086328601153547&permissions=689342597184&integration_type=0&scope=bot)", inline=False)

    await interaction.response.send_message(embed=embed)


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

@bot.tree.command(name="wooper")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey thats me!")
    embed = discord.Embed(
        title=f"WooperBot Info",
        color=discord.Color.teal()
    )
    embed.set_author(name="WooperBot",url="https://x.com/radlup",icon_url=bot.user.avatar.url)
          # Add fields for stats
    embed.add_field(name="What do you do?", value=f"I can give you info and arts for all PTCG cards! I also flip coins sometimes. Use ?commands to see more!", inline=False)
    embed.add_field(name="Who made you?", value=f"@radlup on discord and twitter, feel free to message him with any questions/suggestions or bug reports!", inline=False)
    embed.add_field(name="How do I add you to my server?", value=f"Click this link to add me to your server! [Add Me!](https://discord.com/oauth2/authorize?client_id=1306086328601153547&permissions=689342597184&integration_type=0&scope=bot)", inline=False)

    await interaction.channel.send(embed=embed)

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

@bot.tree.command(name="randomcard")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Here's you're random card! Now do it 19 more times for a very fun and competitive deck.")
    card = randomcard()
    if card:
        final = card
        await interaction.channel.send(final)
    else:
        await interaction.response.send_message("weird error happened :(")


@bot.tree.command(name="randomdeck")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Here's you're random deck, trust me easy 10 game winstreak.")

    

@bot.command(name="help")
async def stats(ctx, *lmao):
    
    await ctx.send(f"[Click here](https://discord.gg/TgytjBRevv) to join the support server!")

@bot.tree.command(name="help")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"[Click here](https://discord.gg/TgytjBRevv) to join the support server!")

@bot.command("faint")
@commands.is_owner()
async def shutdown(ctx):
    """It was Super Effective! Wooper has fainted :()"""
    exit()

bot.run(token)