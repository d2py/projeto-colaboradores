from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from colaboradores.models import CustomUser, Funcionario, Setor, Uniforme
from colaboradores.forms import (
    LoginForm,
    CriarEncarregadaForm,
    EditarEncarregadaForm,
    AssociarFuncionariosEncarregadaForm,
    AssociarSetoresEncarregadaForm,
    FuncionarioFormPreposta,
    FuncionarioForm,
    SetorForm,
    UniformeForm,
    AsssociarSetoresForm,
)
from colaboradores.filters import FuncionarioFilter
from colaboradores.mixins import preposta_required, encarregada_required


# ─────────────────────────────────────────────
#  AUTENTICAÇÃO
# ─────────────────────────────────────────────

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_preposta:
                return redirect('/home/')
            return redirect('/home/')    
        messages.error(request, 'Usuário ou senha incorretos.')
    else:
        form = LoginForm(request)

    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    from django.contrib.messages import get_messages
    storage = get_messages(request)
    for _ in storage:
        pass  # limpa todas as mensagens pendentes
    logout(request)
    return redirect("/login/")


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def _qs_funcionarios(request):
    qs = Funcionario.objects.prefetch_related('setores').order_by('nome_funcionario')
    if request.user.is_encarregada:
        qs = qs.filter(encarregada=request.user)
    return qs


def _verificar_dono(request, funcionario):
    if request.user.is_preposta:
        return
    if funcionario.encarregada != request.user:
        raise PermissionError


# ─────────────────────────────────────────────
#  TELAS DA PREPOSTA
# ─────────────────────────────────────────────
@encarregada_required
def home(request):
    return render(request, 'encarregada/home.html')


'''@encarregada_required
def enc_home(request):
    return render(request, 'encarregada/home.html')'''



'''@preposta_required
def list_colaboradores(request):
    funcionarios = Funcionario.objects.select_related('encarregada').prefetch_related('setores').order_by('nome_funcionario')
    funcionario_filter = FuncionarioFilter(request.GET, queryset=funcionarios)
    paginacao = Paginator(funcionario_filter.qs, 12)
    page_obj = paginacao.get_page(request.GET.get('page'))
    return render(request, 'preposta/list_colaboradores.html', {
        'funcionarios': page_obj,
        'filter': funcionario_filter,
    })'''


@encarregada_required
def setores(request):
    from django.db.models import Count
    encarregadas = CustomUser.objects.filter(role=CustomUser.ENCARREGADA).annotate(
        total=Count('setores')
    )
    
    funcionarios = _qs_funcionarios(request)
    funcionario_filter = FuncionarioFilter(request.GET, queryset=funcionarios)
    paginacao = Paginator(funcionario_filter.qs, 12)
    page_obj = paginacao.get_page(request.GET.get('page'))

    if request.user.is_encarregada:
        setores_qs = Setor.objects.filter(encarregada=request.user).order_by('nome')
    else:
        setores_qs = Setor.objects.all().order_by('nome')

    return render(request, 'encarregada/setores.html', {
        'funcionarios': page_obj,
        'filter': funcionario_filter,
        'setores': setores_qs,
        'encarregadas': encarregadas
    })

@encarregada_required
def setor_por_encarregada(request, pk):
    encarregada = get_object_or_404(CustomUser, pk=pk, role=CustomUser.ENCARREGADA)
    setores = Setor.objects.filter(encarregada=encarregada).order_by('nome')
    funcionarios = Funcionario.objects.filter(encarregada=encarregada).prefetch_related('setores').order_by('nome_funcionario')
    return render(request, 'encarregada/todos_setores.html', {
        'encarregada': encarregada,
        'setores': setores,
        'funcionarios': funcionarios,
    })
    
    
