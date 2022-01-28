import sweetify
from django.shortcuts import render, redirect
from django.contrib import messages

from django.db import connections

from django.views import generic
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponseForbidden, HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django_tables2.views import RequestConfig
from django.views.generic import ListView
from django.contrib.messages.views import SuccessMessageMixin

from django.shortcuts import get_object_or_404

from django.http import HttpResponse
from django.template import loader

from .forms import Parametros_GeraisModelForm, Contato_EmpresaModelForm
from .models import Parametros_Gerais, Contato_Empresa, Eventos
from aplicacao.tables import EventosTable
from aplicacao import tablesconfigure

import datetime

from django_tables2 import RequestConfig

from aplicacao.filters import EventosFilter


from datetime import date
# Create your views here.

@login_required(login_url='login')
def index(request):
    
    return render(request, 'base.html')

@login_required(login_url='login')
def error404(request, ex):
    template = loader.get_template('404.html')
    return HttpResponse(content=template.render(), content_type='text/thml; charset=utf8', status=404)

@login_required(login_url='login')
def error500(request):
    print('er')
    template = loader.get_template('500.html')
    return HttpResponse(content=template.render(), content_type='text/html; charset=utf8', status=500)

@login_required(login_url='login')
def Processa_Eventos_Manual(request):
    try:
        status_ger = ''
        print('testa')
        status_ger = gera_eventos(request)
        print('as',status_ger)
    except Exception as e:
        print('erro:', e)
        error500(request)
    
    if status_ger == 'Processado com Erro':
       #return redirect('index',status=404)
       sweetify.error(request, 'Erro de Processamento', persistent=True)
    
    return redirect('index')

@login_required(login_url='login')
def eventos(request):

    queryset = Eventos.objects.all().order_by('-id')

    print(queryset)

    filtro = EventosFilter(request.GET, queryset)
    table = EventosTable(filtro.qs)

    table.paginate(page=request.GET.get("page", 1), per_page=25)


    #table = EventosTable(queryset)

    print('ed')
    print(table)
    print(request)
    #tablesconfigure.datagrid_configure(request, table)
    print('fsfd fudeu')

    context = {
        'table': table
    }
    
    return render(request, 'eventos.html', {'table': table})
    

