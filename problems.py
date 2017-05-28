from aimacode.planning import Action
from aimacode.search import (
    Node, Problem,
)
from aimacode.utils import expr
from utils import (
    FluentState, encode_state, decode_state,
)


class BeerCargoProblem(Problem):

    def __init__(self, cargos, trucks, warehouses, initial: FluentState, goal: list):
        pass
