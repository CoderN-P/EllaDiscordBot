import discord, os
from keep_alive import keep_alive
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json, random
import datetime, asyncio

bot = commands.Bot(command_prefix="e/", help_command=None, case_insensitive=True)

keep_alive()




@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Game(name="e/help"))
  print('Up and running, systems ready.')

@bot.command(name='add-item')
async def add_item(ctx, *, arg):
  arg = arg.split(':')
  file = json.load(open('shop.json'))
  file[arg[0]] = int(arg[1])
  with open('shop.json', 'w') as f:
    f.write(json.dumps(file))
  await ctx.send('Successfully added that item to the shop')


@bot.command()
async def shop(ctx):
  shop = json.load(open('shop.json'))
  string = ''''''
  
  for y, z in enumerate(shop.items()):
    string = string + f'**{y + 1}.** {z[0]}: {z[1]} coins \n'

  await ctx.send(embed=discord.Embed(title='Shop', description=string, color=0xe67e22))


@bot.command()
async def buy(ctx, *, arg):
  arg = arg.split(':')
  print(arg)
  shop_list = json.load(open('shop.json'))
  if arg[0] not in shop_list.keys():
    embed = discord.Embed(title='Hey!', description=":x: That item doesn't exist")
    await ctx.send(embed=embed)
    return

  else:
    try:
      int(arg[1])

    except:
      embed = discord.Embed(title='Hey!', description=':x: That is not a valid amount!')
      await ctx.send(embed=embed)
      return

    cost = shop_list[arg[0].title()] * int(arg[1])

    try:

      balance = json.load(open('profiles.json'))[str(ctx.author)]

    except:
      embed = discord.Embed(title='Hey!', description=":x: You don't have an account! Type `e/start` to create one!")
      await ctx.send(embed=embed)
      return

    if balance < cost:
      embed = discord.Embed(title='Hey!', description=f":x: You don't have enough money! You only have {balance} coins")
      await ctx.send(embed=embed)
      return

    else:
      file = json.load(open('inv.json'))
      if str(ctx.author) not in file.keys():
        file[str(ctx.author)] = {arg[0].title(): int(arg[1])}

      else:
        file[str(ctx.author)][arg[0].title()] = int(arg[1])

      with open('inv.json', 'w') as f:
        f.write(json.dumps(file))

      
      file = json.load(open('profiles.json'))

      file[str(ctx.author)] = file[str(ctx.author)] - cost

      with open('profiles.json', 'w') as f:
        f.write(json.dumps(file))

      embed = discord.Embed(title='Success', description=f'Successfully bought {arg[1]} {arg[0]}')
      await ctx.send(embed=embed)

@bot.command(aliases=['inv'])
async def inventory(ctx):
  data = json.load(open('inv.json'))
  if str(ctx.author) not in data.keys():
    embed = discord.Embed(title='Inventory', description=':slight_frown: You have nothing in your inventory! Check out `e/shop` to check out things and `e/buy` to buy things')
    await ctx.send(embed=embed)

  else:
    string = ''''''
    for x, i in enumerate(data[str(ctx.author)].items()):
      string = string + f'**{x + 1}.** {i[0]}: {i[1]}\n'
    embed = discord.Embed(title=inventory, description=string)
    await ctx.send(embed=embed)

@commands.cooldown(1, 3600, commands.BucketType.user)
@bot.command()
async def work(ctx):
  bals = json.load(open('profiles.json'))
  if str(ctx.message.author) not in bals.keys():
    await ctx.channel.send("You haven't created an account yet! Create one by running the command `e/start`")
    return


  
  amount = random.randint(1, 100)
  bals[str(ctx.author)] += amount
  with open("profiles.json", "w") as f:
    f.write(json.dumps(bals))
  await ctx.channel.send(f"you work hard and earn `{amount}` <:chb_greek_drachma:787750422214869002>")


