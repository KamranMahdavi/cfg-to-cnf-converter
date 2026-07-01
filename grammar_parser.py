import re

def parse_grammar(grammar):
    productions = dict()
    lines = grammar.splitlines()

    for line in lines:
        _parse_grammar_line(line, productions)

    if "S" not in productions:
        raise ValueError("Invalid grammar format: No start variable (S) detected.")
    
    return productions

def _parse_grammar_line(line, productions):
    normalized_line = _normalize(line)
    split_line = normalized_line.split("->")

    if len(split_line) != 2:
        raise ValueError("Invalid grammar format.")
        
    left_side = split_line[0].strip()
    right_side = split_line[1].strip()

    _check_LHS(left_side)
    
    right_side_list = _check_RHS(right_side)
    right_side_list = list(set(right_side_list))
    
    _add_rules(left_side, right_side_list, productions)


def _check_RHS(string):
    RHS_list = [form.strip() for form in string.split("|")]
    if any(" " in form for form in RHS_list):
        raise ValueError("Invalid grammar format: Invalid RHS expression.")
    return RHS_list

def _check_LHS(string):
    if " " in string:
        raise ValueError("Invalid grammar format: There should be only one variable on the LHS.")
    pattern = "[A-Z][A-Za-z0-9'_]*"
    result = re.match(pattern, string)
    if not result:
        raise ValueError("Invalid grammar format: Invalid LHS variable.")

def _normalize(string):
    or_list = ["∣", "│", "┃", "¦"]
    epsilon_list = ["λ", "epsilon", "eps"]

    normalized_input = ""

    for char in string:
        if char == "→":
            normalized_input += "->"
        elif char in or_list:
            normalized_input += "|"
        elif char in epsilon_list:
            normalized_input += "ε"
        else:
            normalized_input += char

    return normalized_input
    
def _add_rules(LHS, RHS_list, productions):
    if LHS not in productions:
        productions[LHS] = []
    
    productions[LHS].extend(RHS_list)