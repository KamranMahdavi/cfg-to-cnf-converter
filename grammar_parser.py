import re

variable_pattern = r"[A-Z]([a-z]*'*|_[a-z]+|[a-z]*_[0-9]+|[A-Z]*|[0-9]*)"
terminal_pattern = r"[a-zε]"

def parse_grammar(grammar):
    productions = dict()
    variables = set()
    terminals = set()
    lines = grammar.strip().splitlines()

    for line in lines:
        _parse_grammar_line(line, productions, variables, terminals)

    defined_variables = set(productions.keys())

    if "S" not in productions:
        raise ValueError("Invalid grammar format: No start variable (S) detected.")
    
    if len(variables - defined_variables) != 0:
        raise ValueError(
            f"Invalid grammar format: Undefined variable(s) in RHS: "
            f"{variables - defined_variables}.\n"
            "Make sure symbols are separated by spaces."
        )
    
    variables = defined_variables

    formalized_grammar = {
        "start": "S",
        "productions": productions,
        "variables": variables,
        "terminals": terminals
    }
    
    return formalized_grammar

def _parse_grammar_line(line, productions, variables, terminals):
    normalized_line = _normalize(line)
    split_line = normalized_line.split("->")

    if len(split_line) != 2:
        raise ValueError("Invalid grammar format.")
        
    left_side = split_line[0].strip()
    right_side = split_line[1].strip()

    _check_LHS(left_side)
    right_side_list = set(_process_RHS(right_side, variables, terminals))
    _add_rules(left_side, right_side_list, productions)


def _process_RHS(string, variables, terminals):
    RHS_list = [form.strip() for form in string.split("|")]
    elements = list()

    for form in RHS_list:
        elements = form.split()
        for element in elements:
            if re.fullmatch(variable_pattern, element):
                variables.add(element)
            elif re.fullmatch(terminal_pattern, element):
                terminals.add(element)
            else:
                raise ValueError(f"Invalid grammar format: Invalid RHS element: {element}\nMake sure symbols are separated by spaces.")
            
    return RHS_list

def _check_LHS(string):
    if " " in string:
        raise ValueError("Invalid grammar format: There should be only one variable on the LHS.")
    result = re.match(variable_pattern, string)
    if not result:
        raise ValueError("Invalid grammar format: Invalid LHS variable.")

def _normalize(string):
    or_list = {"∣", "│", "┃", "¦"}
    epsilon_list = {"λ", "epsilon", "eps"}

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
        productions[LHS] = set()
    
    productions[LHS].update(RHS_list)

def tupleize_productions(formal_grammar):
    productions = formal_grammar["productions"]
    new_productions = dict()
    new_RHS = set()
    new_expression = tuple()
    for key in productions:
        RHS = productions[key]
        for expression in RHS:
            new_expression = tuple(expression.split(" "))
            new_RHS.add(new_expression)
            new_expression = set()

        new_productions[key] = new_RHS
        new_RHS = set()
    
    formal_grammar["productions"] = new_productions

def stringify_productions(formal_grammar):
    productions = formal_grammar["productions"]
    new_productions = dict()
    new_RHS = set()
    for key in productions:
        RHS = productions[key]
        for expression in RHS:
            new_RHS.add(" ".join(expression))
        new_productions[key] = new_RHS
        new_RHS = set()
    
    formal_grammar["productions"] = new_productions



def order_grammar(formalized_grammar):
    ordered_grammar = {
        'start': formalized_grammar['start'],
        'productions': dict(),
        'variables': list(),
        'terminals': list()
    }

    ordered_grammar["variables"] = _sort_variables(formalized_grammar['variables'], ordered_grammar["start"])
    ordered_grammar["terminals"] = sorted(formalized_grammar['terminals'])
    for variable in ordered_grammar['variables']:
        ordered_grammar["productions"][variable] = sorted(formalized_grammar["productions"][variable])

    return ordered_grammar

def _sort_variables(variables, start):
    sorted_vars = sorted(variables)
    sorted_vars.remove(start)
    sorted_vars.insert(0, start)
    return sorted_vars

def serialize_grammar(ordered_grammar):
    grammar_list = []
    for variable in ordered_grammar['productions']:
        var = [f"{variable} →"]
        line = []
        
        for rule in ordered_grammar['productions'][variable]:
            line.append(" ".join(rule))

        var.append(" | ".join(line))
        grammar_list.append(" ".join(var))

    serialized_grammar = "\n".join(grammar_list)
    return serialized_grammar