@bot.command(name='create-pet')
async def _pet(ctx, *, name):
  name1 = name.split(',')
  try:
    name = name1[0]
    url = name1[1]
  except:
    embed = discord.Embed(title='Incorrect Usage', description='```e/create-pet <name>, <image url>```')
    await ctx.send(embed=embed)
    return

  try:
    embed=discord.Embed(title='Image Set!')
    embed.set_image(url=url)
  except:
    embed = discord.Embed(title='Invalid Url', description=':x: Your url is not valid. Please try a new url!')
    await ctx.send(embed=embed)
    return

  file = json.load(open('pet.json'))

  if str(ctx.author) in file.keys():
    embed = discord.Embed(title='Error', description=':x: You already have a pet. To edit your put type `e/edit-pet <new name>, <url>`')
    await ctx.channel.send(embed=embed)
    return

  file[str(ctx.author)] = [name, url, 0]

  with open('pet.json', 'w') as f:
    f.write(json.dumps(file))

  embed=discord.Embed(title=name)
  embed.set_image(url=url)
  embed.set_footer(text='Click the :white_check_mark: to add a description to your pet! Click :x: to skip. (this will time out in 30 seconds)')

  msg = await ctx.send(embed=embed)

  await msg.add_reaction("✅")
  await msg.add_reaction("❌")

  def check(reaction, user):
    return reaction.message == msg and user == ctx.author and str(reaction.emoji) in ["❌", "✅"]
  
  file = json.load(open('pet.json'))

  try:
    reaction, user = await bot.wait_for('reaction_add', check=check, timeout=30)

    if str(reaction.emoji) == "✅":
      embed = discord.Embed(title='Great!', description='Type the description of your pet below!')
      
      embed.set_footer(text='This will time out in 30 seconds')
      await ctx.send(embed=embed)
      def check(m):
        return m.channel == ctx.channel and m.author == ctx.author

      try:
        msg1 = await bot.wait_for('message', check=check, timeout=30)

        file[str(ctx.author)][2] = msg1.content

        with open('pet.json', 'w') as f:
          f.write(json.dumps(file))

        await ctx.send('Description set!')

      except asyncio.TimeoutError:
        embed = discord.Embed(title='Whoops', description=':x: Time ran out!')
        await ctx.send(embed=embed)


  except asyncio.TimeoutError:
    embed = discord.Embed(title='Whoops', description=':x: Time ran out!')
    await ctx.send(embed=embed)

   

@bot.command()
async def pet(ctx):
  file = json.load(open('pet.json'))
  try:
    pet = file[str(ctx.author)]

  except:
    embed = discord.Embed(title='Error', description=":x: You don't have a pet! Type  `e/create-pet` to add your pet!")
    await ctx.send(embed=embed)
    return

  embed = discord.Embed(title=pet[0])
  if pet[2] != 0:
    embed.description = pet[2]

  else:
    pass

  embed.set_image(url=pet[1])

  await ctx.send(embed=embed)

@bot.command(name='edit-pet')
async def edit_pet(ctx, *, name):
  try:
    file = json.load(open('pet.json'))
    pet_var = file[str(ctx.author)]

  except:
    embed = discord.Embed(title='Hey!!', description=":x: You don't have a pet! Type `e/create-pet` to create a pet!")

    await ctx.send(embed=embed)
    return

  name1 = name.split(',')
  try:
    name = name1[0]
    url = name1[1]
  except:
    embed = discord.Embed(title='Incorrect Usage', description='```e/create-pet <name>, <image url>```')
    await ctx.send(embed=embed)
    return

  try:
    embed=discord.Embed(title='Image Set!')
    embed.set_image(url=url)
  except:
    embed = discord.Embed(title='Invalid Url', description=':x: Your url is not valid. Please try a new url!')
    await ctx.send(embed=embed)
    return

  

  
  file[str(ctx.author)] = [name, url, 0]

  with open('pet.json', 'w') as f:
    f.write(json.dumps(file))

  embed=discord.Embed(title=name)
  embed.set_image(url=url)
  msg = await ctx.send(embed=embed)


  await msg.add_reaction("✅")
  await msg.add_reaction("❌")

  def check(reaction, user):
    return reaction.message == msg and user == ctx.author and str(reaction.emoji) in ["❌", "✅"]
  
  file = json.load(open('pet.json'))

  try:
    reaction, user = await bot.wait_for('reaction_add', check=check, timeout=30)

    if str(reaction.emoji) == "✅":
      embed = discord.Embed(title='Great!', description='Type the description of your pet below!')
      
      embed.set_footer(text='This will time out in 30 seconds')
      await ctx.send(embed=embed)

      def check(m):
        return m.channel == ctx.channel and m.author == ctx.author

      try:
        msg1 = await bot.wait_for('message', check=check, timeout=30)

        file[str(ctx.author)][2] = msg1.content

        with open('pet.json', 'w') as f:
          f.write(json.dumps(file))

        await ctx.send('Description set!')

      except asyncio.TimeoutError:
        embed = discord.Embed(title='Whoops', description=':x: Time ran out!')
        await ctx.send(embed=embed)


  except asyncio.TimeoutError:
    embed = discord.Embed(title='Whoops', description=':x: Time ran out!')
    await ctx.send(embed=embed)





