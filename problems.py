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
        self.state_map = initial.pos + initial.neg
        self.initial_state_TF = encode_state(initial, self.state_map)

        Problem.__init__(self, self.initial_state_TF, goal=goal)
        self.cargos = cargos
        self.trucks = trucks
        self.actions_list = self.get_actions()
