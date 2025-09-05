
from django.urls import path
from colaboradores.views import home, list_colaboradores, encarregadas, setores, uniformes,todos_uniformes, ferias, colabo_encarregadas, todos_setores, todas_ferias
from colaboradores.views import enc_home,enc_colaboradores, enc_setores,enc_uniformes,enc_ferias

#Edicao de Funcionario/exclusão/Adicionar
from colaboradores.views import entrada_funcionario, editar_funcionario, excluir_funcionario, registrar_setor, editar_setor, registrar_uniforme

 

app_colaboradores = 'colaboadores'

urlpatterns = [
    #colaboradores:base ## e para urls reverso (pesquisar o que e )
    path('home/',home, name='home'),
    path('colaboradores/',list_colaboradores, name='colaboradores'),
    path('encarregadas/', encarregadas, name='encarregadas'),
    path('cols_encarregada/', colabo_encarregadas, name='cols_encarregada'),
    path('setores/', setores, name='setores'),
    path('setores/todos_setores/', todos_setores, name='todos_setores'),
    path('uniformes/', uniformes, name='uniformes'),
    path('uniformes/todos_uniformes/', todos_uniformes, name='todos_uniformes'),
    path('ferias/', ferias, name='ferias'),
    path('ferias/todas_ferias/', todas_ferias, name='todas_ferias'),
    # url da encarrega
    path('enc_home/',enc_home, name='enc_home'),
    path('enc_colaboradores/',enc_colaboradores, name='enc_colaboradores'),
    path('enc_setores/',enc_setores, name='enc_setores'),
    path('enc_uniformes/',enc_uniformes, name='enc_uniformes'),
    path('enc_ferias/',enc_ferias, name='enc_ferias'),

    #Formulario 
    path('entrada_funcionario/',entrada_funcionario, name="entrada_funcionario" ),
    path('adicionar_setor/',registrar_setor, name="registrar_setor" ),
    path('adicionar_uniforme/<int:pk>',registrar_uniforme, name="adicionar_uniforme" ),
    # Edicao
    path('editar_funcionario/<int:pk>', editar_funcionario, name="editar_funcionario"),
    path('excluir_funcionario/<int:pk>', excluir_funcionario, name="excluir_funcionario"),
    path('editar_setor/<int:pk>', editar_setor, name="editar_setor"),

]


