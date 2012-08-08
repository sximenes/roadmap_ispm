import re

from django.core.paginator import Paginator

from piston.handler import BaseHandler
from piston.utils import rc, require_mime

from produtospec.models import *


class ProductHandler(BaseHandler):
    allowed_methods = ('GET','POST',)
    model = Product
    fields = ('name', 'price', 
        ('product_spec', 
            (
                'name', 
                ('features', 
                    ('name', 'description',
                        ('feature_values',('value'),),
                    )
                ),
            )
        ),)

    def read(self, request, page=1, id=None):
        '''
        Pode receber uma pagina e um id de product, caso, nao
        receba nenhum id de product, sera retornado todos os product.
        '''
        if id:
            try:
                product = Product.objects.get(id=id)
            except Product.DoesNotExist:
                return rc.NOT_FOUND
            return product

        else:
            objects_list = Product.objects.all()
            objects_paginator = Paginator(objects_list)
            products_list = objects_paginator.page(page)
        
            return products_list

    #@require_mime('json',)
    def create(self, request):
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
                                'features_values': [value: 'Verde'},]
                            },],
                        }
                    }
        '''

        if not request.content_type:
            super(ExpressiveTestModel, self).create(request)
        
        product_dict = request.data
        if self.exists(**product_dict):
            return rc.DUPLICATE_ENTRY

        if not product_dict:
            return rc.BAD_REQUEST

        p_spec = product_dict.get('product_spec')
        name_product_spec = p_spec.get('name')
        if not name_product_spec:
            return rc.BAD_REQUEST

        product_spec, created = ProductSpec.objects.get_or_create(
            name=name_product_spec, 
            defaults={'name': name_product_spec})

        product = Product.objects.create(
            name=product_dict.get('name'),
            price=product_dict.get('price'),
            product_spec=product_spec)
        
        #criando os Features e Features values para o product_spec
        features_list = p_spec.get('features')
        if not features_list:
            return rc.BAD_REQUEST
        #separando as features validas e nao validas
        for feature_dict in features_list:
            #validando as features

            name_feature = feature_dict.get('name')
            description_feature = feature_dict.get('description')

            feature, created = Feature.objects.get_or_create(
                name=name_feature, product_spec=product_spec, 
                defaults={
                    'name': name_feature,
                    'description': description_feature,
                    'product_spec':product_spec})
            
            if not created:
                feature.descriotion = description_feature
                feature.save()

            if not product.feature_is_valid(feature):
                return rc.BAD_REQUEST
            else:
                #atualizando o  value do feature para esse product
                for feature_value_dict in feature_dict.get(
                    'features_values', []):
                    value = dict_feature_value.get('value')
                    feature_value, created = FeatureValue.objects.get_or_create(
                        feature=feature, product=product,
                        defaults={
                            'value': value,
                            'feature': feature,
                            'product': product})
                    if not created:
                        feature_value.value = value
                        feature_value.save()
        if not product: 
            return rc.BAD_REQUEST
        else:
            return rc.CREATED


#class ProductSpecHandler(BaseHandler):

