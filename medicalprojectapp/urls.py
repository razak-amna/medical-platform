from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Use Django's LoginView
    path('profile/', views.profile, name='profile'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('payment/', views.payment_page, name='payment_page'),
    path('confirm_payment/', views.confirm_payment, name='confirm_payment'),
    # path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('doctor_profile/', views.doctor_profile, name='doctor_profile'),  # Doctor profile
    path('receptionist_profile/', views.receptionist_profile, name='receptionist_profile'),
    path('doctor/<int:doctor_id>/update/', views.update_doctor, name='update_doctor'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    # path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('logout/', views.logout_view, name='logout'),  # Use Django's LogoutView
]
