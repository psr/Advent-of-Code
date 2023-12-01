from pathlib import Path
from enum import Enum


input_path = Path(__file__).parent / '..' / 'inputs' / 'day2.txt'
with input_path.open('r', encoding='utf-8') as input_file:
    matches = [tuple(l.strip().split()) for l in input_file]


class HandShape(Enum):
    ROCK = 'SCISSORS'
    PAPER = 'ROCK'
    SCISSORS = 'PAPER'

    def beats(self, other):
        return self.value == other.name


_HAND_SHAPES = list(HandShape)


def score_shape(handshape):
    return _HAND_SHAPES.index(handshape) + 1


def score_result(your_handshape, opponent_handshape):
    if your_handshape.beats(opponent_handshape):
        return 6
    if opponent_handshape.beats(your_handshape):
        return 0
    return 3


def score_match(match):
    opponent_handshape = _HAND_SHAPES[ord(match[0]) - ord('A')]
    your_handshape =  _HAND_SHAPES[ord(match[1]) - ord('X')]

    return score_shape(your_handshape) + score_result(your_handshape, opponent_handshape)


print(sum(score_match(m) for m in matches))


def rig_match(match):
    """Return the score for a match"""
    opponent_handshape = _HAND_SHAPES[ord(match[0]) - ord('A')]
    desired_result = match[1]
    if desired_result == 'X':  # Throw the game by losing
        your_handshape = getattr(HandShape, opponent_handshape.value)
        score = 0    
    elif desired_result == 'Y':  # Draw
        your_handshape = opponent_handshape
        score = 3
    elif desired_result == 'Z':  # Win
        your_handshape = HandShape(opponent_handshape.name)
        score = 6
    else:
        assert False, "Impossible"
    return score + score_shape(your_handshape)


print(sum(rig_match(m) for m in matches))
