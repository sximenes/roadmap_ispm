#python
from decimal import Decimal
#django
import unittest
#project
from produtospec.models import *


class ProductTestCase(unittest.TestCase):
    '''
    Conter todos os testes do modelo Product
    '''
    #fixtures = ['products_testdata.json']

    def test_index(self):
        '''
        Testando a criao dos objetos com o metodo create do django.
        '''
        product_spec01 = ProductSpec.objects.create(
            name = 'Camiseta')
        product_spec02 = ProductSpec.objects.create(
            name= 'Caixas')

        assert product_spec01 is not None
        assert product_spec02 is not None

        product01 = Product.objects.create(
            name = 'MegaBoga',
            price = Decimal('23.20'),
            product_spec = product_spec01)
        
        product02 = Product.objects.create(
            name = 'Caixa Vazia',
            price = '0.00',
            product_spec = product_spec02)

        assert product01 is not None
        assert product02 is not None

        feature01 = Feature.objects.create(
            name = 'Cor',
            description = 'Define a cor do produto',
            product_spec = product_spec01)
    
        feature02 = Feature.objects.create(
            name='Peso',
            description = 'Define o peso do produto',
            product_spec = product_spec02)

        assert feature01 is not None
        assert feature02 is not None        

        feature_value01 = FeatureValue.objects.create(
            value = 'Vermelho',
            feature = feature01,
            product = product01)
        
        feature_value02 = FeatureValue.objects.create(
            value = '20kg',
            feature = feature02,
            product = product02)

        assert feature_value01 is not None
        assert feature_value02 is not None


    def test_product_feature(self):
        '''
        As features_values definidos  para um produto devem pertencer a 
        lista de features do produto_spec.
        '''
        
        product01 = Product.objects.get(pk=2)
        feature01 = Feature.objects.get(pk=1)
        feature02 = Feature.objects.get(pk=2)

        assert product01 is not None
        assert feature01 is not None
        assert feature02 is not None

        self.assertTrue(product01.feature_is_valid(feature01))
        self.assertFalse(product01.feature_is_valid(feature02))
               

