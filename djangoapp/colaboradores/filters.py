import django_filters

from colaboradores.models import Funcionario

class FuncionarioFilter(django_filters.FilterSet):
    class Meta:
        model = Funcionario
        fields = {
            "matricula_funcionario":["icontains"],
            "nome_funcionario":["icontains"],
            
        }