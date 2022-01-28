from django.http import JsonResponse
from django.template.context import Context
from django_tables2 import RequestConfig

###############################################################################

def datagrid_configure(request, tabela):

    print('sfdsfd')

    request.GET._mutable = True

    request.GET['per_page'] = int(request.GET.get('pagination[perpage]', '10'))
    request.GET['page'] = int(request.GET.get('pagination[page]', '1'))

    print('sfdsfd')

    sort = request.GET.get('sort[sort]', 'asc')
    if sort == 'asc':
        request.GET['sort'] = request.GET.get('sort[field]')
    else:
        request.GET['sort'] = '-' + request.GET.get('sort[field]')

    request.GET._mutable = False

    print('sfdsfd')

    print('re', request)
    print('tb',tabela)
    RequestConfig(request).configure(tabela)

def datagrid_configure2(request, tabela):

    request.GET._mutable = True

    request.GET['per_page'] = int(request.GET.get('datatable[pagination][perpage]', '10'))
    request.GET['page'] = int(request.GET.get('datatable[pagination][page]', '1'))

    sort = request.GET.get('datatable[sort][sort]', 'asc')
    if sort == 'asc':
        request.GET['sort'] = request.GET.get('datatable[sort][field]')
    else:
        request.GET['sort'] = '-' + request.GET.get('datatable[sort][field]')

    request.GET._mutable = False

    RequestConfig(request).configure(tabela)

###############################################################################

def datagrid(request, tabela, context_base = {}):

    context = Context(context_base)
    context.update({'table': tabela})

    tabela.context = context
    tabela.before_render(request)
    pagina_solicitada = int(request.GET.get('page', '1'))
    meta = {}

    if tabela._order_by:
        if tabela._order_by[0][0] == '-':
            meta['sort'] = 'desc'
            meta['field'] = tabela._order_by[0][1:]
        else:
            meta['sort'] = 'asc'
            meta['field'] = tabela._order_by[0]

    if tabela.paginator.per_page > 0:
        meta['perpage'] = tabela.paginator.per_page
    else:
        meta['perpage'] = -1

    meta['total'] = tabela.paginator.count
    meta['pages'] = tabela.paginator.num_pages
    meta['page'] = min(tabela.paginator.num_pages, pagina_solicitada)

    data = []
    try:
        for linha in tabela.page.object_list:
            atual = {}

            for coluna, celula in linha.items():        
                atual[str(coluna.name)] = str(celula)

            data.append(atual)
    finally:
        del tabela.context
        context.pop()

    return JsonResponse({'meta': meta, 'data': data})

###############################################################################

def datagrid2(request, tabela, tabela2, context_base = {}):

    context = Context(context_base)
    
    context.update({'table': tabela, 'table2': tabela2})

    tabela.context = context
    tabela.before_render(request)
    tabela2.context = context
    tabela2.before_render(request)

    pagina_solicitada = int(request.GET.get('page', '1'))

    meta = {}
    meta2 = {}

    if tabela._order_by:
        if tabela._order_by[0][0] == '-':
            meta['sort'] = 'desc'
            meta['field'] = tabela._order_by[0][1:]
        else:
            meta['sort'] = 'asc'
            meta['field'] = tabela._order_by[0]

    if tabela.paginator.per_page > 0:
        meta['perpage'] = tabela.paginator.per_page
    else:
        meta['perpage'] = -1

    meta['total'] = tabela.paginator.count
    meta['pages'] = tabela.paginator.num_pages
    meta['page'] = min(tabela.paginator.num_pages, pagina_solicitada)

    if tabela2._order_by:
        if tabela2._order_by[0][0] == '-':
            meta2['sort'] = 'desc'
            meta2['field'] = tabela2._order_by[0][1:]
        else:
            meta2['sort'] = 'asc'
            meta2['field'] = tabela2._order_by[0]

    if tabela2.paginator.per_page > 0:
        meta2['perpage'] = tabela2.paginator.per_page
    else:
        meta2['perpage'] = -1

    meta2['total'] = tabela2.paginator.count
    meta2['pages'] = tabela2.paginator.num_pages
    meta2['page'] = min(tabela2.paginator.num_pages, pagina_solicitada)

    data = []
    data2 = []
    try:
        for linha in tabela.page.object_list:
            atual = {}

            for coluna, celula in linha.items():        
                atual[str(coluna.name)] = str(celula)

            data.append(atual)
        for linha in tabela2.page.object_list:
            atual2 = {}

            for coluna, celula in linha.items():        
                atual2[str(coluna.name)] = str(celula)

            data2.append(atual2)
    finally:
        del tabela.context
        del tabela2.context
        context.pop()

    return JsonResponse({'meta': meta, 'data': data, 'meta2': meta, 'data2': data})

###############################################################################