from urllib import request

from django import  forms 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from colaboradores.models import CustomUser, Funcionario, Setor, Uniforme


# ─────────────────────────────────────────────
#  AUTENTICAÇÃO
# ─────────────────────────────────────────────

class LoginForm(AuthenticationForm):
    """Formulário de login com estilo Bootstrap 5."""
    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome de usuario',
            'autofocus': True,
        }),
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placceholder': 'senha',
        }),
    )


# ─────────────────────────────────────────────
#  PREPOSTA — gerenciamento de encarregadas
# ─────────────────────────────────────────────

class CriarEncarregadaForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password',
        }),
    )
    password2 = forms.CharField(
        label='Confirmação de senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password',
        }),
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username':   forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }
        labels = {
            'username':   'Usuário',
            'first_name': 'Nome',
            'last_name':  'Sobrenome',
            'email':      'E-mail',
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('As senhas não coincidem.')
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.role = CustomUser.ENCARREGADA
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user


class EditarEncarregadaForm(UserChangeForm):
    """Preposta edita dados de uma encarregada (sem campo de senha direta)."""
    password = None # remove o campo de hash de senha do UserChangeForm

    first_name = forms.CharField(
        label='Nome',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}),  
        )
    
    last_name = forms.CharField(
        label='Nome',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form:control'}),
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email','is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }


class AssociarFuncionariosEncarregadaForm(forms.Form):
    """Preposta associa colaboradores a uma encarregada."""
    funcionarios = forms.ModelMultipleChoiceField(
        queryset=Funcionario.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label = 'colaboradores',
    )

class AssociarSetoresEncarregadaForm(forms.Form):
    """Preposta associa setores a uma encarregada."""
    setores = forms.ModelMultipleChoiceField(
        queryset=Setor.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label='Setores',
    )


class FuncionarioFormPreposta(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = [
            "matricula_funcionario",
            "nome_funcionario",
            "status",
            "ferias",
            "encarregada",  # só a preposta pode alterar
        ]
        widgets = {
            'matricula_funcionario': forms.NumberInput(attrs={'class': 'form-control'}),
            'nome_funcionario':      forms.TextInput(attrs={'class': 'form-control'}),
            'status':                forms.Select(attrs={'class': 'form-select'}),
            'ferias':                forms.Select(attrs={'class': 'form-select'}),
            'encarregada':           forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'encarregada': 'Encarregada responsável',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # mostra só encarregadas ativas no select
        self.fields['encarregada'].queryset = CustomUser.objects.filter(
            role=CustomUser.ENCARREGADA,
            is_active=True,
        ).order_by('first_name')
        self.fields['encarregada'].empty_label = 'Sem encarregada'


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
    setores = forms.ModelMultipleChoiceField(
        queryset=Setor.objects.none(),  # começa vazio
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-setores'}),
        required=False,
        label='Setores',
    )

    def __init__(self, *args, setores_queryset=None, **kwargs):
        super().__init__(*args, **kwargs)
        if setores_queryset is not None:
            self.fields['setores'].queryset = setores_queryset
        else:
            self.fields['setores'].queryset = Setor.objects.all()    