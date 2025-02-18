from django.test import TestCase
from webpanel.models import Game

class GameTestCase(TestCase):
    def setUp(self):
        Game.objects.create(name="Assassin's Creed")

    def test_game_creation(self):
        assassins = Game.objects.get(name="Assassin's Creed")
        assert str(assassins) == "Assassin's Creed"

