# Generated by Django 4.2.17 on 2024-12-22 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_book_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]