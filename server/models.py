from django.db import models

class Listener(models.Model):
	port = models.IntegerField()
	ip = models.CharField(max_length=15, default="0.0.0.0")
	secure = models.BooleanField(default=False)
	keyfile = models.TextField(blank=True, null=True)
	certfile = models.TextField(blank=True, null=True)
	def __str__(self):
		return "*:" + str(self.port)

class VirtualHost(models.Model):
	server = models.ForeignKey(Listener)
	base_dir = models.TextField()
	wsgi = models.TextField()

	def __str__(self):
		return self.base_dir + "::" + self.wsgi


class VirtualHostName(models.Model):
	name = models.TextField()
	virtualhost = models.ForeignKey(VirtualHost, related_name="hostnames")

	def __str__(self):
		return self.name
