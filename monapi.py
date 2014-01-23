#!/usr/bin/env python
from flask import Flask
from flask import request
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson.code import Code
from bson.objectid import ObjectId
import json,sys
from flask import jsonify

monapi = Flask(__name__)

class Conf:
	mongoHost = 'localhost'
	mongoPort = 27017

class Message:
	m = ""
	def __init__(self,c,msg):
		self.m = jsonify({ 'status': c, "message": msg })
	def getString(self):
		return self.m

class Response:
	r = ""
	def __init__(self,c,rsp):
		self.r = jsonify({ 'status': c, "message": rsp })
	def getString(self):
		return self.r


# System status
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
		return r.getString()


# Database level
@monapi.route('/<db>')
def getDbInfo(db):
	""" Returns 'db' info """
	host = MongoClient(Conf.mongoHost,Conf.mongoPort)
	if db not in host.database_names():
		r = Message("Error", "Unknown database.")
	else:
		r = Response("OK", json.dumps(host.db.command("dbstats")))
	host.close()
	return r.getString()

@monapi.route('/_dbs')
def listDbs():
	""" List available databases """
	host = MongoClient(Conf.mongoHost,Conf.mongoPort)
	r = Response("OK", json.dumps(host.database_names()))
	host.close()
	return r.getString()

# Collection level
@monapi.route('/<db>/<coll>')
def getCollInfo(db,coll):
	""" Returns 'db.coll' info """
	host = MongoClient(Conf.mongoHost,Conf.mongoPort)
	r = Response("OK", json.dumps(host[db].command({"collstats" : coll})))
	host.close()
	return r.getString()


@monapi.route('/<db>/_colls')
def listColls(db):
	""" Returns 'db' info """
	host = MongoClient(Conf.mongoHost,Conf.mongoPort)	
	r = Response("OK", json.dumps(host[db].collection_names()))
	host.close()
	return r.getString()

# Data retrieval
@monapi.route('/<db>/<coll>/<int:n>')
def getDocByNumber(db,coll,n):
	host = MongoClient(Conf.mongoHost,Conf.mongoPort)
	try:	
		r = Response("OK", json.dumps(str(host[db][coll].find()[n])))
	except IndexError:
		r = Response("Error", "Index out of range: "+str(n)+" >= "+str(host[db][coll].count()))
	host.close()
	return r.getString()

@monapi.route('/<db>/<coll>/_query', methods=['POST'])
def getDocByQuery(db,coll):
	host = MongoClient(Conf.mongoHost,Conf.mongoPort)
	try:	
		query = json.loads(request.data)
		docs = []
		for doc in host[db][coll].find(query):
			docs.append(str(doc).decode('utf8'))
		r = Response("OK",docs)
		#r = Response("OK", json.loads(str(docs)))
	except IndexError:
		r = Response("Error", "Index out of range: "+str(n)+" >= "+str(host[db][coll].count()))
	host.close()
	return r.getString()

# Data storage
@monapi.route('/<db>/<coll>/_insert', methods=['POST'])
def postDoc(db,coll):
	host = MongoClient(Conf.mongoHost,Conf.mongoPort)
	try:
		doc = json.loads(request.data)
		id = host[db][coll].insert(doc)
		r = Message("OK", "Inserted object with ID: "+str(id))
	except ValueError:
		r = Message("Error", "Data must be a valid JSON.")		
	except:
		r = Message("Error", str(sys.exc_info()[0]))
		raise
	host.close()
	return r.getString()

# Map reduce

@monapi.route('/<db>/<coll>/_mr/<output>', methods=['POST'])
def submitMRJob(db,coll,output):
	host = MongoClient(Conf.mongoHost,Conf.mongoPort)
	c = host[db][coll]
	mapper = json.loads(request.data)['mapper']
	reducer = json.loads(request.data)['reducer']
	c.map_reduce(Code(mapper),Code(reducer),output)
	r = Response("OK", "MR job submitted.")
	return r.getString()


# Application start
if __name__ == '__main__':
    monapi.run(debug = True,host='0.0.0.0')
