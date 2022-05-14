from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('my_sekts/',views.list_sekts_created_by_user,name='my-sekts'),
    path('create_sekta',views.create_sekta,name='create-sekta'),
    path('sekta/<int:id>',views.show_sekta,name='show-sekta')
]