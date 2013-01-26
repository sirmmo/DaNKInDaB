from django.contrib.admin import site
from server.models import *

site.register(Listener)
site.register(VirtualHost)
site.register(VirtualHostName)
site.register(App)
site.register(Server)
site.register(Deployment)
