# Generated by Django 5.1.1 on 2024-10-25 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0015_storerequest_id_storerequest_owner_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='address',
            field=models.CharField(default='deafult@gmail.com', max_length=255),
            preserve_default=False,
        ),
    ]
