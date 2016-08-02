# there are some pieces
# there are 55 slots
# each piece fills some slots
# for each piece, find out all the places it can live
# pick the first piece, place it somewhere, then get rid of all the options
# for all the other pieces that would intersect

import itertools, string

# populate the pieces array
pieces = []
pieces.append({"name": "gray", \
	"coords": [[1, 0], [0, 1], [1, 1], [1, 2], [2, 1]], \
	"height": 3, "width": 3})
pieces.append({"name": "red", \
	"coords": [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1]], \
	"height": 2, "width": 3})
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
		board[c[0]][c[1]] = piece["name"][0]

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
		for j in range(BOARD_WIDTH):
			for i in range(BOARD_HEIGHT):
				if is_valid_position(translation, [i, j]):
					positions.append(shift(translation, [i, j]))
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

for piece in pieces:  # sorry about the variable names
	print_board(board)
	if len(piece["possibilities"]) == 0:
		print("Oh noes!")
		break
	placed_piece = piece["possibilities"][0]
	placed.append(placed_piece)
	board_insert(board, placed_piece)
	placed_names.append(placed_piece["name"])
	for p in pieces:
		if p["name"] in placed_names:
			continue
		new_possibilities = []
		for possibility in p["possibilities"]:
			append_bool = True
			for c in possibility["coords"]:
				if c in placed_piece["coords"]:
					append_bool = False
					break
			if append_bool:
				new_possibilities.append(possibility)
		p["possibilities"] = new_possibilities
	print(placed_names)

# for piece in pieces:
# 	print(piece["name"])
# 	for translation in get_unique_translations(piece):
# 		draw(translation)
# 	print("\n\n")

# for possibility in pieces[3]["possibilities"]:
# 	draw(possibility)
# 	print("\n\n")