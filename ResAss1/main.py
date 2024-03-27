class Expression:
    IMPLICATION = '=>'
    IFF = '<=>'
    OR = '|'
    AND = '&'
    NEG = '~'
    FORALL = '∀'
    EXISTS = '∃'

    def _init_(self, op, *args):
        self.op = op
        self.args = args

    def _repr_(self):
        if self.op == self.NEG:
            return f'{self.op}{self.args[0]}'
        elif len(self.args) == 2:
            return f'({self.args[0]} {self.op} {self.args[1]})'
        else:
            return f'({self.op} {self.args[0]})'


def eliminate_implication(expression):
    assert isinstance(expression, Expression)
    if expression.op == Expression.IMPLICATION:
        return Expression(Expression.OR,
                          Expression(Expression.NEG, expression.args[0]), expression.args[1])
    elif expression.op == Expression.IFF:
        return Expression(Expression.AND,
                          Expression(Expression.OR,
                                     Expression(Expression.NEG, expression.args[0]), expression.args[1]),
                          Expression(Expression.OR,
                                     Expression(Expression.NEG, expression.args[1]), expression.args[0]))
    return expression


# Example expression: (P => Q)
expression = Expression(Expression.IMPLICATION, 'P', 'Q')
print("Original Expression:", expression)

# Apply eliminate_implication function
new_expression = eliminate_implication(expression)
print("After Eliminating Implication:", new_expression)


def move_negation_inward(expression):
    assert isinstance(expression, Expression)
    if expression.op == Expression.NEG:
        inner_op = expression.args[0].op
        inner_args = expression.args[0].args
        if inner_op == Expression.NEG:
            return inner_args[0]  # Double negation elimination
        elif inner_op == Expression.AND:
            return Expression(Expression.OR, Expression(Expression.NEG, inner_args[0]),
                              Expression(Expression.NEG, inner_args[1]))  # De Morgan's Law for AND
        elif inner_op == Expression.OR:
            return Expression(Expression.AND, Expression(Expression.NEG, inner_args[0]),
                              Expression(Expression.NEG, inner_args[1]))  # De Morgan's Law for OR
    return expression


# Example expression: ¬(P & Q)
expression = Expression(Expression.NEG, Expression(Expression.AND, 'P', 'Q'))
print("Original Expression:", expression)

# Apply move_negation_inward function
new_expression = move_negation_inward(expression)
print("After Moving Negation Inward:", new_expression)

from sympy import symbols, Or, And, Not, to_cnf

# Define symbolic variables
P, Q, R = symbols('P Q R')

# Logical expression
logical_expr = Or(And(P, Q), Not(R))

# Convert to CNF
cnf_expr = to_cnf(logical_expr)

# Print CNF expression
print("CNF Expression:", cnf_expr)


class Expression:
    FORALL = '∀'
    EXISTS = '∃'
    NEG = '~'

    def _init_(self, op, var, formula=None):
        self.op = op
        self.var = var
        self.formula = formula

    def _repr_(self):
        return f'{self.op}{self.var}.{self.formula}'


def move_quantifiers(expression):
    def helper(expr, quantifiers):
        if expr.op in [Expression.FORALL, Expression.EXISTS]:
            quantifiers.append(expr)
            return helper(expr.formula, quantifiers)
        else:
            return expr, quantifiers

    _, quantifiers = helper(expression, [])

    prenex_expression = quantifiers[0]
    for q in quantifiers[1:]:
        prenex_expression = Expression(q.op, q.var, prenex_expression)

    return prenex_expression


# Example expression
expression = Expression(Expression.EXISTS, 'x', Expression(Expression.FORALL, 'y', Expression(Expression.NEG, 'P')))

# Convert to prenex form
prenex_expression = move_quantifiers(expression)

# Print result
print("Original Expression:", expression)
print("After Moving Quantifiers:", prenex_expression)


class Expression:
    FORALL = '∀'
    EXISTS = '∃'
    NEG = '~'

    def _init_(self, op, var, formula=None):
        self.op = op
        self.var = var
        self.formula = formula

    def _repr_(self):
        return f'{self.op}{self.var}.{self.formula}' if self.op in [Expression.FORALL,
                                                                    Expression.EXISTS] else f'{self.op}{self.formula}'


def remove_universal_quantifiers(expression):
    if expression.op == Expression.FORALL:
        return remove_universal_quantifiers(expression.formula)
    elif expression.op == Expression.EXISTS:
        return Expression(Expression.EXISTS, expression.var, remove_universal_quantifiers(expression.formula))
    else:
        if expression.formula is not None:
            return Expression(expression.op, expression.var, remove_universal_quantifiers(expression.formula))
        else:
            return Expression(expression.op, expression.var)


# Example expression
expression = Expression(Expression.EXISTS, 'x', Expression(Expression.FORALL, 'y', Expression(Expression.NEG, 'P')))

# Remove universal quantifiers
quantifier_removed_expression = remove_universal_quantifiers(expression)

# Print result
print("Original Expression:", expression)
print("Expression with Universal Quantifiers Removed:", quantifier_removed_expression)


def remove_double_negation(statement):
    while '' in statement:
        statement = statement.replace('', '')
    return statement


# Example usage of remove_double_negation
statement = '(P & Q)'
print("Original Statement:", statement)
new_statement = remove_double_negation(statement)
print("After Removing Double Negation:", new_statement)