#______________________
# Uniformes
#______________________
@encarregada_required  # encarregada_required já deixa passar preposta também
def uniformes(request):
    from django.db.models import Count
    
    if request.user.is_preposta:
        # preposta vê cards de encarregadas
        encarregadas = CustomUser.objects.filter(role=CustomUser.ENCARREGADA).annotate(
            total=Count('funcionarios')
        )
        return render(request, 'encarregada/uniformes.html', {'encarregadas': encarregadas})
    
    # encarregada vê seus funcionários
    funcionarios = _qs_funcionarios(request).select_related('uniforme')
    f = FuncionarioFilter(request.GET, queryset=funcionarios)
    page_obj = Paginator(f.qs, 12).get_page(request.GET.get('page'))
    return render(request, 'encarregada/uniformes.html', {
        'funcionarios': page_obj,
        'filter': f,
        'blusa':      Uniforme.objects.filter(funcionario__encarregada=request.user).values('blusa').annotate(total=Count('blusa')),
        'blusa_frio': Uniforme.objects.filter(funcionario__encarregada=request.user).values('blusa_frio').annotate(total=Count('blusa_frio')),
        'calca':      Uniforme.objects.filter(funcionario__encarregada=request.user).values('calca').annotate(total=Count('calca')),
        'sapato':     Uniforme.objects.filter(funcionario__encarregada=request.user).values('sapato').annotate(total=Count('sapato')),
        'galocha':    Uniforme.objects.filter(funcionario__encarregada=request.user).values('galocha').annotate(total=Count('galocha')),
        'setor':      Setor.objects.filter(encarregada=request.user),
    })


@preposta_required
def contabilidade_uniforme_preposta(request):
    contagem = Uniforme.objects.all()
    context={'blusa':       contagem.values('blusa').annotate(total=Count('blusa')).order_by('blusa'),
             'blusa_frio':  contagem.values('blusa_frio').annotate(total=Count('blusa_frio')).order_by('blusa_frio'),
             'calca':       contagem.values('calca').annotate(total=Count('calca')).order_by('calca'),   
             'sapato':       contagem.values('sapato').annotate(total=Count('sapato')).order_by('sapato'),   
             'galocha':       contagem.values('galocha').annotate(total=Count('galocha')).order_by('galocha'),   
             }
    return render(request, 'preposta/contabilidade_uniforme.html',context)


@preposta_required
def uniformes_por_encarregada(request, pk):
    encarregada = get_object_or_404(CustomUser, pk=pk, role=CustomUser.ENCARREGADA)
    funcionarios = Funcionario.objects.filter(encarregada=encarregada).select_related('uniforme').order_by('nome_funcionario')
    
    contagem_uniforme = Uniforme.objects.filter(funcionario__encarregada=encarregada)

    context={
             'encarregada': encarregada,
            'funcionarios': funcionarios,
            'blusa':      contagem_uniforme.values('blusa').annotate(total=Count('blusa')).order_by('blusa'),
            'blusa_frio':      contagem_uniforme.values('blusa_frio').annotate(total=Count('blusa_frio')).order_by('blusa_frio'),              
            'calca':       contagem_uniforme.values('calca').annotate(total=Count('calca')).order_by('calca'),   
            'sapato':       contagem_uniforme.values('sapato').annotate(total=Count('sapato')).order_by('sapato'),   
            'galocha':       contagem_uniforme.values('galocha').annotate(total=Count('galocha')).order_by('galocha'), 
            }
    return render(request, 'preposta/todos_uniformes.html', context)
    



@preposta_required
def ferias(request):
    from django.db.models import Count
    
    if request.user.is_preposta:
        # preposta vê cards de encarregadas
        encarregadas = CustomUser.objects.filter(role=CustomUser.ENCARREGADA).annotate(
            total=Count('funcionarios')
        )   
    context ={
        'encarregadas':encarregadas
    }
    return render(request, 'preposta/ferias.html', context)


@preposta_required
def todas_ferias(request,pk):
    from collections import defaultdict
    encarregada = get_object_or_404(CustomUser, pk=pk, role=CustomUser.ENCARREGADA)
    funcionarios = Funcionario.objects.filter(encarregada=encarregada).order_by('nome_funcionario')

    MESES = [
        ('JAN','Janeiro'),('FEV','Fevereiro'),('MAR','Março'),('ABR','Abril'),
        ('MAI','Maio'),('JUN','Junho'),('JUL','Julho'),('AGO','Agosto'),
        ('SET','Setembro'),('OUT','Outubro'),('NOV','Novembro'),('DEZ','Dezembro'),
    ]

    por_mes = defaultdict(list)
    for f in funcionarios:
        if f.ferias:
            por_mes[f.ferias].append(f)

    calendario = [
        {'codigo': cod, 'nome': nome, 'funcionarios': por_mes.get(cod, []), 'total': len(por_mes.get(cod, []))}
        for cod, nome in MESES
    ]
    return render(request, 'preposta/todas_ferias.html',{
        'encarregada': encarregada,
        'calendario': calendario,
        'total_agendado': funcionarios.exclude(ferias=None).exclude(ferias='').count(),
        'total_sem_ferias': funcionarios.filter(ferias=None).count(),
    })


