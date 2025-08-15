from django.shortcuts import render

# Create your views here.
def base(request):
    return render(request, 'base.html')

# Tela da Preposta
def home(request):
    return render(request, 'preposta/home.html')

def list_colaboradores(request):
    return render(request, 'preposta/list_colaboradores.html')

def encarregadas(request):
    return render(request, 'preposta/encarregadas.html')

def colabo_encarregadas(request):
    return render(request, 'preposta/colabo_encarregada.html')

def setores(request):
    return render(request, 'preposta/setores.html')

def todos_setores(request):
    return render(request, 'preposta/todos_setores.html')

def uniformes(request):
    return render(request, 'preposta/uniformes.html')

def todos_uniformes(request):
    return render(request, 'preposta/todos_uniformes.html')

def ferias(request):
    return render(request, 'preposta/ferias.html')

def todas_ferias(request):
    return render(request, 'preposta/todas_ferias.html')


# Tela encarregada

def enc_home(request):
    return render(request, 'encarregada/enc_home.html')

def enc_colaboradores(request):
    return render(request, 'encarregada/enc_colaboradores.html')

def enc_setores(request):
    return render(request, 'encarregada/enc_setores.html')

def enc_uniformes(request):
    return render(request, 'encarregada/enc_uniformes.html')

def enc_ferias(request):
    return render(request, 'encarregada/enc_ferias.html')