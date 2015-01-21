# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

PROFESSIONAL_CATEGORIES = {'a': ('colaborador-nao-remunerado-docente', 'Colaborador Não Remunerado Docente'),
                   'b':  ('equipmonitor-clic', 'Equip.Monitor C/Lic'),
                   'c': ('equipprofassociado-convidado', 'Equip.Prof.Associado Convidado'),
                   'd': ('equip-assistente-convidado', 'Equip. Assistente Convidado'),
                   'e': ('equiparado-professor-catedratico', 'Equiparado Professor Catedrático'),
                   'f': ('equiparado-professor-extraordinario', 'Equiparado Professor Extraordinário'),
                   'g': ('equiparado-assistente-eventual', 'Equiparado Assistente Eventual'),
                   'h': ('segundo-assistente', 'Segundo Assistente'),
                   'i': ('equiparado-assistente', 'Equiparado Assistente'),
                   'j': ('professor-associado-visitante', 'Professor Associado Visitante'),
                   'k': ('professor-catedratico-visitante', 'Professor Catedrático Visitante'),
                   'l': ('assistente-eventual', 'Assistente Eventual'),
                   'm': ('equiparado-professor-auxiliar', 'Equiparado Professor Auxiliar'),
                   'n': ('monitor-ecdu-clicenciatura', 'Monitor-E.C.D.U. c/Licenciatura'),
                   'o': ('equipmonitor-slic', 'Equip.Monitor S/Lic'),
                   'p': ('equipassistente-estagiario', 'Equip.Assistente Estagiario'),
                   'q': ('equip-assistente', 'Equip. Assistente'),
                   'r': ('equipprofauxiliar-convidado', 'Equip.Prof.Auxiliar Convidado'),
                   's': ('equip-prof-auxiliar', 'Equip. Prof. Auxiliar'),
                   't': ('monitor-ecduslicenciatura', 'Monitor-E.C.D.U.s/Licenciatura'),
                   'u': ('assistente-estagiario', 'Assistente Estagiario'),
                   'v': ('assistente-convidado', 'Assistente Convidado'),
                   'w': ('assistente', 'Assistente'),
                   'x': ('prof-auxiliar-convidado', 'Prof Auxiliar Convidado'),
                   'y': ('professor-auxiliar', 'Professor Auxiliar'),
                   'z': ('prof-auxiliar-cagregacao', 'Prof Auxiliar C/Agregação'),
                   'A': ('professor-associado-convidado', 'Professor Associado Convidado'),
                   'B': ('professor-associado', 'Professor Associado'),
                   'C': ('professor-associado-cagregacao', 'Professor Associado c/Agregação'),
                   'D': ('professor-catedratico-convidado', 'Professor Catedrático Convidado'),
                   'E': ('professor-catedratico', 'Professor Catedrático')}

class Migration(DataMigration):

    def forwards(self, orm):
        # Create initial professional categories
        for key, value in PROFESSIONAL_CATEGORIES.iteritems():
            slug, name = value
            category = orm.ProfessionalCategory.objects.create(slug=slug, name=name)
            category.save()

        # Change professional category from string
        teachers = orm.ExternalTeacher.objects.all()
        for teacher in teachers:
            if PROFESSIONAL_CATEGORIES.has_key(teacher.professional_category_str):
                slug, name = PROFESSIONAL_CATEGORIES[teacher.professional_category_str]
                pro_category = orm.ProfessionalCategory.objects.get(slug=slug)
                teacher.professional_category = pro_category
                teacher.save()
    
    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'app.externalteacher': {
            'Meta': {'unique_together': "(('semester', 'ist_id'),)", 'object_name': 'ExternalTeacher'},
            'card': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'close_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'closed_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'costs_center': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
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
            'professional_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.ProfessionalCategory']", 'null': 'True'}),
            'professional_category_str': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['app.Semester']"})
        },
        u'app.professionalcategory': {
            'Meta': {'object_name': 'ProfessionalCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'app.profile': {
            'Meta': {'object_name': 'Profile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'app.semester': {
            'Meta': {'object_name': 'Semester'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'year_final': ('django.db.models.fields.IntegerField', [], {}),
            'year_initial': ('django.db.models.fields.IntegerField', [], {})
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
    symmetrical = True
