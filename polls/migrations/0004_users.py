# Generated by Django 4.2.1 on 2023-05-18 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_delete_customuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
            ],
        ),
    ]
