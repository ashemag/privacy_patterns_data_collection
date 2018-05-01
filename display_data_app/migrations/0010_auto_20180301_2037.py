# Generated by Django 2.0.1 on 2018-03-01 20:37

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('display_data_app', '0009_auto_20180301_2033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataentry',
            name='subprinciples',
        ),
        migrations.AddField(
            model_name='dataentry',
            name='subprinciples',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('1', '1'), ('1.1.0', '1.1.0, Privacy Policy'), ('1.1.1', '1.1.1, Communication to Internal Personnel'), ('1.1.2', '1.1.2, Responsibility and Accountability for Policies'), ('1.2.1', '1.2.1, Review and Approval'), ('1.2.2', '1.2.2, Consistency of Privacy Policies and Procedures With Laws and Regulations'), ('1.2.3', '1.2.3, PI/PII Identification and Classification'), ('1.2.4', '1.2.4, Risk Assessment'), ('1.2.5', '1.2.5, Consistency of Commitments With Privacy Policies and Procedures'), ('1.2.6', '1.2.6, Infrastructure and Systems Management')], help_text="<div style='float:right;font-size:12px;color:red'> HELP TEXT DISPLAYED HERE</div>", max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='SubprincipleOptions',
        ),
    ]