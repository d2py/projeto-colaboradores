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

def col_encarregadas(request):
    return render(request, 'tela_preposta/colabo_encarregada.html')

def setores(request):
    return render(request, 'tela_preposta/setores.html')

def todos_setores(request):
    return render(request, 'tela_preposta/todos_setores.html')

def uniformes(request):
    return render(request, 'tela_preposta/uniformes.html')

def todos_uniformes(request):
    return render(request, 'tela_preposta/todos_uniformes.html')

def ferias(request):
    return render(request, 'tela_preposta/ferias.html')

def todas_ferias(request):
    return render(request, 'tela_preposta/todas_ferias.html')