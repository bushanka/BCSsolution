# Generated by Django 3.2.5 on 2022-05-16 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('txApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionsinfo',
            old_name='description',
            new_name='Description',
        ),
        migrations.RenameField(
            model_name='transactionsinfo',
            old_name='txid',
            new_name='Txid',
        ),
    ]
