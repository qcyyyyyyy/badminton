import random
from django.shortcuts import render, redirect, get_object_or_404
from .models import Player,MatchResult
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'index.html')

# 添加选手视图
def add_player(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        hide_score = request.POST.get('hide_score')
        score = request.POST.get('score')
        Player.objects.create(name=name, email=email, hide_score=hide_score, score=score)
        return redirect('view_players')
    return render(request, 'add_player.html')

# 删除选手视图
def delete_player(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    player.delete()
    return redirect('view_players')

def edit_player(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    if request.method == 'POST':
        player.name = request.POST.get('name')
        player.email = request.POST.get('email')
        player.score = request.POST.get('score')
        player.hide_score = request.POST.get('hide_score')
        player.save()
        return redirect('view_players')
    return render(request, 'edit_player.html', {'player': player})
# 查看选手列表视图
def view_players(request):
    players = Player.objects.all()
    player_list_with_index = [{'index': i + 1, 'player': player} for i, player in enumerate(players)]
    return render(request, 'view_players.html', {'players': player_list_with_index})

# 开始比赛视图
def start_tournament(request):
    players = list(Player.objects.all())
    if len(players) < 2:
        return render(request, 'index.html', {'message': '选手数量不足，需至少2名选手。'})

    request.session['round'] = 1
    matches, winners, bye_player = run_round(players)
    request.session['winners'] = [winner.id for winner in winners]
    request.session['bye_player'] = bye_player.id if bye_player else None
    return render(request, 'tournament.html', {'matches': matches, 'round': 1})

# 运行单轮比赛逻辑
def run_round(players):
    random.shuffle(players)
    players = sorted(players, key=lambda p: p.score * p.hide_score, reverse=True)
    matches = []
    winners = []
    bye_player = None

    if len(players) % 2 != 0:
        bye_player = random.choice(players)
        players.remove(bye_player)
        winners.append(bye_player)

    for i in range(0, len(players), 2):
        match = (players[i], players[i + 1])
        matches.append(match)

    return matches, winners, bye_player

# 下一轮比赛视图（手动选择获胜者）
@csrf_exempt
def next_round(request):
    round_number = request.session.get('round', 1)
    bye_player_id = request.session.get('bye_player')
    bye_player = Player.objects.get(id=bye_player_id) if bye_player_id else None

    if request.method == 'POST':
        
        winner_ids = request.POST.getlist('winners')
        winners = [get_object_or_404(Player, id=winner_id) for winner_id in winner_ids]
        
        if bye_player:
            winners.append(bye_player)
        if len(winners) == 1:
            champion = winners[0]
            return render(request, 'result.html', {'champion': champion})
        
        
        matches, new_winners, new_bye_player = run_round(winners)
        request.session['winners'] = [winner.id for winner in new_winners]
        request.session['bye_player'] = new_bye_player.id if new_bye_player else None
        request.session['round'] = round_number + 1
        return render(request, 'tournament.html', {'matches': matches, 'round': round_number + 1})

    winners = [get_object_or_404(Player, id=id) for id in request.session.get('winners', [])]
    matches, _, _ = run_round(winners)
    return render(request, 'tournament.html', {'matches': matches, 'round': round_number})

# 重置比赛视图
def reset_tournament(request):
    request.session.flush()
    return redirect('index')

# 更新部分，包含双败淘汰赛逻辑  
# 添加新的视图用于双败淘汰赛  
def start_double_elimination_tournament(request):
    players = list(Player.objects.all())
    if len(players) <2:
        return render(request, 'index.html', {'message': '选手数量不足，需至少4名选手。'})
    request.session['round'] = 1
    request.session['losers'] = []# 用于存储输家的列表  
    losers=[]
    matches, losers_matches, winners, losers_winners, losers, bye_player, bye_losers = run_double_elimination_round(players,losers)
    
    request.session['winners'] = [winner.id for winner in (winners or [])]
    request.session['losers_winners'] = [losers_winner.id for losers_winner in (losers_winners or [])]
    request.session['bye_player'] = bye_player.id if bye_player else None
    request.session['bye_losers'] = bye_losers.id if bye_losers else None
    request.session['losers'] = [loser.id for loser in (losers or [])]# 存储输者 
    
    return render(request, 'double_tournament.html', {'matches': matches,'losers_matches': losers_matches, 'round': 1})

def run_double_elimination_round(players,llosers):
    winners = []
    matches = []
    losers = []
    bye_player = None
    if players!=[]:
        random.shuffle(players)
        players = sorted(players, key=lambda p: p.score * p.hide_score, reverse=True)
        if len(winners) == 1:
            winners=players
        else:
            if len(players) % 2 != 0:
                bye_player = random.choice(players)
                players.remove(bye_player)
                winners.append(bye_player)
            for i in range(0, len(players), 2):
                match = (players[i], players[i + 1])
                matches.append(match)
                losers.append(match[0] if match[1] in winners else match[1])# 将输者添加到输者列表
    losers_matches = []
    losers_winners = []
    bye_losers = None
    if llosers!=[]:
        random.shuffle(llosers)
        llosers = sorted(llosers, key=lambda p: p.score * p.hide_score, reverse=True)
        if len(llosers) % 2 != 0:
            bye_losers = random.choice(llosers)
            llosers.remove(bye_losers)
            losers_winners.append(bye_losers)
        for i in range(0, len(llosers), 2):
            losers_match = (llosers[i], llosers[i + 1])
            losers_matches.append(losers_match)
    return matches, losers_matches, winners, losers_winners, losers, bye_player, bye_losers

def double_next_round(request):
    round_number = request.session.get('round', 1)
    bye_player_id = request.session.get('bye_player')
    bye_player = Player.objects.get(id=bye_player_id) if bye_player_id else None
    bye_losers_id = request.session.get('bye_losers')
    bye_losers = Player.objects.get(id=bye_losers_id) if bye_losers_id else None
    if request.method == 'POST':
        winner_ids = request.POST.getlist('winners')
        losers_winner_ids = request.POST.getlist('losers_winners')
        losers = [get_object_or_404(Player, id=id) for id in request.session.get('losers', [])]
        winners = [get_object_or_404(Player, id=winner_id) for winner_id in winner_ids]  
        losers_winners = [get_object_or_404(Player, id=losers_winner_id) for losers_winner_id in losers_winner_ids] 
        losers.extend(losers_winners)
        if bye_player:
            winners.append(bye_player)
        if bye_losers:
            losers.append(bye_losers)  
        if len(winners) == 1 and len(losers) == 1:
            request.session['bye_player'] = None
            return render(request, 'tournament.html', {'matches': [(winners[0],losers[0])], 'round': round_number})

        matches, losers_matches, new_winners, new_losers_winners ,new_losers,new_bye_player,new_bye_losers = run_double_elimination_round(winners,losers)
        request.session['winners'] = [winner.id for winner in new_winners]
        request.session['losers_winners'] = [losers_winner.id for losers_winner in new_losers_winners]
        request.session['losers'] = [losers.id for losers in new_losers]
        request.session['bye_player'] = new_bye_player.id if new_bye_player else None
        request.session['bye_losers'] = new_bye_losers.id if new_bye_losers else None
        request.session['round'] = round_number + 1
        return render(request, 'double_tournament.html', {'matches': matches,'losers_matches': losers_matches, 'round': round_number + 1})

    winners = [get_object_or_404(Player, id=id) for id in request.session.get('winners', [])]
    losers_winners = [get_object_or_404(Player, id=id) for id in request.session.get('losers_winners', [])]
    matches, losers_matches,new_winners,new_losers_winners ,new_losers,new_bye_player,new_bye_losers = run_double_elimination_round(winners,losers_winners)
    return render(request, 'double_tournament.html', {'matches': matches, 'losers_matches': losers_matches,'round': round_number})

#循环赛
def turn_tournament(request):
    players = list(Player.objects.all())
    if len(players) < 2:
        return render(request, 'index.html', {'message': '选手数量不足，需至少2名选手。'})
    
    # 生成所有可能的对战组合
    generate_all_matches(players)
    
    return redirect('view_matches')

def generate_all_matches(players):
    MatchResult.objects.all().delete()  # 清除之前的比赛结果
    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            MatchResult.objects.create(player1=players[i], player2=players[j])

def view_matches(request):
    matches = MatchResult.objects.filter(played=False)
    return render(request, 'turn_tournament.html', {'matches': matches, 'round': '循环赛'})

@csrf_exempt
def turn_next_round(request):
    if request.method == 'POST':
        match_ids = request.POST.getlist('match_ids')
        for match_id in match_ids:
            match = get_object_or_404(MatchResult, id=match_id)
            winner_id = request.POST.get(f'winner_{match_id}')
            match.winner = get_object_or_404(Player, id=winner_id)
            match.played = True
            match.save()
        # 检查是否所有比赛都已完成
        if not MatchResult.objects.filter(played=False).exists():
            results = MatchResult.objects.all()
            champions = calculate_champions(results)
            return render(request, 'turn_result.html', {'champions': champions})

    matches = MatchResult.objects.filter(played=False)
    return render(request, 'turn_tournament.html', {'matches': matches, 'round': '循环赛'})

def calculate_champions(matches):
    scores = {}
    for match in matches:
        if match.winner:
            scores[match.winner] = scores.get(match.winner, 0) + 1
    # 找到得分最高的选手
    champions = [player for player, score in scores.items() if score == max(scores.values())]
    return champions

def turn_reset_tournament(request):
    MatchResult.objects.all().delete()
    request.session.flush()
    return redirect('index')