@commands.cooldown(1, 3600, commands.BucketType.user)
@bot.command()
async def crime(ctx):
  coins = random.randint(1, 100)
  chance = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

  file = json.load(open('profiles.json'))
  if chance <= 4:
    #you were successful
    if ctx.author not in file.keys():
      file[str(ctx.author)] = coins

    else:
      file[str(ctx.author)] = file[str(ctx.author)] + coins

    await ctx.channel.send(embed=discord.Embed(title='Success', description=f"You successfully stole {coins} <:chb_greek_drachma:787750422214869002> from CHB's database. :party:"))

  else:
    if ctx.author not in file.keys():
      file[str(ctx.author)] = coins * -1

    else:
      file[str(ctx.author)] = file[str(ctx.author)] - coins

    
    await ctx.channel.send(embed=discord.Embed(title='Failed', description=f"You were caught stealing. You had to pay {coins} <:chb_greek_drachma:787750422214869002> as a fine."))
    #you failed sike

@work.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Cooldown",description=f"Deyex doesn't want you to make money now. Take some rest, come back in `{str(datetime.timedelta(seconds = error.retry_after))[2:][:5]}`.")
        await ctx.send(embed=em)

@crime.error
async def crime_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Cooldown",description=f"Hey you can't do crime right now! The police are looking for you. Come back in `{str(datetime.timedelta(seconds = error.retry_after))[2:][:5]}`.")
        await ctx.send(embed=em)


@bot.command()
async def profile(ctx, *arg):
  balance1 = json.load(open('profiles.json'))
  pet = json.load(open('pet.json'))
  weapon = json.load(open('weapon.json'))
  pegasi = json.load(open('pegasi.json'))
  
  try:
    balance = balance1[str(ctx.author)]
    sorted_keys = sorted(balance1, key=balance1.get, reverse=True) 
    sorted_dict = {}
    for w in sorted_keys:
        sorted_dict[w] =  balance1[w]

    list1 = list(sorted_dict.keys())
    rank = list1.index(str(ctx.author)) + 1
  except:
    balance = 'Unregistered'
    rank = 'Unregistered'
    
  try:
    weapon = weapon[str(ctx.author)][0]
  except:
    weapon = 'Unregistered'

  try:
    pet = pet[str(ctx.author)][0]
  except:
    pet = 'Unregistered'
  
  try:
    pegasi = pegasi[str(ctx.author)][0]
  except:
    pegasi = 'Unregistered'

  embed = discord.Embed(title=f"{ctx.author}'s Profile")



  embed.add_field(name='Balance', value=balance)
  embed.add_field(name='Rank', value=rank)
  embed.add_field(name='Weapon', value=weapon)
  embed.add_field(name='Pet', value=pet)
  embed.add_field(name='Pegasi', value=pegasi)
  

  embed.set_thumbnail(url=ctx.author.avatar_url)

  await ctx.channel.send(embed=embed)

  
  

@bot.command()
async def help(ctx):
  help_embed = discord.Embed(title='Help', description='''Welcome to Ella, the CHB economy bot. Our prefix is `e/`.
  
  An economy bot, Ella manages all aspects related to coins and money. You can run the commands e/work and e/theft to earn/lose <:chb_greek_drachma:787750422214869002>. There are also other commands as well.''') 
  await ctx.send(embed=help_embed)

@bot.command()
async def start(ctx):
  bals = json.load(open('profiles.json'))
  if str(ctx.message.author) in bals.keys():
    await ctx.channel.send('You already have an account!!')
    return
  bals = json.load(open('profiles.json'))
  bals[str(ctx.message.author)] = 0

  with open("profiles.json", "w") as f:
    f.write(json.dumps(bals))
  await ctx.channel.send('Account sucessfully created!!')

@bot.command(aliases = ['lb'])
async def leaderboard(ctx):
  a = json.load(open('profiles.json'))
  sorted_keys = sorted(a, key=a.get, reverse=True) 
  sorted_dict = {}
  for w in sorted_keys:
      sorted_dict[w] =  a[w]
  
  string = ''''''
  

  other_dict = {}

  for i in range(0, len(sorted_dict)):
    other_dict[i + 1] = list(sorted_dict.keys())[i]

  other_dict = {y: x for x, y in other_dict.items()}

  for x, y in sorted_dict.items():
    string = string + f'**{other_dict[x]}.** {x} : {y}<:chb_greek_drachma:787750422214869002> \n'

  await ctx.send(embed=discord.Embed(title="Leaderboard", description=string, color=0xe67e22))






@bot.command(aliases=['balance'])
async def bal(ctx):
  bals = json.load(open('profiles.json'))
  if str(ctx.message.author) not in bals.keys():
    await ctx.channel.send('You dont have an account, use `e\start` to create one')
    return
  embed = discord.Embed(title=str(ctx.message.author), description=f'Your balance is: {bals[str(ctx.message.author)]} <:chb_greek_drachma:787750422214869002>')

  await ctx.channel.send(embed=embed)


