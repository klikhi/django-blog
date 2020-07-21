# Generated by Django 3.0.1 on 2020-07-15 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20200715_0131'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='comment',
            constraint=models.UniqueConstraint(fields=('author', 'post'), name='unique_comment'),
        ),
    ]