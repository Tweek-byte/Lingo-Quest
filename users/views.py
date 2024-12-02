from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from games.models import GameSession, Player, PlayerScore
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from .forms import CustomUserCreationForm

def home(request):
    return render(request, 'users/home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def guest_login(request):
    # Create or retrieve a guest user
    guest_user = User.objects.create_user(username=f'guest_{User.objects.count()}', password='guest_password')
    login(request, guest_user)
    return redirect('/')


@login_required
def profile(request):
    # Fetch the user's games and scores
    player_games = Player.objects.filter(user=request.user)
    player_scores = PlayerScore.objects.filter(player__user=request.user).order_by('-game_session__created_at')

    return render(request, 'users/profile.html', {
        'player_games': player_games,
        'player_scores': player_scores,
    })

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = '/login/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'login.html'