# Generated by Django 4.2.17 on 2024-12-22 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_alter_book_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['category'], 'verbose_name': 'Book', 'verbose_name_plural': 'Books'},
        ),
        migrations.AlterField(
            model_name='book',
            name='distribution_expense',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
