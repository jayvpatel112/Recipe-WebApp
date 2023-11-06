from django.urls import path
from . import views

urlpatterns = [
    path("recipes/", views.recipes, name='recipes'),
    path('delete-recipe/<id>', views.delete_recipe, name='delete-recipe'),
    path('update-recipe/<id>', views.update_recipe, name='update-recipe'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_page, name='logout')
]

