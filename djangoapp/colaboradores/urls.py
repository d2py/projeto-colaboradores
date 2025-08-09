
from django.urls import path, include
from colaboradores.views import base, home, list_colaboradores, encarregadas, setores, uniformes, ferias, col_encarregadas, todos_setores

app_colaboradores = 'colaboadores'

urlpatterns = [
    #colaboradores:base ## e para urls reverso (pesquisar o que e )
    path('', base, name='base'),
    path('home/',home, name='home'),
    path('colaboradores/',list_colaboradores, name='colaboradores'),
    path('encarregadas/', encarregadas, name='encarregadas'),
    path('cols_encarregada/', col_encarregadas, name='cols_encarregada'),
    path('setores/', setores, name='setores'),
    path('todos_setores/', todos_setores, name='todos_setores'),
    path('uniformes/', uniformes, name='uniformes'),
    path('ferias/', ferias, name='ferias'),
]


