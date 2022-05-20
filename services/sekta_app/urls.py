from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('welcome/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('my_sekts/',views.list_user_sekts,name='my-sekts'),
    path('create_sekta',views.create_sekta,name='create-sekta'),
    path('sekta/<int:id>',views.show_sekta,name='show-sekta'),
    path('sekta/<int:id>/invite',views.invite_to_sekta,name='sekta-invite'),
    path('invite',views.invite_sektant,name='invite-sektant')
]