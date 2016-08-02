# there are some pieces
# there are 55 slots
# each piece fills some slots
# for each piece, find out all the places it can live
# pick the first piece, place it somewhere, then get rid of all the options
# for all the other pieces that would intersect

import itertools, string, copy

# populate the pieces array
pieces = []
pieces.append({"name": "red", \
	"coords": [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1]], \
	"height": 2, "width": 3})
pieces.append({"name": "gray", \
	"coords": [[1, 0], [0, 1], [1, 1], [1, 2], [2, 1]], \
	"height": 3, "width": 3})
pieces.append({"name": "blue", \
	"coords": [[0, 0], [0, 1], [0, 2], [0, 3], [1, 3]], \
	"height": 2, "width": 4})
pieces.append({"name": "cyan", \
	"coords": [[0, 0], [0, 1], [0, 2], [1, 0], [2, 0]], \
	"height": 3, "width": 3})
pieces.append({"name": "purple", \
	"coords": [[0, 0], [0, 1], [0, 2], [0, 3]], \
	"height": 1, "width": 4})
pieces.append({"name": "lime", \
	"coords": [[0, 0], [0, 1], [1, 1], [1, 0]], \
	"height": 2, "width": 2})
pieces.append({"name": "green", \
	"coords": [[0, 0], [0, 1], [1, 1], [1, 2], [1, 3]], \
	"height": 2, "width": 4})
pieces.append({"name": "white", \
	"coords": [[1, 0], [0, 1], [0, 0]], \
	"height": 2, "width": 2})
pieces.append({"name": "magenta", \
	"coords": [[0, 0], [0, 1], [1, 1], [1, 2], [2, 2]], \
	"height": 3, "width": 3})
pieces.append({"name": "pink", \
	"coords": [[0, 0], [0, 1], [1, 1], [0, 2], [0, 3]], \
	"height": 2, "width": 4})
pieces.append({"name": "yellow", \
	"coords": [[0, 0], [0, 1], [1, 0], [0, 2], [1, 2]], \
	"height": 2, "width": 3})
pieces.append({"name": "orange", \
	"coords": [[0, 0], [0, 1], [1, 0], [0, 2]], \
	"height": 2, "width": 3})

pieces[0]["name"] = '\033[4;31m' + u"\u25C9" + '\033[0m'
pieces[1]["name"] = '\033[4;37m' + u"\u25C9" + '\033[0m'
pieces[2]["name"] = '\033[0;34m' + u"\u25C9" + '\033[0m'
pieces[3]["name"] = '\033[0;36m' + u"\u25C9" + '\033[0m'
pieces[4]["name"] = '\033[4;35m' + u"\u25C9" + '\033[0m'
pieces[5]["name"] = '\033[1;32m' + u"\u25C9" + '\033[0m'
pieces[6]["name"] = '\033[0;32m' + u"\u25C9" + '\033[0m'
pieces[7]["name"] = '\033[0;37m' + u"\u25C9" + '\033[0m'
pieces[8]["name"] = '\033[1;35m' + u"\u25C9" + '\033[0m'
pieces[9]["name"] = '\033[0;35m' + u"\u25C9" + '\033[0m'
pieces[10]["name"] = '\033[0;33m'+ u"\u25C9" + '\033[0m'
pieces[11]["name"] = '\033[1;31m'+ u"\u25C9" + '\033[0m'

# sort the coordinates so we can check for equality
for piece in pieces:
	piece["coords"] = sorted(piece["coords"])

# print a representation of the piece to the terminal
def draw(piece):
	bar = "  " + "+---" * piece["width"] + "+"

	# find the min x and y, so draw works for shifted pieces
	min_x = BOARD_WIDTH + 1
	min_y = BOARD_HEIGHT + 1
	for coord in piece["coords"]:
		if coord[0] < min_x:
			min_x = coord[0]
		if coord[1] < min_y:
			min_y = coord[1]

	# draw a grid with dimensions width by height
	for i in range(min_x, min_x + piece["height"]):
		print(bar)
		row = "  |"
		for j in range(min_y, min_y + piece["width"]):
			if [i, j] in piece["coords"]:
				# if the piece contains this cell, print the coordinates
				cell = "%s,%s" % (i, j)
				if len(cell) > 3:  # (for neatness)
					cell = string.replace(cell, ',', '')
				row += cell
			else:
				row += "   "
			row += "|"
		print(row)
	print(bar)

# rotate the piece counterclockwise
def rotate(piece):
	new_coords = []
	for coord in piece["coords"]:
		new_coords.append([(-1 * coord[1]) + piece["width"] - 1, coord[0]])
	new_piece = {"name": piece["name"], "coords": sorted(new_coords), \
		"height": piece["width"], "width": piece["height"]}
	return new_piece

# reflect the piece across its own center line
def reflect(piece):
	new_coords = []
	for coord in piece["coords"]:
		new_coords.append([coord[0], (piece["width"] - 1) - coord[1]])
	new_piece = {"name": piece["name"], "coords": sorted(new_coords), \
		"height": piece["height"], "width": piece["width"]}
	return new_piece

# shift the piece so its origin, previously (0,0), is now at (position)
def shift(piece, position):
	new_coords = []
	for coord in piece["coords"]:
		new_coords.append([coord[0] + position[0], coord[1] + position[1]])
	new_piece = {"name": piece["name"], "coords": sorted(new_coords), \
		"height": piece["height"], "width": piece["width"]}
	return new_piece

