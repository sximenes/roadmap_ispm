#python
import unittest
import mock
#django
from django.utils import simplejson
from piston.utils import rc
#project
from produtospec.models import *
from api.handler import *

__all__ = ['HandlerProductSpecTestCase', 'HandlerProductTestCase']


class HandlerProductSpecTestCase(unittest.TestCase):
    '''
    Conter tosos os testes de ProductSpec na api
    '''

    @mock.patch.object(ProductSpec, 'objects')
    def test_read_with_id(self, objects_mock):
        '''
        Garantir que ao chamar o metodo read do ProductSpecHandler,
        o mesmo chame o metodo get do objects passando um id como
        parametro.
        '''
        id = 1
        handler = ProductSpecHandler()
        request = mock.Mock()
        request.META = {'CONTENT_TYPE': 'application/json'}
        request.content_type = 'aplication/json'
        request.data = {'id': id}
        objects_mock.get = mock.Mock()
        objects_mock.get.return_value = Product()
        handler = ProductSpecHandler()
        handler.read(request)
        objects_mock.get.assert_called_with(id=id)
        self.assertTrue(objects_mock.get.called)

    @mock.patch.object(ProductSpec, 'objects')
    def test_read_without_id(self, objects_mock):
        '''Garantir que ao chamar o metodo read do ProductSpecHandler
        sem passar um id o mesmo deve chamar o metodo all do objects.'''

        request = mock.Mock()
        request.META = {'CONTENT_TYPE': 'application/json'}
        request.content_type = 'aplication/json'
        request.data = {}
        objects_mock.get = mock.Mock()
        objects_mock.get.return_value = Product()
        objects_mock.all = mock.Mock()
        objects_mock.all.return_value = []
        handler = ProductSpecHandler()
        handler.read(request)
        self.assertTrue(objects_mock.all.called)
        self.assertFalse(objects_mock.get.called)

    @mock.patch('produtospec.models.ProductSpec')
    def test_create(self, ProductSpecMock):
        pass


class HandlerProductTestCase(unittest.TestCase):
    '''
    Conter todos os testes de Product na api
    '''

    def test_create(self):
        '''Testando se o retorno do metodo create e igual ao codigo
        rc.CREATED do piston'''
        product_dict = {
            'name': 'Camiseta Mega Boga',
            'price': '20.30',
            'product_spec': {
                'name': 'Camiseta',
                'features': [
                    {
                        'name': 'Cor',
                        'description': 'Produto com varias cores',
                        'feature_value': [
                            {'value': 'Verde'},
                            {'value': 'Laranja'},
                        ]
                    }
                ]
            }
        }
        handler = ProductHandler()
        request = mock.Mock()
        request.META = {'CONTENT_TYPE': 'application/json'}
        request.content_type = 'aplication/json'
        request.data = product_dict
        resp = handler.create(request)
        self.assertEqual(resp.content, rc.CREATED.content)

    def test_bad_request(self):
        '''
        Testando o retorno do metodo create para quando e passado
        um dicionario invalido, o retorno deve ser o codigo para
        BAD_REQUEST
        '''
        product_dict = {
            'name': 'Camiseta Mega Boga',
            'price': '20.30',
            'product_spec':
            {
                'name': 'Camiseta',
                'features': []
            }
        }

        handler = ProductHandler()
        request = mock.Mock()
        request.META = {'CONTENT_TYPE': 'application/json'}
        request.content_type = 'application/json'
        request.data = product_dict

        #verificando se ao passar os parametros errados
        #retorna o codigo de erro correto.
        resp = handler.create(request)
        self.assertEqual(
            resp.content, rc.BAD_REQUEST.content)

    @mock.patch.object(Product, 'objects')
    def test_read_without_id(self, objects_mock):
        '''
        Garantir que quando a chamada do metodo for feita sem um id,
        o retorno seja uma lista de Product
        '''

        list_objects = []

        request = mock.Mock()
        request.META = {'CONTENT_TYPE': 'application/json'}
        request.content_type = 'application/json'
        request.data = {}

        objects_mock.all = mock.Mock()
        objects_mock.all.return_value = list_objects
        handler = ProductHandler()
        products = handler.read(request)
        self.assertFalse(objects_mock.get.called)
        self.assertTrue(objects_mock.all.called)
        self.assertEqual(products, list_objects)

    @mock.patch.object(Product, 'objects')
    def test_read_with_id(self, objects_mock):
        '''
        Garantir que quando a chamada for feita passando um id
        apenas um product sera retornado.
        '''
        id = 1
        request = mock.Mock()
        request.META = {'CONTENT_TYPE': 'application/json'}
        request.content_type = 'application/json'
        request.data = {'id': id}
        product = Product()
        objects_mock.get = mock.Mock()
        objects_mock.get.return_value = product
        handler = ProductHandler()
        handler.read(request)
        objects_mock.get.assert_called_with(id=id)
        self.assertTrue(objects_mock.get.called)
        self.assertFalse(objects_mock.all.called)
