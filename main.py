import discord, os
from keep_alive import keep_alive
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json, random
import datetime, asyncio

bot = commands.Bot(command_prefix="e/", help_command=None, case_insensitive=True, owner_ids=[751594192739893298, 759174828568870963])

keep_alive()




@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Game(name="e/help"))
  print('Up and running, systems ready.')


@commands.cooldown(1, 3600, commands.BucketType.user)
@bot.command(aliases=['steal'])
async def rob(ctx, user: discord.Member=None):
  file = json.load(open('profiles.json'))
  if user == ctx.author:
    await ctx.send('You are not allowed to rob yourself. ')
    return
  if user is None:
    await ctx.send('Who are you robbing? Mention an user.')
    return

  else:
    if str(user.id) not in file.keys():
      await ctx.send("Hey! This person doesn't have an account")
    else:
      amount = random.randint(1, 100)
      chance = random.randint(1, 2)

      if chance == 1:
        await ctx.send(f'You stole {amount} from {user} :sunglasses:')
        file[str(ctx.author.id)] = file[str(ctx.author.id)] + amount
        file[str(user.id)] = file[str(user.id)] - amount

        with open('profiles.json', 'w') as f:
          f.write(json.dumps(file))
      else:
        await ctx.send(':x: You were caught by the police. You were fined 100')
        file[str(ctx.author.id)] = file[str(ctx.author.id)] - 100

        with open('profiles.json', 'w') as f:
          f.write(json.dumps(file))
        
@rob.error
async def rob_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.MemberNotFound):
    await ctx.send('Not a valid user.')
  else:
    await ctx.send(f'SLOW DOWN. Try again in `{str(datetime.timedelta(seconds = error.retry_after))[2:][:5]}`')

@commands.is_owner()
@bot.command(name='add-item')
async def add_item(ctx, *, arg):
  arg = arg.split(':')
  file = json.load(open('shop.json'))
  file[arg[0]] = [int(arg[1]), arg[2]]
  with open('shop.json', 'w') as f:
    f.write(json.dumps(file))
  await ctx.send('Successfully added that item to the shop')

@bot.command(name='work-set')
async def work_set(ctx, user: discord.Member, amount):
  bals = json.load(open('work-set.json'))
  bals[str(user.id)] = amount
  with open('work-set.json', 'w') as f:
    f.write(json.dumps(bals))
  await ctx.send(f'{user} will now get {amount} every time they work')
@commands.is_owner()
@bot.command(name='delete-item')
async def delete_item(ctx, *, arg):
  file = json.load(open('shop.json'))
  try:
    del file[arg]
    with open('shop.json', 'w') as f:
      f.write(json.dumps(file))
    await ctx.send('Successfully deleted that item from the shop')

  except:
    await ctx.send(":x: That item doesn't exist.")

@commands.is_owner()
@bot.command(name='add-money')
async def add_money(ctx, user: discord.Member, amount: int):
  file = json.load(open('profiles.json'))
  if str(user.id) not in file.keys():
    await ctx.send('this user does not have an account yet')
  else:
    
    file[str(user.id)] = file[str(user.id)] + amount
    with open('profiles.json', 'w') as f:
      f.write(json.dumps(file))
    await ctx.send(user.name + f' now has {file[str(user.id)]} :coin:')

@commands.is_owner()
@bot.command(name='remove-money')
async def remove_money(ctx, user: discord.Member, amount: int):
  file = json.load(open('profiles.json'))
  if str(user.id) not in file.keys():
    await ctx.send('this user does not have an account yet')
  else:
    
    file[str(user.id)] = file[str(user.id)] - amount
    with open('profiles.json', 'w') as f:
      f.write(json.dumps(file))
    await ctx.send(user.name + f' now has {file[str(user.id)]} :coin:')

@bot.command()
async def shop(ctx):
  shop = json.load(open('shop.json'))
  string = ''''''
  embed = discord.Embed(title='Shop', color=0xe67e22)
  
  for y, z in enumerate(shop.items()):
    embed.add_field(name=f'**{y + 1}.** <:chb_greek_drachma:787750422214869002>{z[1][0]} - {z[0]}', value=f'{z[1][1]}\n\n', inline=False)


  await ctx.send(embed=embed)


