from django.db import models
from django.core.validators import MinValueValidator


class Categoria(models.Model):
    nome = models.CharField(
        "Nome", max_length=50, help_text="Nome da categoria de pizza"
    )
    descricao = models.TextField(
        "Descrição", blank=True, help_text="Descrição detalhada da categoria"
    )
    ativa = models.BooleanField(
        "Ativa", default=True, help_text="Indica se esta categoria está ativa para uso"
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


class Pizza(models.Model):
    TAMANHOS = [
        ("P", "Pequena"),
        ("M", "Média"),
        ("G", "Grande"),
        ("F", "Família"),
    ]

    nome = models.CharField("Nome", max_length=100, help_text="Nome da pizza")
    descricao = models.TextField(
        "Descrição", help_text="Descrição detalhada da pizza com ingredientes"
    )
    preco = models.DecimalField(
        "Preço",
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        help_text="Preço da pizza em reais",
    )
    categoria = models.ForeignKey(
        Categoria,
        verbose_name="Categoria",
        on_delete=models.PROTECT,
        related_name="pizzas",
        help_text="Categoria à qual esta pizza pertence",
    )
    tamanho = models.CharField(
        "Tamanho", max_length=1, choices=TAMANHOS, help_text="Tamanho da pizza"
    )
    disponivel = models.BooleanField(
        "Disponível",
        default=True,
        help_text="Indica se esta pizza está disponível para venda",
    )
    foto = models.ImageField(
        "Foto", upload_to="pizzas/", null=True, blank=True, help_text="Foto da pizza"
    )
    data_cadastro = models.DateTimeField(
        "Data de Cadastro", auto_now_add=True, help_text="Data de criação do registro"
    )
    data_atualizacao = models.DateTimeField(
        "Data de Atualização", auto_now=True, help_text="Data da última atualização"
    )

    def __str__(self):
        return f"{self.nome} - {self.get_tamanho_display()}"

    class Meta:
        verbose_name = "Pizza"
        verbose_name_plural = "Pizzas"
        ordering = ["nome", "tamanho"]
