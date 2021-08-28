from pathing import *




#testing
def test_walk_direct():
	start_pos = (0,0)
	end_pos = (3,8)
	route = walk_direct(start_pos, end_pos, None)
	print(route)

def test_bfs():
	R = 10
	C = 10
	s = (0,0)
	e = (3,8)
	world = World((R, C))
	path = bfs_path(s, e, world)
	print("bfs test result:")
	print(path)

def test_bfs_X():
	R = 10
	C = 10
	s = (7,0)
	e = 9
	world = World((R, C))
	path = bfs_path_to_side(s, e, world)
	print("bfs test result:")
	print(path)


if __name__ == "__main__":
	test_bfs()
	test_bfs_X()