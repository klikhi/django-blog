# Generated by Django 3.0.1 on 2020-07-21 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20200718_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likes',
            name='value',
            field=models.CharField(choices=[('Like', 'Like'), ('Unlike', 'Unlike')], default='Like', max_length=10),
        ),
        migrations.AlterField(
            model_name='post',
            name='draft',
            field=models.BooleanField(default=False, null=True),
        ),
    ]