from django.contrib import admin
from .models import Word, PlayerScore

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('text', 'correct_transcription')
    search_fields = ('text', 'correct_transcription')

@admin.register(PlayerScore)
class PlayerScoreAdmin(admin.ModelAdmin):
    list_display = ('player', 'game_session', 'score', 'time_taken')
    search_fields = ('player__user__username', 'game_session__name')
