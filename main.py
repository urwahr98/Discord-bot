import discord
import os
from replit import db
from keep_alive import keep_alive
import random
from random import choice
import requests
import time
import asyncio
import pykakasi

kks = pykakasi.kakasi()

client = discord.Client()
client.sniped_messages = {}

def mess_up(message):
  return ''.join(choice((str.upper, str.lower))(c) for c in message)

async def reply(message):
  if message.author == client.user:
      return

  if message.content in db.keys():
      reply = db[message.content]
      return await message.channel.send(reply)

colorList = [discord.Color.blue(), discord.Color.dark_blue(), discord.Color.purple(), discord.Color.dark_purple(), discord.Color.red(), discord.Color.gold(), discord.Color.dark_gold(), discord.Color.green(), discord.Color.dark_green(), discord.Color.magenta(), discord.Color.teal(), discord.Color.orange(), discord.Color.dark_red()]

deleted_msg = None

async def embedMSG(message):
  if not message.attachments and message.reference is None:
    await message.delete()
    embed = discord.Embed(description = str(message.content) +"\n___", color=choice(colorList))
    embed.set_author(name = str(message.author.display_name), icon_url = message.author.avatar_url)
    embed.set_footer(text="-"+str(message.author.name))
    await message.channel.send(embed=embed)
    if "http" in str(message.content):
      await message.channel.send(str(message.content))

@client.event
async def on_ready():
    print("We have logged as {0.user}".format(client))
    db['devMode'] = 'off'

    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name='Ohayo Sekai GM'))

