# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Listener'
        db.create_table('server_listener', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('port', self.gf('django.db.models.fields.IntegerField')()),
            ('secure', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('server', ['Listener'])

        # Adding model 'VirtualHost'
        db.create_table('server_virtualhost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['server.Listener'])),
            ('base_dir', self.gf('django.db.models.fields.TextField')()),
            ('wsgi', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('server', ['VirtualHost'])

        # Adding model 'VirtualHostName'
        db.create_table('server_virtualhostname', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('virtualhost', self.gf('django.db.models.fields.related.ForeignKey')(related_name='hostnames', to=orm['server.VirtualHost'])),
        ))
        db.send_create_signal('server', ['VirtualHostName'])


    def backwards(self, orm):
        # Deleting model 'Listener'
        db.delete_table('server_listener')

        # Deleting model 'VirtualHost'
        db.delete_table('server_virtualhost')

        # Deleting model 'VirtualHostName'
        db.delete_table('server_virtualhostname')


    models = {
        'server.listener': {
            'Meta': {'object_name': 'Listener'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('django.db.models.fields.IntegerField', [], {}),
            'secure': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'server.virtualhost': {
            'Meta': {'object_name': 'VirtualHost'},
            'base_dir': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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