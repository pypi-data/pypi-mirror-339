import unittest
import maravilla.num as num 

class Tests(unittest.TestCase):
    def test_pgcd(self):
        self.assertEqual(num.totient(10),4)
        self.assertEqual(num.totient(50),20)
        self.assertEqual(num.totient(125),100)

if __name__ == '__main__':
    unittest.main()
