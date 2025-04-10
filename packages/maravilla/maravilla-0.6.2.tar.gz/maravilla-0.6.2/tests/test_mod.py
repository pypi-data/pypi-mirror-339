import unittest
from maravilla.mod import Modulo

class testMod(unittest.TestCase):
	def test_creation(self):
			Modulo(3,5)
			Modulo(4,6)
			Modulo(-2,3)
	def test_add(self):
			self.assertEqual(Modulo(5,3) + Modulo(7,3),Modulo(0,3))
			self.assertEqual(Modulo(5,4) + Modulo(7,4),Modulo(0,4))
	def test_mul(self):
			self.assertEqual(Modulo(5,3) * Modulo(7,3),Modulo(2,3))
			self.assertEqual(Modulo(5,4) * Modulo(7,4),Modulo(3,4))
	def test_pow(self):
			self.assertEqual(Modulo(5,3)**2 ,Modulo(1,3))

if __name__ == '__main__':
	unittest.main()
		
