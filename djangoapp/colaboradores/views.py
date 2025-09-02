from django.shortcuts import get_object_or_404,render, redirect

from django.contrib import messages
# Create your views here.
from colaboradores.models import Funcionario, Setores
# Formulario
from colaboradores.forms import FuncionarioForm, SetorForm



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
    colaboradores = Funcionario.objects.all()
    return render(request, 'encarregada/enc_colaboradores.html', {'colaboradores': colaboradores})


def enc_setores(request):
    setores = Setores.objects.all().order_by('setor')
    return render(request, 'encarregada/enc_setores.html',{'setores':setores})

def enc_uniformes(request):
    return render(request, 'encarregada/enc_uniformes.html')

def enc_ferias(request):

    return render(request, 'encarregada/enc_ferias.html')


#Formularios
def entrada_funcionario(request):
    if request.method == "POST":
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("enc_home")
    else:
        form = FuncionarioForm()
    return render(request, "forms/entrada_funcionario.html", {'form':form})    


def registrar_setor(request):
    if request.method == "POST":
        form = SetorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("enc_home")
    else:
        form = SetorForm()
    return render(request, "forms/setor_form.html", {'form':form}) 




# Editar informaçoes
def editar_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == "POST":
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            return redirect('enc_colaboradores')
    else:
        form = FuncionarioForm(instance=funcionario)

    return render(request, 'edicao/editar_funcionario.html', {"form":form, 'funcionario':funcionario})

def editar_setor(request, pk):
    setor = get_object_or_404(Setores, pk=pk)
    if request.method == "POST":
        form = SetorForm(request.POST, instance=setor)
        if form.is_valid():
            form.save()
            return redirect('enc_setores')
    else:
        form = SetorForm(instance=setor)

    return render(request, 'edicao/editar_setor.html', {"forms":form, 'setor':setor})



# Excluir um Funcionario 
def excluir_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)   
    if request.method == "POST":
        funcionario.delete()
        messages.success(request,'Funcionario excluido com sucesso')
        return redirect('enc_colaboradores')
    else:
        return render(request, 'edicao/excluir_funcionario.html', {'funcionario':funcionario})

  