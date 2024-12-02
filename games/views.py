from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import GameSession, Player, Word, PlayerScore
import random
from django.http import JsonResponse
from django.contrib.auth import logout

@login_required
def create_game(request):
    if request.method == 'POST':
        game_name = request.POST.get('name')
        game_session = GameSession.objects.create(name=game_name, host=request.user)
        Player.objects.create(user=request.user, game_session=game_session)

        # Preselect 10 unique random words for the game session
        selected_words = Word.objects.order_by('?')[:10]  # Randomly pick 10 words
        game_session.words_used.set(selected_words)
        return redirect('game_lobby', game_id=game_session.id)
    return render(request, 'games/create_game.html')


@login_required
def join_game(request, game_id=None):
    if request.method == 'POST':
        game_id = request.POST.get('game_id')  # Retrieve the game_id from POST data
        game_session = get_object_or_404(GameSession, id=game_id)
        if not Player.objects.filter(user=request.user, game_session=game_session).exists():
            Player.objects.create(user=request.user, game_session=game_session)
        return redirect('game_lobby', game_id=game_session.id)
    return render(request, 'games/join_game.html')  # Return the join game page




@login_required
def game_lobby(request, game_id):
    game_session = get_object_or_404(GameSession, id=game_id)
    players = game_session.players.all()
    return render(request, 'games/game_lobby.html', {'game_session': game_session, 'players': players})


@login_required
def start_game(request, game_id):
    game_session = get_object_or_404(GameSession, id=game_id)

    # Fetch the first unused word
    used_word_ids = game_session.words_attempted.values_list('id', flat=True)
    next_word = game_session.words_used.exclude(id__in=used_word_ids).first()

    if not next_word:
        return redirect('scoreboard', game_id=game_id)

    return render(request, 'games/play_game.html', {'game_session': game_session, 'word': next_word})


@login_required
def submit_transcription(request, game_id):
    if request.method == 'POST':
        game_session = get_object_or_404(GameSession, id=game_id)
        player = get_object_or_404(Player, user=request.user, game_session=game_session)

        word_id = request.POST.get('word_id')
        transcription = request.POST.get('transcription')
        time_taken = float(request.POST.get('time_taken', 0.0))

        word = get_object_or_404(Word, id=word_id)
        player_score, _ = PlayerScore.objects.get_or_create(player=player, game_session=game_session)

        # Check the transcription
        if word.correct_transcription.lower() == transcription.lower():
            player_score.score += 10  # Increment score for correct answer
        player_score.time_taken += time_taken
        player_score.save()

        # Mark the word as attempted
        game_session.words_attempted.add(word)

        # Check if all 10 words have been used
        if game_session.words_attempted.count() >= 10:
            return JsonResponse({
                'success': True,
                'game_over': True,
                'redirect_url': f'/games/scoreboard/{game_id}/',
            })

        # Fetch the next unused word
        unused_words = game_session.words_used.exclude(
            id__in=game_session.words_attempted.values_list('id', flat=True)
        )
        next_word = unused_words.first()

        return JsonResponse({'success': True, 'next_word': next_word.text, 'word_id': next_word.id})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})

@login_required
def scoreboard(request, game_id):
    game_session = get_object_or_404(GameSession, id=game_id)
    scores = PlayerScore.objects.filter(game_session=game_session).order_by('-score', 'time_taken')
    return render(request, 'games/scoreboard.html', {'game_session': game_session, 'scores': scores})

def custom_logout(request):
    logout(request)  # This logs the user out
    return redirect('home') 