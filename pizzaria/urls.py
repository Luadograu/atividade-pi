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
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("cadastrar/", views.CadastrarView.as_view(), name="cadastrar_usuario"),
    path("carrinho/", views.ver_carrinho, name="ver_carrinho"),
    path(
        "carrinho/adicionar/<int:pizza_id>/",
        views.adicionar_ao_carrinho,
        name="adicionar_ao_carrinho",
    ),
    path(
        "carrinho/remover/<int:item_id>/",
        views.remover_do_carrinho,
        name="remover_do_carrinho",
    ),
    path(
        "carrinho/atualizar/<int:item_id>/",
        views.atualizar_quantidade,
        name="atualizar_quantidade",
    ),
]
