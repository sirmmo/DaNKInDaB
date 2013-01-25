from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

import gevent
from gevent.pywsgi import WSGIServer
import inspect
from server.models import *
import importlib
import subprocess

import multiprocessing

from datetime import datetime
import os
import re
import sys
import socket

from django.core.servers.basehttp import run, WSGIServerException, get_internal_wsgi_application
from django.utils import autoreload

import time

import zmq
from random import choice

import xmlrpclib

class Command(BaseCommand):
	help = 'The DaNKInDaB server'

	

	def handle(self, *args, **options):
		context = zmq.Context()
		publisher = context.socket (zmq.PUB)
		publisher.bind ("tcp://*:42712")
		subscriber = context.socket (zmq.SUB)
		subscriber.setsockopt(zmq.SUBSCRIBE, "")
		subscriber.connect ("tcp://127.0.0.1:7721")
	
		self.listeners = []
		#self.handle_daemon(*args, **options)
		for listener in Listener.objects.all():
			s = xmlrpclib.ServerProxy('http://localhost:9091')
			print listener
			listener.pid = rand_port()
			cmd = " ".join([
				sys.executable, 
				'/root/www/DaNKInDaB/scripts/run_dankindab_dispatcher.py', 
				str(listener.ip), 
				str(listener.port), 
				"tcp://localhost:42712",
				"tcp://*:42713",				
			])
			s.twiddler.addProgramToGroup('wsgi', 'test'+str(listener.pid),{'command':cmd})
			
			listener.save()
		

def rand_port ():
	return choice(range(1025,64000))
'''
    def handle_daemon(self, *args, **options):
	ports = range(4000,5000)
        i = 0
	for vh in VirtualHost.objects.all():
	    print vh
	    port = ports[i]
            i = i+1
	    vh.port = port
	    vh.save()
	    cmd_subfolder = vh.base_dir
	    if cmd_subfolder not in sys.path:
                sys.path.insert(0, cmd_subfolder)
            m = importlib.import_module(vh.wsgi)
	    # subprocess.call(['gunicorn', vh.wsgi+":application", "-b 0.0.0.0:"+str(port)])
        for listener in Listener.objects.all():
	    print listener
            self.listeners.append(DWSGIServer(listener))
        for l in self.listeners:
	    print l
            l.serve_forever()
       '''
