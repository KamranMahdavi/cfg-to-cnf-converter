import copy
from converter import normalize_start_symbol, remove_epsilon_rules, remove_unit_rules, binarize, create_terminal_variables
from grammar_parser import parse_grammar, tupleize_productions, serialize_grammar

def convert(grammar):
    formalized_grammar = parse_grammar(grammar)
    tupleize_productions(formalized_grammar)
    normalize_start_symbol(formalized_grammar)
    remove_epsilon_rules(formalized_grammar)
    remove_unit_rules(formalized_grammar)
    binarize(formalized_grammar)
    create_terminal_variables(formalized_grammar)
    return serialize_grammar(formalized_grammar)

def analyze(grammar):
    step_list = []
    title = "The Original Grammar"
    description = "The original grammar before any changes."

    formalized_grammar = parse_grammar(grammar)
    tupleize_productions(formalized_grammar)
    step_list.append(_take_snapshot(formalized_grammar['productions'], title, description))

    normalize_start_symbol(formalized_grammar)
    title = "Step 1: Remove the start symbol from the right-hand side"
    if formalized_grammar['start'] == 'S':
        description = "No changes were required in this step."
    else:
        description = (
            "Since the start symbol (S) occured on the right-hand side of the grammar, "
            f"we introduced a new start variable ({formalized_grammar['start']}), "
            "which does not occur on any rule's right-hand side."
        )
    step_list.append(_take_snapshot(formalized_grammar['productions'], title, description))

    changed = remove_epsilon_rules(formalized_grammar)
    title = "Step 2: Remove ε-rules"
    if not changed:
        description = "No changes were required in this step."
    else:
        description = (
            'An ε-rule is a rule of the form "R → ε", where R is not the start symbol.\n'
            'To remove these rules, we first need to determine all "nullable" variables, that is, '
            'variables that either have a rule of the form "R → ε" on their right-hand side, or have a right-hand side of the form '
            '"W X Y Z..." which is composed entirely of variables, and every variable is nullable.\n'
            'In this step, we replace each rule with all different combinations '
            'obtained by omitting any subset of its nullable variables.\n' 
            f'This procedure is done for all variables except for the start variable {formalized_grammar["start"]}.'
        )
    step_list.append(_take_snapshot(formalized_grammar['productions'], title, description))

    changed = remove_unit_rules(formalized_grammar)
    title = "Step 3: Remove unit rules"
    if not changed:
        description = "No changes were required in this step."
    else:
        description = (
            'A unit rule is a rule of the form "R → T", where both R and T are variables.\n'
            'To remove them, simply replace T with the non-unit rules on its right-hand side.\n'
            'This process is repeated until all unit rules get removed.'
        )
    step_list.append(_take_snapshot(formalized_grammar['productions'], title, description))

    changed = binarize(formalized_grammar)
    title = "Step 4: Binarize rules"
    if not changed:
        description = "No changes were required in this step."
    else:
        description = (
            'A rule is in binary form if its right-hand side has at most two symbols (terminals or variables).\n'
            'First, we find the rules whose right-hand side contains three or more symbols.\n'
            'Then, we repeatedly split them into smaller rules by introducing new helper variables.\n'
            'Each helper variable replaces a part of the original production, until every rule has a right-hand side\n'
            'of at most two symbols.'
        )
    step_list.append(_take_snapshot(formalized_grammar['productions'], title, description))

    changed = create_terminal_variables(formalized_grammar)
    title = "Step 5: Terminal replacement"
    if not changed:
        description = "No changes were required in this step."
    else:
        description = (
            'A mixed rule is a rule whose right-hand side contains both terminals and variables.\n'
            'Terminals in Chomsky Normal Form can only appear in rules of the form "R → a", where "R" is a variable and "a" is a terminal.\n'
            'As a result, any terminal that appears next to other symbols is replaced with a new helper variable\n'
            'that only derives that specific terminal.\n\n'
            'With this, the conversion is complete.'
        )
    step_list.append(_take_snapshot(formalized_grammar['productions'], title, description))

    return step_list

class ConversionStep:

    def __init__(self, snapshot, title="", description=""):
        self.title = title
        self.description = description
        self.snapshot = snapshot

def _take_snapshot(snapshot, title="", description=""):
    display_grammar = copy.deepcopy(snapshot)
    step = ConversionStep(display_grammar, title, description)
    return step