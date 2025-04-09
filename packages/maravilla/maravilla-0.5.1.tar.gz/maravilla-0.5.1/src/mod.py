
class Modulo():
	def __init__(self,objet,mod):
		self.objet = objet % mod
		self.mod = mod

	def __add__(self,other):
		return (self.objet  + other.objet) % mod

	def __mul__(self,other):
		return (self.objet * other.objet) % mod

	def __pow__(self,other):
		result = self
		for i in range(int(other)):
			result *= self
		return result

	def __eq__(self,other):
		return (self.ojet == other.objet and self.mod == other.mod)

	
		
