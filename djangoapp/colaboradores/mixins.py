"""
mixins.py — Mixins de autenticação e autorização do sistema.
 
Como usar nas views:
    class MinhaView(PrepostaRequiredMixin, View): ...
    class MinhaView(EncarregadaRequiredMixin, View): ...
    class MinhaView(LoginRequiredMixin, View): ...   # qualquer usuário logado
"""

from functools import wraps
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages


class PrepostaRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/login/'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_preposta

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('/login/')
        messages.error(self.request, 'Acesso restrito à preposta.')
        return redirect('home')


class EncarregadaRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/login/'

    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.is_encarregada or self.request.user.is_preposta
        )

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('/login/')
        messages.error(self.request, 'Você não tem permissão para acessar esta página.')
        return redirect('/login/')


# ── Decorators para function-based views ─────────────────────────────────────

def preposta_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/')
        if not request.user.is_preposta:
            messages.error(request, 'Acesso restrito à preposta.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def encarregada_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/')
        if not (request.user.is_encarregada or request.user.is_preposta):
            messages.error(request, 'Você não tem permissão.')
            return redirect('/login/')
        return view_func(request, *args, **kwargs)
    return wrapper