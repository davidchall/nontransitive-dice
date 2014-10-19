import numpy as np
import itertools


class DiscreteRV(object):

    """A discrete random variable."""

    def __init__(self, values, probs):
        """Initialises an instance of the DiscreteRV class.

        Args:
            values: List of possible values
            probs: List of associated probabilities. If these do
                not sum to unity, they will be normalised.
        """
        self.values = values
        probs = [float(p) / sum(probs) for p in probs]
        self.bins = np.cumsum(probs)

    def generate(self):
        """Generate random variable.
        """
        x = np.random.random_sample(size=1)
        bin = np.digitize(x, self.bins)
        return self.values[bin]

    @classmethod
    def standard_die(cls, n_faces=6):
        """Initialises an instance of the DiscreteRV class,
        which conforms to the rules of a standard die.

        Args:
            n_faces: Number of die faces
        """
        values = range(1, n_faces + 1)
        probs = [1] * n_faces
        return cls(values, probs)

    @classmethod
    def die_faces(cls, faces):
        """Initialises an instance of the DiscreteRV class,
        which conforms to the geometry of a die.

        Args:
            faces: List of die face values
        """
        values = list(set(faces))
        probs = [faces.count(v) for v in values]
        return cls(values, probs)


class Game(object):

    """A class representing the game under test.

    In a round, each participant rolls their die to achieve a score.
    A participant beats all other participants who achieve a lower score.
    The game is easily extended to include continuous random variables."""

    def __init__(self):
        """Initialises an instance of the Game class.
        """
        self.participants = {}
        self.win_prob = {}

    def add_participant(self, participant, name=None):
        """Adds a participant to the game.

        Args:
            participant: A random variable
            name: String to identify participant [optional]
        """
        if name is None:
            name = chr(ord('A') + len(self.participants))
        if name in self.participants:
            print('Error: participant \'{0}\' already exists'.format(name))
            return
        self.participants[name] = participant

    def play(self, n_rounds):
        """Play some rounds of the game.

        Args:
            n_rounds: The number of rounds to play
        """
        self._initialise_counters()
        for i in range(n_rounds):
            self._play_single_round()

        for w, l in self._get_comparisons():
            self.win_prob[(w, l)] = float(
                self.win_prob[(w, l)]) / float(self.n_rounds_played)

    def _play_single_round(self):
        """Play a single round of the game.
        """
        scores = {name: p.generate() for name, p in self.participants.items()}

        for w, l in self._get_comparisons():
            if scores[w] > scores[l]:
                self.win_prob[(w, l)] += 1

        self.n_rounds_played += 1

    def _initialise_counters(self):
        """Reset counters.
        """
        self.n_rounds_played = 0
        for w, l in self._get_comparisons():
            self.win_prob[(w, l)] = 0.0

    def _get_comparisons(self):
        """Returns a list of possible comparisons between participants.
        """
        if self.n_rounds_played == 0:
            self.comparisons = [(w, l) for w, l in itertools.product(
                self.participants.keys(), repeat=2) if w != l]
        return self.comparisons

    def print_win_table(self):
        """Prints a list of probabilities for participants beating each other.
        """
        for w, l in self._get_comparisons():
            print('{winner} beats {loser} {prob:.2%}'.format(
                winner=w, loser=l, prob=win_prob[(w, l)]))

    def get_mutual_win_probability(self):
        """Returns the mutual win probability after the game is played.

        The mutual win probability (MWP) is defined by considering all possible
        cyclic sequences of win-lose participant comparisons, e.g.
            A beats B, B beats C, C beats A
            A beats C, C beats B, B beats A

        The MWP for a sequence is defined by the smallest win probability in
        the sequence, and the MWP for the entire game is defined by the largest
        MWP of the sequences.
        """
        # TODO: remove permutations that are cyclic duplications, since these
        # have equal mutual win probabilities
        max_mutual_win_prob = 0.0
        for seq in itertools.permutations(self.participants.keys()):
            mutual_win_prob = min(
                [self.win_prob[(seq[i - 1], seq[i])] for i in range(len(seq))])
            max_mutual_win_prob = max(mutual_win_prob, max_mutual_win_prob)

        return max_mutual_win_prob