@bot.command()
async def buy(ctx, *, arg):
  arg = arg.split(':')
  print(arg)
  shop_list = json.load(open('shop.json'))
  if arg[0] not in shop_list.keys():
    embed = discord.Embed(title='Hey!', description=":x: That item doesn't exist! Format: e/buy (item):(amount)")
    await ctx.send(embed=embed)
    return

  else:
    try:
      balance = int(arg[1])

    except:
      embed = discord.Embed(title='Hey!', description=':x: That is not a valid amount!')
      await ctx.send(embed=embed)
      return

    cost = shop_list[arg[0].title()][0] * int(arg[1])

    try:


      balance = json.load(open('profiles.json'))[str(ctx.author.id)]

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
      if str(ctx.author.id) not in file.keys():
        file[str(ctx.author.id)] = {arg[0].title(): int(arg[1])}

      else:
        file[str(ctx.author.id)][arg[0].title()] = int(arg[1])

      with open('inv.json', 'w') as f:
        f.write(json.dumps(file))

      
      file = json.load(open('profiles.json'))

      file[str(ctx.author.id)] = file[str(ctx.author.id)] - cost

      with open('profiles.json', 'w') as f:
        f.write(json.dumps(file))

      embed = discord.Embed(title='Success', description=f'Successfully bought {arg[1]} {arg[0]}')
      await ctx.send(embed=embed)

@bot.command(aliases=['inv'])
async def inventory(ctx, user: discord.Member=None):
  data = json.load(open('inv.json'))
  if user is None:
    user = ctx.author
 
  if str(user.id) not in data.keys():
    embed = discord.Embed(title='Inventory', description=':slight_frown: You/or the person you are viewing have nothing in your inventory! Check out `e/shop` to check out things and `e/buy` to buy things')
    await ctx.send(embed=embed)

  else:
    string = ''''''
    for x, i in enumerate(data[str(user.id)].items()):
      string = string + f'**{x + 1}.** {i[0]}: {i[1]}\n'
    embed = discord.Embed(title=inventory, description=string)
    await ctx.send(embed=embed)





@bot.command()
@commands.cooldown(1, 1800, commands.BucketType.user)
async def work(ctx):
  bals = json.load(open('profiles.json'))
  if str(ctx.message.author.id) not in bals.keys():
    await ctx.channel.send("You haven't created an account yet! Create one by running the command `e/start`")
    return

  
  file = json.load(open('work-set.json'))
  if str(ctx.author.id) not in file:
    amount = random.randint(1, 500)
  else:
    if file[str(ctx.author.id)] == 'random':
      amount = random.randint(1, 500)
    else:
      amount = file[str(ctx.author.id)]


  
  await ctx.channel.send(f"you work hard and earn `{amount}` <:chb_greek_drachma:787750422214869002>")


  

  
  
  bals[str(ctx.author.id)] = bals[str(ctx.author.id)] + int(amount)

  with open("profiles.json", "w") as f:
    f.write(json.dumps(bals))

  


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

  if str(ctx.author.id) in file.keys():
    embed = discord.Embed(title='Error', description=':x: You already have a pet. To edit your put type `e/edit-pet <new name>, <url>`')
    await ctx.channel.send(embed=embed)
    return

  file[str(ctx.author.id)] = [name, url, 0]

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

        file[str(ctx.author.id)][2] = msg1.content

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
    pet = file[str(ctx.author.id)]

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
    pet_var = file[str(ctx.author.id)]

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

  

  
  file[str(ctx.author.id)] = [name, url, 0]

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

        file[str(ctx.author.id)][2] = msg1.content

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
      file[str(ctx.author.id)] = coins

    else:
      file[str(ctx.author.id)] = file[str(ctx.author)] + coins

    await ctx.channel.send(embed=discord.Embed(title='Success', description=f"You successfully stole {coins} <:chb_greek_drachma:787750422214869002> from CHB's database. :party:"))

  else:
    if ctx.author not in file.keys():
      file[str(ctx.author.id)] = coins * -1

    else:
      file[str(ctx.author.id)] = file[str(ctx.author.id)] - coins

    
    await ctx.channel.send(embed=discord.Embed(title='Failed', description=f"You were caught stealing. You had to pay {coins} <:chb_greek_drachma:787750422214869002> as a fine."))
    #you failed sike

@work.error
async def work_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Cooldown",description=f"Deyex doesn't want you to make money now. Take some rest, come back in `{str(datetime.timedelta(seconds = error.retry_after))[2:][:5]}`.")
        await ctx.send(embed=em)

    else:
      raise error

@crime.error
async def crime_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Cooldown",description=f"Hey you can't do crime right now! The police are looking for you. Come back in `{str(datetime.timedelta(seconds = error.retry_after))[2:][:5]}`.")
        await ctx.send(embed=em)