@preposta_required
def colabo_encarregadas(request, pk):
    encarregada = get_object_or_404(CustomUser, pk=pk, role=CustomUser.ENCARREGADA)
    funcionarios = Funcionario.objects.filter(encarregada=encarregada).all()
    return render(request, 'preposta/colabo_encarregada.html', {'encarregada': encarregada, 'funcionarios':funcionarios})


@preposta_required
def encarregadas(request):
    from django.db.models import Count
    encarregadas = CustomUser.objects.filter(role=CustomUser.ENCARREGADA).annotate(
        total=Count('funcionarios')
    )
    return render(request, 'preposta/encarregadas.html', {'encarregadas': encarregadas})


@preposta_required
def criar_encarregada(request):
    if request.method == 'POST':
        form = CriarEncarregadaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Encarregada criada com sucesso!')
            return redirect('/encarregadas/')
    else:
        form = CriarEncarregadaForm()  # ← sem instance, sempre vazio
    return render(request, 'preposta/criar_encarregada.html', {'form': form})


@preposta_required
def editar_encarregada(request, pk):
    encarregada = get_object_or_404(CustomUser, pk=pk, role=CustomUser.ENCARREGADA)
    if request.method == 'POST':
        form = EditarEncarregadaForm(request.POST, instance=encarregada)
        if form.is_valid():
            form.save()
            messages.success(request, 'Encarregada atualizada.')
            return redirect('/editar_encarregada/')
    else:
        form = EditarEncarregadaForm(instance=encarregada)
    return render(request, 'preposta/editar_encarregada.html', {'form': form, 'encarregada': encarregada})


@preposta_required
def excluir_encarregada(request, pk):
    encarregada = get_object_or_404(CustomUser, pk=pk, role=CustomUser.ENCARREGADA)
    if request.method == 'POST':
        encarregada.delete()
        messages.success(request, 'Encarregada removida.')
        return redirect('encarregadas')
    return render(request, 'preposta/excluir_encarregada.html', {'encarregada': encarregada})


@preposta_required
def associar_funcionarios_encarregada(request, pk):
    encarregada = get_object_or_404(CustomUser, pk=pk, role=CustomUser.ENCARREGADA)
    if request.method == 'POST':
        form = AssociarFuncionariosEncarregadaForm(request.POST)
        if form.is_valid():
            Funcionario.objects.filter(encarregada=encarregada).update(encarregada=None)
            form.cleaned_data['funcionarios'].update(encarregada=encarregada)
            messages.success(request, 'Colaboradores associados com sucesso!')
            return redirect('encarregadas')
    else:
        form = AssociarFuncionariosEncarregadaForm(
            initial={'funcionarios': Funcionario.objects.filter(encarregada=encarregada)}
        )
    return render(request, 'preposta/associar_funcionarios.html', {
        'form': form, 'encarregada': encarregada,
    })


@preposta_required
def associar_setores_encarregada(request, pk):
    encarregada = get_object_or_404(CustomUser, pk=pk, role=CustomUser.ENCARREGADA)
    if request.method == 'POST':
        form = AssociarSetoresEncarregadaForm(request.POST)
        if form.is_valid():
            Setor.objects.filter(encarregada=encarregada).update(encarregada=None)
            form.cleaned_data['setores'].update(encarregada=encarregada)
            messages.success(request, 'Setores associados com sucesso!')
            return redirect('encarregadas')
    else:
        form = AssociarSetoresEncarregadaForm(
            initial={'setores': Setor.objects.filter(encarregada=encarregada)}
        )
    return render(request, 'preposta/associar_setores.html', {
        'form': form, 'encarregada': encarregada,
    })


# ─────────────────────────────────────────────
#  TELAS DA ENCARREGADA
# ─────────────────────────────────────────────




@encarregada_required
def colaboradores(request):
    funcionarios = _qs_funcionarios(request)
    funcionario_filter = FuncionarioFilter(request.GET, queryset=funcionarios)
    paginacao = Paginator(funcionario_filter.qs, 12)
    page_obj = paginacao.get_page(request.GET.get('page'))
    return render(request, 'encarregada/enc_colaboradores.html', {
        'funcionarios': page_obj,
        'filter': funcionario_filter,
    })


