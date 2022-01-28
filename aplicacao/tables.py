import django_tables2 as tables
from django_tables2.utils import A

from aplicacao.models import Eventos



class EventosTable(tables.Table):

    #id = tbl.Column(verbose_name='id',  orderable=True)
    #Data_Criacao_Evento = tables.Column() #tbl.Column(verbose_name='Data Criacao Evento')

    class Meta:
        model = Eventos
        #exclude = ('id',)
        #sequence = ('Data_Criacao_Evento')
        #fields = ('id', 'Data_Criacao_Evento')
        template_name = "bootstrap4-custom.html"