# Generated by Django 2.0.1 on 2018-03-22 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('display_data_app', '0024_dataentry_subprinciples'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendation',
            name='note',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='recommendation',
            name='principle_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='priority_number',
            field=models.IntegerField(default=0),
        ),
    ]