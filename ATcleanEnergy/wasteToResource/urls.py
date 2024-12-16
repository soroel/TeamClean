from django.urls import path

from . import views

# urlpatterns = [
#     path("", views.index, name="index"),
# ]
urlpatterns = [
    path('list/', views.list_waste, name='list_waste'),
    path('browse/', views.browse_waste, name='browse_waste'),
    path('claim/<int:waste_id>/', views.claim_waste, name='claim_waste'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/', views.view_profile, name='view_profile'),
    path('', views.homepage, name='homepage'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
]