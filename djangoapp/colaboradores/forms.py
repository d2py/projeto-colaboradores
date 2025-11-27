from django import  forms 

from colaboradores.models import Funcionario, Setor, Uniforme


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields=[
            "matricula_funcionario",
            "nome_funcionario",
            "status",
            "ferias",
            
        ]


class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields=[
            "nome",
            
        ]

class UniformeForm(forms.ModelForm):
    class Meta:
        model = Uniforme
        fields=[
            
            "calca",
            "blusa",
            "blusa_frio",
            "sapato",
            "galocha",
            
        ]


class AsssociarSetoresForm(forms.Form):
    setores = forms.ModelMultipleChoiceField(queryset=Setor.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-setores'}), required=False, label="Setores")
