# there are some pieces
# there are 55 slots
# each piece fills some slots
# for each piece, find out all the places it can live
# pick the first piece, place it somewhere, then get rid of all the options
# for all the other pieces that would intersect

import itertools

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

for piece in pieces:
	piece["coords"] = sorted(piece["coords"])

def draw(piece):
	bar = "  " + "+---" * piece["width"] + "+"

	# find the min x and y so we can draw shifted pieces
	min_x = BOARD_WIDTH + 1
	min_y = BOARD_HEIGHT + 1
	for coord in piece["coords"]:
		if coord[0] < min_x:
			min_x = coord[0]
		if coord[1] < min_y:
			min_y = coord[1]

	# draw 4x4 grid with coordinates where the piece is
	for i in range(min_x, min_x + piece["height"]):
		print(bar)
		row = "  |"
		for j in range(min_y, min_y + piece["width"]):
			if [i, j] in piece["coords"]:
				cell = "%s,%s" % (i, j)
				if len(cell) > 3:
					import string
					cell = string.replace(cell, ',', '')
				row += cell
			else:
				row += "   "
			row += "|"
		print(row)
	print(bar)

def rotate(piece):
	new_coords = []
	for coord in piece["coords"]:
		new_coords.append([(-1 * coord[1]) + piece["width"] - 1, coord[0]])
	new_piece = {"name": piece["name"], "coords": sorted(new_coords), \
		"height": piece["width"], "width": piece["height"]}
	return new_piece

def reflect(piece):
	new_coords = []
	for coord in piece["coords"]:
		new_coords.append([coord[0], (piece["width"] - 1) - coord[1]])
	new_piece = {"name": piece["name"], "coords": sorted(new_coords), \
		"height": piece["height"], "width": piece["width"]}
	return new_piece

def shift(piece, position):
	new_coords = []
	for coord in piece["coords"]:
		new_coords.append([coord[0] + position[0], coord[1] + position[1]])
	new_piece = {"name": piece["name"], "coords": sorted(new_coords), \
		"height": piece["height"], "width": piece["width"]}
	return new_piece

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

def print_board(placed):
	bar = " " + "+---" * BOARD_WIDTH + "+"
	for i in range(BOARD_HEIGHT):
		print(bar)
		row = ""
		for j in range(BOARD_WIDTH):
			row += " | " + board[i][j]
		row += " |"
		print(row)
	print(bar)

board = [[" " for j in range(BOARD_WIDTH)] for i in range(BOARD_HEIGHT)]
print_board(board)


def get_all_positions(piece, board):
	positions = []
	for translation in get_unique_translations(piece):
		for i, j in itertools.product(range(BOARD_WIDTH), range(BOARD_HEIGHT)):
			if is_valid_position(translation, [i, j]):
				positions.append(shift(translation, [i, j]))
	return positions

def is_valid_position(piece, position):
	if position[0] + piece["width"] > BOARD_WIDTH:
		return False
	if position[1] + piece["height"] > BOARD_HEIGHT:
		return False
	return True

for piece in pieces:  # maybe not the best way to do this
	piece["possibilities"] = get_all_positions(piece, board)

print("got possibilities")

placed = []
placed_names = []

def board_insert(board, piece):
	for c in piece["coords"]:
		if board[c[0]][c[1]] == None:
			print("ahh!")
		board[c[0]][c[1]] = piece["name"][0]

for piece in pieces:  # sorry about the variable names
	if len(piece["possibilities"]) == 0:
		print_board(board)
		print("Oh noes!")
		break
	placed_piece = piece["possibilities"][0]
	placed.append(placed_piece)
	board_insert(board, piece)
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
			if append_bool:
				new_possibilities.append(possibility)
		p["possibilities"] = new_possibilities
	print(placed_names)

# for piece in pieces:
# 	print(piece["name"])
# 	for translation in get_unique_translations(piece):
# 		draw(translation)
# 	print("\n\n")

for possibility in pieces[3]["possibilities"]:
	draw(possibility)
	print("\n\n")