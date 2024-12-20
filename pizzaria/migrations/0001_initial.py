# Generated by Django 4.2.16 on 2024-11-12 21:17

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Categoria",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=50)),
                ("descricao", models.TextField(blank=True)),
                ("ativa", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Categoria",
                "verbose_name_plural": "Categorias",
            },
        ),
        migrations.CreateModel(
            name="Pizza",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=100)),
                ("descricao", models.TextField()),
                (
                    "preco",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=6,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                (
                    "tamanho",
                    models.CharField(
                        choices=[
                            ("P", "Pequena"),
                            ("M", "Média"),
                            ("G", "Grande"),
                            ("F", "Família"),
                        ],
                        max_length=1,
                    ),
                ),
                ("disponivel", models.BooleanField(default=True)),
                ("foto", models.ImageField(blank=True, null=True, upload_to="pizzas/")),
                ("data_cadastro", models.DateTimeField(auto_now_add=True)),
                ("data_atualizacao", models.DateTimeField(auto_now=True)),
                (
                    "categoria",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="pizzas",
                        to="pizzaria.categoria",
                    ),
                ),
            ],
            options={
                "verbose_name": "Pizza",
                "verbose_name_plural": "Pizzas",
                "ordering": ["nome", "tamanho"],
            },
        ),
    ]
