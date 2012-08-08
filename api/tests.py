#python
import unittest
from mock import Mock
#django
from django.utils import simplejson
from piston.utils import rc
#project
from produtospec.models import Product
from api.handler import *


class HandlerTestCase(unittest.TestCase):
    '''
    Conter todos os testes da api
    '''

    def test_create(self):
        '''
        Testando se o retorno do metodo create e igual ao codigo
        rc.CREATED do piston
        '''
        product_json = [{
           'name': 'Camiseta Mega Boga',
           'price': '20.30',
           'product_spec': {
                    'name': 'Camiseta',
                    'features': [{
                        'name': 'Cor',
                        'description': 'Produto com varias cores',
                        'feature_value': [
                            {'value': 'Verde'},
                            {'value': 'Laranja'},]
                        }]
                    }}]

        handler = ProductHandler()
        request = Mock()
        request.META.return_value = {'CONTENT_TYPE': 'application/json'}
        request.content_type.return_value = 'aplication/json'
        request.data.return_value = product_json
        resp = handler.create(request)
        self.assertEqual(resp.content, rc.CREATED.content)
    
    def test_bad_request(self):
        '''
        Testando o retorno do metodo create para quando e passado
        um dicionario invalido, o retorno deve ser o codigo para 
        BAD_REQUEST
        '''
        product_json = [{
            'name': 'Camiseta Mega Boga',
            'price': '20.30',
            'product_spec':
                {
                    'name': 'Camiseta',
                    'features': []
                }}]
        
        handler = ProductHandler()
        request = Mock()
        request.META.return_value = {'CONTENT_TYPE': 'application/json'}
        request.content_type.return_value = 'application/json'
        request.data.return_value = simplejson.loads(product_json)

        #verificando se ao passar os parametros errados
        #retorna o codigo de erro correto.
        resp = handler.create(request)
        self.assertEqual(
            resp.content, rc.BAD_REQUEST.content)

    #def test_duplicated_product(self):
    #    '''
    #    Testa se o argumento for um dicionario contendo um product
    #    ja cadastrado se o retorno vai ser o rc.DUPLICATE_ENTRY
    #    '''
    #    
    #    product = Product.objects.get(pk=1)
        



