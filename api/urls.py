#django
from django.conf.urls import patterns, include, url
from piston.resource import Resource
#projects
from api.handler import ProductHandler

product_handler = Resource(ProductHandler)

urlpatterns = patterns('api.handler',
    url(r'product/create/$', product_handler.create ),
)
