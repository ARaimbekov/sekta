from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('welcome/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/',views.logout,name='logout'),
    path('my_sekts/',views.list_user_sekts,name='my-sekts'),
    path('all_sekts/',views.list_all_sekts,name='all-sekts'),
    path('create_sekta/',views.create_sekta,name='create-sekta'),
    path('token/', views.join_by_token,name='token'),
    path('sekta/<int:id>/',views.show_sekta,name='show-sekta'),
    path('sekta/<int:id>/invite/',views.invite_to_sekta,name='sekta-invite'),
    path('sekta/<int:id>/invite_sektant/',views.invite_sektant,name='invite-sektant'),
    path('sekta/<int:id>/sacrifice/',views.sacrifice,name='sekta-sacrifice'),
    path('sekta/<int:id>/sacrifice_sektant/', views.sacrifice_sektant, name='sacrifice-sektant'),
]