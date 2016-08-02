# there are some pieces
# there are 55 slots
# each piece fills some slots
# for each piece, find out all the places it can live
# pick the first piece, place it somewhere, then get rid of all the options
# for all the other pieces that would intersect

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
	# draw 4x4 grid with O's where the piece is
	for i in range(piece["height"]):
		print(bar)
		row = "  |"
		for j in range(piece["width"]):
			if [i, j] in piece["coords"]:
				row += " O "
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

board = []
for i in range(0, BOARD_WIDTH):
	for j in range(0, BOARD_HEIGHT):
		board.append([i, j])

def get_all_positions(piece, board):
	positions = []
	for translation in get_unique_translations(piece):
		for position in board:
			if is_valid_position(translation, position):
				positions.append(shift(translation, position))
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

for piece in pieces:  # sorry about the variable names
	if len(piece["possibilities"]) == 0:
		print("Oh noes!")
		break
	placed_piece = piece["possibilities"][0]
	placed.append(placed_piece)
	placed_names.append(placed_piece["name"])
	for p in pieces:
		if p["name"] in placed_names:
			continue
		new_possibilities = []
		for possibility in p["possibilities"]:
			for c in possibility["coords"]:
				if c not in placed_piece["coords"]:
					new_possibilities.append(possibility)
		p["possibilities"] = new_possibilities
	print(placed_names)

# for piece in pieces:
# 	print(piece["name"])
# 	for translation in get_unique_translations(piece):
# 		draw(translation)
# 	print("\n\n")

