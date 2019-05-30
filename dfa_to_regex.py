import copy


def regex_state(state, states_expressions, i, j):
    if state in states_expressions:
        if states_expressions[state][0] == "":
            statesExpressions[state][0] = f"{alphabets[j]}*"
        else:
            expression_before = ""
            if states_expressions[state][0][-2] == ')':
                expression_before = states_expressions[state][0][1:-2]
            else:
                expression_before = states_expressions[state][0][0:-1]
            states_expressions[state][0] = f'({expression_before}|{alphabets[j]})*'
    else:
        states_expressions[state] = [f"{alphabets[j]}*"]


def regex_transition(state, states_expressions, i, j):
    if state in states_expressions:
        states_expressions[state].append(
            (f"{alphabets[j]}", transition_matrix[i][j]))
    else:
        states_expressions[state] = [""]
        states_expressions[state].append(
            (f"{alphabets[j]}", transition_matrix[i][j]))


def build_paths(state, states_expressions, final_states):
    isFinished = False
    current_state = state
    reg_string = ""
    if state == init_state and state in final_states:
        if states_expressions[state][0] != "":
            reg_string = f"{states_expressions[state][0]}"
        else:
            reg_string = 'ε'
        paths.append(reg_string)
        final_states.remove(state)
        build_paths(state, states_expressions, final_states)
        return

    while not isFinished:
        reg_string = f"{reg_string}{states_expressions[current_state][0]}"
        if current_state in final_states:
            paths.append(reg_string)
            final_states.remove(current_state)
            build_paths(init_state, states_expressions, final_states)
            return
        if len(states_expressions[current_state]) > 1:
            if len(states_expressions[current_state]) > 2:
                states_expressions_copy = copy.deepcopy(states_expressions)
                states_expressions_copy[current_state].pop(1)
                final_states_copy = final_states[:]
                build_paths(init_state, states_expressions_copy, final_states_copy)
            reg_string = f"{reg_string}{states_expressions[current_state][1][0]}"
            current_state = states_expressions[current_state][1][1]
        else:
            isFinished = True


def build_regex(paths):
    regex_string = ""
    if len(paths) == 1:
        return paths[0]
    regex_string = f"({paths[0]})|"
    for i in range(1, len(paths)):
        if f"({paths[i]})" in regex_string:
            continue
        if i + 1 == len(paths):
            regex_string = f"{regex_string}({paths[i]})"
        else:
            regex_string = f"{regex_string}({paths[i]})|"

    return regex_string


states = input('Enter the states in your DFA : ')
states = states.split()
alphabets = input('Enter the alphabets : ')
alphabets = alphabets.split()
init_state = input('Enter initial state : ')
final_states = input('Enter the final states : ')
final_states = final_states.split()
print('Define the transition function : ')
transition_matrix = [list(map(str, input().split())) for _ in range(len(states))]
statesExpressions = {}
paths = []

for i in range(len(transition_matrix)):
    for j in range(len(transition_matrix[i])):
        if transition_matrix[i][j] == states[i]:
            regex_state(states[i], statesExpressions, i, j)
        else:
            regex_transition(states[i], statesExpressions, i, j)

build_paths(init_state, statesExpressions, final_states)
print(build_regex(paths))
