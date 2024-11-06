#算法
import sqlite3

from django.shortcuts import render, redirect
from .models import Player
import random


def index(request):
    return render(request, 'index.html')


def add_player(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        Player.objects.create(name=name,age=age, email=email)
        return redirect('view_players')
    return render(request, 'add_player.html')



def view_players(request):
    players = Player.objects.all()
    return render(request, 'view_players.html', {'players': players})


def start_tournament(request):
    players = list(Player.objects.all())
    if len(players) < 8:
        return render(request, 'index.html', {'message': '选手数量不足，需至少8名选手。'})

    matches, winners = run_round(players, 1)
    request.session['winners'] = winners
    return render(request, 'tournament.html', {'matches': matches, 'round': 1})


def run_round(players, round_number):
    random.shuffle(players)
    matches = []
    winners = []

    for i in range(0, len(players), 2):
        match = (players[i], players[i + 1])
        winner = random.choice(match)  # 随机选择胜者
        matches.append(match)
        winners.append(winner)

    return matches, winners


def next_round(request):
    winners = request.session.get('winners', [])

    if len(winners) < 2:  # 赛程结束，只有一个冠军
        champion = winners[0] if winners else None
        return render(request, 'result.html', {'champion': champion})

    matches, new_winners = run_round(winners, 2)
    request.session['winners'] = new_winners
    return render(request, 'tournament.html', {'matches': matches, 'winners': new_winners, 'round': 2})


def reset_tournament(request):
    request.session.flush()
    return redirect('index')