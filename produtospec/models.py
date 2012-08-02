from django.db import models

#Default configs
DECIMAL = {'max_digits':5, 'decimal_places':2}

class Product(models.Model):
    '''
    Classe que define um produto.
    '''
    name = models.CharField(max_length=200)
    price = models.DecimalField(**DECIMAL)
    product_specs = models.ForeignKey('ProductSpec')


class Feature(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    products_specs = models.ForeignKey('ProductSpec')


class FeatureValue(models.Model):
    value = models.DecimalField(**DECIMAL)
    features = models.ForeignKey('Feature')
    products = models.ForeignKey('Product')


class ProductSpec(models.Model):
    '''
    Classe que define um especifical de produto
    ''' 
    name = models.CharField(max_length=200)
    

