def normalize_start_symbol(formalized_grammar):
    products = formalized_grammar["productions"]
    variables = formalized_grammar["variables"]
    if not _check_start_RHS(products):
        new_variable = _generate_new_variable(products, variables, start=True)
        formalized_grammar["start"] = new_variable

def _generate_new_variable(productions, variables, rules=None, start=False):
    index = 0
    new_variable = "S" if start == True else "A"

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
    start_RHS = productions['S']
    for element in start_RHS:
        if "S" in element:
            return False
    return True



def remove_epsilon_rules(formalized_grammar):
    products = formalized_grammar["productions"]
    start = formalized_grammar["start"]
    nullables = _find_nullable(products, start)
    while(len(nullables) != 0):
        _remove_epsilon(products, nullables)
        nullables = _find_nullable(products, start)

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
    while(len(unit_rules_dict) != 0):
        _remove_unit(products, unit_rules_dict)
        unit_rules_dict = _find_unit_rules(products, variables)

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
            productions[variable].remove(tuple(unit_var))



def binarize(formalized_grammar):
    products = formalized_grammar['productions']
    variables = formalized_grammar['variables']
    longs = _find_long_RHS(products)

    while(len(longs) != 0):
        _binarize_help(products, variables, longs)
        longs = _find_long_RHS(products)

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