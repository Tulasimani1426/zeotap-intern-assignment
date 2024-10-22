import unittest
from rule_engine import create_rule, combine_rules, evaluate_rule


class TestRuleEngine(unittest.TestCase):

    def test_create_rule(self):
        rule = create_rule("age > 30 AND department = 'Sales'")
        self.assertIsNotNone(rule)
        self.assertEqual(rule.value, 'age > 30')


    def test_combine_rules(self):
        rule1 = create_rule("age > 30 AND department = 'Sales'")
        rule2 = create_rule("age < 25 AND department = 'Marketing'")
        combined_rule = combine_rules([rule1, rule2])
        self.assertIsNotNone(combined_rule)
        self.assertEqual(combined_rule.value, 'AND')

    def test_evaluate_rule(self):
        rule = create_rule("age > 30 AND salary > 50000")
        data = {"age": 35, "salary": 60000}
        result = evaluate_rule(rule, data)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
