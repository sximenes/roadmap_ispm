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
    
    #def create_by_json(self, product_dict):
    #'''
    #Recebe um dicionario contendo as informacoes do produto e
    #crua um product com as informacoes, desde que elas sejam validas.
    #Retorna uma instancia de product em caso de sucesso ou 
    #None em caso de falha.
    #'''
    #if not product_dict:
    #    return False


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
    product_spec = models.ForeignKey('ProductSpec')

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
    feature = models.ForeignKey('Feature')
    product = models.ForeignKey('Product')
    
    class Meta:
        unique_together = ('feature', 'product',)

    def __unicode__(self):
        return '%s-%s-%s' % (self.feature, self.product, self.value)
