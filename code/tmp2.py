
import piece
from piece import PIECES


for p_type in PIECES:
	p = piece.Piece(p_type)

	for i in range(10000):
		p.rotate_right()
	for i in range(10000):
		p.rotate_left()

