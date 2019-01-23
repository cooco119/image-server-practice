# Generated by Django 2.1.4 on 2019-01-03 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0002_auto_20181226_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='processed',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='is_private',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='pub_date',
            field=models.DateTimeField(null=True),
        ),
    ]
