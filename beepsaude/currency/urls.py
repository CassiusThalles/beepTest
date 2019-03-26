from django.urls import path
from . import views

app_name = 'currency'
urlpatterns = [
    path('', views.MyView.as_view(), name="myview"),
    path('test/', views.Index.as_view(), name="test"),
]