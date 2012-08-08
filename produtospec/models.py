from django.db import models

__all___ = ['Product', 'ProductSpec', 'Feature', 'FeatureValue']


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
    product_spec = models.ForeignKey('ProductSpec', related_name='products')

    def feature_is_valid(self, feature):
        '''
        Recebe uma feature e verifica se o product_spec do produto 
        e o mesmo da feature passada
        '''
        valid_features = Feature.objects.filter(
            product_spec=self.product_spec)
        if feature.product_spec != self.product_spec:
            return False
        return True

    def __unicode__(self):
        return self.name
    


class ProductSpec(models.Model):
    '''
    Classe que define um tipo/especificao de produto
    ex.
        {
            'camiseta'
        }
    ''' 
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name
     


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
    product_spec = models.ForeignKey('ProductSpec', related_name='features')

    def __unicode__(self):
        return self.name


class FeatureValue(models.Model):
    '''
    Classe que define o valor de uma determinada caracteristica 
    de produto.
    ex.
        {
            'Vermelho',
            <<cor>>,
            <<Camiseta MegaBoga>>
        }
    
    obs. O product_spec da feature deve ser igual ao do produto escolhido.
    '''
    value = models.CharField(max_length=200)
    feature = models.ForeignKey('Feature', related_name='features_values')
    product = models.ForeignKey('Product', related_name='features_values')
    
    class Meta:
        unique_together = ('feature', 'product',)

    def __unicode__(self):
        return '%s-%s-%s' % (self.feature, self.product, self.value)

