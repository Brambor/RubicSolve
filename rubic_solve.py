from copy import deepcopy
print("Rubic's cube")

def out(*args, **kwargs):
	kwargs["end"] = ""
	print(*args, **kwargs)

def sp(x=1):
	print(end=" "*x)

def nl():
	print()

"""
 0
123
 4
 5
back
left top right
front
bottom

	678
	345
	012

852 012 036
741 345 147
630 678 258

	210
	543
	876
	
	012
	345
	678
"""

class Cube():
	def __init__(self, other=None):
		if other == None:
			self.cube = list(list(j for _ in range(9)) for j in range(6))
		else:
			self.cube = deepcopy(other.cube)
		self.actions = (
			self.turn_top_right,
			self.turn_top_left,
			self.turn_right_back,
			self.turn_right_front,
			self.turn_left_back,
			self.turn_left_front,
			self.turn_bottom_right,
			self.turn_bottom_left,
			self.turn_back_right,
			self.turn_back_left,
			self.turn_front_right,
			self.turn_front_left,
		)
	
	def __eq__(self, other):
		return type(other) == type(self) and self.cube == other.cube
	
	def print_gen(self, side, order):
		for i, o in enumerate(order):
				out(self.cube[side][o])
				if i % 3 == 2:
					yield

	def get_sides(self):
		return tuple(
			self.print_gen(s, order) for s, order in enumerate((
				(6,7,8,3,4,5,0,1,2),
				(8,5,2,7,4,1,6,3,0),
				(0,1,2,3,4,5,6,7,8),
				(0,3,6,1,4,7,2,5,8),
				(2,1,0,5,4,3,8,7,6),
				(0,1,2,3,4,5,6,7,8),
			))
		)
				
	def print(self):
		sides = self.get_sides()
		for _ in range(3):
			sp(4), sides[0].__next__(), nl()
		nl()
		for _ in range(3):
			sides[1].__next__(), sp(), sides[2].__next__(), sp(), sides[3].__next__(), nl()
		for _ in range(3):
			sp(4), sides[4].__next__(), nl()
		nl()
		for _ in range(3):
			sp(4), sides[5].__next__(), nl()
		print("---------")

	def _turn_same_side(self, side, order):
		c = self.cube[side]
		c[0], c[1], c[2], c[3], c[5], c[6], c[7], c[8] = c[order[0]], c[order[1]], c[order[2]], c[order[3]], c[order[4]], c[order[5]], c[order[6]], c[order[7]]  # note missing 4
		return c[order[0]], c[order[1]], c[order[2]], c[order[3]], c[4], c[order[4]], c[order[5]], c[order[6]], c[order[7]]

	def _turn_adjacent_sides(self, sides, orders):
		for a,b,c,d in orders:
			self.cube[sides[0]][a], self.cube[sides[1]][b], self.cube[sides[2]][c], self.cube[sides[3]][d] = self.cube[sides[1]][b], self.cube[sides[2]][c], self.cube[sides[3]][d], self.cube[sides[0]][a]

	#-----------------------------

	def turn_top_right(self):
		self._turn_same_side(2, (6,3,0,7,1,8,5,2))
		self._turn_adjacent_sides((0,1,3,4),(
			((i for _ in range(4)) for i in range(3))
		))
	
	def turn_top_left(self):
		for _ in range(3):
			self.turn_top_right()
		
	def turn_right_back(self):
		self._turn_same_side(3, (2,5,8,1,7,0,3,6))
		self._turn_adjacent_sides((0,2,4,5), (
			(8,2,0,2),
			(5,5,3,5),
			(2,8,6,8),
		))
	
	def turn_right_front(self):
		for _ in range(3):
			self.turn_right_back()

	def turn_left_back(self):
		self._turn_same_side(1, (2,1,0,5,3,8,7,6))
		self._turn_adjacent_sides((0,2,4,5), (
			(6,0,2,0),
			(3,3,5,3),
			(0,6,8,6),
		))
	
	def turn_left_front(self):
		for _ in range(3):
			self.turn_left_back()
	
	def turn_bottom_right(self):
		self._turn_same_side(5, (2,5,8,1,7,0,3,6))
		self._turn_adjacent_sides((0,1,3,4),
			((i for _ in range(4)) for i in range(6,9))
		)
	
	def turn_bottom_left(self):
		for _ in range(3):
			self.turn_bottom_right()

	def turn_back_right(self):
		self._turn_same_side(0, (0,3,6,1,7,2,5,8))
		self._turn_adjacent_sides((5,3,2,1), (
			(0,0,0,8),
			(1,3,1,5),
			(2,6,2,2),
		))
	
	def turn_back_left(self):
		for _ in range(3):
			self.turn_back_right()

	def turn_front_right(self):
		self._turn_same_side(4, (8,5,2,7,1,6,3,0))
		self._turn_adjacent_sides((5,3,2,1), ( # wrong?
			(2,2,6,6),
			(1,5,7,3),
			(0,8,8,0),
		))
	
	def turn_front_left(self):
		for _ in range(3):
			self.turn_front_right()
	
	#-----------------------------

	def is_solved(self):
		return self == solved_cube
	
	def BFS_layer(self, depth=0, cube_start=None):
		for a in range(len(self.actions)):
			if cube_start == None:
				cube = Cube(self)
			else:
				cube = Cube(cube_start)
			cube.actions[a]()
			if depth <= 0:
				cube.print()
			else:
				self.BFS_layer(depth-1, cube)

solved_cube = Cube()

rb = Cube()

assert(rb.is_solved())
for i in range(3):
	rb.turn_top_right()
	assert(not rb.is_solved())
rb.turn_top_right()
assert(rb.is_solved())

rb.turn_right_back()
#rb.print()

rb.turn_left_back()
#rb.print()

rb = Cube()
rb.BFS_layer(1)
