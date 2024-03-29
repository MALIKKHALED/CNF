import re


def Eliminate_implication(expression):
    pattern = r'(¬?)([(A-Za-z)]+)\s*=>\s*(¬?)([(A-Za-z)]+)'
    expression = re.sub(pattern, r'¬\1\2 | \3\4', expression)
    pattern = r'(¬?)([(A-Za-z)]+)\s*<=>\s*(¬?)([(A-Za-z)]+)'
    expression = re.sub(pattern, r'(¬\1\2 | \3\4) & (\1\2 | ¬\3\4)', expression)
    return expression


def DeMorgans_laws(expression):
    pattern1 = r'¬\((.*?)\s*&\s*(.*?)\)'
    pattern2 = r'¬\((.*?)\s*\|\s*(.*?)\)'
    expression = re.sub(pattern1, r'(¬\1 | ¬\2)', expression)
    expression = re.sub(pattern2, r'(¬\1 & ¬\2)', expression)
    return expression


def remove_double_negation(expression):
    while '¬¬' in expression:
        expression = expression.replace('¬¬', '')
    return expression


def get_unique_variable(used_variables):
    # Generate a new variable that is not used before
    for i in range(ord('a'), ord('z') + 1):
        new_variable = chr(i)
        if new_variable not in used_variables:
            return new_variable
    return None


def Standardize_variable_scope(expression):
    # Regular expression pattern to match ∀ or ∃ followed by variables
    pattern = r'(∀|∃)[a-zA-Z]+'

    # Find all parts separated by '&'
    parts = re.split(r'\s*&\s*(?=∃|∀)', expression)
    replaced_parts = []
    used_variables = set()
    for part in parts:
        # Extract the variable after the first ∀ or ∃
        match = re.search(pattern, part)
        if match:
            old_expression = match.group(0)
            old_variable = old_expression[1:]  # Extract variable from the matched expression
            new_variable = get_unique_variable(used_variables)
            if new_variable:
                used_variables.add(new_variable)
                replaced_part = part.replace(old_variable, new_variable)
                replaced_part = replaced_part.replace(old_expression, old_expression[0] + new_variable)
                replaced_parts.append(replaced_part)
            else:
                print("Error: No more unique variables available.")
                return None
        else:
            replaced_parts.append(part)

    # Join the replaced parts back using '&'
    replaced_expression = ' & '.join(replaced_parts)
    return replaced_expression


def prenex_form(expression):
    pattern = r'∀[a-zA-Z]|∃[a-zA-Z]+'
    pattern1 = r'∀[a-zA-Z]+'
    pattern2 = r'∃[a-zA-Z]+'
    match1 = re.findall(pattern1, expression)
    match2 = re.findall(pattern2, expression)

    expression = re.sub(pattern, '', expression)
    expression = ' '.join(match1) + " " + ' '.join(match2) + expression

    return expression


def Skolemization_for_existential_quantifiers(expression):
    # Regular expression pattern to match ∃ followed by variables
    pattern = r'∃[a-zA-Z]+'
    pattern2 = r'∀([a-zA-Z]+)\s∃([a-zA-Z]+)'
    match = re.findall(pattern2, expression)
    expression = re.sub(pattern, '', expression)
    for i in match:
        var1 = i[0]
        var2 = i[1]
        expression = expression.replace(var2, "f(" + var1 + ")")
    return expression


def Eliminate_universal_quantifiers(expression):
    pattern = r'∀[a-zA-Z]+'
    match = re.findall(pattern, expression)
    expression = re.sub(pattern, '', expression)
    return expression


def CNF_Algorithm(expression):
    expression = Eliminate_implication(expression)
    expression = DeMorgans_laws(expression)
    expression = remove_double_negation(expression)
    expression = Standardize_variable_scope(expression)
    expression = Skolemization_for_existential_quantifiers(expression)
    expression = prenex_form(expression)
    expression = Eliminate_universal_quantifiers(expression)
    return expression


print(CNF_Algorithm("∀x (¬P(x) => Q(x)) & ∀x ∃y ((S(x) | R(y)) & ∀x ∃z (S(x) <=> R(z))"))
