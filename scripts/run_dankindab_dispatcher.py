#!/usr/bin/env python

from optparse import make_option


import gevent
from gevent.pywsgi import WSGIServer
import inspect

import importlib
import subprocess

import multiprocessing

from datetime import datetime
import os
import re
import sys
import socket
import time
import json
import zmq

def main():
	argv = sys.argv
	print argv 
	l = DWSGIServer(argv[1], argv[2], argv[3], argv[4])
	l.serve_forever()

def connected_dispatcher(zmq_sub, zmq_pub):
	context = zmq.Context()
	subscriber = context.socket (zmq.SUB)
	subscriber.connect(zmq_sub)
	#subscriber.rcvtimeo  = 1000
	publisher = context.socket (zmq.PUB)
	publisher.bind(zmq_pub)
	def dispatcher(environ, setup_response):
		print "got request"
		vh = environ.get('HTTP_HOST')
		e_lite = environ
		del e_lite['wsgi.input']
		del e_lite['wsgi.errors']
		#print zmq_sub, zmq_pub
		
		#print environ			
		print "send request"
		publisher.send("%s %s" % (vh, json.dumps(e_lite)))
		print "get response"		
		subscriber.setsockopt (zmq.SUBSCRIBE, "")
		ret = subscriber.recv()
		#ret = vh 
		setup_response("200 OK", [('Content-Type', 'text/plain')])
		return ret
	return dispatcher
    
    
class DWSGIServer(WSGIServer):
	def __init__(self, ip, port, zmq_sub, zmq_pub):
		super(DWSGIServer, self).__init__(('', int(port)), connected_dispatcher(zmq_sub, zmq_pub))

if __name__ == "__main__":
	main()