from django.contrib import admin

# Register your models here.
from .models import Contato_Empresa, Eventos, Log_Sincronizacao, Parametros_Gerais, CustomUsuario

from django.contrib.auth.admin import UserAdmin

from .forms import CustomUsuarioCreateForm, CustomUsuarioChangeForm


@admin.register(Contato_Empresa)
class Contato_EmpresaAdmin(admin.ModelAdmin):
    list_display = ('Nome', 'Funcao', 'Telefone', 'Celular', 'Observacao')

@admin.register(Eventos)
class EventosAdmin(admin.ModelAdmin):
    list_display = ('Data_Criacao_Evento', 'Tipo_Doc_Fiscal', 'Data_Emissao', 'Num_Doc', 'Serie_Dov', 'Status_Doc', 'Id_Tab_Orig', 'Registro_Sincronizado')

@admin.register(Log_Sincronizacao)
class Log_SincronizacaoAdmin(admin.ModelAdmin):
    list_display = ('Data_Tentativa_Envio', 'Id_Eventos', 'Status_Envio')

@admin.register(Parametros_Gerais)
class Parametros_GeraisAdmin(admin.ModelAdmin):
    list_display = ('Tempo_Sincr_Minutos', 'Mod_Sincron_Nfe', 'Mod_Sincron_Nfce', 'Situacao_Sincronizacao', 'Sistema_Sincronizacao', 'Ender_Endpoint_Servidor', 'Data_Inicial_Sinc')

@admin.register(CustomUsuario)
class CustomUsuarioAdmin(UserAdmin):
    add_form = CustomUsuarioCreateForm
    form = CustomUsuarioChangeForm
    model = CustomUsuario
    list_display = ('first_name', 'last_name', 'email', 'fone', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'fone')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
