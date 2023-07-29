
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index,name='index'),
    path('about',views.about,name='AboutUs'),
    path('tracker',views.tracker,name='TrackingStatus'),
    path('search',views.search,name='Search'),
    path('contact',views.contact,name='ContactUs'),
    path('product/<int:myid>',views.productView,name='ProductView'),
    path('checkout',views.checkout,name='Checkout')
]
