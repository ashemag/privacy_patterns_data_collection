# Generated by Django 2.0.1 on 2018-03-22 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('display_data_app', '0026_recommendation_subprinciple'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='principle_id',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]