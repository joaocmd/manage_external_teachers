# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profile'
        db.create_table(u'app_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'app', ['Profile'])

        # Adding model 'ExternalTeacher'
        db.create_table(u'app_externalteacher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ist_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('is_closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('close_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('professional_category', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('hours_per_week', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('park', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('card', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('degree', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('course', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('course_manager', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'app', ['ExternalTeacher'])

        # Adding model 'FenixAPIUserInfo'
        db.create_table(u'app_fenixapiuserinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('access_token', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('refresh_token', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('token_expires', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'app', ['FenixAPIUserInfo'])


    def backwards(self, orm):
        # Deleting model 'Profile'
        db.delete_table(u'app_profile')

        # Deleting model 'ExternalTeacher'
        db.delete_table(u'app_externalteacher')

        # Deleting model 'FenixAPIUserInfo'
        db.delete_table(u'app_fenixapiuserinfo')


    models = {
        u'app.externalteacher': {
            'Meta': {'object_name': 'ExternalTeacher'},
            'card': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'close_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'course': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'course_manager': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'degree': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'hours_per_week': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ist_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'park': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'professional_category': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'app.fenixapiuserinfo': {
            'Meta': {'object_name': 'FenixAPIUserInfo'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'refresh_token': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'token_expires': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'app.profile': {
            'Meta': {'object_name': 'Profile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['app']