# Generated by Django 2.2.3 on 2019-09-09 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scale_set', '0035_auto_20190909_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infofields',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='infofields',
            name='publish_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]