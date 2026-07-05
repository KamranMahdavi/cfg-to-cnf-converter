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