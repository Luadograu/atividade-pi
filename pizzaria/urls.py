from django.urls import path
from . import views

app_name = "pizzaria"

urlpatterns = [
    path("", views.ListaPizzasView.as_view(), name="lista_pizzas"),
    path("nova/", views.CriarPizzaView.as_view(), name="criar_pizza"),
    path(
        "editar/<int:pk>/", views.AtualizarPizzaView.as_view(), name="atualizar_pizza"
    ),
    path("excluir/<int:pk>/", views.ExcluirPizzaView.as_view(), name="excluir_pizza"),
    path("categorias/", views.ListaCategoriasView.as_view(), name="lista_categorias"),
    path(
        "categorias/nova/", views.CriarCategoriaView.as_view(), name="criar_categoria"
    ),
    path(
        "categorias/editar/<int:pk>/",
        views.AtualizarCategoriaView.as_view(),
        name="atualizar_categoria",
    ),
    path(
        "categorias/excluir/<int:pk>/",
        views.ExcluirCategoriaView.as_view(),
        name="excluir_categoria",
    ),
]