#@login_required(login_url='login')
def gera_eventos():

    situacao_nfce = ''
    situacao_nfe  = ''
    status_registro = ''
    dados_array = []
    datasincronizacao = ''
    empresa = ''

    try:
        parametro = Parametros_Gerais.objects.get(id=1)
    except Parametros_Gerais.DoesNotExist:
        parametro = None
    
    try:
        contato = Contato_Empresa.objects.get(id=1)
    except Contato_Empresa.DoesNotExist:
        contato = None

    print('st01')
    try:
        if (parametro != None) and (contato !=None):
            ###############################################################
            if (parametro.Sistema_Sincronizacao == 'Sistema Smc_Light'):

                query_nfce = """
                    SELECT 
	                    CODIGO ,DATA_EMISSAO, HORA_EMISSAO ,DATA_TRANSMISSAO ,HORA_TRANSMISSAO,CODIGO_VENDA, VALOR_NFCE, ACRESCIMOS_NFCE, DESCONTOS_NFCE,
	                    TOTAL_NFCE, VALOR_PAGO, TROCO, LOTE, SERIE, CHAVE, CAMINHO_XML, TIPO_EMISSAO, STATUS_NFCE, RETORNO_NFCE, ERRO_ROTINA, CNF
                    FROM nfce
                    WHERE 1 = 1 AND DATA_EMISSAO >= (%s)
                """

                query_nfe = """
                    SELECT 
                        ID, NUMERO, CODIGO_VENDA, LOTE, SERIE, CAMINHO_XML, CHAVE, CHAVE_REFERENCIADA, ID_NAT_OP, STATUS_NFE, 
                        TIPO_EMISSAO, TIPO_NFE, INDICACAO_PAGAMENTO, ID_EMITENTE, ID_CLIENTE, DATA_EMISSAO, DATA_TRANSMISSAO, 
                        BASE_ICMS, VALOR_ICMS, ICMS_DESONERADO, BASE_ICMS_ST, VALOR_ICMS_ST, VALOR_NFE, VALOR_FRETE, 
                        VALOR_SEGURO, VALOR_DESPESAS, VALOR_DESCONTO, VALOR_II, VALOR_IPI, VALOR_PIS, VALOR_COFINS, 
                        TOTAL_NFE, VALOR_PAGO, TROCO, TIPO_FRETE, ID_TRANSPORTADOR, QUANTIDADE_CARGA, NUMERO_VOLUME, 
                        ESPECIE_CARGA, MARCA_CARGA, PESO_LIQUIDO, PESO_BRUTO, OBSERVACOES, RETORNO_NFE, ERRO_ROTINA
                    FROM NFE
                    WHERE 1 = 1 AND DATA_EMISSAO >= %s
                """
                #WHERE 1 = 1 AND DATA_EMISSAO >= %s AND DATA_EMISSAO >= (CURDATE() - INTERVAL 2 DAY)

                
                with connections['Smc_Light'].cursor() as cursor:

                    #LOCALIZA ENVENTOS DO TIPO NFCE
                    if (parametro.Mod_Sincron_Nfce == 'Enviadas'):
                        situacao_nfce = " STATUS_NFCE IN ('AUTORIZADA','INUTILIZADA','CANCELADA') "

                    if (parametro.Mod_Sincron_Nfce == 'Pendentes'):
                        situacao_nfce = " STATUS_NFCE = 'PENDENTE' "

                    if (parametro.Mod_Sincron_Nfce == 'Contigencia'):
                        situacao_nfce = " TIPO_EMISSAO = 'CONTINGENCIA' "

                    if (parametro.Mod_Sincron_Nfce == 'Erro'):
                        situacao_nfce = " ERRO_ROTINA != 'NENHUM' "

                    query_nfce = query_nfce + situacao_nfce
                    print('tersrta')
                    print(parametro.Data_Inicial_Sinc)
                    print('ere', parametro.Data_Inicial_Sinc.strftime("%m/%d/%Y"))
                    datasincronizacao = parametro.Data_Inicial_Sinc.strftime("%Y-%m-%d")
                    cursor.execute(query_nfce, [datasincronizacao])
                    #cursor.execute(query_nfce, [])
                    print('estpi')
                    for lista in cursor.fetchall():
                        if (lista[19] != 'NENHUM'):
                            status_registro = lista[19]
                        else:
                            status_registro = lista[17] 

                        dados_array.append({
                            'Id_Tab_Orig': lista[0],
                            'Data_Emissao': lista[1],
                            'Data_Criacao_Evento': date.today(),
                            'Tipo_Doc_Fiscal': 'NFCE',
                            'Num_Doc': lista[20],
                            'Serie_Dov': lista[13],
                            'Registro_Sincronizado': 'Nao',
                            'Status_Doc': status_registro,
                            'Empresa': contato.Empresa,
                            'Nome': contato.Nome,
                            'Funcao': contato.Funcao,
                            'Telefone': contato.Telefone,
                            'Celular': contato.Celular
                    })

                    #print(dados_array)

                    #LOCALIZA ENVENTOS DO TIPO NFE
                    if (parametro.Mod_Sincron_Nfe == 'Enviadas'):
                        situacao_nfe = " STATUS_NFE IN ('AUTORIZADA','INUTILIZADA','CANCELADA') "

                    if (parametro.Mod_Sincron_Nfe == 'Pendentes'):
                        situacao_nfe = " STATUS_NFE = 'PENDENTE' "

                    if (parametro.Mod_Sincron_Nfe == 'Contigencia'):
                        situacao_nfe = " TIPO_EMISSAO = 'CONTINGENCIA' "

                    if (parametro.Mod_Sincron_Nfe == 'Erro'):
                        situacao_nfe = " ERRO_ROTINA != 'NENHUM' "

                    query_nfe = query_nfe + situacao_nfe

                    #print(query_nfe)
                    #cursor.execute(query_nfc, [parametro.Data_Inicial_Sinc])
                    datasincronizacao = parametro.Data_Inicial_Sinc.strftime("%Y-%m-%d")
                    cursor.execute(query_nfe, [datasincronizacao])

                    for lista_nfe in cursor.fetchall():
                        if (lista_nfe[19] != 'NENHUM'):
                            status_registro = lista_nfe[19]
                        else:
                            #if (lista_nfe[17] == 'AUTORIZADA') or (lista_nfe[17] == 'INUTILIZADA') or (lista_nfe[17] == 'CANCELADA'):
                            #    status_registro = 'ENVIADAS'
                            status_registro = lista_nfe[17] 

                        dados_array.append({
                            'Id_Tab_Orig': lista_nfe[0],
                            'Data_Emissao': lista_nfe[15],
                            'Data_Criacao_Evento': date.today(),
                            'Tipo_Doc_Fiscal': 'NFE',
                            'Num_Doc': lista_nfe[1],
                            'Serie_Dov': lista_nfe[4],
                            'Registro_Sincronizado': 'Nao',
                            'Status_Doc': status_registro
                    })                    

            ###############################################################
            if (parametro.Sistema_Sincronizacao == 'Sistema Merchant'):
                
                query_nfce = """
                    SELECT 
	                    CODIGO ,DATA_EMISSAO, HORA_EMISSAO ,DATA_TRANSMISSAO ,HORA_TRANSMISSAO,CODIGO_VENDA, VALOR_NFCE, ACRESCIMOS_NFCE, DESCONTOS_NFCE,
	                    TOTAL_NFCE, VALOR_PAGO, TROCO, LOTE, SERIE, CHAVE, CAMINHO_XML, TIPO_EMISSAO, STATUS_NFCE, RETORNO_NFCE, ERRO_ROTINA, CNF
                    FROM nfce
                    WHERE 1 = 1
                """

                query_nfe = """
                    SELECT 
                        ID, NUMERO, CODIGO_VENDA, LOTE, SERIE, CAMINHO_XML, CHAVE, CHAVE_REFERENCIADA, ID_NAT_OP, STATUS_NFE, 
                        TIPO_EMISSAO, TIPO_NFE, INDICACAO_PAGAMENTO, ID_EMITENTE, ID_CLIENTE, DATA_EMISSAO, DATA_TRANSMISSAO, 
                        BASE_ICMS, VALOR_ICMS, ICMS_DESONERADO, BASE_ICMS_ST, VALOR_ICMS_ST, VALOR_NFE, VALOR_FRETE, 
                        VALOR_SEGURO, VALOR_DESPESAS, VALOR_DESCONTO, VALOR_II, VALOR_IPI, VALOR_PIS, VALOR_COFINS, 
                        TOTAL_NFE, VALOR_PAGO, TROCO, TIPO_FRETE, ID_TRANSPORTADOR, QUANTIDADE_CARGA, NUMERO_VOLUME, 
                        ESPECIE_CARGA, MARCA_CARGA, PESO_LIQUIDO, PESO_BRUTO, OBSERVACOES, RETORNO_NFE, ERRO_ROTINA
                    FROM NFE
                    WHERE 1 = 1
                """
                #WHERE 1 = 1 AND DATA_EMISSAO >= %s AND DATA_EMISSAO >= (CURDATE() - INTERVAL 2 DAY)

                with connections['Smc_Light'].cursor() as cursor:

                    #LOCALIZA ENVENTOS DO TIPO NFCE
                    if (parametro.Mod_Sincron_Nfce == 'Enviadas'):
                        situacao_nfce = " STATUS_NFCE IN ('AUTORIZADA','INUTILIZADA','CANCELADA') "

                    if (parametro.Mod_Sincron_Nfce == 'Pendentes'):
                        situacao_nfce = " STATUS_NFCE = 'PENDENTE' "

                    if (parametro.Mod_Sincron_Nfce == 'Contigencia'):
                        situacao_nfce = " TIPO_EMISSAO = 'CONTINGENCIA' "

                    if (parametro.Mod_Sincron_Nfce == 'Erro'):
                        situacao_nfce = " ERRO_ROTINA != 'NENHUM' "

                    query_nfce = query_nfce + situacao_nfce

                    print(query_nfce)
                    cursor.execute(query_nfce, [parametro.Data_Inicial_Sinc])
                    cursor.execute(query_nfce, [])

                    for lista in cursor.fetchall():
                        if (lista[19] != 'NENHUM'):
                            status_registro = lista[19]
                        else:
                            status_registro = lista[17] 

                        dados_array.append({
                            'Id_Tab_Orig': lista[0],
                            'Data_Emissao': lista[1],
                            'Data_Criacao_Evento': date.today(),
                            'Tipo_Doc_Fiscal': 'NFCE',
                            'Num_Doc': lista[20],
                            'Serie_Dov': lista[13],
                            'Registro_Sincronizado': 'Nao',
                            'Status_Doc': status_registro
                    })

                    #LOCALIZA ENVENTOS DO TIPO NFE
                    if (parametro.Mod_Sincron_Nfe == 'Enviadas'):
                        situacao_nfe = " STATUS_NFE IN ('AUTORIZADA','INUTILIZADA','CANCELADA') "

                    if (parametro.Mod_Sincron_Nfe == 'Pendentes'):
                        situacao_nfe = " STATUS_NFE = 'PENDENTE' "

                    if (parametro.Mod_Sincron_Nfe == 'Contigencia'):
                        situacao_nfe = " TIPO_EMISSAO = 'CONTINGENCIA' "

                    if (parametro.Mod_Sincron_Nfe == 'Erro'):
                        situacao_nfe = " ERRO_ROTINA != 'NENHUM' "

                    query_nfe = query_nfe + situacao_nfe

                    #print(query_nfe)
                    #cursor.execute(query_nfc, [parametro.Data_Inicial_Sinc])
                    cursor.execute(query_nfe, [])

                    for lista_nfe in cursor.fetchall():
                        if (lista_nfe[19] != 'NENHUM'):
                            status_registro = lista_nfe[19]
                        else:
                            status_registro = lista_nfe[17] 

                        dados_array.append({
                            'Id_Tab_Orig': lista_nfe[0],
                            'Data_Emissao': lista_nfe[15],
                            'Data_Criacao_Evento': date.today(),
                            'Tipo_Doc_Fiscal': 'NFE',
                            'Num_Doc': lista_nfe[1],
                            'Serie_Dov': lista_nfe[4],
                            'Registro_Sincronizado': 'Nao',
                            'Status_Doc': status_registro
                    })
                
                #print(parametro.Sistema_Sincronizacao)

            atu = 0
            novo = 0
            naim = 0
            #print('cris', dados_array)
            for item in dados_array:

                try:

                    busca_evento = Eventos.objects.get(Id_Tab_Orig=item['Id_Tab_Orig'])

                    if busca_evento != None:
                        if busca_evento.Data_Criacao_Evento != item['Data_Criacao_Evento'] or busca_evento.Status_Doc != item['Status_Doc']:
                            busca_evento.Data_Criacao_Evento   = item['Data_Criacao_Evento']
                            busca_evento.Tipo_Doc_Fiscal       = item['Tipo_Doc_Fiscal']
                            busca_evento.Data_Emissao          = item['Data_Emissao']
                            busca_evento.Num_Doc               = item['Num_Doc']
                            busca_evento.Serie_Dov             = item['Serie_Dov']
                            busca_evento.Status_Doc            = item['Status_Doc']
                            busca_evento.Id_Tab_Orig           = item['Id_Tab_Orig']
                            busca_evento.Registro_Sincronizado = item['Registro_Sincronizado']
                            busca_evento.save() 
                            atu = atu + 1
                        else:
                            naim = naim + 1
                except Eventos.DoesNotExist:
                    novo_evento = Eventos()
                    novo_evento.Data_Criacao_Evento   = item['Data_Criacao_Evento']
                    novo_evento.Tipo_Doc_Fiscal       = item['Tipo_Doc_Fiscal']
                    novo_evento.Data_Emissao          = item['Data_Emissao']
                    novo_evento.Num_Doc               = item['Num_Doc']
                    novo_evento.Serie_Dov             = item['Serie_Dov']
                    novo_evento.Status_Doc            = item['Status_Doc']
                    novo_evento.Id_Tab_Orig           = item['Id_Tab_Orig']
                    novo_evento.Registro_Sincronizado = item['Registro_Sincronizado']
                    novo_evento.save()
                    novo = novo + 1
                    
    except Exception as e:
        print('erro:', e)
        return 'Processado com Erro'
    #print('atu', atu,'novo', novo, 'naim', naim)

    #return redirect('index')
    return 'Sucesso'

