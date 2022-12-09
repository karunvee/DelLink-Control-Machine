# Generated by Django 3.2.15 on 2022-12-08 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('morebusapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machineinfo',
            name='lineID',
        ),
        migrations.AlterField(
            model_name='machineinfo',
            name='line_name',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='morebusapp.lineinfo'),
        ),
    ]