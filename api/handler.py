from django.core.paginator import Paginator
from django.utils import simplejson
from piston.handler import BaseHandler

from produtospec.models import Product, ProductSpec


class ProductHandler(BaseHandler):
    allowed_methods = ('GET','POST',)
    model = Product
    fields = ('name', 'price', 
    ('product_spec', ('name',)))
    exclude = ('id',)

    def read(self, request, *arga, **kwargs):
       '''
        Retorna um json com uma lista de products paginados,
        o metodo espera uma inteiro que vai derterminar em 
        que paqina esta sendo consultada.
        Retorna uma lista de QuerySets ou None em caso de falha
        '''
        page = kwargs.get('page', 1) 
        objects_list = Project.objects.all()
        objects_paginator = Paginator(objects_list)

        products_list = objects_paginator.page(page)
        
        #@TODO: Ver como retornar json
        return simplejson.dumps(products_list)

    @require_mime('json',)
    def create(self, request, *args, **kwargs):
        '''
        Cria um product com base em um json recebido,
        o json deve conter a seguinte estrutura:
            obj = {
                    'name': 'Camiseta MegaBoga',
                    'price': '21.31',
                    'product_spec': {
                        'name': 'Camiseta'
                        'features': [
                            {
                                'name': 'Cor',
                                'description': 'bla',
                                'features_values': [
                                    {
                                        'value':'Verde',
                                    }
                                ]
                            }],
                        }
                  }
        '''
        product_dict = simplejson.load(request.POST.get('product', None))
        if not product_dict:
            return None
        
        p_spec = product_dict.get('product_spec')
        p_spec_name = p_spec.get('name')

        try:
            product_spec = ProductSpec.objects.get(name=p_spec_name)
        except ProductSpec.DoesNotExist:
            product_spec = ProductSpec.objects.create(
                name=p_spec_name)

        if not product_spec:
            return None

        product = Product.objects.create(
            name=product_dict.get('name'), 
            price=product_dict.get('price'),
            product_spec=product_spec)
        
        #criando os Features e Features values para o product_spec
        features_list = p_spec.get('features')
        for feature_dict in features_list:
            feature = 
        



class ProductSpecHandler(BaseHandler):

