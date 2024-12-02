from django.db import models
from django.contrib.auth.models import User

class GameSession(models.Model):
    name = models.CharField(max_length=100)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hosted_games")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    words_used = models.ManyToManyField('Word', blank=True)  # Track used words
    words_attempted = models.ManyToManyField('Word', related_name='games_attempted', blank=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name="players")
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in {self.game_session.name}"

class Word(models.Model):
    text = models.CharField(max_length=100)  # Word to transcribe
    correct_transcription = models.CharField(max_length=100)

    def __str__(self):
        return self.text

class PlayerScore(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    time_taken = models.FloatField(default=0.0)  # Time to complete the transcription

    def __str__(self):
        return f"{self.player.user.username}'s score in {self.game_session.name}"

class UsedWord(models.Model):
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name="used_words")
    word = models.ForeignKey(Word, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.word.text} in {self.game_session.name}"