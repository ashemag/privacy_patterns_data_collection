# Generated by Django 2.0.1 on 2018-03-01 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('display_data_app', '0004_auto_20180301_1726'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dataentry',
            old_name='data_type',
            new_name='data_usage',
        ),
        migrations.RenameField(
            model_name='dataentry',
            old_name='pos_rec',
            new_name='positive_recommendations',
        ),
        migrations.RenameField(
            model_name='usermodel',
            old_name='data_type',
            new_name='data_usage',
        ),
    ]
