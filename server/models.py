from django.db import models

class Listener(models.Model):
	port = models.IntegerField()
	ip = models.CharField(max_length=15, default="0.0.0.0")
	secure = models.BooleanField(default=False)
	keyfile = models.TextField(blank=True, null=True)
	certfile = models.TextField(blank=True, null=True)

	pid = models.IntegerField(default=0)

	def __str__(self):
		return str(self.ip) + ":" + str(self.port)

class VirtualHost(models.Model):
	server = models.ForeignKey(Listener)
	deployment = models.ForeignKey('Deployment')
	pid = models.IntegerField(default=0)
	
	def __str__(self):
		return str(self.deployment.server) + ":/"+self.deployment.path + "::" + self.deployment.app.wsgi

class App(models.Model):
	name = models.TextField()
	wsgi = models.TextField()
	repo = models.URLField(null=True, blank=True)
	def __str__(self):
		return self.name


class VirtualHostName(models.Model):
	name = models.TextField()
	virtualhost = models.ForeignKey(VirtualHost, related_name="hostnames")

	def __str__(self):
		return self.name
	
class Server(models.Model):
	hostname = models.CharField(max_length=255)
	ip = models.IPAddressField()
	supervisor_port = models.IntegerField()
	supervisor_username = models.TextField()
	supervisor_password = models.TextField()
	is_main = models.BooleanField(default=False)
	
	def __str__(self):
		return "%s(%s)" % (self.hostname, str(self.ip), )
	
	def get_url(self):
		return "http://%s:%s@%s:%s" % (self.supervisor_username, self.supervisor_password, self.ip, self.supervisor_port)
	
class Deployment (models.Model):
	server = models.ForeignKey(Server)
	app = models.ForeignKey(App)
	path = models.TextField()
	repo = models.URLField(null=True, blank=True)
	repo_type = models.CharField(max_length=50, null=True, blank=True)
	last_update = models.DateTimeField(null=True, blank=True)
	
	def __str__(self):
		return "%s@%s" % (self.app, self.server)