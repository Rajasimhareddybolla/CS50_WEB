# Generated by Django 5.0 on 2023-12-18 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raja', '0003_member_prod'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='seller_id',
            field=models.IntegerField(default=1, verbose_name='prodouct id'),
            preserve_default=False,
        ),
    ]