# get all possible rotations and reflections for the piece
def get_unique_translations(piece):
	dummy = [piece, \
		rotate(piece), \
		rotate(rotate(piece)), \
		rotate(rotate(rotate(piece))), \
		reflect(piece), \
		reflect(rotate(piece)), \
		reflect(rotate(rotate(piece))), \
		reflect(rotate(rotate(rotate(piece))))]
	translations = []
	for translation in dummy:
		if translation not in translations:
			translations.append(translation)
	return translations

BOARD_WIDTH = 11
BOARD_HEIGHT = 5

# insert a piece into the board (by the first letter of its name, for now)
def board_insert(board, piece):
	for c in piece["coords"]:
		board[c[0]][c[1]] = piece["name"]

def board_remove(board, piece):
	for c in piece["coords"]:
		board[c[0]][c[1]] = " "


# print a representation of the board to the terminal
def print_board(placed):
	bar = " " + "+---" * BOARD_WIDTH + "+"
	for i in range(BOARD_HEIGHT):
		print(bar)
		row = ""
		for j in range(BOARD_WIDTH):
			row += " | " + placed[i][j]
		row += " |"
		print(row)
	print(bar)

# populate the board with empty spaces
board = [[" " for j in range(BOARD_WIDTH)] for i in range(BOARD_HEIGHT)]

# check all the possible translations, shifting them to all possible spots,
# and return all valid possibilities
def get_all_positions(piece, board):
	positions = []
	for translation in get_unique_translations(piece):
		for i in range(BOARD_HEIGHT):
			for j in range(BOARD_WIDTH):
				if is_valid_position(translation, [i, j]):
					positions.append(shift(translation, [i, j]))
	# for position in positions:
	# 	b1 = [[" " for j in range(BOARD_WIDTH)] for i in range(BOARD_HEIGHT)]
	# 	board_insert(b1, position)
	# 	print_board(b1)
	# 	print("\n")
	return positions

# check if the piece, shifted to the given position, falls within the board's
# dimensions
def is_valid_position(piece, position):
	if position[1] + piece["width"] > BOARD_WIDTH:
		return False
	if position[0] + piece["height"] > BOARD_HEIGHT:
		return False
	return True

# give each piece an array of all of its own possibilities
for piece in pieces:
	piece["possibilities"] = get_all_positions(piece, board)

placed = []
placed_names = []

# for piece in pieces:  # sorry about the variable names
# 	print_board(board)
# 	if len(piece["possibilities"]) == 0:
# 		print("Oh noes!")
# 		break
# 	placed_piece = piece["possibilities"][0]
# 	placed.append(placed_piece)
# 	board_insert(board, placed_piece)
# 	placed_names.append(placed_piece["name"])
# 	for p in pieces:
# 		if p["name"] in placed_names:
# 			continue
# 		new_possibilities = []
# 		for possibility in p["possibilities"]:
# 			append_bool = True
# 			for c in possibility["coords"]:
# 				if c in placed_piece["coords"]:
# 					append_bool = False
# 					break
# 			if append_bool:
# 				new_possibilities.append(possibility)
# 		p["possibilities"] = new_possibilities
# 	print(placed_names)

def hole_around(c, empties):
	hole = [c]
	for h in hole:
		left = [h[0] - 1, h[1]]
		right = [h[0] + 1, h[1]]
		up = [h[0], h[1] - 1]
		down = [h[0], h[1] + 1]
		neighbors = [left, right, up, down]
		for n in neighbors:
			if n in empties:
				empties.remove(n)
				hole.append(n)
				newBool = True
	min_x = BOARD_WIDTH + 1
	min_y = BOARD_HEIGHT + 1
	for h in hole:
		if h[0] < min_x:
			min_x = h[0]
		if h[1] < min_y:
			min_y = h[1]
	origin_hole = []
	for h in hole:
		origin_hole.append([h[0] - min_x, h[1] - min_y])
	return hole

def tiny_hole(board, pieces):
	empties = []
	for i in range(BOARD_HEIGHT):
		for j in range(BOARD_WIDTH):
			if board[i][j] == " ":
				empties.append([i, j])
	holes = []
	for e in empties:
		holes.append(hole_around(e, empties))
	for hole in holes:
		pBool = False
		for piece in pieces:
			for poss in piece["possibilities"]:
				fitBool = True
				for c in poss["coords"]:
					if c not in hole:
						fitBool = False
						break
				if fitBool:
					pBool = True
					break
		if not pBool:
			return True
	return False

def place_piece(i):
	global pieces
	global board
	if i == len(pieces):
		print_board(board)
		return
	piece = pieces[i]
	l = len(piece["possibilities"])
	# print("l: " + str(l))
	if l == 0:
		return
	for j in range(l):
		board_copy = copy.deepcopy(board)
		pieces_copy = copy.deepcopy(pieces)
		piece_copy = copy.deepcopy(piece)
		translation = piece["possibilities"][j]
		board_insert(board, translation)
		if tiny_hole(board, pieces[i + 1:]):
			board_remove(board, translation)
			continue
		for p in pieces:
			new_possibilities = []
			for possibility in p["possibilities"]:
				append_bool = True
				for c in possibility["coords"]:
					if c in translation["coords"]:
						append_bool = False
						break
				if append_bool:
					new_possibilities.append(possibility)
			p["possibilities"] = new_possibilities
		place_piece(i + 1)
		board = board_copy
		pieces = pieces_copy
		piece = piece_copy

place_piece(0)
print_board(board)

# for piece in pieces:
# 	print(piece["name"])
# 	for translation in get_unique_translations(piece):
# 		draw(translation)
# 	print("\n\n")

# for possibility in pieces[3]["possibilities"]:
# 	draw(possibility)
# 	print("\n\n")
