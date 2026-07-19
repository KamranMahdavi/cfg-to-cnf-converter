from converter import normalize_start_symbol, remove_epsilon_rules, remove_unit_rules, binarize, create_terminal_variables
from grammar_parser import parse_grammar, tupleize_productions, serialize_grammar

def convert(grammar):
    formalized_grammar = parse_grammar(grammar)
    tuple_grammar = tupleize_productions(formalized_grammar)
    normalize_start_symbol(tuple_grammar)
    remove_epsilon_rules(tuple_grammar)
    remove_unit_rules(tuple_grammar)
    binarize(tuple_grammar)
    create_terminal_variables(tuple_grammar)
    return serialize_grammar(tuple_grammar)