@login_required(login_url='login')
def parametro(request):
    if str(request.user) != 'AnonymousUser':

        try:
            parametro_instance = Parametros_Gerais.objects.get(id=1)
        except Parametros_Gerais.DoesNotExist:
            parametro_instance = None

        if request.method == 'POST':
            form = Parametros_GeraisModelForm(request.POST, instance=parametro_instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'Salvo com sucesso')
                #form = Parametros_GeraisModelForm()
            else:
                messages.error(request, 'Erro ao salvar')
            
        else:
            form = Parametros_GeraisModelForm(instance=parametro_instance)
        
        context = {
            'form': form
        }
        
        return render(request, 'parametro_gerais.html', context)
    else:
        return redirect('index')

@login_required(login_url='login')
def contato(request):
    if str(request.user) != 'AnonymousUser':
        
        try:
            contato_instance = Contato_Empresa.objects.get(id=1)
        except Contato_Empresa.DoesNotExist:
            contato_instance = None

        print('eu')
        if request.method == 'POST':
            form = Contato_EmpresaModelForm(request.POST, instance=contato_instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'Salvo com sucesso')
                #form = Parametros_GeraisModelForm()
            else:
                messages.error(request, 'Erro ao salvar')
            
        else:
            form = Contato_EmpresaModelForm(instance=contato_instance)
        
        context = {
            'form': form
        }
        
        return render(request, 'contato_empresa.html', context)
    else:
        return redirect('index')