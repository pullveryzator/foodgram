# Generated by Django 3.2.3 on 2024-06-16 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_rename_ingredient_ingredientinrecipe_ingredients'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredientinrecipe',
            old_name='ingredients',
            new_name='ingredient',
        ),
        migrations.RemoveField(
            model_name='ingredientinrecipe',
            name='recipes',
        ),
        migrations.AddField(
            model_name='ingredientinrecipe',
            name='recipe',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт'),
            preserve_default=False,
        ),
    ]
