# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'VirtualHost.pid'
        db.add_column('server_virtualhost', 'pid',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'VirtualHost.pid'
        db.delete_column('server_virtualhost', 'pid')


    models = {
        'server.listener': {
            'Meta': {'object_name': 'Listener'},
            'certfile': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'default': "'0.0.0.0'", 'max_length': '15'}),
            'keyfile': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'port': ('django.db.models.fields.IntegerField', [], {}),
            'secure': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'server.virtualhost': {
            'Meta': {'object_name': 'VirtualHost'},
            'base_dir': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pid': ('django.db.models.fields.IntegerField', [], {}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Listener']"}),
            'wsgi': ('django.db.models.fields.TextField', [], {})
        },
        'server.virtualhostname': {
            'Meta': {'object_name': 'VirtualHostName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'virtualhost': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hostnames'", 'to': "orm['server.VirtualHost']"})
        }
    }

    complete_apps = ['server']