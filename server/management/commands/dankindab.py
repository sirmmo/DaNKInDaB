from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

import gevent
from gevent.pywsgi import WSGIServer
import inspect
from server.models import *
import importlib
import os
import sys
import subprocess


def dispatcher(environ, setup_response):
    print environ
    vh = VirtualHostName.objects.filter(name=environ.get('HTTP_HOST'))
    if len(vh)>0:
        vh = vh[0]
        cmd_subfolder = vh.virtualhost.base_dir
        if cmd_subfolder not in sys.path:
            sys.path.insert(0, cmd_subfolder)
        m = importlib.import_module(vh.virtualhost.wsgi)
        return m.application(environ, setup_response)
    else:
        setup_response('500 ERROR', None)
        return ["ERROR"]
    
    
class DWSGIServer(WSGIServer):
    def __init__(self, listener):
        super(DWSGIServer, self).__init__(('',listener.port), dispatcher)

class Command(BaseCommand):
    help = 'The DaNKInDaB server'

    def handle(self, *args, **options):
        self.listeners = []
        self.handle_daemon(*args, **options)

    def handle_daemon(self, *args, **options):
        for listener in Listener.objects.all():
	    print listener
            self.listeners.append(DWSGIServer(listener))
        for l in self.listeners:
	    print l
            l.serve_forever()
        
