import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import json

bot = commands.Bot(command_prefix='&')

@bot.event
async def on_ready():
	print("Le robot est connecté comme {0.user}".format(bot))

@bot.command()
async def helpme(ctx):
	"""command to send message about bot's command"""
	await ctx.send("Voici les commandes disponibles :\n - definition mot_clé : obtenir la définition d'un mot clé (anglais uniquement). la commande '$definition liste' affiche la liste des mots clés.\n - carte : permet d'afficher l'image des cartes recherché (anglais uniquement). Exemple '$carte Ms.'")

@bot.command()
async def definition(ctx, arg):
	"""commend to obtain a key world's description """

	"""lancement de bs4 pour récupérer les définitions"""
	url_definition = "https://hallofheroeslcg.com/marvel-champions-lcg-keyword-list/"
	page_definition = requests.get(url_definition)
	soup_definition = BeautifulSoup(page_definition.content, 'html5lib')
	print(arg)
	if arg == "liste":
		liste_definition_h3 = soup_definition.find_all('h3')
		liste_definition = []
		for mot in liste_definition_h3:
			liste_definition.append(mot)
		await ctx.send(liste_definition)
	else:
		""" we get the next <p> after the <h3> who contains our search """
		definitions = soup_definition.find(text = arg).findNext("p").contents
		await ctx.send(definitions)

@bot.command()
async def carte(ctx, *arg):
	""" command to see a pull of search card (english) """

	""" break the search without name of card """
	if len(arg) == 0:
		await ctx.send("Tu n'as pas préciser de carte!")

	else:

		""" tupl become a str """
		recherche = ' '.join(arg) 
		""" str formating """
		recherche.lower().replace(" " , "+")

		"""" request the marvelcdb base search with our search """
		url_carte = 'https://marvelcdb.com/find?q=' + recherche + '&sort=set&view=card&decks=all'
		page_carte = requests.get(url_carte)
		soup_carte = BeautifulSoup(page_carte.content, 'html5lib')

		carte = soup_carte.find_all("img")

		
		""" send every image fund in the precedent request """
		for image in carte:
			await ctx.send("https://marvelcdb.com/" + image['src'])

@bot.command()
async def random(ctx):
	""" command to send the Halion's randomizer """
	await ctx.send("Vous pouvez randomizer une partie ici : https://canthom.github.io/randomizer-mc/")

@bot.command()
async def cartefr(ctx, *arg):
	
	""" WIP : search a french card """

	""" Definition de arg en str pour recherche. Création de la variable dict pour le resultat"""
	recherche = ' '.join(arg)
	resultat_carte = []

	""" On élimine la recherche à 0 """
	if len(arg) == 0:
		await ctx.send("Tu n'as pas préciser de carte!")

	else:

		"""ouverture du json"""
		with open("data.json", encoding ="utf8") as json_file:
			data = json.load(json_file)

		""""on rajoute chaque id octgn dans le dictionnaire resultat_carte"""
		for i in data:
			if i['real_name'] == recherche:
				if i['octgn_id'] in data[i]:
					resultat_carte.append(i['octgn_id'])

		""" on envoie chaque image """
		for id_carte in resultat_carte:
			print(id_carte)
			await ctx.send(file=discord.File('/Images/' + id_carte + ".jpg"))

bot.run("TOKEN")

