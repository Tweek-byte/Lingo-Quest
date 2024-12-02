from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('create/', views.create_game, name='create_game'),
    path('join/<int:game_id>/', views.join_game, name='join_game'), 
    path('lobby/<int:game_id>/', views.game_lobby, name='game_lobby'),
    path('<int:game_id>/submit/', views.submit_transcription, name='submit_transcription'),
    path('<int:game_id>/start/', views.start_game, name='start_game'),
    path('scoreboard/<int:game_id>/', views.scoreboard, name='scoreboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
