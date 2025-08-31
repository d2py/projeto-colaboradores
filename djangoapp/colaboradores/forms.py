from django import  forms 

from colaboradores.models import Funcionario


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields=[
            "matricula_funcionario",
            "nome_funcionario",
            "status",
            "ferias"
        ]