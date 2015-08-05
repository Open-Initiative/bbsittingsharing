# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BBSitting'
        db.create_table(u'bbsittingsharing_bbsitting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('start', self.gf('django.db.models.fields.TimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
            ('bbsitter_found', self.gf('django.db.models.fields.BooleanField')()),
            ('at_authors', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('authors_children', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('children_capacity', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbsittingsharing.Parent'])),
        ))
        db.send_create_signal(u'bbsittingsharing', ['BBSitting'])

        # Adding model 'Equipment'
        db.create_table(u'bbsittingsharing_equipment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('default', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'bbsittingsharing', ['Equipment'])

        # Adding model 'District'
        db.create_table(u'bbsittingsharing_district', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
        ))
        db.send_create_signal(u'bbsittingsharing', ['District'])

        # Adding model 'School'
        db.create_table(u'bbsittingsharing_school', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
        ))
        db.send_create_signal(u'bbsittingsharing', ['School'])

        # Adding model 'Parent'
        db.create_table(u'bbsittingsharing_parent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('kidsnb', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('bbsitter', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('ok_at_home', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('ok_at_others', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('female', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('referer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='referees', null=True, to=orm['bbsittingsharing.Parent'])),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(related_name='users', null=True, to=orm['bbsittingsharing.District'])),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(related_name='users', null=True, to=orm['bbsittingsharing.School'])),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'bbsittingsharing', ['Parent'])

        # Adding M2M table for field groups on 'Parent'
        m2m_table_name = db.shorten_name(u'bbsittingsharing_parent_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('parent', models.ForeignKey(orm[u'bbsittingsharing.parent'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['parent_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'Parent'
        m2m_table_name = db.shorten_name(u'bbsittingsharing_parent_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('parent', models.ForeignKey(orm[u'bbsittingsharing.parent'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['parent_id', 'permission_id'])

        # Adding M2M table for field friends on 'Parent'
        m2m_table_name = db.shorten_name(u'bbsittingsharing_parent_friends')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_parent', models.ForeignKey(orm[u'bbsittingsharing.parent'], null=False)),
            ('to_parent', models.ForeignKey(orm[u'bbsittingsharing.parent'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_parent_id', 'to_parent_id'])

        # Adding M2M table for field equipment on 'Parent'
        m2m_table_name = db.shorten_name(u'bbsittingsharing_parent_equipment')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('parent', models.ForeignKey(orm[u'bbsittingsharing.parent'], null=False)),
            ('equipment', models.ForeignKey(orm[u'bbsittingsharing.equipment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['parent_id', 'equipment_id'])

        # Adding model 'Booking'
        db.create_table(u'bbsittingsharing_booking', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbsittingsharing.Parent'])),
            ('bbsitting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbsittingsharing.BBSitting'])),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'bbsittingsharing', ['Booking'])

        # Adding unique constraint on 'Booking', fields ['parent', 'bbsitting']
        db.create_unique(u'bbsittingsharing_booking', ['parent_id', 'bbsitting_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Booking', fields ['parent', 'bbsitting']
        db.delete_unique(u'bbsittingsharing_booking', ['parent_id', 'bbsitting_id'])

        # Deleting model 'BBSitting'
        db.delete_table(u'bbsittingsharing_bbsitting')

        # Deleting model 'Equipment'
        db.delete_table(u'bbsittingsharing_equipment')

        # Deleting model 'District'
        db.delete_table(u'bbsittingsharing_district')

        # Deleting model 'School'
        db.delete_table(u'bbsittingsharing_school')

        # Deleting model 'Parent'
        db.delete_table(u'bbsittingsharing_parent')

        # Removing M2M table for field groups on 'Parent'
        db.delete_table(db.shorten_name(u'bbsittingsharing_parent_groups'))

        # Removing M2M table for field user_permissions on 'Parent'
        db.delete_table(db.shorten_name(u'bbsittingsharing_parent_user_permissions'))

        # Removing M2M table for field friends on 'Parent'
        db.delete_table(db.shorten_name(u'bbsittingsharing_parent_friends'))

        # Removing M2M table for field equipment on 'Parent'
        db.delete_table(db.shorten_name(u'bbsittingsharing_parent_equipment'))

        # Deleting model 'Booking'
        db.delete_table(u'bbsittingsharing_booking')


    models = {
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
        u'bbsittingsharing.bbsitting': {
            'Meta': {'object_name': 'BBSitting'},
            'at_authors': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbsittingsharing.Parent']"}),
            'authors_children': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'bbsitter_found': ('django.db.models.fields.BooleanField', [], {}),
            'booked': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'booked'", 'symmetrical': 'False', 'through': u"orm['bbsittingsharing.Booking']", 'to': u"orm['bbsittingsharing.Parent']"}),
            'children_capacity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.TimeField', [], {})
        },
        u'bbsittingsharing.booking': {
            'Meta': {'unique_together': "(('parent', 'bbsitting'),)", 'object_name': 'Booking'},
            'bbsitting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbsittingsharing.BBSitting']"}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbsittingsharing.Parent']"})
        },
        u'bbsittingsharing.district': {
            'Meta': {'object_name': 'District'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'bbsittingsharing.equipment': {
            'Meta': {'object_name': 'Equipment'},
            'default': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'bbsittingsharing.parent': {
            'Meta': {'object_name': 'Parent'},
            'bbsitter': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'users'", 'null': 'True', 'to': u"orm['bbsittingsharing.District']"}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'blank': 'True'}),
            'equipment': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['bbsittingsharing.Equipment']", 'symmetrical': 'False', 'blank': 'True'}),
            'female': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'friends_rel_+'", 'null': 'True', 'to': u"orm['bbsittingsharing.Parent']"}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'kidsnb': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'ok_at_home': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'ok_at_others': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'referer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'referees'", 'null': 'True', 'to': u"orm['bbsittingsharing.Parent']"}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'users'", 'null': 'True', 'to': u"orm['bbsittingsharing.School']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'bbsittingsharing.school': {
            'Meta': {'object_name': 'School'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bbsittingsharing']