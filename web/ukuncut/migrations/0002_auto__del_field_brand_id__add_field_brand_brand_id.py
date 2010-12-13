# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Brand.id'
        db.delete_column('ukuncut_brand', 'id')

        # Adding field 'Brand.brand_id'
        db.add_column('ukuncut_brand', 'brand_id', self.gf('django.db.models.fields.CharField')(default='', max_length=100, primary_key=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Brand.id'
        db.add_column('ukuncut_brand', 'id', self.gf('django.db.models.fields.AutoField')(default=1, primary_key=True), keep_default=False)

        # Deleting field 'Brand.brand_id'
        db.delete_column('ukuncut_brand', 'brand_id')


    models = {
        'ukuncut.brand': {
            'Meta': {'object_name': 'Brand'},
            'brand_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'ukuncut.dodger': {
            'Meta': {'object_name': 'Dodger'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address4': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ukuncut.Brand']", 'null': 'True'}),
            'company': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'doger_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        }
    }

    complete_apps = ['ukuncut']
