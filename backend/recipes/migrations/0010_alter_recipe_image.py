# Generated by Django 3.2.3 on 2024-07-19 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_alter_ingredientinrecipe_ingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='recipes/recipe_images/', verbose_name='Изображение'),
        ),
    ]
