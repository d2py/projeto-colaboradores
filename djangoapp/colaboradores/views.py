from django.shortcuts import render

# Create your views here.
def base(request):
    return render(request, 'base.html')

# Telas da Preposta
def home(request):
    return render(request, 'tela_preposta/home.html')

def list_colaboradores(request):
    return render(request, 'tela_preposta/list_colaboradores.html')

def encarregadas(request):
    return render(request, 'tela_preposta/encarregadas.html')

def setores(request):
    return render(request, 'tela_preposta/setores.html')

def uniformes(request):
    return render(request, 'tela_preposta/uniformes.html')