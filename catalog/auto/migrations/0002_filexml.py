# Generated by Django 4.2.7 on 2023-11-20 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileXML',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='xml/')),
            ],
        ),
    ]