# Generated by Django 4.1.7 on 2023-05-19 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_history', '0002_loginhistory_is_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginhistory',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
