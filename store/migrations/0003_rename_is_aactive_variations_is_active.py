# Generated by Django 4.0.4 on 2022-06-23 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_variations'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variations',
            old_name='is_aactive',
            new_name='is_active',
        ),
    ]
