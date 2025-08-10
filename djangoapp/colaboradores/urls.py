
from django.urls import path, include
from colaboradores.views import base, home, list_colaboradores, encarregadas, setores, uniformes,todos_uniformes, ferias, col_encarregadas, todos_setores, todas_ferias

app_colaboradores = 'colaboadores'

urlpatterns = [
    #colaboradores:base ## e para urls reverso (pesquisar o que e )
    path('', base, name='base'),
    path('home/',home, name='home'),
    path('colaboradores/',list_colaboradores, name='colaboradores'),
    path('encarregadas/', encarregadas, name='encarregadas'),
    path('cols_encarregada/', col_encarregadas, name='cols_encarregada'),
    path('setores/', setores, name='setores'),
    path('setores/todos_setores/', todos_setores, name='todos_setores'),
    path('uniformes/', uniformes, name='uniformes'),
    path('uniformes/todos_uniformes/', todos_uniformes, name='todos_uniformes'),
    path('ferias/', ferias, name='ferias'),
    path('ferias/todas_ferias/', todas_ferias, name='todas_ferias'),
]


