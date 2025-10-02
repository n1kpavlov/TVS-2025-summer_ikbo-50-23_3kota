import unittest
from unittest.mock import patch
from io import StringIO
#from Andrew import add, subtraction, multiply, divide, check_action
from mutant_andrew import add, subtraction, multiply, divide, check_action


class TestCalculatorFunctions(unittest.TestCase):

    def test_add(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            add(5, 3)
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "5 + 3 = 8")

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            add(-2, 7)
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "-2 + 7 = 5")

    def test_subtraction(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            subtraction(10, 4)
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "10 - 4 = 6")

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            subtraction(5, 8)
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "5 - 8 = -3")

    def test_multiply(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            multiply(3, 4)
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "3 * 4 = 12")

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            multiply(-2, 5)
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "-2 * 5 = -10")

    def test_divide(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            divide(10, 3)
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "10 / 3 = 3")

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            divide(8, 2)
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "8 / 2 = 4")

    @patch('builtins.input')
    def test_check_action_addition(self, mock_input):
        mock_input.side_effect = ['5', '3']

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            check_action('+')
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "5.0 + 3.0 = 8.0")

    @patch('builtins.input')
    def test_check_action_subtraction(self, mock_input):
        mock_input.side_effect = ['10', '4']

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            check_action('-')
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "10.0 - 4.0 = 6.0")

    @patch('builtins.input')
    def test_check_action_multiply(self, mock_input):
        mock_input.side_effect = ['3', '4']

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            check_action('*')
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "3.0 * 4.0 = 12.0")

    @patch('builtins.input')
    def test_check_action_divide(self, mock_input):
        mock_input.side_effect = ['10', '3']

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            check_action('/')
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "10.0 / 3.0 = 3.0")

    def test_check_action_invalid_operation(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            check_action('invalid')
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "Такого действия нет")


if __name__ == '__main__':
    unittest.main()