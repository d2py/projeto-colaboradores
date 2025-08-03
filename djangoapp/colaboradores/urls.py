
from django.urls import path, include
from colaboradores.views import base


app_colaboradores = 'colaboadores'

urlpatterns = [
    #colaboradores:base ## e para urls reverso (pesquisar o que e )
    path('', base, name='base'),
]


