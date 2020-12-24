from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.mediaHome, name='MediaHome'),
    path('media/add', views.addItem, name='AddMedia'),
    path('media/edit', views.editItem, name='EditMedia'),
    path('media/delete', views.deleteItem, name='DeleteMedia'),
    path('media/view/<str:mediatype>', views.displayItem, name='DisplayMedia'),
    path('media/view', views.displayItem, name='DisplayMedia'),
]
