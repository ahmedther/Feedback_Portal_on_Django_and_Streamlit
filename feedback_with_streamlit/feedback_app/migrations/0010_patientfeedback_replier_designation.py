# Generated by Django 4.0.3 on 2022-07-29 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback_app', '0009_patientfeedback_departments_reply_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientfeedback',
            name='replier_designation',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
