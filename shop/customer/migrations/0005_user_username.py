# Generated by Django 3.2.12 on 2022-04-10 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_auto_20220410_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default=1, max_length=30, unique=True),
            preserve_default=False,
        ),
    ]
