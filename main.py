from collections import defaultdict

class NFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def __repr__(self):
        result = []
        result.append("NFA(")
        result.append(f"  States: {sorted(self.states)},")
        result.append(f"  Alphabet: {sorted(self.alphabet)},")
        result.append("  Transitions:")
        for state, trans in sorted(self.transitions.items()):
            result.append(f"    {state}:")
            for symbol, next_states in sorted(trans.items()):
                result.append(f"      {symbol} -> {next_states}")
        result.append(f"  Start State: {self.start_state},")
        result.append(f"  Accept States: {sorted(self.accept_states)}")
        result.append(")")
        return "\n".join(result)

def epsilon_closure(nfa, states):
    stack = list(states)
    closure = set(states)

    while stack:
        state = stack.pop()
        for next_state in nfa.transitions[state].get('', []):  # '' is used for epsilon transitions
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return closure

def move(nfa, states, symbol):
    next_states = set()
    for state in states:
        if symbol in nfa.transitions[state]:
            next_states.update(nfa.transitions[state][symbol])
    return next_states

def nfa_to_dfa(nfa):
    dfa_start_state = frozenset(epsilon_closure(nfa, {nfa.start_state}))
    dfa_states = {dfa_start_state}
    dfa_transitions = {}
    unmarked_states = [dfa_start_state]
    dfa_accept_states = set()

    while unmarked_states:
        dfa_state = unmarked_states.pop()
        dfa_transitions[dfa_state] = {}

        for symbol in nfa.alphabet:
            next_states = epsilon_closure(nfa, move(nfa, dfa_state, symbol))
            next_dfa_state = frozenset(next_states)

            if not next_states:
                continue

            dfa_transitions[dfa_state][symbol] = next_dfa_state

            if next_dfa_state not in dfa_states:
                dfa_states.add(next_dfa_state)
                unmarked_states.append(next_dfa_state)

            if any(state in nfa.accept_states for state in next_dfa_state):
                dfa_accept_states.add(next_dfa_state)

    return DFA(dfa_states, nfa.alphabet, dfa_transitions, dfa_start_state, dfa_accept_states)

class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def __repr__(self):
        result = []
        result.append("DFA(")
        result.append(f"  States: {sorted([sorted(s) for s in self.states])},")
        result.append(f"  Alphabet: {sorted(self.alphabet)},")
        result.append("  Transitions:")
        for state, trans in sorted(self.transitions.items(), key=lambda item: sorted(item[0])):
            result.append(f"    {sorted(state)}:")
            for symbol, next_state in sorted(trans.items()):
                result.append(f"      {symbol} -> {sorted(next_state)}")
        result.append(f"  Start State: {sorted(self.start_state)},")
        result.append(f"  Accept States: {sorted([sorted(s) for s in self.accept_states])}")
        result.append(")")
        return "\n".join(result)

# Example NFA
states = {'A', 'B', 'C'}
alphabet = {'0', '1'}
transitions = {
    'A': {'0': ['A', 'B'], '1': ['A']},
    'B': {'1': ['C']},
    'C': {}
}
start_state = 'A'
accept_states = {'C'}

nfa = NFA(states, alphabet, transitions, start_state, accept_states)
dfa = nfa_to_dfa(nfa)

print(nfa)
print(dfa)
