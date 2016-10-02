#!/usr/bin/python
# -*- coding: utf-8 -*-

import itertools, string, copy
import sqlite3, sys

con = sqlite3.connect('db.sqlite3')

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

pieces[0]["uni"] = '\033[0;31m' + u"\u25C9" + '\033[0m'
pieces[1]["uni"] = '\033[1;37m' + u"\u25C9" + '\033[0m'
pieces[2]["uni"] = '\033[0;34m' + u"\u25C9" + '\033[0m'
pieces[3]["uni"] = '\033[0;36m' + u"\u25C9" + '\033[0m'
pieces[4]["uni"] = '\033[0;35m' + u"\u25CE" + '\033[0m'
pieces[5]["uni"] = '\033[1;32m' + u"\u25C9" + '\033[0m'
pieces[6]["uni"] = '\033[0;32m' + u"\u25C9" + '\033[0m'
pieces[7]["uni"] = '\033[0;37m' + u"\u25C9" + '\033[0m'
pieces[8]["uni"] = '\033[1;35m' + u"\u25C9" + '\033[0m'
pieces[9]["uni"] = '\033[0;35m' + u"\u25C9" + '\033[0m'
pieces[10]["uni"] ='\033[0;33m' + u"\u25C9" + '\033[0m'
pieces[11]["uni"] ='\033[1;31m' + u"\u25C9" + '\033[0m'

# sort the coordinates so we can check for equality
for piece in pieces:
  piece["coords"] = sorted(piece["coords"])

# rotate the piece counterclockwise
def rotate(piece):
  new_coords = []
  for coord in piece["coords"]:
    new_coords.append([(-1 * coord[1]) + piece["width"] - 1, coord[0]])
  new_piece = {"name": piece["name"], "coords": sorted(new_coords), \
    "height": piece["width"], "width": piece["height"], \
    "uni": piece["uni"]}
  return new_piece

# reflect the piece across its own center line
def reflect(piece):
  new_coords = []
  for coord in piece["coords"]:
    new_coords.append([coord[0], (piece["width"] - 1) - coord[1]])
  new_piece = {"name": piece["name"], "coords": sorted(new_coords), \
    "height": piece["height"], "width": piece["width"], \
    "uni": piece["uni"]}
  return new_piece

# shift the piece so its origin, previously (0,0), is now at (position)
def shift(piece, position):
  new_coords = []
  for coord in piece["coords"]:
    new_coords.append([coord[0] + position[0], coord[1] + position[1]])
  new_piece = {"name": piece["name"], "coords": sorted(new_coords), \
    "height": piece["height"], "width": piece["width"], \
    "uni": piece["uni"]}
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

# insert a piece into the board
def board_insert(board, piece):
  for c in piece["coords"]:
    board[c[0]][c[1]]["name"] = piece["name"]
    board[c[0]][c[1]]["uni"] = piece["uni"]

def board_remove(board, piece):
  for c in piece["coords"]:
    board[c[0]][c[1]]["name"] = ""
    board[c[0]][c[1]]["uni"] = " "

# print a representation of the board to the terminal
def print_board(placed):
  bar = " " + "+---" * BOARD_WIDTH + "+"
  for i in range(BOARD_HEIGHT):
    print(bar)
    row = ""
    for j in range(BOARD_WIDTH):
      row += " | " + placed[i][j]["uni"]
    row += " |"
    print(row)
  print(bar)

# add board to the sqlite database so we can look at it later
def add_board_to_database(board, num):
  coord_list = []
  for i in range(BOARD_HEIGHT):
    for j in range(BOARD_WIDTH):
      c = (i, j, board[i][j]["name"], num)
      coord_list.append(c)
  coord_tuple = tuple(coord_list)

  with con:
    cur = con.cursor()
    cur.executemany("insert into coord values(?, ?, ?, ?)", coord_tuple)

# populate the board with empty spaces
board = [[{"name" : "", "uni" : " "} for j in range(BOARD_WIDTH)] \
          for i in range(BOARD_HEIGHT)]

# check all the possible translations, shifting them to all possible spots,
# and return all valid possibilities
def get_all_positions(piece):
  positions = []
  for translation in get_unique_translations(piece):
    for i in range(BOARD_HEIGHT):
      for j in range(BOARD_WIDTH):
        if is_valid_position(translation, [i, j]):
          positions.append(shift(translation, [i, j]))
  return positions

# check one of the possible translations, shifting them to all possible spots,
# and return all valid possibilities
def get_some_positions(piece):
  positions = []
  rotated = rotate(piece)
  for i in range(BOARD_HEIGHT):
    for j in range(BOARD_WIDTH):
      if is_valid_position(piece, [i, j]):
        positions.append(shift(piece, [i, j]))
      if is_valid_position(rotated, [i, j]):
        positions.append(shift(rotated, [i, j]))
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
  piece["possibilities"] = get_all_positions(piece)

# special case the first piece, to avoid double counting solutions
pieces[0]["possibilities"] = get_some_positions(pieces[0])

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
      if board[i][j]["uni"] == " ":
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

solutions = 0

def place_piece(i):
  global pieces
  global board
  global solutions
  if i == len(pieces):
    solutions += 1
    print("#" + str(solutions))
    print_board(board)
    add_board_to_database(board, solutions)
    print
    return
  piece = pieces[i]
  l = len(piece["possibilities"])
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
add_board_to_database(board, solutions)

