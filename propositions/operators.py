# This file is part of the materials accompanying the book
# "Mathematical Logic through Python" by Gonczarowski and Nisan,
# Cambridge University Press. Book site: www.LogicThruPython.org
# (c) Yannai A. Gonczarowski and Noam Nisan, 2017-2022
# File name: propositions/operators.py

"""Syntactic conversion of propositional formulas to use only specific sets of
operators."""

from propositions.syntax import *
from propositions.semantics import *

def to_not_and_or(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'~'``, ``'&'``, and ``'|'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'~'``, ``'&'``, and
        ``'|'``.
    """
    # Task 3.5
    if is_variable(formula.root):
        return formula
    if is_constant(formula.root):
        var = next(iter(formula.variables()), 'p')
        if formula.root == 'T':
            return Formula('|', Formula(var), Formula('~', Formula(var)))
        return Formula('&', Formula(var), Formula('~', Formula(var)))
    if is_unary(formula.root):
        return Formula('~', to_not_and_or(formula.first))
    assert is_binary(formula.root)
    left = to_not_and_or(formula.first)
    right = to_not_and_or(formula.second)
    if formula.root == '&':
        return Formula('&', left, right)
    if formula.root == '|':
        return Formula('|', left, right)
    if formula.root == '->':
        return Formula('|', Formula('~', left), right)
    if formula.root == '+':
        return Formula('|',
                       Formula('&', left, Formula('~', right)),
                       Formula('&', Formula('~', left), right))
    if formula.root == '<->':
        return Formula('|',
                       Formula('&', left, right),
                       Formula('&', Formula('~', left), Formula('~', right)))
    if formula.root == '-&':
        return Formula('~', Formula('&', left, right))
    if formula.root == '-|':
        return Formula('~', Formula('|', left, right))
    raise ValueError('Unknown operator: ' + formula.root)

def to_not_and(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'~'`` and ``'&'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'~'`` and ``'&'``.
    """
    # Task 3.6a
    def convert(f: Formula) -> Formula:
        if is_variable(f.root):
            return f
        if is_unary(f.root):
            return Formula('~', convert(f.first))
        if f.root == '&':
            return Formula('&', convert(f.first), convert(f.second))
        if f.root == '|':
            return Formula('~',
                           Formula('&',
                                   Formula('~', convert(f.first)),
                                   Formula('~', convert(f.second))))
        raise ValueError('Unexpected operator: ' + f.root)
    return convert(to_not_and_or(formula))

def to_nand(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'-&'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'-&'``.
    """
    # Task 3.6b
    def convert(f: Formula) -> Formula:
        if is_variable(f.root):
            return f
        if is_unary(f.root):
            a = convert(f.first)
            return Formula('-&', a, a)
        if f.root == '&':
            a = convert(f.first)
            b = convert(f.second)
            nand = Formula('-&', a, b)
            return Formula('-&', nand, nand)
        if f.root == '|':
            a = convert(f.first)
            b = convert(f.second)
            return Formula('-&', Formula('-&', a, a), Formula('-&', b, b))
        raise ValueError('Unexpected operator: ' + f.root)
    return convert(to_not_and_or(formula))

def to_implies_not(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'->'`` and ``'~'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'->'`` and ``'~'``.
    """
    # Task 3.6c
    def convert(f: Formula) -> Formula:
        if is_variable(f.root):
            return f
        if is_unary(f.root):
            return Formula('~', convert(f.first))
        if f.root == '|':
            return Formula('->', Formula('~', convert(f.first)),
                           convert(f.second))
        if f.root == '&':
            return Formula('~',
                           Formula('->', convert(f.first),
                                   Formula('~', convert(f.second))))
        raise ValueError('Unexpected operator: ' + f.root)
    return convert(to_not_and_or(formula))

def to_implies_false(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'->'`` and ``'F'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'->'`` and ``'F'``.
    """
    # Task 3.6d
    def convert(f: Formula) -> Formula:
        if is_variable(f.root):
            return f
        if is_constant(f.root):
            if f.root == 'F':
                return f
            return Formula('->', Formula('F'), Formula('F'))
        if is_unary(f.root):
            return Formula('->', convert(f.first), Formula('F'))
        if f.root == '->':
            return Formula('->', convert(f.first), convert(f.second))
        raise ValueError('Unexpected operator: ' + f.root)
    return convert(to_implies_not(formula))
