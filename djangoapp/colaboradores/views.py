from itertools import chain
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404,render, redirect
from django.db.models import Prefetch
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count

# Create your views here.
from colaboradores.models import Funcionario, Setor, Uniforme
# Formulario
from colaboradores.forms import FuncionarioForm, SetorForm, UniformeForm, AsssociarSetoresForm

#Filtrar dados
from colaboradores.filters import FuncionarioFilter

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
    funcionarios = Funcionario.objects.prefetch_related('setores').all().order_by('nome_funcionario')
    funcionario_filter = FuncionarioFilter(request.GET, queryset=funcionarios)

    paginacao = Paginator(funcionario_filter.qs, 12)
    numero_pagina = request.GET.get("page")
    page_obj = paginacao.get_page(numero_pagina)

    context = {

        'funcionarios': page_obj,
        'filter':funcionario_filter
    }
    return render(request, 'encarregada/enc_colaboradores.html',context)


def enc_setores(request):
    funcionarios = Funcionario.objects.prefetch_related('setores').all().order_by('nome_funcionario')
    funcionario_filter = FuncionarioFilter(request.GET, queryset=funcionarios)

    paginacao = Paginator(funcionario_filter.qs, 12)
    numero_pagina = request.GET.get("page")
    page_obj = paginacao.get_page(numero_pagina)

    setores = Setor.objects.all().order_by('nome')
    context = {
        'funcionarios': page_obj,
        'filter':funcionario_filter,
        'setores':setores,
    }
    return render(request, 'encarregada/enc_setores.html',context)


def associar_setor_colaborador(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == "POST":
        form = AsssociarSetoresForm(request.POST)
        if form.is_valid():
            setores_selecionados = form.cleaned_data['setores']
            funcionario.setores.set(setores_selecionados) 
            return redirect('enc_setores')
    else:
        # Preenche com os setores já associados
        form = AsssociarSetoresForm(initial={
            'setores': funcionario.setores.all()
        })    
    context = {
        'funcionario': funcionario,
        'form':form
    }
    return render(request, 'encarregada/setor_colaborador.html',context)
      

def enc_uniformes(request):
    try:
        # Busca todos os funcionários com seus relacionamentos
        setor = Setor.objects.all()
        funcionarios = Funcionario.objects.select_related('uniforme').all().order_by('nome_funcionario')      
        funcionario_filter = FuncionarioFilter(request.GET, queryset=funcionarios)
        '''Chama uniforme e faz a contabilidade'''
        blusa = Uniforme.objects.values('blusa').annotate(total=Count('blusa'))
        blusa_frio = Uniforme.objects.values('blusa_frio').annotate(total=Count('blusa_frio'))
        calca = Uniforme.objects.values('calca').annotate(total=Count('calca'))
        sapato = Uniforme.objects.values('sapato').annotate(total=Count('sapato'))
        galocha = Uniforme.objects.values('galocha').annotate(total=Count('galocha'))
        """Faz a pginação, a cada 12 funcionario registrado e criada uma nova pagina de navegação"""
        paginacao = Paginator(funcionario_filter.qs, 12)
        numero_pagina = request.GET.get("page")
        page_obj = paginacao.get_page(numero_pagina)

        context = {
            'blusa':blusa,
            'blusa_frio':blusa_frio,
            'calca':calca,
            'sapato':sapato,
            'galocha':galocha,
            'funcionarios': page_obj,
            'filter':funcionario_filter,
            'setor':setor,
        }
        return render(request, 'encarregada/enc_uniformes.html', context)
    except Exception as e:
        print(f"Erro na query: {e}")
        # Fallback: dados simples
        funcionarios = Funcionario.objects.all()
        context = {
            'uniformes':uniformes,
            'funcionarios': funcionarios,
            'erro': str(e)
        }
        return render(request, 'encarregada/enc_uniformes.html', context)


def enc_ferias(request):
    ferias = Funcionario.objects.all()
    return render(request, 'encarregada/enc_ferias.html',{'ferias':ferias})


#Formularios
def entrada_funcionario(request):
    if request.method == "POST":
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("enc_colaboradores")
    else:
        form = FuncionarioForm()
    return render(request, "forms/entrada_funcionario.html", {'form':form})    


def registrar_setor(request):
    if request.method == "POST":
        form = SetorForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Setor cadastrado com sucesso")
                return redirect("registrar_setor")
            except IntegrityError:
                messages.error(request, "Erro: Este setor ja existe!")
    else:
        form = SetorForm()
    return render(request, "forms/setor_form.html", {'form':form}) 


def registrar_uniforme(request, pk):  
    funcionario = Funcionario.objects.get(pk=pk)
    # busca o funcionário
    if request.method == "POST":
        form = UniformeForm(request.POST)
        if form.is_valid():
            uniforme = form.save()
            uniforme.funcionario = funcionario # atribui o objeto
            uniforme.save()
            return redirect('enc_uniformes')
    else:
        form = UniformeForm()
    return render(request, "forms/uniforme_form.html", {'forms':form, 'funcionario':funcionario})


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
    setor = get_object_or_404(Setor, pk=pk)
    if request.method == "POST":
        form = SetorForm(request.POST, instance=setor)
        if form.is_valid():
            form.save()
            return redirect('enc_setores')
    else:
        form = SetorForm(instance=setor)
    return render(request, 'edicao/editar_setor.html', {"forms":form, 'setor':setor})


def editar_uniforme(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    uniforme = Uniforme.objects.get(funcionario=funcionario)
    if request.method == "POST":
        form = UniformeForm(request.POST, instance=uniforme)
        if form.is_valid():
            form.save()
            return redirect('enc_uniformes')
    else:
        form = UniformeForm(instance=uniforme)
    return render(request, 'edicao/editar_uniforme.html', {"forms":form, 'funcionario':funcionario, 'uniforme':uniforme})
    

# Excluir um Funcionario 
def excluir_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)   
    if request.method == "POST":
        funcionario.delete()
        messages.success(request,'Funcionario excluido com sucesso')
        return redirect('enc_colaboradores')
    else:
        return render(request, 'edicao/excluir_funcionario.html', {'funcionario':funcionario})
  