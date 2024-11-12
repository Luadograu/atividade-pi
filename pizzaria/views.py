from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.db import models
from .models import Pizza, Categoria


class ListaPizzasView(ListView):
    model = Pizza
    template_name = "lista_pizzas.html"
    context_object_name = "pizzas"

    def get_queryset(self):
        return Pizza.objects.select_related("categoria").all()


class CriarPizzaView(CreateView):
    model = Pizza
    template_name = "form_pizza.html"
    fields = [
        "nome",
        "descricao",
        "preco",
        "categoria",
        "tamanho",
        "disponivel",
        "foto",
    ]
    success_url = reverse_lazy("pizzaria:lista_pizzas")

    def form_valid(self, form):
        messages.success(self.request, "Pizza cadastrada com sucesso!")
        return super().form_valid(form)


class AtualizarPizzaView(UpdateView):
    model = Pizza
    template_name = "form_pizza.html"
    fields = [
        "nome",
        "descricao",
        "preco",
        "categoria",
        "tamanho",
        "disponivel",
        "foto",
    ]
    success_url = reverse_lazy("pizzaria:lista_pizzas")

    def form_valid(self, form):
        messages.success(self.request, "Pizza atualizada com sucesso!")
        return super().form_valid(form)


class ExcluirPizzaView(DeleteView):
    model = Pizza
    template_name = "confirmar_exclusao.html"
    success_url = reverse_lazy("pizzaria:lista_pizzas")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Pizza excluída com sucesso!")
        return super().delete(request, *args, **kwargs)


class ListaCategoriasView(ListView):
    model = Categoria
    template_name = "lista_categorias.html"
    context_object_name = "categorias"


class CriarCategoriaView(CreateView):
    model = Categoria
    template_name = "form_categoria.html"
    fields = ["nome", "descricao", "ativa"]
    success_url = reverse_lazy("pizzaria:lista_categorias")

    def form_valid(self, form):
        messages.success(self.request, "Categoria cadastrada com sucesso!")
        return super().form_valid(form)


class AtualizarCategoriaView(UpdateView):
    model = Categoria
    template_name = "form_categoria.html"
    fields = ["nome", "descricao", "ativa"]
    success_url = reverse_lazy("pizzaria:lista_categorias")

    def form_valid(self, form):
        messages.success(self.request, "Categoria atualizada com sucesso!")
        return super().form_valid(form)


class ExcluirCategoriaView(DeleteView):
    model = Categoria
    template_name = "confirmar_exclusao_categoria.html"
    success_url = reverse_lazy("pizzaria:lista_categorias")

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except models.ProtectedError:
            messages.error(
                request,
                "Não é possível excluir esta categoria pois existem pizzas vinculadas a ela.",
            )
            return redirect("pizzaria:lista_categorias")
