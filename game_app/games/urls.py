from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Games
    path('games/fizzbuzz/', views.fizzbuzz_game, name='fizzbuzz_game'),
    path('games/fizzbuzz/reset/', views.fizzbuzz_reset, name='fizzbuzz_reset'),
    path('games/tictactoe/', views.tictactoe_game, name='tictactoe_game'),
    path('games/tictactoe/reset/', views.tictactoe_reset, name='tictactoe_reset'),
    
    # Leaderboard
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
