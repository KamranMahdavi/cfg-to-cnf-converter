def normalize_start_symbol(formalized_grammar):
    products = formalized_grammar["productions"]
    variables = formalized_grammar["variables"]
    if not _check_start_RHS(products):
        new_variable = _generate_new_variable(products, variables, start=True)
        formalized_grammar["start"] = new_variable

def _generate_new_variable(productions, variables, rules=None, start=False, terminal=False):
    index = 0
    new_variable = "A"
    if terminal == True:
        new_variable = "T"
    else:
        new_variable = "S"

    while(f'{new_variable}{index}' in variables):
        index += 1

    new_variable += f'{index}'

    if start == True:
        productions[new_variable] = {("S",)}
    else:
        productions[new_variable] = {rules}

    variables.add(new_variable)
    return new_variable

def _check_start_RHS(productions):
    for variable in productions:
        variable_RHS = productions[variable]
        for element in variable_RHS:
            if "S" in element:
                return False
    return True

def remove_epsilon_rules(formalized_grammar):
    products = formalized_grammar["productions"]
    start = formalized_grammar["start"]
    nullables = _find_nullable(products, start)
    if len(nullables) == 0:
        return False
    while(len(nullables) != 0):
        _remove_epsilon(products, nullables)
        nullables = _find_nullable(products, start)
    return True

def _find_nullable(productions, start):
    nullables = set()
    for key in productions:
        if ("ε",) in productions[key] and key != start:
            nullables.add(key)
    return nullables

def _remove_epsilon(productions, nullables):
    for variable in productions:
        if variable in nullables:
            productions[variable].remove(("ε",))
        current = productions[variable]
        new_productions = set()
        for expression in current:
            new_productions.update(_get_nullable_combinations(expression, nullables))
        
        productions[variable] = new_productions

def _get_nullable_combinations(expression, nullables):    
    new_expressions = set()
    if all(i in nullables for i in expression):
        new_expressions.add(('ε',))
    
    new_expressions = _get_nullable_combinations_help(expression, nullables)
    if tuple() in new_expressions:
        new_expressions.remove(tuple())
        new_expressions.add(('ε',))

    return new_expressions

def _get_nullable_combinations_help(expression, nullables, index=0):
    if index >= len(expression):
        return {()}
    
    if expression[index] in nullables:
        a = _get_nullable_combinations_help(expression, nullables, index + 1)
        b = {(expression[index],) + i for i in _get_nullable_combinations_help(expression, nullables, index + 1)}

        a.update(b)
        return a

    else:
        return {(expression[index],) + i for i in _get_nullable_combinations_help(expression, nullables, index + 1)}
    


def remove_unit_rules(formalized_grammar):
    products = formalized_grammar['productions']
    variables = formalized_grammar['variables']
    unit_rules_dict = _find_unit_rules(products, variables)
    if len(unit_rules_dict) == 0:
        return False
    while(len(unit_rules_dict) != 0):
        _remove_unit(products, unit_rules_dict)
        unit_rules_dict = _find_unit_rules(products, variables)
    return True

def _find_unit_rules(productions, variables):
    unit_rules = dict()
    for variable in productions:
        for rule in productions[variable]:
            if len(rule) == 1 and rule[0] in variables:
                if not variable in unit_rules:
                    unit_rules[variable] = set()
                unit_rules[variable].add(rule[0])
    return unit_rules

def _remove_unit(productions, unit_rules_dict):
    for variable in unit_rules_dict:
        for unit_var in unit_rules_dict[variable]:
            productions[variable].update(productions[unit_var])
            productions[variable].remove((unit_var,))



def binarize(formalized_grammar):
    products = formalized_grammar['productions']
    variables = formalized_grammar['variables']
    longs = _find_long_RHS(products)
    if len(longs) == 0:
        return False
    while(len(longs) != 0):
        _binarize_help(products, variables, longs)
        longs = _find_long_RHS(products)
    return True

def _find_long_RHS(productions):
    long_RHS_dict = dict()
    for variable in productions:
        for rule in productions[variable]:
            if len(rule) > 2:
                if variable not in long_RHS_dict:
                    long_RHS_dict[variable] = set()
                long_RHS_dict[variable].add(rule)
    return long_RHS_dict

def _binarize_help(productions, variables, long_rules):
    for variable in long_rules:
        for rule in long_rules[variable]:
            new_var = _generate_new_variable(productions, variables, rule[1:])
            productions[variable].add((rule[0], new_var))
            productions[variable].remove(rule)



def create_terminal_variables(formalized_grammar):
    products = formalized_grammar['productions']
    variables = formalized_grammar['variables']
    terminals = formalized_grammar['terminals']

    mixed_rules = _get_mixed_RHS_rules(products, terminals)
    if len(mixed_rules) == 0:
        return False
    _create_terminal_variables_help(products, variables, terminals, mixed_rules)
    return True

def _get_mixed_RHS_rules(productions, terminals):
    mixed_RHS_dict = dict()
    for variable in productions:
        for rule in productions[variable]:
            if len(rule) > 1:
                for element in rule:
                    if element in terminals:
                        if variable not in mixed_RHS_dict:
                            mixed_RHS_dict[variable] = set()
                        mixed_RHS_dict[variable].add(rule)
    return mixed_RHS_dict

def _create_terminal_variables_help(productions, variables, terminals, mixed_rules):
    to_update = dict()
    to_remove = dict()
    for variable in mixed_rules:
        to_update[variable] = set()
        to_remove[variable] = set()
        new_rule = list()
        for rule in mixed_rules[variable]:
            for element in rule:
                term_var = element
                if element in terminals:
                    term_var = _get_terminal_variable(element, productions)
                    if not term_var:
                        term_var = _generate_new_variable(productions, variables, tuple(element), terminal=True)

                new_rule.append(term_var)

            to_update[variable].add(tuple(new_rule))
            to_remove[variable].add(rule)
            new_rule.clear()

    _add_new_terminal_rules(productions, to_update, to_remove)

def _get_terminal_variable(terminal, productions):
    for variable in productions:
        if productions[variable] == {tuple(terminal)}:
            return variable
    return None

def _add_new_terminal_rules(productions, new_rules, rules_to_remove):
    for variable in rules_to_remove:
        for rule in rules_to_remove[variable]:
            productions[variable].remove(rule)
        productions[variable].update(new_rules[variable])