from django.db import models

class Listener(models.Model):
	port = models.IntegerField()
	secure = models.Booleanfield()
	def __str__(self):
		return "*:"+str(self.port)

class VirtualHost(models.Model):
	server = models.ForeignKey(Listener)
	base_dir=models.TextField()
	wsgi = models.TextField()

	def __str__(self):
		return self.base_dir + "::" + self.wsgi


class VirtualHostName(models.Model):
	name=models.TextField()
	virtualhost = models.ForeignKey(VirtualHost, related_name="hostnames")


