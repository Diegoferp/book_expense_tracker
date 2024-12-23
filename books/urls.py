from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import CustomLoginView
from django.views.generic import TemplateView

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),  # Login route
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),  # Logout route
    path('dashboard/', views.dashboard, name='dashboard'),
    path('books/', views.books_list, name='books'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/edit/<str:pk>/', views.edit_book, name='edit_book'),  # Change <int:pk> to <str:pk>
    path('books/delete/<str:pk>/', views.delete_book, name='delete_book'),  # Change <int:pk> to <str:pk>
    path('login/', CustomLoginView.as_view(), name='login'),  # Login route
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),  # Logout route
    path('privacy-policy/', TemplateView.as_view(template_name="privacy-policy.html"), name='privacy-policy'),
    path('terms-of-service/', TemplateView.as_view(template_name="terms-of-service.html"), name='terms-of-service'),
]