@encarregada_required
def enc_setores(request):
    funcionarios = _qs_funcionarios(request)
    funcionario_filter = FuncionarioFilter(request.GET, queryset=funcionarios)
    paginacao = Paginator(funcionario_filter.qs, 12)
    page_obj = paginacao.get_page(request.GET.get('page'))

    if request.user.is_encarregada:
        setores_qs = Setor.objects.filter(encarregada=request.user).order_by('nome')
    else:
        setores_qs = Setor.objects.all().order_by('nome')

    return render(request, 'encarregada/setores.html', {
        'funcionarios': page_obj,
        'filter': funcionario_filter,
        'setores': setores_qs,
    })


'''@encarregada_required
def enc_uniformes(request):
    try:
        funcionarios = _qs_funcionarios(request).select_related('uniforme')
        setor = Setor.objects.all()
        funcionario_filter = FuncionarioFilter(request.GET, queryset=funcionarios)

        blusa      = Uniforme.objects.values('blusa').annotate(total=Count('blusa'))
        blusa_frio = Uniforme.objects.values('blusa_frio').annotate(total=Count('blusa_frio'))
        calca      = Uniforme.objects.values('calca').annotate(total=Count('calca'))
        sapato     = Uniforme.objects.values('sapato').annotate(total=Count('sapato'))
        galocha    = Uniforme.objects.values('galocha').annotate(total=Count('galocha'))

        paginacao = Paginator(funcionario_filter.qs, 12)
        page_obj = paginacao.get_page(request.GET.get('page'))

        return render(request, 'encarregada/enc_uniformes.html', {
            'blusa': blusa, 'blusa_frio': blusa_frio, 'calca': calca,
            'sapato': sapato, 'galocha': galocha,
            'funcionarios': page_obj, 'filter': funcionario_filter, 'setor': setor,
        })
    except Exception as e:
        print(f'Erro na query: {e}')
        return render(request, 'uniformes.html', {
            'funcionarios': Funcionario.objects.all(), 'erro': str(e)
        })'''


@encarregada_required
def enc_ferias(request):
    from collections import defaultdict

    MESES = [
        ('JAN','Janeiro'),('FEV','Fevereiro'),('MAR','Março'),('ABR','Abril'),
        ('MAI','Maio'),('JUN','Junho'),('JUL','Julho'),('AGO','Agosto'),
        ('SET','Setembro'),('OUT','Outubro'),('NOV','Novembro'),('DEZ','Dezembro'),
    ]

    # filtra só os funcionários desta encarregada
    funcionarios = Funcionario.objects.filter(
        encarregada=request.user
    ).order_by('nome_funcionario')

    por_mes = defaultdict(list)
    for f in funcionarios:
        if f.ferias:
            por_mes[f.ferias].append(f)

    calendario = [
        {
            'codigo': cod,
            'nome': nome,
            'funcionarios': por_mes.get(cod, []),
            'total': len(por_mes.get(cod, [])),
        }
        for cod, nome in MESES
    ]

    return render(request, 'preposta/ferias.html', {
        'calendario': calendario,
        'total_agendado': funcionarios.exclude(ferias=None).exclude(ferias='').count(),
        'total_sem_ferias': funcionarios.filter(ferias=None).count(),
    })


# ─────────────────────────────────────────────
#  FORMULÁRIOS
# ─────────────────────────────────────────────

@encarregada_required
def entrada_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            funcionario = form.save(commit=False)
            if request.user.is_encarregada:
                funcionario.encarregada = request.user
            funcionario.save()
            form.save_m2m()
            return redirect('enc_colaboradores')
    else:
        form = FuncionarioForm()
    return render(request, 'forms/entrada_funcionario.html', {'form': form})


@encarregada_required
def registrar_setor(request):
    if request.method == 'POST':
        form = SetorForm(request.POST)
        if form.is_valid():
            try:
                setor = form.save(commit=False)
                if request.user.is_encarregada:
                    setor.encarregada = request.user
                setor.save()
                messages.success(request, 'Setor cadastrado com sucesso')
                return redirect('registrar_setor')
            except IntegrityError:
                messages.error(request, 'Erro: Este setor já existe!')
    else:
        form = SetorForm()
    return render(request, 'forms/setor_form.html', {'form': form})


