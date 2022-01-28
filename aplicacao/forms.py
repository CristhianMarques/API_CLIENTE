from django import forms

from .models import Parametros_Gerais, Contato_Empresa

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUsuario


class DateInput(forms.DateInput):
    input_type = 'date'

class Parametros_GeraisModelForm(forms.ModelForm):
    
    class Meta:
        model = Parametros_Gerais
        fields = ['Tempo_Sincr_Minutos', 'Mod_Sincron_Nfe', 'Mod_Sincron_Nfce', 'Situacao_Sincronizacao', 'Sistema_Sincronizacao', 'Ender_Endpoint_Servidor', 'Data_Inicial_Sinc']
        
        widgets = {
        'Data_Inicial_Sinc': forms.DateInput(format=('%m/%d/%Y')),
    }

class Contato_EmpresaModelForm(forms.ModelForm):
    
    class Meta:
        model = Contato_Empresa
        fields = ['Empresa', 'Nome', 'Funcao', 'Telefone', 'Celular', 'Observacao',]

class CustomUsuarioCreateForm(UserCreationForm):

    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'fone')
        labels = {'username': 'Username/E-mail'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["username"]
        if commit:
            user.save()
        return user


class CustomUsuarioChangeForm(UserChangeForm):

    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'fone')
        