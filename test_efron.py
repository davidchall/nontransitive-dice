import nose
import numpy as np

from ntdice import Game, DiscreteRV


def test_efrons_dice():
    """Tests the classic configuration of Efron's dice, which
    have a mutual win probability of 2/3.
    """
    game = Game()
    game.add_participant(DiscreteRV.die_faces((4, 4, 4, 4, 0, 0)))
    game.add_participant(DiscreteRV.die_faces((3, 3, 3, 3, 3, 3)))
    game.add_participant(DiscreteRV.die_faces((6, 6, 2, 2, 2, 2)))
    game.add_participant(DiscreteRV.die_faces((5, 5, 5, 1, 1, 1)))

    np.random.seed(2)
    game.play(100000)
    result = game.get_mutual_win_probability()
    print(result)
    nose.tools.assert_almost_equals(result, 2. / 3., places=2)
