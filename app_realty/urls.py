from django.urls import path
from . import views

urlpatterns = [
    path('', views.HouseList.as_view(), name='main'),
    path('realty/myadv/', views.MyHouseList.as_view(), name='my_house'),
    path('realty/<int:pk>/', views.HouseDetail.as_view(), name='house_detail'),
    path('realty/<int:pk>/edit/', views.HouseEdit.as_view(), name='house_edit'),
    path('realty/<int:pk>/delete/', views.HouseDelete.as_view(), name='house_delete'),
    path('realty/add/', views.HouseCreate.as_view(), name='house_create'),
    path('realty/foto/<int:pk>/delete/', views.HouseFotoDelete.as_view(), name='delete_foto'),
]
