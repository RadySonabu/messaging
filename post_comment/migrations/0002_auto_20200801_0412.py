# Generated by Django 3.0.8 on 2020-07-31 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post_comment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='parent',
            new_name='threadId',
        ),
    ]