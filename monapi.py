#!/usr/bin/env python
from flask import Flask
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson.code import Code
from bson.objectid import ObjectId
import json

monapi = Flask(__name__)

class Conf:
	mongoHost = 'localhost'
	mongoPort = 27017

class Message:
	m = ""
	def __init__(self,c,msg):
                self.m = '{ "status": "'+c+'", "message": "'+msg+'" }'
	def getMsg(self):
		return self.m

class Response:
	r = ""
	def __init__(self,c,rsp):
		self.r = '{ "status": "'+c+'", "mongoResponse": '+rsp+' }'
	def getRsp(self):
		return self.r

@monapi.route('/')
def index():
	"""Checks local mongodb status"""
	r = Message("N/A", "Unknown")
	try:
		host = MongoClient(Conf.mongoHost,Conf.mongoPort)
		r = Message("OK","MongoDB is running")
		host.close()
	except ConnectionFailure:
		r = Message("Error","No MongoDB instance found.") 
	finally:
		return r.getMsg()

@monapi.route('/<db>')
def getDbInfo(db):
	""" Returns 'db' info """
	host = MongoClient(Conf.mongoHost,Conf.mongoPort)
	r = Response("OK", json.dumps(host.db.command("dbstats")))
	return r.getRsp()

if __name__ == '__main__':
    monapi.run(debug = True,host='0.0.0.0')
