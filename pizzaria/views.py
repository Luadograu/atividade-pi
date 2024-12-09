from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import models
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Pizza, Categoria, ItemCarrinho, Carrinho
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class ListaPizzasView(ListView):
    model = Pizza
    template_name = "lista_pizzas.html"
    context_object_name = "pizzas"

    def get_queryset(self):
        return Pizza.objects.select_related("categoria").all()


class CriarPizzaView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
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

    def test_func(self):
        return self.request.user.is_superuser


class AtualizarPizzaView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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

    def test_func(self):
        return self.request.user.is_superuser


class ExcluirPizzaView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Pizza
    template_name = "confirmar_exclusao.html"
    success_url = reverse_lazy("pizzaria:lista_pizzas")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Pizza excluída com sucesso!")
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_superuser


class ListaCategoriasView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Categoria
    template_name = "lista_categorias.html"
    context_object_name = "categorias"

    def test_func(self):
        return self.request.user.is_superuser


class CriarCategoriaView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Categoria
    template_name = "form_categoria.html"
    fields = ["nome", "descricao", "ativa"]
    success_url = reverse_lazy("pizzaria:lista_categorias")

    def form_valid(self, form):
        messages.success(self.request, "Categoria cadastrada com sucesso!")
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser


class AtualizarCategoriaView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Categoria
    template_name = "form_categoria.html"
    fields = ["nome", "descricao", "ativa"]
    success_url = reverse_lazy("pizzaria:lista_categorias")

    def form_valid(self, form):
        messages.success(self.request, "Categoria atualizada com sucesso!")
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser


class ExcluirCategoriaView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
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

    def test_func(self):
        return self.request.user.is_superuser


class CadastrarView(CreateView):
    form_class = UserCreationForm
    template_name = "cadastrar.html"
    success_url = reverse_lazy("pizzaria:lista_pizzas")

    def form_valid(self, form):
        form.save()
        usuario = form.cleaned_data.get("username")
        senha = form.cleaned_data.get("password1")
        usuario = authenticate(username=usuario, password=senha)
        login(self.request, usuario)
        return redirect(self.success_url)


def login_view(request):
    if request.method == "POST":
        usuario = request.POST["username"]
        senha = request.POST["password"]
        usuario = authenticate(request, username=usuario, password=senha)
        if usuario is not None:
            login(request, usuario)
            return redirect("pizzaria:lista_pizzas")
    return render(request, "login.html")


@login_required
def adicionar_ao_carrinho(request, pizza_id):
    try:
        pizza = get_object_or_404(Pizza, id=pizza_id, disponivel=True)
        carrinho, created = Carrinho.objects.get_or_create(
            usuario=request.user, finalizado=False
        )

        item, created = ItemCarrinho.objects.get_or_create(
            carrinho=carrinho, pizza=pizza, defaults={"preco_unitario": pizza.preco}
        )

        if not created:
            item.quantidade += 1
            item.save()

        return JsonResponse(
            {
                "status": "success",
                "mensagem": f"Pizza {pizza.nome} adicionada ao carrinho!",
            }
        )
    except Exception:
        return JsonResponse(
            {
                "status": "error",
                "mensagem": "Erro ao adicionar pizza ao carrinho.",
            },
            status=400,
        )


@login_required
def remover_do_carrinho(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id, carrinho__usuario=request.user)
    item.delete()
    return redirect("pizzaria:ver_carrinho")


@login_required
def atualizar_quantidade(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id, carrinho__usuario=request.user)
    nova_quantidade = int(request.POST.get("quantidade", 1))

    if nova_quantidade > 0:
        item.quantidade = nova_quantidade
        item.save()
    else:
        item.delete()

    return JsonResponse(
        {"subtotal": float(item.subtotal), "total_carrinho": float(item.carrinho.total)}
    )


@login_required
def ver_carrinho(request):
    carrinho, created = Carrinho.objects.get_or_create(
        usuario=request.user, finalizado=False
    )

    if (request.method == 'POST'):
        carrinho.finalizado = True
        carrinho.save()
        return redirect("pizzaria:lista_pizzas")
    return render(request, "carrinho.html", {"carrinho": carrinho})


@login_required
def logout_view(request):
    logout(request)
    return redirect("pizzaria:lista_pizzas")
