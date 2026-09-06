import copy
from .converter import normalize_start_symbol, remove_epsilon_rules, remove_unit_rules, binarize, create_terminal_variables
from .grammar_parser import parse_grammar, tupleize_productions, serialize_grammar

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
            "Since the start symbol (S) appears on the right-hand side of a rule, "
            f"a new start variable ({formalized_grammar['start']}) is introduced.\n"
            "This ensures the new start variable never appears on the right-hand side."
        )
    step_list.append(_take_snapshot(formalized_grammar['productions'], title, description))

    changed = remove_epsilon_rules(formalized_grammar)
    title = "Step 2: Remove ε-rules"
    if not changed:
        description = "No changes were required in this step."
    else:
        description = (
            'An ε-rule allows a variable to create the empty string.\n'
            'We identify all nullable variables, then generate the necessary alternatives\n'
            'by omitting nullable variables from existing rules.\n'
            'ε-rules are then removed, except where ε must be kept for the start variable.'
        )
    step_list.append(_take_snapshot(formalized_grammar['productions'], title, description))

    changed = remove_unit_rules(formalized_grammar)
    title = "Step 3: Remove unit rules"
    if not changed:
        description = "No changes were required in this step."
    else:
        description = (
            'A unit rule has the form "R → T", where both R and T are variables.\n'
            'We remove it by giving R the non-unit productions reachable by T.\n'
            'This process is repeated until all unit rules get removed.'
        )
    step_list.append(_take_snapshot(formalized_grammar['productions'], title, description))

    changed = binarize(formalized_grammar)
    title = "Step 4: Binarize rules"
    if not changed:
        description = "No changes were required in this step."
    else:
        description = (
            'In CNF, at most two variables are allowed on the right-hand side of a rule.\n'
            'Rules with three or more symbols are split into smaller rules by creating new helper variables.\n'
            'This repeats until every affected rule has at most two symbols on its right-hand side.'
        )
    step_list.append(_take_snapshot(formalized_grammar['productions'], title, description))

    changed = create_terminal_variables(formalized_grammar)
    title = "Step 5: Terminal replacement"
    if not changed:
        description = "No changes were required in this step."
    else:
        description = (
            'In CNF, terminals can only appear alone on the right-hand side, for example "R → a".\n'
            'Any terminal appearing alongside other symbols is replaced\n'
            'by a new helper variable that derives that terminal.\n'
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