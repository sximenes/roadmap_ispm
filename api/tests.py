#django
import unittest
from django.utils import simplejson
from piston.utils import rc
#project
from produtospec.models import Product
from api.handler import *


class HandlerTestCase(unittest.TestCase):
    '''
    Conter todos os testes da api
    '''

    def test_create_method(self):
        '''
        Testando se o retorno do metodo create e um instancia da classe
        Product
        '''
        product_dict = {
           'name': 'Camiseta Mega Boga',
           'price': '20.30',
           'product_spec': [
                {
                    'name': 'Camiseta',
                    'features': [
                    {
                        'name': 'Cor',
                        'description': 'Produto com varias cores',
                        'feature_value': [{'value': 'Verde'},
                        {'value': 'Laranja'},]
                    }]
                },]}
        handler = ProductHandler()
        #verificando se o retorno e do tipo Product
        self.assertIsInstance(handler.create(product_dict), Product)
    
    def test_bad_request(self):
        '''
        Testando o retorno do metodo create para quando e passado
        um dicionario invalido, o retorno deve ser o codigo para 
        BAD_REQUEST
        '''
        product_list = {
            'name': 'Camiseta Mega Boga',
            'price': '20.30',
            'product_spec': [
                {
                    'name': 'Camiseta',
                    'features': []
                },]}
        
        handler = ProductHandler()
        #verificando se ao passar os parametros errados
        #retorna o codigo de erro correto.
        self.assertEqual(handler.create(product_dict), rc.BAD_REQUEST)

