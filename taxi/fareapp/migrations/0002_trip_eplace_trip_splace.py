# Generated by Django 5.1.1 on 2024-10-25 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fareapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='eplace',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='splace',
            field=models.CharField(default='Kuttipuram', max_length=100),
            preserve_default=False,
        ),
    ]
