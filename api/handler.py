import re
from django.core.paginator import Paginator
from django.utils import simplejson
from piston.handler import BaseHandler

from produtospec.models import Product, ProductSpec


class ProductHandler(BaseHandler):
    allowed_methods = ('GET','POST',)
    model = Product
    fields = ('name', 'price', 
    ('product_spec', ('name',)))
    exclude = ('id', re.compile(r'^private_'))

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
                        'name': '',
                        'features': [
                            {
                                'name': 'Cor',
                                'description': 'Alguma coisa',
                                'feature_value': [value: 'Verde'},]
                            },],
                        }
                    }
        '''
        product_dict = simplejson.load(request.POST.get('product', None))
        if not product_dict:
            return None
        p_spec = product_dict.get('product_spec')
        name_product_spec = p_spec.get('name')
        if not name_product_spec:
            return None

        product_spec, created = ProductSpec.objects.get_or_create(
            name=name_product_spec, defaults={'name': name_product_spec})

        product = Product.objects.create(
            name=product_dict.get('name'),
            price=product_dict.get('price'),
            product_spec=product_spec)
        
        #criando os Features e Features values para o product_spec
        features_list = p_spec.get('features')
        
        #separando as features validas e nao validas
        list_invalid_features = []
        list_valid_features = []

        for feature_dict in features_list:
            #validando as features

            name_feature = feature_dict.get('name')
            description_feature = feature_dict.get('description')

            feature, created = Feature.objects.get_or_create(name=name_feature, product_spec=product_spec, 
                defaults={
                    'name': name_feature,
                    'description': description_feature,
                    'product_spec':product_spec})
            
            if not created:
                feature.descriotion = description_feature
                feature.save()

            if not product.is_valid_feature(feature):
                list_invalid_feature.append(feature)
            else:
                list_valid_feature.append(feature)
                #atualizando o  value do feature para esse product
                for feature_value_dict in feture_dict.get('features_values', []):
                    value = dict_feature_value.get('value')
                    feature_value, created = FeatureValue.objects.get_or_create(feature=feature, product=product,
                        defaults={
                            'value': value,
                            'feature': feature,
                            'product': product})
                    if not created:
                        feature_value.value = value
                        feature_value.save()


#class ProductSpecHandler(BaseHandler):

