from django.urls import path

from ..data import views

urlpatterns = [
    path('save_one', views.save_one),
    path('save_many', views.save_many),
    path('update_many', views.update_many),
    path('delete_one', views.delete_one),
    path('delete_many', views.delete_many),
    path('find_one', views.find_one),
    path('find_many', views.find_many),
    path('meta', views.meta),

]
