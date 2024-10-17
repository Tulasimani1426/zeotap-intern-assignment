class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.node_type = node_type  # 'operator' or 'operand'
        self.value = value  # Optional for operators, value for operands (e.g., 'age > 30')
        self.left = left  # Reference to another Node (left child)
        self.right = right  # Reference to another Node (right child for operators)

import re

def create_rule(rule_string):
    # Parse the rule string and create the AST using Node class
    tokens = re.split(r'(\sAND\s|\sOR\s)', rule_string)  # Split by AND/OR
    root = None
    current_node = None
    
    for token in tokens:
        token = token.strip()
        
        if token in ('AND', 'OR'):
            new_node = Node('operator', token)
            if root is None:
                root = new_node
            else:
                current_node.right = new_node
            new_node.left = current_node
            current_node = new_node
        else:
            operand_node = Node('operand', token)
            if current_node is None:
                root = operand_node
            else:
                current_node.right = operand_node
            current_node = operand_node

    return root

def combine_rules(rules):
    # Combine multiple ASTs into one by joining them with 'AND'
    combined_root = None
    for rule in rules:
        if combined_root is None:
            combined_root = rule
        else:
            new_root = Node('operator', 'AND', combined_root, rule)
            combined_root = new_root
    return combined_root

def evaluate_rule(node, data):
    if node.node_type == 'operand':
        # Evaluate the condition (simple eval for demonstration purposes)
        return eval(node.value, {}, data)
    
    elif node.node_type == 'operator':
        left_result = evaluate_rule(node.left, data)
        right_result = evaluate_rule(node.right, data)
        
        if node.value == 'AND':
            return left_result and right_result
        elif node.value == 'OR':
            return left_result or right_result

# Test the code with example rules and data

# Example rule 1
rule1 = create_rule("age > 30 AND department = 'Sales'")
# Example rule 2
rule2 = create_rule("age < 25 AND department = 'Marketing'")

# Combine both rules
combined_rule = combine_rules([rule1, rule2])

# Test data
sample_data = {'age': 35, 'department': 'Sales', 'salary': 60000, 'experience': 3}

# Evaluate combined rule
result = evaluate_rule(combined_rule, sample_data)
print(result)  # True or False depending on whether the data matches the rule