@client.event
async def on_message(message):

    ran = random.randint(0, 49)
    msg = str(message.content)
    msgL = msg.lower()

    if message.author == client.user:
        return

    if (db['devMode']
            == 'on') and (str(message.author) != "nekoking98#3782"):
        return

    
    if message.content.startswith('$test'):
      if "wtv" in str(message.author.roles):
        await message.channel.send(message.author.roles)
      # emojilist = ['<a:towa:806768843585355787>','<a:towaaa:806784212811120650>']
      # await message.add_reaction(choice(emojilist))
      # for emoji in message.guild.emojis:
      #   print(str(emoji.id) + " : " + emoji.name)
      # emoji = '<a:towa:806768843585355787>'
      # if emoji:
      #   await message.add_reaction(emoji)

    if message.content.startswith('$devon'):
        if db['devMode'] == 'off':
            db['devMode'] = 'on'
            await message.channel.send(
                "Dev Mode is On! I will not reply to other than Urwah")
            await client.change_presence(activity=discord.Game(
                name='In Dev'))
        else:
            await message.channel.send("Dev Mode is already On!")

    if message.content.startswith('$devoff'):
        if db['devMode'] == 'on':
            db['devMode'] = 'off'
            await message.channel.send(
                "Dev Mode is Off! Proceeding normal behaviour.")
            await client.change_presence(activity=discord.Activity(
                type=discord.ActivityType.watching, name='Chino mandi'))
        else:
            await message.channel.send("Dev Mode is already Off!")
    
    # if "🐷" in str(message.author.roles):
    #   try:
    #     await embedMSG(message)
    #   except:
    #     pass

    if message.content.startswith('$check'):
      text3 = msg.split('$check ')[-1]
      if text3 in db.keys():
        await message.channel.send(
                "The key `"+text3+"` exist in the database.")
      else:
        await message.channel.send(
                "The key `"+text3+"` does not exist in the database!")

    if message.content.startswith('pls snipe'):

      try: 
        contents, author, channel_name, time = client.sniped_messages[message.guild.id]
      except:
        await message.channel.send("Nothing to snipe!")
        return
      
      embed = discord.Embed(description=contents, color=choice(colorList), timestamp=time)
      embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
      embed.set_footer(text= f"Deleted in : #{channel_name}")
      await message.channel.send(embed=embed)
      client.sniped_messages[message.guild.id] = {}



    if message.content.startswith('$ee'):
      await message.channel.send(
                "Try send a message with this keyword included :"+
                "\nuwu, nene, glasses, nigger, weeb, wowo, baka, nande, pekopeko, degen, arigathanks, cringe, gas gas gas, no confidence, yahoo, disgusting, ok google, naaa, faq, yabe, shut up bitch, yabai, sexy, yagoo, pizza, okiro.")

    if message.content.startswith('$selfie'):
      if msg == "$selfie":
        await message.channel.send(message.author.avatar_url)
      else:
       for user in message.mentions:
        await message.channel.send(user.avatar_url)


    if message.content.startswith('$help'):
      await message.channel.send("`$react x == y` for me to reply with y whenever i see x."
                                  +"\n`$del x` for me to delete x from reply list."
                                  +"\n`$list` or `$list_` for me to list all what I will reply."
                                  +"\n`$romaji x` for me to turn x from jp to romaji."
                                  +"\n`$decide x or y or ..` for me to decide which is the best choice."
                                  +"\n`$loy` to ping loi."
                                  +"\n`$cs` to summon Kamen Rider."
                                  +"\n`$delay msg` to put a delay in your message by hours."
                                  +"\n`$em msg` to put your message as embed."
                                  +"\n`$selfie @someone` to get their profile picture." 
                                  +"\n`$ee` for easter egg.")

    if message.content.startswith('$romaji'):
      text = msg.split('$romaji ')[-1]
      try:
        result = kks.convert(text)
        sentence = ""
        for item in result:
          sentence = sentence+item['hepburn'] + " "
        await message.channel.send(sentence)
      except:
        await message.channel.send("Conversion failed!")

    if message.content.startswith('$decide'):
      sentence = ["my calculation.", "the movement of the stars.", "chaos theory.", "the anime I watched yesterday.", "my feeling.", "my best friend, Bagak!", "your mother.", "dy/dx = 0.", "the photosynthesis of the choices!", "what's best for you."]
      listword = msg.split("$decide ")[-1]
      listword = listword.split(" or ")
      await message.channel.send("I think that "+ choice(listword) + " is the best choice here || with "+ str(random.randint(1,100)) +"% certainty according to "+ choice(sentence)+"||")

    if ran == 1:

      # if str(message.author) == "po_sama#8588":
      #   poreply = ["Ye la Po", "Apa apa je la Po.", "Asalkan kau happy Po.", "Hidup kau Po.", "Congrats!", "Nice one Po!", "No pressure Po.", "Next time."]
      #   await(await message.channel.send(choice(poreply))).delete(delay=10)

      if str(message.author) == "Amree#2113":
        amreelist = ["です!", "ですね~", "Betul betul betul.", "ね~", "うんうん", "うむ!", "まさか?!", "すごい", "なる程!"]
        await(await message.channel.send(choice(amreelist))).delete(delay=10)

      # if str(message.author) == "nekoking98#3782":
      #   try:
      #     await embedMSG(message)
      #   except:
      #     pass

      # if str(message.author) == "Murada#5664":
      #   raulreply = ["Serious la?", "True.", "Same.", "I agree", "Me too.", "Sure.", "You do you.", "Are you sure?", "Oh really?"]
      #   await(await message.channel.send(choice(raulreply))).delete(delay=10)

      if str(message.author) == "Loy-kun#9866":
        emojilist = ['<a:towa:806768843585355787>','<a:towaaa:806784212811120650>', '\N{THUMBS UP SIGN}']
        await message.add_reaction(choice(emojilist))

      # if str(message.author) == "Lexxy157#1516":
      #   emoji = '\N{THUMBS UP SIGN}'
      #   # emoji = '<:kappapride:619936943815393291>'
      #   if emoji:
      #     await message.add_reaction(emoji)


    if message.content.startswith('$react '):
      remove1 = msg.split('$react ')[-1]
      remove2 = remove1.split(' == ')
      db[remove2[0].strip()] = remove2[-1].strip()
      await(await message.channel.send("When i see this: `" + remove2[0] + "`"
                                  '\n i reply with this: `' + remove2[-1]+"`")).delete(delay=5)
      await message.channel.send(
          'Database succesfully updated.')

    if msgL == "amree" or msg == "<@!797753144641716245>":
      replieslist = ["Ye?", "Padia?", "Awat?", "Hang nak pa?", "Que?", "Pardon?", "Yo!", "Nani?", "Wassup", "At your service, my lady.", "I like Abby.", "...", "Naruhodo ne!", "Hai, Amree desu!", "Amree dayo!"]
      await(await message.channel.send(choice(replieslist))).delete(delay=5)

    if msg in db.keys():
      reply = db[msg]
      return await message.channel.send(reply)

    if message.content.startswith('$list'):
      if not db.keys():
          await message.channel.send("No Available Reply!")
      else:
          list = '['
          for key in db.keys():
            if message.content.startswith('$list_'):
              list = list + "`" + key + '`, '
            else:
              list = list + key + ', '
          list = list[:-2]
          list = list + ']'
          await message.channel.send(list)

    if message.content.startswith('$del '):
      remove1 = msg.split('$del ')[-1]
      if remove1 in db.keys():
          del db[remove1]
          await message.channel.send(
              "Reply Successfully deleted!")
      else:
          await message.channel.send(
              "Could not find `"+ remove1 + "` in database!")

    if message.content.startswith('$delay '):
      await message.delete()
      icon = message.author.avatar_url
      rawUserInput = msg.split('$delay ')[-1]
      await(await message.channel.send(
              "Sure! How many hours do you wanna delay it?")).delete(delay=13)
      try:
        newUserInput = await client.wait_for("message", timeout=30)
        newUserInput = newUserInput.content.strip()
        await(await message.channel.send(
              "Sending your message in approximately " + newUserInput + " hours!")).delete(delay=5)
        totalsec = float(newUserInput)*3600
        await asyncio.sleep(int(totalsec))
        await message.channel.send("Hear, Hear! A message from around " + newUserInput + " hours ago brought to the future!")
        await asyncio.sleep(3)
        embed = discord.Embed(description = rawUserInput +"\n___", color=choice(colorList))
        embed.set_author(name = str(message.author.display_name), icon_url = icon)
        embed.set_footer(text="-"+str(message.author))
        await message.channel.send(embed=embed)
        if "http" in rawUserInput:
          await message.channel.send(rawUserInput)

      except asyncio.TimeoutError:
        await message.channel.send("Sorry, you didn't reply in time!")

    if message.content.startswith('$em '):
      await message.delete()
      icon = message.author.avatar_url
      rawUserInput = msg.split('$em ')[-1]
      embed = discord.Embed(description = rawUserInput +"\n___", color=choice(colorList))
      embed.set_author(name = str(message.author.display_name), icon_url = icon)
      embed.set_footer(text="-"+str(message.author))
      # embed.add_field(name="__", value="__", inline=False)
      await message.channel.send(embed=embed)
      if "http" in rawUserInput:
        await message.channel.send(rawUserInput)
  

    if message.content.startswith('$clear'):
        for key in db.keys():
          del db[key]
        db['devMode'] = 'on'
        await message.channel.send(
                "Database cleared!")

    if (msgL).startswith('uwu'):
        await(await message.channel.send(
                "⡆⣐⢕⢕⢕⢕⢕⢕⢕⢕⠅⢗⢕⢕⢕⢕⢕⢕⢕⠕⠕⢕⢕⢕⢕⢕⢕⢕⢕⢕ ⢐⢕⢕⢕⢕⢕⣕⢕⢕⠕⠁⢕⢕⢕⢕⢕⢕⢕⢕⠅⡄⢕⢕⢕⢕⢕⢕⢕⢕⢕ ⢕⢕⢕⢕⢕⠅⢗⢕⠕⣠⠄⣗⢕⢕⠕⢕⢕⢕⠕⢠⣿⠐⢕⢕⢕⠑⢕⢕⠵⢕ ⢕⢕⢕⢕⠁⢜⠕⢁⣴⣿⡇⢓⢕⢵⢐⢕⢕⠕⢁⣾⢿⣧⠑⢕⢕⠄⢑⢕⠅⢕ ⢕⢕⠵⢁⠔⢁⣤⣤⣶⣶⣶⡐⣕⢽⠐⢕⠕⣡⣾⣶⣶⣶⣤⡁⢓⢕⠄⢑⢅⢑ ⠍⣧⠄⣶⣾⣿⣿⣿⣿⣿⣿⣷⣔⢕⢄⢡⣾⣿⣿⣿⣿⣿⣿⣿⣦⡑⢕⢤⠱⢐ ⢠⢕⠅⣾⣿⠋⢿⣿⣿⣿⠉⣿⣿⣷⣦⣶⣽⣿⣿⠈⣿⣿⣿⣿⠏⢹⣷⣷⡅⢐ ⣔⢕⢥⢻⣿⡀⠈⠛⠛⠁⢠⣿⣿⣿⣿⣿⣿⣿⣿⡀⠈⠛⠛⠁⠄⣼⣿⣿⡇⢔ ⢕⢕⢽⢸⢟⢟⢖⢖⢤⣶⡟⢻⣿⡿⠻⣿⣿⡟⢀⣿⣦⢤⢤⢔⢞⢿⢿⣿⠁⢕ ⢕⢕⠅⣐⢕⢕⢕⢕⢕⣿⣿⡄⠛⢀⣦⠈⠛⢁⣼⣿⢗⢕⢕⢕⢕⢕⢕⡏⣘⢕ ⢕⢕⠅⢓⣕⣕⣕⣕⣵⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣷⣕⢕⢕⢕⢕⡵⢀⢕⢕ ⢑⢕⠃⡈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢃⢕⢕⢕ ⣆⢕⠄⢱⣄⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢁⢕⢕⠕⢁ ⣿⣦⡀⣿⣿⣷⣶⣬⣍⣛⣛⣛⡛⠿⠿⠿⠛⠛⢛⣛⣉⣭⣤⣂⢜⠕⢑⣡⣴⣿")).delete(delay=5)

    if msg == "$loy":
        url_towa = "https://www.youtube.com/channel/UC1uv2Oq6kNxgATlCiez59hw"
        try:
          response = requests.get(url_towa)

          if "{\"text\":\" watching\"}" in response.text:
              await message.channel.send("Towa-sama currently streaming so no.")

          elif "{\"text\":\" waiting\"}" in response.text:
              await message.channel.send(
                  "Towa-sama has a stream planned so prolly no.")

          else:
              await message.channel.send("Towa-sama not streaming.")
              await message.channel.send("Proceeding to ping Loy-kun!")
              time.sleep(1)
              await message.channel.send("<@362632187943714846> play?")
        except: 
          pass
        
    if msg == "$cs":
      await message.channel.send("Assembling Kamen Rider!")
      time.sleep(1)

      await message.channel.send("<@232899365876924416> DECADE~ HENSHIN!")
      await(await message.channel.send("https://media1.tenor.com/images/7f3fa20decc1235cadbb506e398d4ad3/tenor.gif?itemid=20002399")).delete(delay=15)
      await asyncio.sleep(4)

      await message.channel.send("<@362632187943714846> BUILD~ HENSHIN!")
      await(await message.channel.send("https://media1.tenor.com/images/fd982b2ce5fc1fceb0fe526084186015/tenor.gif?itemid=19053759")).delete(delay=15)
      await asyncio.sleep(4)

      await message.channel.send("<@461782041856311306> KABUTO~ HENSHIN!")
      await(await message.channel.send("https://media1.tenor.com/images/0420603fd57767514baf07ffbb3dd22a/tenor.gif?itemid=18459720")).delete(delay=15)
      await asyncio.sleep(4)

      await message.channel.send("<@523783786123755532> 555~ HENSHIN!")
      await(await message.channel.send("https://media1.tenor.com/images/f2a87aed0599ff89817bcfa4d10486f5/tenor.gif?itemid=10467352")).delete(delay=15)

    if "nene" in msgL:
      await(await message.channel.send("Is there a vtuber that could even possibly EVEN TOUCH Momosuzu Nene Let alone defeat her. And I'm not talking about Suzumomo Nene. I'm not talking about Super Nenechi either. Hell, I'm not even talking about Perfect Nenechi with God Steam (with the Ringfit Adventure), after eating gyoza for lunch. I’m also not talking about Nenemax 300k subs vtuber (which is capable of speaking Japanese, English and Spanish), her two wives Ina and Lamy and a third random tall guy clicking his tongue at her as he passes by. I'm definitely NOT talking about NENEMAXMAXMAXSTORONG with 4 parallel universe wives (Ina, Lamy, Suisei, Okayu), equipped with sexy bikini while paying her employees 4 billion yen per hour after having become the CEO of Neneproduction, capable of glitching Craftopia bosses to only target her and pranking Flare in Minecraft, and having eaten Haachama's gyoza. I'm talking about Super Hyper Ultra Ultimate Deluxe Perfect Amazing Shining God 東方不敗 Master Ginga Victory Strong Cute Beautiful Galaxy Baby 無限 無敵 無双 Nenechi with 4 wives, 4 Hololive auditions, 300k husbands, IQ 3 (π, 5G), Perfect Japanglish, and Spanish, while singing La Lion, getting her water stolen by Polka and Botan (but surprised her with gaming skills) and set herself on fire in Craftopia after having become the CEO of Nenepro who punches and kicks every employee, after having disconnected while singing Connect with Kiara, as well as having her name flipped into ƎИƎИ and turned into 3D cardboard, wearing a sexy bikini, after marathoning iCarly and VICTORIOUS and having eaten Haachama's gyoza while convincing Ame to trust her and having mastered singing Shiny Smiley Story")).delete(delay=5)

    if "kelantan" in msgL:
      await(await message.channel.send("Kalu beci sangat nge ore Kelate ikut mu la. Ado ko ore Kelate caro pasa sekmu, tadok kei? Sore keno, abih sor Kelate mu cop jahak. Eh, nok oyak sor karo. Ore Kelate dok berlapa nok ko sekmu eh. Mu kalo teringin makae budu mu buleh DM aku sek kito bley oyak")).delete(delay=5)

    if "glasses" in msgL:
      await(await message.channel.send('Glasses are really versatile. First, you can have glasses-wearing girls take them off and suddenly become beautiful, or have girls wearing glasses flashing those cute grins, or have girls stealing the protagonist\'s glasses and putting them on like, "Haha, got your glasses!" That\'s just way too cute! Also, boys with glasses! I really like when their glasses have that suspicious looking gleam, and it\'s amazing how it can look really cool or just be a joke. I really like how it can fulfill all those abstract needs. Being able to switch up the styles and colors of glasses based on your mood is a lot of fun too! It\'s actually so much fun! You have those half rim glasses, or the thick frame glasses, everything! It\'s like you\'re enjoying all these kinds of glasses at a buffet. I really want Luna to try some on or Marine to try some on to replace her eyepatch. We really need glasses to become a thing in hololive and start selling them for HoloComi. Don\'t. You. Think. We. Really. Need. To. Officially. Give. Everyone. Glasses?')).delete(delay=5)

    if "nigger" in msgL:
      await message.channel.send('Not cool, <@'+ str(message.author.id) +">!")

    if "weeb" in msgL:
      await(await message.channel.send('Watashi wa :tongue: a :ok_hand: victim of :sweat_drops: cyberbullying. Everyday :calendar_spiral: someone :bust_in_silhouette: online :computer: calls :speaking_head: me :sob: a :ok_hand: "weeb" desu. :ok_hand: Watashi won\'t :no_entry_sign: stand :dash: for :eggplant: this. :point_left: 26 percent :keycap_ten: of :sweat_drops: bullying :joy: victims are :1234: chosen due to :sweat_drops: their :eggplant: race :middle_finger: or :person_tipping_hand: religion :kaaba: desu. :ok_hand: I :eye: may :calendar_spiral: look :eyes: like :sparkling_heart: a :ok_hand: basic :steam_locomotive: white :blond_haired_person: boy, :boy: but :peach: deep :scream: down :small_red_triangle_down: I :eye: am :clap: Nihongo desu. :ok_hand: Watashi religion :kaaba: is :sweat_drops: anime. :joy_cat: Anata wa :tongue: bullying :joy: me :sob: because :person_tipping_hand: of :sweat_drops: my :man: race :middle_finger: and :clap: religion :kaaba: desu :ok_hand: ka? Disgusting :stuck_out_tongue_closed_eyes: desu. :ok_hand: Anata should :cupid: be :bee: ashamed :flushed: of :sweat_drops: yourself, :rolling_eyes: pig. A :ok_hand: baka gaijin like :sparkling_heart: anata is :sweat_drops: probably :heart_eyes_cat: jealous :unamused: of :sweat_drops: my :man: race :middle_finger: and :clap: culture, cause :kiss: Nippon is :sweat_drops: more :poultry_leg: sugoi than :point_right: your :clap: shitty :poop: country :person_running: desu. :ok_hand: Watashi pity :cry: anata. You\'ll :point_right: never :person_gesturing_no: be :bee: Nihongo like :sparkling_heart: watashi. I\'m :cupid: a :ok_hand: weeb? Pfft. I :eye: AM :clap: AN :japanese_ogre: OTAKU DESU. :ok_hand: Educate yourself :rolling_eyes: on :on: nani a :ok_hand: "weeb" is :sweat_drops: before :joy: anata try :neutral_face: to :sweat_drops: insult :frowning: watashi desu. :ok_hand: I :eye: WILL :clap: NOT :no_entry_sign: BE :bee: CYBERBULLIED ANYMORE. :fire: REPORTED.')).delete(delay=3)

    if "wowo" in msgL:
      await message.channel.send("https://tenor.com/view/inugamikorone-korone-koronelfr-lfrhahaha-gif-19740883")

    if "baka" in msgL:
      with open('audio/bakatare.wav', 'rb') as fp:
        await message.channel.send(file=discord.File(fp, 'Pekora_bakatare.wav'))

    if "nande" in msgL:
      with open('audio/nande.mp3', 'rb') as fp:
        await message.channel.send(file=discord.File(fp, 'Rushia_nande.mp3'))

    if "pekopeko" in msgL:
      with open('audio/PekoPekoPekomischievous.mp3', 'rb') as fp:
        await message.channel.send(file=discord.File(fp, 'Pekora_pekopeko.mp3'))

    if "degen" in msgL:
      with open('audio/degenewates_haato.mp3', 'rb') as fp:
        await message.channel.send(file=discord.File(fp, 'Haachama_degenelates.mp3'))

    if "arigathanks" in msgL:
      with open('audio/akai-haato-arigathanks.mp3', 'rb') as fp:
        await message.channel.send(file=discord.File(fp, 'Haachama_arigathanks.mp3'))

    if "cringe" in msgL:
      with open('audio/amelia-watson-thats-pretty-cringe_1j8RUDZ.mp3', 'rb') as fp:
        await message.channel.send(file=discord.File(fp, 'Ame_cringe.mp3'))

    if "gas gas gas" in msgL:
      with open('audio/gawr-gura-gas-gas-gas.mp3', 'rb') as fp:
        await message.channel.send(file=discord.File(fp, 'Gura_gas_gas_gas.mp3'))
    
    if "no confidence" in msgL:
      with open('audio/inugami-korone-have-confidence-no-confidence.mp3', 'rb') as fp:
        await message.channel.send(file=discord.File(fp, 'Korone_no_confidence.mp3'))

    if "yahoo" in msgL:
      with open('audio/jacky-makan-makan-serambi-teruntum-mp3cut-mp3cut.mp3', 'rb') as fp:
        await message.channel.send(file=discord.File(fp, 'yahoo.mp3'))

    if "disgusting" in msgL:
      with open('audio/korone-kimoi.mp3', 'rb') as fp:
        await message.channel.send(file=discord.File(fp, 'Korone_kimoi.mp3'))

    if "ok google" in msgL:
      with open('audio/luna-ok-google.mp3', 'rb') as fp:
        await message.channel.send(file=discord.File(fp, 'Luna_ok_google.mp3'))

    if "naaa" in msgL:
      with open('audio/lunaaaa.mp3', 'rb') as fp:
        await message.channel.send(file=discord.File(fp, 'Luna_Naaaa.mp3'))

    if "faq" in msgL:
      with open('audio/sakura-miko-faq.mp3', 'rb') as fp:
        await message.channel.send(file=discord.File(fp, 'Miko_faq.mp3'))
    
    if "yabe" in msgL:
      with open('audio/shirakami-fubuki-yabe.mp3', 'rb') as fp:
        await message.channel.send(file=discord.File(fp, 'FBK_yabe.mp3'))

    if "shut up bitch" in msgL:
      with open('audio/shutup-bitch-peko.mp3', 'rb') as fp:
        await message.channel.send(file=discord.File(fp, 'Pkora_shut_up.mp3'))

    if "yabai" in msgL:
      with open('audio/uruha-rushia-yabai-yaaaaaaaaaaa.mp3', 'rb') as fp:
        await message.channel.send(file=discord.File(fp, 'Rushia_yabai.mp3'))

    if "sexy" in msgL:
      with open('audio/wowowow-pekora.mp3', 'rb') as fp:
        await message.channel.send(file=discord.File(fp, 'Pekora_sexy.mp3'))

    if "yagoo" in msgL:
      with open('audio/yagoo-is-best-girl.mp3', 'rb') as fp:
        await message.channel.send(file=discord.File(fp, 'Polka_best_grill.mp3'))

    if "pizza" in msgL:
      with open('audio/pepeloni.mp3', 'rb') as fp:
        await message.channel.send(file=discord.File(fp, 'Haachama_pepeloni.mp3'))

    if "okiro" in msgL:
      with open('audio/Rushia_Okiro_Hentai.mp3', 'rb') as fp:
        await message.channel.send(file=discord.File(fp, 'Rushia_Okiro.mp3'))

@client.event
async def on_message_delete(message):
  client.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)
        


keep_alive()
client.run(os.getenv('TOKEN'))
