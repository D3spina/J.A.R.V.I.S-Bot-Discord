import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import json
import random

bot = commands.Bot(command_prefix='&')

@bot.event
async def on_ready():
	""" check if bot is connected """
	print("Le robot est connecté comme {0.user}".format(bot))

@bot.command()
async def helpme(ctx):
	""" send bot command """
	await ctx.send("Voici les commandes disponibles :\n")
	await ctx.send(" - definition 'mot_clé'' : obtenir la définition d'un mot clé (anglais uniquement). la commande '$definition liste' affiche la liste des mots clés.\n")
	await ctx.send(" - carte 'nom_carte' : permet d'afficher l'image des cartes recherchées. Exemple '$carte Miss Marvel'")
	await ctx.send(" - randomizer : afficher le lien du randomizer de Halion")
	await ctx.send(" - citation : obtenir une citation aléatoire d'une carte du jeu")
	await ctx.send(" - deck 'id' : obtenir les cartes du deck via marvelcdb. Exemple '&deck 12921'. Ne marche qu'avec les decks public")
	await ctx.send("MP D3spina#8685 si besoin")

@bot.command()
async def definition(ctx, arg):
	""" get key world definition """

	""" get the html page from hallofheroes """
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
		""" def if the next p before h3 text """
		definitions = soup_definition.find(text = arg).findNext("p").contents
		await ctx.send(definitions)

@bot.command()
async def randomizer(ctx):
	""" get the Halion's randomizer link """
	await ctx.send("Vous pouvez randomizer une partie ici : https://canthom.github.io/randomizer-mc/")

@bot.command()
async def carte(ctx, *arg):
	""" post the image of card """

	""" get the *arg in string and lower ; creating list for result and resultat_Null to send message if =1 """
	recherche = ' '.join(arg)
	recherche = str(recherche.lower())
	resultat_carte = []
	resultat_Null = 0

	""" we break the null search """
	if len(arg) == 0:
		await ctx.send("Tu n'as pas préciser de carte!")

	else:

		""" opening data.json with all references """
		with open("C:\\Users\\meelo\\Documents\\Dev\\Python\\Cardbot for Discord\\Ressource\\data.json", encoding ="utf8") as json_file:
			data = json.load(json_file)

		"""" put octgn_id in the resultat_carte list """
		for i in data:
			""" search french and english name """
			if i['name'] == recherche or i['real_name'] == recherche:
				""" check if we have an octgn_id for the card  """
				if "octgn_id" in i:
					""" check if the id is already on the list """
					if i['octgn_id'] not in resultat_carte:
						resultat_carte.append(i['octgn_id'])
						resultat_Null = 1

		""" on envoie chaque image """
		if resultat_Null == 1:
			for id_carte in resultat_carte:
				await ctx.send(file=discord.File('C:\\Users\\meelo\\Documents\\Dev\\Python\\Cardbot for Discord\\Images\\' + id_carte + ".jpg"))
				""" to send the AE form """
				await ctx.send(file=discord.File('C:\\Users\\meelo\\Documents\\Dev\\Python\\Cardbot for Discord\\Images\\' + id_carte + ".b.jpg"))
		else:
			""" if resultat_Null is 0, we don't have found any card """
			await ctx.send("Pas de carte trouvé dans la base de donnée")

@bot.command()
async def citation(ctx):
	""" send a flavor """
	with open("C:\\Users\\meelo\\Documents\\Dev\\Python\\Cardbot for Discord\\Ressource\\data.json", encoding ="utf8") as json_file:
		data = json.load(json_file)

	loop = 0
	""" loop because some card don't have a flavor. The loop stop when a card with flavor is found """
	while loop != 1:
		place_citation = random.randint(1, len(data))
		if 'flavor' in data[place_citation]:
			citation = data[place_citation]['flavor']
			loop = 1
			await ctx.send(citation)

@bot.command()
async def deck(ctx, arg):
	""" send the deck's content """

	id_deck = arg

	""" get the json from marvelcdb api """
	data = requests.get("https://fr.marvelcdb.com/api/public/decklist/" + id_deck)
	data_deck = data.json()


	""" only keep the slots deck """
	data_deck = data_deck['slots']
	nom_carte = None

	""" creating the resultat variable dict """
	deck = {}

	with open("C:\\Users\\meelo\\Documents\\Dev\\Python\\Cardbot for Discord\\Ressource\\data.json", encoding ="utf8") as json_file:
		ressource = json.load(json_file)

	""" we check for every card code in deck_data, we found the name of this card with data.json and add this to the new dict deck """
	for carte in data_deck:
		for i in ressource:
			if i["code"] == carte:
				nom_carte = i['name']
				deck[nom_carte] = data_deck[carte]

	await ctx.send(deck)

""" for bot token """
bot.run("ODgyNjAxNzM0NzQzMTYyOTMw.YS9w6w.5bIqEvBFp_dtnQVzRcgns_gU9OU")

