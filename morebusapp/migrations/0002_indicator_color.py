# Generated by Django 3.2.15 on 2022-11-22 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('morebusapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='color',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]