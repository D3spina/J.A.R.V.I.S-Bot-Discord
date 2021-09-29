import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import json
import random
import yaml
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="config")

bot = commands.Bot(command_prefix='!', case_insensitive=True)

@bot.event
async def on_ready():
	""" check if bot is connected """
	print("Le robot est connecté comme {0.user}".format(bot))
	
	embed_connexion = discord.Embed(title = "J.A.R.V.I.S", description = "Votre base de donnée Marvel Champions", color = discord.Color.blue())
	embed_connexion.add_field(name = "Just A Rather Very Intelligent System", value = "Veuillez taper '&helpme' pour plus d'informations")

	""" this message on comment for don't spam the channel with test """
	await bot.get_guild(865522776876908546).get_channel(882711486844256256).send(embed=embed_connexion)


@bot.command(name="helpme")
async def helpme(ctx):
	""" send all the bot commands """
	embed_help = discord.Embed(title = "Liste des commandes", description = "Voici la liste des commandes disponibles pour J.A.R.V.I.S", color = discord.Color.blue())
	embed_help.add_field(name = "Bienvenue sur l'aide", value = "Toutes les commandes commencent par le préfixe '&'.", inline = False)
	embed_help.add_field(name = "Definition", value = "Obtenir la définition d'un mot clé (anglais uniquement pour le moment). Commande : &Definition mot_clé ; La commande '&definition liste' affiche la liste des mots clés disponibles.")
	embed_help.add_field(name = "Randomizer", value = "Afficher le lien du randomizer de notre ami Halion. Commande : &Randomizer ")
	embed_help.add_field(name = "Citation", value = "Obtenir une citation aléatoire d'une carte du jeu. Commande : &Citation ")
	embed_help.add_field(name = "Carte", value = "Obtenir l'image de la carte recherchée en français. La recherche peut se faire avec le nom FR ou EN. Commande : &Carte nom_de_la_carte ")
	embed_help.add_field(name = "Deck", value = "Obtenir la liste des cartes d'un deck !public! de marvelcdb. Commande : &Deck numero_id ")
	embed_help.add_field(name = "Contact", value = "Vous pouvez MP D3spina#8586 pour toutes questions", inline = False)
	
	await ctx.send(embed=embed_help)

@bot.command(name="definition")
async def definition(ctx, arg):
	""" get key world definition """

	""" get the html page from hallofheroes """
	url_definition = "https://hallofheroeslcg.com/marvel-champions-lcg-keyword-list/"
	page_definition = requests.get(url_definition)
	soup_definition = BeautifulSoup(page_definition.content, 'html5lib')
	if arg == "liste":
		liste_definition_h3 = soup_definition.find_all('h3')
		liste_definition = []
		for mot in liste_definition_h3:
			liste_definition.append(mot.string)

		del liste_definition[-1]

		embed_liste=discord.Embed(name = "Liste des mots clés", color = discord.Color.blue())
		embed_liste.add_field(name = "Liste des mots clés disponible :", value = liste_definition)
		await ctx.send(embed=embed_liste)
	else:
		""" definition if the next p before h3 text """
		definitions = soup_definition.find(text = arg).findNext("p").contents

		embed_definitions = discord.Embed(name = "Définition", color = discord.Color.blue())
		embed_definitions.add_field(name = arg, value = definitions)

		await ctx.send(embed=embed_definitions)

@bot.command(name="randomizer")
async def randomizer(ctx):
	""" get the Halion's randomizer link """
	embed_randomizer = discord.Embed(name = "Randomizer de Halion", color = discord.Color.blue())
	embed_randomizer.add_field (name = "Randomizer", value = "Vous pouvez randomizer une partie ici : https://canthom.github.io/randomizer-mc/")

	await ctx.send (embed=embed_randomizer)

