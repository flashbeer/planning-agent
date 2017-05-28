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

        def unload_actions():
            unloads = []
            for t in self.trucks:
                for c in self.cargos:
                    for w in self.warehouses:
                        precond_pos = [
                            expr('In({}, {})'.format(c, t)),
                            expr('At({}, {})'.format(t, w))
                        ]
                        precond_neg = []
                        effect_add = [expr('At({}, {})'.format(c, w))]
                        effect_rem = [expr('In({}, {})'.format(c, t))]
                        unload = Action(expr('Load({}, {}, {})'.format(c, t, w)),
                                        [precond_pos, precond_neg],
                                        [effect_add, effect_rem])
                        unloads.append(unload)

        def drive_actions():
            trips = []
            for fr in self.warehouses:
                for to in self.warehouses:
                    if fr != to:
                        for t in self.trucks:
                            precond_pos = [expr('At({}, {})'.format(t, fr))]
                            precond_neg = []
                            effect_add = [expr('At({}, {})'.format(t, to))]
                            effect_rem = [expr('At({}, {})'.format(t, fr))]
                            trip = Action(expr('Fly({}, {}, {})'.format(t, fr, to)),
                                          [precond_pos, precond_neg],
                                          [effect_add, effect_rem])
                            trip.append(trip)
            return trips

        return load_actions() + unload_actions() + drive_actions()

    def actions(self, state: str) -> list:
        possible_actions = []
        kb = PropKB()
        kb.tell(decode_state(state, self.state_map).pos_sentence())
        for action in self.actions_list:
            is_possible = True
            for clause in action.precond_pos:
                if clause not in kb.clauses:
                    is_possible = False
            for clause in action.precond_neg:
                if clause in kb.clauses:
                    is_possible = False
            if is_possible:
                possible_actions.append(action)
        return possible_actions

    def result(self, state: str, action: Action):
        new_state = FluentState([], [])
        old_state = decode_state(state, self.state_map)
        for fluent in old_state.pos:
            if fluent not in action.effect_rem:
                new_state.pos.append(fluent)
        for fluent in action.effect_add:
            if fluent not in new_state.pos:
                new_state.pos.append(fluent)
        for fluent in old_state.neg:
            if fluent not in action.effect_add:
                new_state.neg.append(fluent)
        for fluent in action.effect_rem:
            if fluent not in new_state.neg:
                new_state.neg.append(fluent)
        return encode_state(new_state, self.state_map)

    def goal_test(self, state: str) -> bool:
        kb = PropKB()
        kb.tell(decode_state(state, self.state_map).pos_sentence())
        for clause in self.goal:
            if clause not in kb.clauses:
                return False
        return True

    def h_1(self, node: Node):
        '''False Heuristic
        '''
        return 1

    def h_pg_levelsum(self, node: Node):
        pass

    def h_ignore_preconditions(self, node: Node):
        count = 0
        kb = PropKB()
        kb.tell(decode_state(node.state, self.state_map).pos_sentence())
        for clause in self.goal:
            if clause not in kb.clauses:
                count += 1
        return count


def beer_cargo_p1() -> BeerCargoProblem:
    pass
