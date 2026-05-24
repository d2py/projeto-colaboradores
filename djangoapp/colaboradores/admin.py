from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from colaboradores.models import CustomUser, Funcionario, Setor, Uniforme


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Campos exibidos na listagem
    list_display  = ('username', 'first_name', 'last_name', 'role', 'is_active')
    list_filter   = ('role', 'is_active')
    search_fields = ('username', 'first_name', 'last_name')
    ordering      = ('username',)

    # Adiciona o campo "role" nos fieldsets do formulário de edição
    fieldsets = UserAdmin.fieldsets + (
        ('Perfil do sistema', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Perfil do sistema', {'fields': ('role',)}),
    )


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display  = ('matricula_funcionario', 'nome_funcionario', 'encarregada', 'status')
    list_filter   = ('encarregada', 'status', 'ferias')
    search_fields = ('nome_funcionario', 'matricula_funcionario')
    filter_horizontal = ('setores',)


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display  = ('nome', 'encarregada')
    list_filter   = ('encarregada',)
    search_fields = ('nome',)


@admin.register(Uniforme)
class UniformeAdmin(admin.ModelAdmin):
    list_display  = ('funcionario', 'blusa', 'calca', 'sapato', 'galocha')
    search_fields = ('funcionario__nome_funcionario',)