@bot.command()
async def profile(ctx, user: discord.Member=None):
  if user == None:
    user = ctx.author
  balance1 = json.load(open('profiles.json'))
  pet = json.load(open('pet.json'))
  weapon = json.load(open('weapon.json'))
  pegasi = json.load(open('pegasi.json'))
  
  try:
    balance = balance1[str(user.id)]
    sorted_keys = sorted(balance1, key=balance1.get, reverse=True) 
    sorted_dict = {}
    for w in sorted_keys:
        sorted_dict[w] =  balance1[w]

    list1 = list(sorted_dict.keys())
    rank = list1.index(str(user.id)) + 1
  except:
    balance = 'Unregistered'
    rank = 'Unregistered'
    
  try:
    weapon = weapon[str(user.id)][0]
  except:
    weapon = 'Unregistered'

  try:
    pet = pet[str(user.id)][0]
  except:
    pet = 'Unregistered'
  
  try:
    pegasi = pegasi[str(user.id)][0]
  except:
    pegasi = 'Unregistered'

  embed = discord.Embed(title=f"{user}'s Profile")



  embed.add_field(name='Balance', value=balance)
  embed.add_field(name='Rank', value=rank)
  embed.add_field(name='Weapon', value=weapon)
  embed.add_field(name='Pet', value=pet)
  embed.add_field(name='Pegasi', value=pegasi)
  

  embed.set_thumbnail(url=user.avatar_url)

  await ctx.channel.send(embed=embed)

  
  



@bot.command()
async def start(ctx):
  bals = json.load(open('profiles.json'))
  if str(ctx.message.author.id) in bals.keys():
    await ctx.channel.send('You already have an account!!')
    return
  bals = json.load(open('profiles.json'))
  bals[str(ctx.message.author.id)] = 0

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
    string = string + f'**{other_dict[x]}.** {await ctx.guild.fetch_member(x)} : {y}<:chb_greek_drachma:787750422214869002> \n'

  await ctx.send(embed=discord.Embed(title="Leaderboard", description=string, color=0xe67e22))






@bot.command(aliases=['balance'])
async def bal(ctx, user: discord.Member=None):
  if user == None:
    user = ctx.author

  
  bals = json.load(open('profiles.json'))
  if str(user.id) not in bals.keys():
    await ctx.channel.send("You or the person your are viewing dont/doesn't have an account, use `e\start` to create one")
    return
  embed = discord.Embed(title=str(user), description=f'Your/Their balance is: {bals[str(user.id)]} <:chb_greek_drachma:787750422214869002>')

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

  if str(ctx.author.id) in file.keys():
    embed = discord.Embed(title='Error', description=':x: You already have a weapon. To edit your put type `e/edit-weapon <new name>, <url>`')
    await ctx.channel.send(embed=embed)
    return
  file[str(ctx.author.id)] = [name, url]

  with open('weapon.json', 'w') as f:
    f.write(json.dumps(file))

  embed=discord.Embed(title=name)
  embed.set_image(url=url)
  await ctx.send(embed=embed)

  

@bot.command()
async def weapon(ctx):
  file = json.load(open('weapon.json'))
  try:
    pet = file[str(ctx.author.id)]

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

  
  file[str(ctx.author.id)] = [name, url]

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

  if str(ctx.author.id) in file.keys():
    embed = discord.Embed(title='Error', description=':x: You already have a pegasi. To edit your put type `e/edit-pegasi <new name>, <url>`')
    await ctx.channel.send(embed=embed)
    return
  file[str(ctx.author.id)] = [name, url]

  with open('pegasi.json', 'w') as f:
    f.write(json.dumps(file))

  embed=discord.Embed(title=name)
  embed.set_image(url=url)
  await ctx.send(embed=embed)

@bot.command()
async def pegasi(ctx):
  file = json.load(open('pegasi.json'))
  try:
    pet = file[str(ctx.author.id)]

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

  
  file[str(ctx.author.id)] = [name, url]

  with open('pegasi.json', 'w') as f:
    f.write(json.dumps(file))

  embed=discord.Embed(title=name)
  embed.set_image(url=url)
  await ctx.send(embed=embed)

deyex = ['work-set', 'add-item', 'delete-item', 'add-money', 'remove-money']
other = ['create-pet', 'create-weapon', 'create-pegasi', 'edit-pet', 'edit-pegasi', 'edit-weapon']
@bot.command()
async def help(ctx):
  embed = discord.Embed(title='Help Page', description='''Welcome to Ella, the CHB economy bot. Our prefix is `e/`.
  
  An economy bot, Ella manages all aspects related to coins and money. You can run the commands e/work and e/crime to earn/lose <:chb_greek_drachma:787750422214869002>. There are also other commands as well. (listed below)''')
  deyex_string = ''''''
  normal_string = ''''''
  other_string = ''''''
  for command in bot.commands:
    if command.name in deyex:
      deyex_string += f'`{command.name}` | '
    elif command.name in other:
      other_string += f'`{command.name}` | '
    else:
      normal_string += f'`{command.name}` | '

  embed.add_field(name='Economy', value=normal_string)

  embed.add_field(name='Roleplay', value=other_string)

  embed.add_field(name='Deyex/Admin Commands', value=deyex_string)
      
  await ctx.send(embed=embed)


  

bot.run(os.environ['TOKEN'])