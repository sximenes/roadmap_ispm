#django
import unittest
from django.utils import simplejson
#project
from produtospec.models import Product
from api.handler import *


class HandlerTestCase(unittest.TestCase):
    '''
    Conter todos os testes da api
    '''

    def test_index(self):
    '''
    Inicializando a base de dados para os testes
    '''

    def test_create_product(self):
    '''
    Testando a criacao de um product com base no json recebido
    '''
    product_dict = {
            'name': 'Camiseta Mega Boga',
            'product_spec': {'name': 'Camiseta'},
            'price': '34.21'
        }
    product_json = simplejson.dumps(product_dict)
    
    self.assertIsNotNone(product_json)
    
    product = self.client.post('/api/product/create/', product_json)
    self.assertIsInstance(product, Product)
