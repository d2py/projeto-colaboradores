
from django.urls import path, include
from colaboradores.views import base, home, list_colaboradores, encarregadas, setores, uniformes


app_colaboradores = 'colaboadores'

urlpatterns = [
    #colaboradores:base ## e para urls reverso (pesquisar o que e )
    path('', base, name='base'),
    path('home/',home, name='home'),
    path('colaboradores/',list_colaboradores, name='colaboradores'),
    path('encarregadas/', encarregadas, name='encarregadas'),
    path('setores/', setores, name='setores'),
    path('uniformes/', uniformes, name='uniformes'),
]


