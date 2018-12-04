#Made by the meme factory
#Copyright 2018

#Imports
import requests

#Classes
class Webhook:
	def __init__(self,id,token):
		self.id = id
		self.token = token
		self.url = "https://discordapp.com/api/webhooks/" + id + "/" + token
	def send(self,msg,embed=None):
		if embed != None:
			req = {
				"content": msg,
				"embeds": [
					embed
				]
			}
		else:
			req = {"content": msg}

		res = requests.post(self.url,json=req,headers={"Content-type": "application/json"})