@bot.command(name='create-weapon')
async def _weapon(ctx, *, name):
  name1 = name.split(',')
  try:
    name = name1[0]
    url = name1[1]
  except:
    embed = discord.Embed(title='Incorrect Usage', description='```e/create-weapon <name>, <image url>```')
    await ctx.send(embed=embed)
    return

  try:
    embed=discord.Embed(title='Image Set!')
    embed.set_image(url=url)
  except:
    embed = discord.Embed(title='Invalid Url', description=':x: Your url is not valid. Please try a new url!')
    await ctx.send(embed=embed)
    return

  file = json.load(open('weapon.json'))

  if str(ctx.author) in file.keys():
    embed = discord.Embed(title='Error', description=':x: You already have a weapon. To edit your put type `e/edit-weapon <new name>, <url>`')
    await ctx.channel.send(embed=embed)
    return
  file[str(ctx.author)] = [name, url]

  with open('weapon.json', 'w') as f:
    f.write(json.dumps(file))

  embed=discord.Embed(title=name)
  embed.set_image(url=url)
  await ctx.send(embed=embed)

  

@bot.command()
async def weapon(ctx):
  file = json.load(open('weapon.json'))
  try:
    pet = file[str(ctx.author)]

  except:
    embed = discord.Embed(title='Error', description=":x: You don't have a weapon! Type  `e/create-weapon` to add your weapon!")
    await ctx.send(embed=embed)
    return

  embed = discord.Embed(title=pet[0])
  embed.set_image(url=pet[1])

  await ctx.send(embed=embed)

@bot.command(name='edit-weapon')
async def edit_weapon(ctx, *, name):
  name1 = name.split(',')
  try:
    name = name1[0]
    url = name1[1]
  except:
    embed = discord.Embed(title='Incorrect Usage', description='```e/create-weapon <name>, <image url>```')
    await ctx.send(embed=embed)
    return

  try:
    embed=discord.Embed(title='Image Set!')
    embed.set_image(url=url)
  except:
    embed = discord.Embed(title='Invalid Url', description=':x: Your url is not valid. Please try a new url!')
    await ctx.send(embed=embed)
    return

  file = json.load(open('weapon.json'))

  
  file[str(ctx.author)] = [name, url]

  with open('weapon.json', 'w') as f:
    f.write(json.dumps(file))

  embed=discord.Embed(title=name)
  embed.set_image(url=url)
  await ctx.send(embed=embed)



@bot.command(name='create-pegasi')
async def _pegasi(ctx, *, name):
  name1 = name.split(',')
  try:
    name = name1[0]
    url = name1[1]
  except:
    embed = discord.Embed(title='Incorrect Usage', description='```e/create-pegasi <name>, <image url>```')
    await ctx.send(embed=embed)
    return

  try:
    embed=discord.Embed(title='Image Set!')
    embed.set_image(url=url)
  except:
    embed = discord.Embed(title='Invalid Url', description=':x: Your url is not valid. Please try a new url!')
    await ctx.send(embed=embed)
    return

  file = json.load(open('pegasi.json'))

  if str(ctx.author) in file.keys():
    embed = discord.Embed(title='Error', description=':x: You already have a pegasi. To edit your put type `e/edit-pegasi <new name>, <url>`')
    await ctx.channel.send(embed=embed)
    return
  file[str(ctx.author)] = [name, url]

  with open('pegasi.json', 'w') as f:
    f.write(json.dumps(file))

  embed=discord.Embed(title=name)
  embed.set_image(url=url)
  await ctx.send(embed=embed)

@bot.command()
async def pegasi(ctx):
  file = json.load(open('pegasi.json'))
  try:
    pet = file[str(ctx.author)]

  except:
    embed = discord.Embed(title='Error', description=":x: You don't have a pegasi! Type  `e/create-pegasi` to add your pegasi!")
    await ctx.send(embed=embed)
    return

  embed = discord.Embed(title=pet[0])
  embed.set_image(url=pet[1])

  await ctx.send(embed=embed)

@bot.command(name='edit-pegasi')
async def edit_pegasi(ctx, *, name):
  name1 = name.split(',')
  try:
    name = name1[0]
    url = name1[1]
  except:
    embed = discord.Embed(title='Incorrect Usage', description='```e/create-weapon <name>, <image url>```')
    await ctx.send(embed=embed)
    return

  try:
    embed=discord.Embed(title='Image Set!')
    embed.set_image(url=url)
  except:
    embed = discord.Embed(title='Invalid Url', description=':x: Your url is not valid. Please try a new url!')
    await ctx.send(embed=embed)
    return

  file = json.load(open('pegasi.json'))

  
  file[str(ctx.author)] = [name, url]

  with open('pegasi.json', 'w') as f:
    f.write(json.dumps(file))

  embed=discord.Embed(title=name)
  embed.set_image(url=url)
  await ctx.send(embed=embed)

bot.run(os.environ['TOKEN'])