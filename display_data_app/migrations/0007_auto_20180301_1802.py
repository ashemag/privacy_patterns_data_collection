# Generated by Django 2.0.1 on 2018-03-01 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('display_data_app', '0006_remove_dataentry_company_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataentry',
            name='subprinciples',
            field=models.CharField(choices=[('N/A', '1'), ('Privacy Policy', 'Access'), ('Disclosure', 'Disclosure')], max_length=100),
        ),
    ]