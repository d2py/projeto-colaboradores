from django import  forms 

from colaboradores.models import Funcionario, Setores, Uniformes


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields=[
            "matricula_funcionario",
            "nome_funcionario",
            "status",
            "ferias"
        ]


class SetorForm(forms.ModelForm):
    class Meta:
        model = Setores
        fields=[
            "setor"
        ]

class UniformeForm(forms.ModelForm):
    class Meta:
        model = Uniformes
        fields=[
            "calca",
            "blusa",
            "blusa_frio",
            "sapato",
            "galocha",
            
        ]