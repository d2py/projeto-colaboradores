from django.urls import path

from colaboradores.views import (
    login_view, logout_view,
    home,  encarregadas, setores, uniformes,contabilidade_uniforme_preposta,
     ferias, colabo_encarregadas, setor_por_encarregada, todas_ferias,
    criar_encarregada, editar_encarregada, excluir_encarregada,
    associar_funcionarios_encarregada, associar_setores_encarregada,
    colaboradores, enc_setores, enc_ferias,
    entrada_funcionario, editar_funcionario, excluir_funcionario,
    registrar_setor, associar_setor_colaborador, editar_setor,
    registrar_uniforme, editar_uniforme,uniformes_por_encarregada,
    editar_funcionario_preposta
)

#app_name = 'colaboradores'

urlpatterns = [
    # Autenticação — rotas explícitas, sem ambiguidade
    path('login/',  login_view,  name='login'),
    path('logout/', logout_view, name='logout'),

    # Preposta
    path('home/',                                  home,                name='home'),
    #path('colaboradores/',                    list_colaboradores,  name='colaboradores'),
    path('colaboradores/encarregada/<int:pk>/',    colabo_encarregadas, name='cols_encarregada'),
    path('setores/',                               setores,             name='setores'),
    path('setor/por/encarregada/<int:pk>/',        setor_por_encarregada,       name='setor_por_encarregada'),
    path('contabilidade/uniforme/preposta/',                             contabilidade_uniforme_preposta,           name='contabilidade_uniformes'),
    path('uniformes/',                             uniformes,           name='uniformes'),
    path('ferias/',                                ferias,              name='ferias'),
    path('ferias/todas/<int:pk>/',                 todas_ferias,        name='todas_ferias'),
    path('uniformes/encarregada/<int:pk>/',        uniformes_por_encarregada, name='uniformes_por_encarregada'),


    # Gestão de encarregadas
    path('encarregadas/',                           encarregadas,                      name='encarregadas'),
    path('encarregadas/criar/',                     criar_encarregada,                 name='criar_encarregada'),
    path('editar/encarregada/<int:pk>/',            editar_encarregada,                name='editar_encarregada'),
    path('excluir/encarregada/<int:pk>/',           excluir_encarregada,               name='excluir_encarregada'),
    path('encarregadas/funcionarios/<int:pk>/',      associar_funcionarios_encarregada, name='associar_funcionarios_encarregada'),
    path('encarregadas/setores/<int:pk>/',           associar_setores_encarregada,      name='associar_setores_encarregada'),

    # Encarregada
    #path('encarregada/home/',          enc_home,          name='enc_home'),
    path('encarregada/colaboradores/', colaboradores, name='enc_colaboradores'),
    path('encarregada/setores/',       enc_setores,       name='enc_setores'),
    #path('encarregada/uniformes/',     enc_uniformes,     name='enc_uniformes'),
    path('encarregada/ferias/',        enc_ferias,        name='enc_ferias'),

    # Formulários
    path('entrada/funcionario/',                 entrada_funcionario,       name='entrada_funcionario'),
    path('adicionar/setor/',                     registrar_setor,           name='registrar_setor'),
    path('adicionar/setor/funcionario/<int:pk>', associar_setor_colaborador,name='setor_colaborador'),
    path('adicionar/uniforme/<int:pk>',          registrar_uniforme,        name='adicionar_uniforme'),

    # Edição / exclusão
    path('editar/funcionario/preposta/<int:pk>',  editar_funcionario_preposta,  name='editar_funcionario_preposta'),
    path('editar/funcionario/<int:pk>',  editar_funcionario,  name='editar_funcionario'),
    path('excluir/funcionario/<int:pk>', excluir_funcionario, name='excluir_funcionario'),
    path('editar/setor/<int:pk>',        editar_setor,        name='editar_setor'),
    path('editar/uniforme/<int:pk>',     editar_uniforme,     name='editar_uniforme'),
]