@bot.command(name="carte")
async def carte(ctx, *arg):
	""" post the image of card """

	""" get the *arg in string and lower ; creating list for result and resultat_Null to send message if = 1 """
	recherche = ' '.join(arg)
	recherche = str(recherche.lower())
	resultat_carte = []
	resultat_Null = 0
	identite = 0
	img = []
	url_image = "C:\\Users\\meelo\\Documents\\Dev\\Python\\Cardbot for Discord\\Images\\"
	place = 0
	img_weight = 0

	""" size in pixel of Marvel champions cards = 394 * 560 """

	""" we break the null search """
	if len(arg) == 0:
		embed_no_carte = discord.Embed(name = "no result", color = discord.Color.blue())
		embed_no_carte.add_field(name = "Erreur", value = "Tu n'as pas précisé de carte à rechercher")

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
				if i['type_code'] == "hero":
					identite = 1
					img_weight = 1

		if len(resultat_carte) == 0:
			embed_no_carte = discord.Embed(name = "no result", color = discord.Color.blue())
			embed_no_carte.add_field(name = "Erreur", value = "Aucune carte n'a été trouvée")

			await ctx.send(embed = embed_no_carte)

		else:

			""" define the size of the result with the number of card found """
			img_weight = (img_weight + len(resultat_carte)) * 394
			img_height = 560

			""" add every patch in the list img """
			for i in resultat_carte:
				img.append(url_image + i + ".jpg")
				""" add the AE image in the list """
				if identite == 1:
					img.append(url_image + i + ".b.jpg")

			""" creating the new img who will be send """
			new_img = Image.new('RGB', (img_weight, img_height), (250,250,250))

			""" we paste every image in the new_img """
			for i in img:
				image = Image.open(i)
				largeur = 0+(place*394)
				new_img.paste(image, (largeur, 0))
				place += 1

			""" saving the result in a png """
			new_img.save("requête.png", "PNG")

			""" beautiful embed """
			embed_carte = discord.Embed(name = recherche, color = discord.Color.blue())
			file = discord.File("requête.png", filename = "image.png")
			embed_carte.set_image(url ="attachment://image.png")

			await ctx.send(file=file,embed=embed_carte)

@bot.command(name="citation")
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
			embed_citations = discord.Embed(name ="Citations")
			embed_citations.add_field(name = "Citation", value = citation)
			await ctx.send(embed=embed_citations)

@bot.command(name="deck")
async def deck(ctx, arg):
	""" send the deck's content """

	id_deck = arg

	""" get the json from marvelcdb api """
	data = requests.get("https://fr.marvelcdb.com/api/public/decklist/" + id_deck)
	data = data.json()

	thumbnail_url_code = None

	""" only keep the slots deck, heroes name and meta """
	data_deck = data['slots']

	heros = data["investigator_name"]
	
	affinite = data['meta']
	if 'leadership' in affinite:
		affinite = 'Leadership'
	elif 'justice' in affinite:
		affinite = 'Justice'
	elif 'aggression' in affinite:
		affinite = 'Aggression'
	else:
		affinite = 'Protection'

	nom_carte = None

	""" creating the resultat variable dict """
	deck = {}

	with open("C:\\Users\\meelo\\Documents\\Dev\\Python\\Cardbot for Discord\\Ressource\\data.json", encoding ="utf8") as json_file:
		ressource = json.load(json_file)

	""" get the heros img for the embed thumbnail """
	for i in ressource:
		if i['name'] == heros.lower() or i['real_name'] == heros.lower():
			if i['type_code'] == "hero":
				thumbnail_url_code = i['code']
				thumbnail_url_code = str(thumbnail_url_code)
	

	""" we check for every card code in deck_data, we found the name of this card with data.json and add this to the new dict deck """
	for carte in data_deck:
		for i in ressource:
			if i["code"] == carte:
				nom_carte = i['name']
				deck[nom_carte] = data_deck[carte]

	deck_forme = yaml.dump(deck, sort_keys=False, default_flow_style=False, allow_unicode=True)

	embed_deck = discord.Embed(title = "Deck", color = discord.Color.blue())
	embed_deck.add_field(name = "Héros : ", value = heros, inline = False)
	embed_deck.add_field(name = "Affinité :", value = affinite, inline = False)
	embed_deck.add_field(name = "Liste des cartes : ", value = deck_forme)
	embed_deck.set_thumbnail(url="https://fr.marvelcdb.com/bundles/cards/" + thumbnail_url_code + ".png")

	await ctx.send(embed = embed_deck)

""" for bot token """
bot.run(os.getenv("TOKEN"))

