# myapp/models.py

from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()  # 例如可以添加邮箱信息
    score = models.IntegerField(default=0)  # 添加整数型的 score 字段，默认值为0
    hide_score = models.FloatField(default=0.0)  # 添加浮点数型的 hide_score 字段，默认值为0.0
    def __str__(self):
        return f'{self.name}'
    
class MatchResult(models.Model):
    player1 = models.ForeignKey(Player, related_name='player1_matches', on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name='player2_matches', on_delete=models.CASCADE)
    winner = models.ForeignKey(Player, related_name='won_matches', on_delete=models.CASCADE, null=True, blank=True)
    played = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.player1} vs {self.player2}'