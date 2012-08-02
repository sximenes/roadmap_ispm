#python
from decimal import Decimal
#django
from django.test import TestCase
#project
from produtospec.models import *


class ProductTestCase(TestCase):
    '''
    Conter todos os testes do modelo Product
    '''
    def test_index(self):
        '''
        Testando a criao dos objetos com o metodo create do django.
        '''
        product_spec01 = ProductSpec.objects.create(
            name = 'Camiseta MegaBoga')
        
        product01 = Product.objects.create(
            name = 'Camiseta MegaBoga',
            price = Decimal('23.20'),
            product_spec = product_spec01)
        
        feature01 = Feature.objects.create(
            name = 'Feature 1',
            description = 'Isso e um teste de feature',
            product_spec = produto_spec01)
        
        feature_value01 = FeatureValue.objects.create(
            value = Decimal('12.31'),
            feature = feature01,
            product = product01)
