# Generated by Django 4.2.2 on 2023-09-10 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tguser',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
