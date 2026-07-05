def normalize_start_symbol(formalized_grammar):
    products = formalized_grammar["productions"]
    if not _check_start_RHS(products):
        new_variable = _generate_new_variable(products, start=True)
        formalized_grammar["start"] = new_variable

def _generate_new_variable(productions, start=False):
    variables = set(productions.keys())
    index = 0
    new_variable = "S" if start == True else "A"

    while(f'{new_variable}{index}' in variables):
        index += 1

    new_variable += f'{index}'

    if start == True:
        productions[new_variable] = ["S"]
        return new_variable

def _check_start_RHS(productions):
    start_RHS = productions['S']
    symbols = set()
    for element in start_RHS:
        symbols = set(element.split(" "))
        if "S" in symbols:
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