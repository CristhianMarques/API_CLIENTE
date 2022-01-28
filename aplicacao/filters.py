from django import forms
from django.utils import six
from django.db.models import Q




###############################################################################

class FormularioFiltro(forms.Form):

    pesquisar = forms.CharField(required=False)

###############################################################################

class FiltroOpcoes:
    def __init__(self, opcoes = None):
        self.fields = getattr(opcoes, 'fields', None)

###############################################################################

class FiltroMetaclasse(type):
    def __new__(cls, name, bases, attrs):
        attrs['filtro'] = ''

        new_class = super(FiltroMetaclasse, cls).__new__(cls, name, bases, attrs)
        new_class._meta = FiltroOpcoes(getattr(new_class, 'Meta', None))

        return new_class

###############################################################################

class FiltroBase:

    def __init__(self, dados, queryset):
        #assert(queryset)

        self.dados = dados or {}
        self.queryset = queryset
    
    @property
    def qs(self):
        if not hasattr(self, '_qs'):
            if self.form.is_valid():
                termo_pesquisa = self.form.cleaned_data['pesquisar']
                if not termo_pesquisa:
                    termo_pesquisa = self.dados.get('query[pesquisar]', '')

                filtro = Q()
                for field in self.get_fields():
                    field_name = '%s__icontains' % field                    
                    filtro = filtro | Q(**{field_name: termo_pesquisa})

                self._qs = self.queryset.filter(filtro)
            else:
                self._qs = self.queryset.all()

        return self._qs

    @classmethod
    def get_fields(cls):
        return cls._meta.fields

    @property
    def form(self):
        if not hasattr(self, '_form'):
            self._form = FormularioFiltro(self.dados)

        return self._form
            
###############################################################################

class Filtro(six.with_metaclass(FiltroMetaclasse, FiltroBase)):
    pass

###############################################################################

class EventosFilter(Filtro):

    class Meta:
        fields = ('Data_Criacao_Evento','id')