# pythontiles Library
- board_size(height, width)
- reset_to_empty()
- import_from_nme(filename)
- value_at_tile(x, y) -> string
- is_legal_tile(x, y) -> boolean
- change_tile(x, y, text)
- move_piece(x1, y1, x2, y2)
- NME_Decode_File(filename) -> array of arrays

# NME File Format
- First line denotes the number of sections per line
- For instance:
- **`6`**
- **`<name>/<piece1>/<piece2>/<piece3>/<piece4>/<piece5>/`**
