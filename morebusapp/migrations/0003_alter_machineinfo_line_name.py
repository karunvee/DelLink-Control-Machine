# Generated by Django 3.2.15 on 2022-12-09 01:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('morebusapp', '0002_auto_20221208_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machineinfo',
            name='line_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='morebusapp.lineinfo'),
        ),
    ]