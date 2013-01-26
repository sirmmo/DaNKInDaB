# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Server'
        db.create_table('server_server', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('supervisor_port', self.gf('django.db.models.fields.IntegerField')()),
            ('supervisor_username', self.gf('django.db.models.fields.TextField')()),
            ('supervisor_password', self.gf('django.db.models.fields.TextField')()),
            ('is_main', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('server', ['Server'])

        # Adding model 'App'
        db.create_table('server_app', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('wsgi', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('server', ['App'])

        # Adding model 'Deployment'
        db.create_table('server_deployment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['server.Server'])),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['server.App'])),
            ('path', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('server', ['Deployment'])

        # Deleting field 'VirtualHost.wsgi'
        db.delete_column('server_virtualhost', 'wsgi')

        # Deleting field 'VirtualHost.base_dir'
        db.delete_column('server_virtualhost', 'base_dir')

        # Adding field 'VirtualHost.deployment'
        db.add_column('server_virtualhost', 'deployment',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['server.Deployment']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Server'
        db.delete_table('server_server')

        # Deleting model 'App'
        db.delete_table('server_app')

        # Deleting model 'Deployment'
        db.delete_table('server_deployment')

        # Adding field 'VirtualHost.wsgi'
        db.add_column('server_virtualhost', 'wsgi',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'VirtualHost.base_dir'
        db.add_column('server_virtualhost', 'base_dir',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Deleting field 'VirtualHost.deployment'
        db.delete_column('server_virtualhost', 'deployment_id')


    models = {
        'server.app': {
            'Meta': {'object_name': 'App'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'wsgi': ('django.db.models.fields.TextField', [], {})
        },
        'server.deployment': {
            'Meta': {'object_name': 'Deployment'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.App']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.TextField', [], {}),
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