@encarregada_required
def registrar_uniforme(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    try:
        _verificar_dono(request, funcionario)
    except PermissionError:
        messages.error(request, 'Você não tem permissão para editar este colaborador.')
        return redirect('uniformes')

    if request.method == 'POST':
        form = UniformeForm(request.POST)
        if form.is_valid():
            uniforme = form.save(commit=False)
            uniforme.funcionario = funcionario
            uniforme.save()
            return redirect('uniformes')
    else:
        form = UniformeForm()
    return render(request, 'forms/uniforme_form.html', {'forms': form, 'funcionario': funcionario})


@encarregada_required
def associar_setor_colaborador(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    try:
        _verificar_dono(request, funcionario)
    except PermissionError:
        messages.error(request, 'Você não tem permissão para editar este colaborador.')
        return redirect('/encarregada/setores/')

    # define o queryset conforme o perfil
    if request.user.is_encarregada:
        setores_qs = Setor.objects.filter(encarregada=request.user).order_by('nome')
    else:
        setores_qs = Setor.objects.all().order_by('nome')

    if request.method == 'POST':
        form = AsssociarSetoresForm(request.POST, setores_queryset=setores_qs)
        if form.is_valid():
            funcionario.setores.set(form.cleaned_data['setores'])
            return redirect('/encarregada/setores/')
    else:
        form = AsssociarSetoresForm(
            initial={'setores': funcionario.setores.all()},
            setores_queryset=setores_qs,
        )

    return render(request, 'encarregada/setor_colaborador.html', {
        'funcionario': funcionario,
        'form': form,
    })


@encarregada_required
def editar_funcionario_preposta(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    try:
        _verificar_dono(request, funcionario)
    except PermissionError:
        messages.error(request, 'Sem permissão.')
        return redirect('/encarregada/colaboradores/')

    # form diferente para cada perfil
    FormClass = FuncionarioFormPreposta if request.user.is_preposta else FuncionarioForm

    if request.method == 'POST':
        form = FormClass(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            if request.user.is_preposta:
                return redirect('/encarregada/colaboradores/')
            return redirect('/encarregada/colaboradores/')
    else:
        form = FormClass(instance=funcionario)

    return render(request, 'edicao/editar_funcionario.html', {
        'form': form,
        'funcionario': funcionario,
    })





@encarregada_required
def editar_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    try:
        _verificar_dono(request, funcionario)
    except PermissionError:
        messages.error(request, 'Você não tem permissão para editar este colaborador.')
        return redirect('enc_colaboradores')

    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            return redirect('enc_colaboradores')
    else:
        form = FuncionarioForm(instance=funcionario)
    return render(request, 'edicao/editar_funcionario.html', {'form': form, 'funcionario': funcionario})


@encarregada_required
def excluir_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    try:
        _verificar_dono(request, funcionario)
    except PermissionError:
        messages.error(request, 'Você não tem permissão para excluir este colaborador.')
        return redirect('enc_colaboradores')

    if request.method == 'POST':
        funcionario.delete()
        messages.success(request, 'Funcionário excluído com sucesso')
        return redirect('enc_colaboradores')
    return render(request, 'edicao/excluir_funcionario.html', {'funcionario': funcionario})


@encarregada_required
def editar_setor(request, pk):
    setor = get_object_or_404(Setor, pk=pk)
    if request.method == 'POST':
        form = SetorForm(request.POST, instance=setor)
        if form.is_valid():
            form.save()
            return redirect('enc_setores')
    else:
        form = SetorForm(instance=setor)
    return render(request, 'edicao/editar_setor.html', {'forms': form, 'setor': setor})


@encarregada_required
def editar_uniforme(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    try:
        _verificar_dono(request, funcionario)
    except PermissionError:
        messages.error(request, 'Você não tem permissão para editar este colaborador.')
        return redirect('uniformes')

    uniforme = get_object_or_404(Uniforme, funcionario=funcionario)
    if request.method == 'POST':
        form = UniformeForm(request.POST, instance=uniforme)
        if form.is_valid():
            form.save()
            return redirect('uniformes')
    else:
        form = UniformeForm(instance=uniforme)
    return render(request, 'edicao/editar_uniforme.html', {
        'forms': form, 'funcionario': funcionario, 'uniforme': uniforme,
    })