from django.test import TestCase

from produtospec.models import *

class ProductTestCase(TestCase):
    '''
    Classe onde deve conter todos os testes do modelo Product
    '''
    def test_get_all(self):
        instace = Product.objects.all()
        self.assertIs(product)

    def teste_instance(self):
        self.assertTrue(1==2)
