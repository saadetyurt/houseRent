from django.urls import path

from . import views

urlpatterns = [
    # ex: /home/
    path('', views.index, name='index'),
    path('update/',views.user_update, name='user_update'),
    path('password/',views.change_password, name='change_password'),
    path('comments/',views.comments, name='comments'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),
    path('addhouse/', views.addhouse, name='addhouse'),
    path('houses/', views.houses, name='houses'),
    path('houseedit/<int:id>', views.houseedit, name='houseedit'),
    path('housedelete/<int:id>', views.housedelete, name='housedelete'),
    path('houseaddimage/<int:id>', views.houseaddimage, name='houseaddimage'),
]