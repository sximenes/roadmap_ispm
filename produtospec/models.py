from django.db import models


class Product(models.Model):
    '''
    Classe que define um produto.
    ex. {
            'Camiseta MegaBoga',
            23,00,
            <<camiseta>>
        }
    '''
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    product_spec = models.ForeignKey('ProductSpec')

    def feature_is_valid(self, feature):
        '''
        Recebe uma feature e verifica se o product_spec do produto e o mesmo
        da feature passada
        '''
        valid_features = Feature.objects.filter(product_spec=self.product_spec)
        if feature.product_spec != self.product_spec:
            return False
        return True


class ProductSpec(models.Model):
    '''
    Classe que define um tipo/especificao de produto
    ex.
        {
            'camiseta'
        }
    ''' 
    name = models.CharField(max_length=200)
 

class Feature(models.Model):
    '''
    Classe que define uma caracteristica de uma especificacao de produto
    ex.
        {
            'Cor',
            'Define a cor do produto',
            <<camiseta>>
        }
    '''
    name = models.CharField(max_length=200)
    description = models.TextField()
    product_spec = models.ForeignKey('ProductSpec')


class FeatureValue(models.Model):
    '''
    Classe que define o valor de uma determinada caracteristica de produto em um produto especifico
    ex.
        {
            'Vermelho',
            <<cor>>,
            <<Camiseta MegaBoga>>
        }
    
    obs. As features escolhidas devem pertencer ao grupo de features do produto_spec do produto
    '''
    value = models.CharField(max_length=200)
    feature = models.ForeignKey('Feature')
    product = models.ForeignKey('Product')

