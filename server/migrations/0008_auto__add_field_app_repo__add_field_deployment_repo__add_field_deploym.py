# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'App.repo'
        db.add_column('server_app', 'repo',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Deployment.repo'
        db.add_column('server_deployment', 'repo',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Deployment.repo_type'
        db.add_column('server_deployment', 'repo_type',
                      self.gf('django.db.models.fields.CharField')(default='git', max_length=50),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'App.repo'
        db.delete_column('server_app', 'repo')

        # Deleting field 'Deployment.repo'
        db.delete_column('server_deployment', 'repo')

        # Deleting field 'Deployment.repo_type'
        db.delete_column('server_deployment', 'repo_type')


    models = {
        'server.app': {
            'Meta': {'object_name': 'App'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'repo': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'wsgi': ('django.db.models.fields.TextField', [], {})
        },
        'server.deployment': {
            'Meta': {'object_name': 'Deployment'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.App']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.TextField', [], {}),
            'repo': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'repo_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Server']"})
        },
        'server.listener': {
            'Meta': {'object_name': 'Listener'},
            'certfile': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'default': "'0.0.0.0'", 'max_length': '15'}),
            'keyfile': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pid': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'port': ('django.db.models.fields.IntegerField', [], {}),
            'secure': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'server.server': {
            'Meta': {'object_name': 'Server'},
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'is_main': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'supervisor_password': ('django.db.models.fields.TextField', [], {}),
            'supervisor_port': ('django.db.models.fields.IntegerField', [], {}),
            'supervisor_username': ('django.db.models.fields.TextField', [], {})
        },
        'server.virtualhost': {
            'Meta': {'object_name': 'VirtualHost'},
            'deployment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Deployment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pid': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Listener']"})
        },
        'server.virtualhostname': {
            'Meta': {'object_name': 'VirtualHostName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'virtualhost': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hostnames'", 'to': "orm['server.VirtualHost']"})
        }
    }

    complete_apps = ['server']