# Generated by Django 3.2.18 on 2023-05-08 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('criteria', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='criteria',
            options={'ordering': ['created_at']},
        ),
    ]