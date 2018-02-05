import unittest

import intro


class TestIntro(unittest.TestCase):
    def test_logged_in(self):
        self.assertEqual('I have logged into both the Edlab and Gradescope.', intro.logged_in())

    def test_add(self):
        self.assertEqual(7, intro.add(3, 4))
        self.assertEqual(-1, intro.add(3, -4))

    def test_divide(self):
        self.assertEqual(3.5, intro.divide(7, 2))
        self.assertEqual(3, intro.divide(12, 4))

    def test_value_equal(self):
        x = [1]
        y = [1]
        z = [2]
        self.assertTrue(intro.value_equal(x, y))
        self.assertFalse(intro.value_equal(x, z))

    def test_memory_equal(self):
        x = [1]
        y = x
        z = [1]
        self.assertTrue(intro.memory_equal(x, y))
        self.assertFalse(intro.memory_equal(x, z))

    def test_hello(self):
        self.assertEqual('Hello Joe', intro.hello('Joe'))

    def test_nth(self):
        self.assertEqual('c', intro.nth('abcde', 2))
        self.assertEqual(6, intro.nth([0, 2, 4, 6], 3))

    def test_subsequence(self):
        self.assertEqual('cd', intro.subsequence('abcde', 2, 4))
        self.assertEqual([0, 2], intro.subsequence([0, 2, 4, 6], 0, 2))

    def test_last(self):
        self.assertEqual('e', intro.last('abcde'))
        self.assertEqual(6, intro.last([0, 2, 4, 6]))

    def test_append(self):
        l = []
        intro.append_to(l, 1)
        self.assertEqual([1], l)
        intro.append_to(l, 2)
        self.assertEqual([1, 2], l)

    def test_sum_of(self):
        self.assertEqual(10, intro.sum_of([1, 2, 3, 4]))

    def test_all_even(self):
        self.assertTrue(intro.all_even([2, 4, 6]))
        self.assertFalse(intro.all_even([1, 2, 4, 6]))
        self.assertFalse(intro.all_even([2, 4, 6, 7]))
        self.assertTrue(intro.all_even([]))
        self.assertFalse(intro.all_even('banana'))

    def test_lookup(self):
        d = {1: 'a', 2: 'b'}
        self.assertEqual('a', intro.lookup(d, 1))

    def test_insert(self):
        d = {1: 'a', 2: 'b'}
        intro.insert(d, 3, 'c')
        self.assertEqual({1: 'a', 2: 'b', 3: 'c'}, d)

    def test_read_all(self):
        s = '''Hello, this is a test.\nThis is only a test.\n'''
        self.assertEqual(s, intro.read_all('test.txt'))


if __name__ == '__main__':
    unittest.main()
