# Generated by Django 3.1.2 on 2020-11-03 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_remove_category_catimg'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='website',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
