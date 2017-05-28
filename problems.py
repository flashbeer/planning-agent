from aimacode.logic import PropKB
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

    def get_actions(self):
        def load_actions():
            loads = []
            for t in self.trucks:
                for c in self.cargos:
                    for w in self.warehouses:
                        precond_pos = [
                            expr('At({}, {})'.format(c, w)),
                            expr('At({}, {})'.format(t, w))
                        ]
                        precond_neg = []
                        effect_add = [expr('In({}, {})'.format(c, t))]
                        effect_rem = [expr('At({}, {})'.format(c, w))]
                        load = Action(expr('Load({}, {}, {})'.format(c, t, w)),
                                      [precond_pos, precond_neg],
                                      [effect_add, effect_rem])
                        loads.append(load)

    def drive_actions():
        drives = []
