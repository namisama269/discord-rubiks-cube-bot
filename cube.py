import json

def rotate_face_cw(face):
    return list(map(list,zip(*face[::-1])))

orientation = "WOGRBY"

class Cube:
    def __init__(self, size):
        # User specified colour orientation
        self.orientation = orientation
        # 3x3, 4x4 or 5x5
        self.size = size
        # Set whether should automatically choose cycle break location when getting memo
        self.auto_cb = True
        # Check if waiting for user to provide a cycle break location
        self.waiting_cb = False
        # Store the next cycle break location when no longer waiting for user input
        self.next_cb = None
        # List of next cycle breaks
        self.breaks = []
        # Keep track of what has been memorised so far if need to print partial memo
        self.memo = {
            'c': None,
            'e': None,
            'w': None,
            'x': None,
            't': None,
        }
        
        if size not in (3,4,5):
            raise ValueError("Cube must be 3x3, 4x4 or 5x5")
        
        i = self.size
        with open(f"initface{i}{i}{i}.json", 'r') as f:
            self.faces = json.load(f)

        for item in self.faces.items():
            face_colour = orientation["ULFRBD".index(item[0])]
            for i in range(self.size):
                for j in range(self.size):
                    item[1][i][j][1] = face_colour


    def is_solved(self):
        for item in self.faces.items():
            for i in range(self.size):
                for j in range(self.size):
                    if item[1][i][j][1] != item[1][0][0][1]:
                        return False
        return True

    def reset(self):
        i = self.size
        with open(f"initface{i}{i}{i}.json", 'r') as f:
            self.faces = json.load(f)

        for item in self.faces.items():
            face_colour = self.orientation["ULFRBD".index(item[0])]
            for i in range(self.size):
                for j in range(self.size):
                    item[1][i][j][1] = face_colour
        

    def do_move(self, move):
        """
        Do either 1, 2 or 3 clockwise moves depending on if move ends in ', 2 or none.
        """
        if move[-1] in "'2":
            repeater = 2 if move[-1] == '2' else 3
            move = move[:-1]
        else:
            repeater = 1
        for _ in range(repeater):
            # Rotations: x, y, z
            if move in "xyz":
                self.rotation(move)
            # Single moves: U, L, F, R, B, D, u, l, f, r, b, d, M, E, S
            elif move in "ULFBRDulfbrdMES":
                self.single_move(move)
            # Compound moves: all others
            else:
                self.compound_move(move)

    def do_scramble(self, scr):
        for move in scr.split():
            self.do_move(move)


    def single_move(self, move):
        # Outer layer moves: U, L, F, R, B, D
        # 4x4 and 5x5 only: u, l, f, r, b, d
        # 3x3 and 5x5 only: M, E, S

        if move in "ULFRBD":
            self.faces[move] = rotate_face_cw(self.faces[move])
            if move == 'U':
                self.faces['L'][0], self.faces['F'][0], self.faces['R'][0], self.faces['B'][0] = \
                self.faces['F'][0], self.faces['R'][0], self.faces['B'][0], self.faces['L'][0]
            if move == 'D':
                self.faces['L'][-1], self.faces['F'][-1], self.faces['R'][-1], self.faces['B'][-1] = \
                self.faces['B'][-1], self.faces['L'][-1], self.faces['F'][-1], self.faces['R'][-1]
            if move == 'L':
                for i in range(self.size):
                    self.faces['U'][i][0], self.faces['F'][i][0], self.faces['D'][i][0], self.faces['B'][-1-i][-1] = \
                    self.faces['B'][-1-i][-1], self.faces['U'][i][0], self.faces['F'][i][0], self.faces['D'][i][0]
            if move == 'R':
                for i in range(self.size):
                    self.faces['U'][i][-1], self.faces['F'][i][-1], self.faces['D'][i][-1], self.faces['B'][-1-i][0] = \
                    self.faces['F'][i][-1], self.faces['D'][i][-1], self.faces['B'][-1-i][0], self.faces['U'][i][-1]
            if move == 'F':
                for i in range(self.size):
                    self.faces['U'][-1][i], self.faces['R'][i][0], self.faces['D'][0][-1-i], self.faces['L'][-1-i][-1] = \
                    self.faces['L'][-1-i][-1], self.faces['U'][-1][i], self.faces['R'][i][0], self.faces['D'][0][-1-i]
            if move == 'B':
                for i in range(self.size):
                    self.faces['U'][0][i], self.faces['R'][i][-1], self.faces['D'][-1][-1-i], self.faces['L'][-1-i][0] = \
                    self.faces['R'][i][-1], self.faces['D'][-1][-1-i], self.faces['L'][-1-i][0], self.faces['U'][0][i]

        elif move in "ulfbrd":
            if self.size == 3:
                self.compound_move(move.upper()+'w')
                return
            if move == 'u':
                self.faces['L'][1], self.faces['F'][1], self.faces['R'][1], self.faces['B'][1] = \
                self.faces['F'][1], self.faces['R'][1], self.faces['B'][1], self.faces['L'][1]
            if move == 'd':
                self.faces['L'][-2], self.faces['F'][-2], self.faces['R'][-2], self.faces['B'][-2] = \
                self.faces['B'][-2], self.faces['L'][-2], self.faces['F'][-2], self.faces['R'][-2]
            if move == 'l':
                for i in range(self.size):
                    self.faces['U'][i][1], self.faces['F'][i][1], self.faces['D'][i][1], self.faces['B'][-1-i][-2] = \
                    self.faces['B'][-1-i][-2], self.faces['U'][i][1], self.faces['F'][i][1], self.faces['D'][i][1]
            if move == 'r':
                for i in range(self.size):
                    self.faces['U'][i][-2], self.faces['F'][i][-2], self.faces['D'][i][-2], self.faces['B'][-1-i][1] = \
                    self.faces['F'][i][-2], self.faces['D'][i][-2], self.faces['B'][-1-i][1], self.faces['U'][i][-2]
            if move == 'f':
                for i in range(self.size):
                    self.faces['U'][-2][i], self.faces['R'][i][1], self.faces['D'][1][-1-i], self.faces['L'][-1-i][-2] = \
                    self.faces['L'][-1-i][-2], self.faces['U'][-2][i], self.faces['R'][i][1], self.faces['D'][1][-1-i]
            if move == 'b':
                for i in range(self.size):
                    self.faces['U'][1][i], self.faces['R'][i][-2], self.faces['D'][-2][-1-i], self.faces['L'][-1-i][1] = \
                    self.faces['R'][i][-2], self.faces['D'][-2][-1-i], self.faces['L'][-1-i][1], self.faces['U'][1][i]

        elif move in "MES":
            if self.size not in (3,5):
                return
            mid = self.size // 2
            if move == 'M':
                for i in range(self.size):
                    self.faces['U'][i][mid], self.faces['F'][i][mid], self.faces['D'][i][mid], self.faces['B'][-1-i][mid] = \
                    self.faces['B'][-1-i][mid], self.faces['U'][i][mid], self.faces['F'][i][mid], self.faces['D'][i][mid]
            if move == 'E':
                self.faces['L'][mid], self.faces['F'][mid], self.faces['R'][mid], self.faces['B'][mid] = \
                self.faces['B'][mid], self.faces['L'][mid], self.faces['F'][mid], self.faces['R'][mid]
            if move == 'S':
                for i in range(self.size):
                    self.faces['U'][mid][i], self.faces['R'][i][mid], self.faces['D'][mid][-1-i], self.faces['L'][-1-i][mid] = \
                    self.faces['L'][-1-i][mid], self.faces['U'][mid][i], self.faces['R'][i][mid], self.faces['D'][mid][-1-i]

    def compound_move(self, move):
        """
        For a compound move, reduce into a sequence of clockwise single moves.
        """
        
        # 3x3: Uw, Dw, Lw, Rw, Fw, Bw
        if self.size == 3:
            move_seq = {
                'Uw': ['U'] + ['E']*3,
                'Dw': ['D','E'],
                'Lw': ['L','M'],
                'Rw': ['R'] + ['M']*3,
                'Fw': ['F','S'],
                'Bw': ['B'] + ['S']*3,
            }[move]
        else: 
            # The base move_seq for a wide move is outer + inner layers on 4x4 and 5x5
            idx = 1 if move[0] in "34" else 0
            move_seq = [move[idx], move[idx].lower()]
            # If move involves more than 2 layers
            if move[0] in "34":
                # If cube is 5x5 and move is either 3_w or 4_w, case-specific middle layer move is required
                if self.size == 5: 
                    move_seq += {
                        'U': ['E']*3,
                        'D': ['E'],
                        'R': ['M']*3,
                        'L': ['M'],
                        'F': ['S'],
                        'B': ['S']*3,
                    }[move[0]]
                # If move is 3Rw on 4x4 or 4Rw on 5x5, do a counterclockwise turn in parallel axis
                if move[0] == str(self.size - 1):
                    move_seq += [{
                        'U': 'd',
                        'D': 'u',
                        'R': 'l',
                        'L': 'r',
                        'F': 'b',
                        'B': 'f'
                    }[move[1]]]*3
        
        # Do each single move in the move_seq to do the compound move
        for sub_move in move_seq:
            self.single_move(sub_move)


    def rotation(self, move):
        # Case for 4x4 and 5x5: add wide move number at the start
        wide = ''
        if self.size in (4,5):
            wide = str(self.size - 1)

        # Compute equivalent single/compound moves to a rotation
        if move == 'x':
            move_seq = [wide + 'Rw'] + ['L']*3
        if move == 'y':
            move_seq = [wide + 'Uw'] + ['D']*3
        if move == 'z':
            move_seq = [wide + 'Fw'] + ['B']*3

        # Apply the moves
        for sub_move in move_seq:
            if len(sub_move) == 1:
                self.single_move(sub_move)
            else:
                self.compound_move(sub_move)

    def orient(self, orientation):
        pass

    def print_cube(self, mode):
        """
        Print out each face of the cube to standard output for debugging.
        """
        for item in self.faces.items():
            print(item[0])
            for row in item[1]:
                if mode == 1:
                    print([x[0] for x in row])
                elif mode == 2:
                    print(row)

    def get_cube_colormap(self):
        out = {}
        for f in "ULFRBD":
            for row in self.faces[f]:
                for face, color in row:
                    out[face] = color

        return out

    def get_sticker_colors(self, targets):
        out = []
        colormap = self.get_cube_colormap()
        for t in targets:
            out.append(colormap[t])

        return out
    
    def get_u_colors(self):
        out = []
        out.append(self.faces["U"][0][0][1])
        out.append(self.faces["U"][0][1][1])
        out.append(self.faces["U"][0][2][1])
        out.append(self.faces["U"][1][0][1])
        out.append(self.faces["U"][1][1][1])
        out.append(self.faces["U"][1][2][1])
        out.append(self.faces["U"][2][0][1])
        out.append(self.faces["U"][2][1][1])
        out.append(self.faces["U"][2][2][1])
        return out
    
    def get_d_colors(self):
        out = []
        out.append(self.faces["D"][2][0][1])
        out.append(self.faces["D"][2][1][1])
        out.append(self.faces["D"][2][2][1])
        out.append(self.faces["D"][1][0][1])
        out.append(self.faces["D"][1][1][1])
        out.append(self.faces["D"][1][2][1])
        out.append(self.faces["D"][0][0][1])
        out.append(self.faces["D"][0][1][1])
        out.append(self.faces["D"][0][2][1])
        return out
    
    def get_l_colors(self):
        out = []
        out.append(self.faces["L"][0][0][1])
        out.append(self.faces["L"][0][1][1])
        out.append(self.faces["L"][0][2][1])
        out.append(self.faces["L"][1][0][1])
        out.append(self.faces["L"][1][1][1])
        out.append(self.faces["L"][1][2][1])
        out.append(self.faces["L"][2][0][1])
        out.append(self.faces["L"][2][1][1])
        out.append(self.faces["L"][2][2][1])
        return out
    
    def get_r_colors(self):
        out = []
        out.append(self.faces["R"][0][2][1])
        out.append(self.faces["R"][0][1][1])
        out.append(self.faces["R"][0][0][1])
        out.append(self.faces["R"][1][2][1])
        out.append(self.faces["R"][1][1][1])
        out.append(self.faces["R"][1][0][1])
        out.append(self.faces["R"][2][2][1])
        out.append(self.faces["R"][2][1][1])
        out.append(self.faces["R"][2][0][1])
        return out
    
    def get_f_colors(self):
        out = []
        out.append(self.faces["F"][0][0][1])
        out.append(self.faces["F"][0][1][1])
        out.append(self.faces["F"][0][2][1])
        out.append(self.faces["F"][1][0][1])
        out.append(self.faces["F"][1][1][1])
        out.append(self.faces["F"][1][2][1])
        out.append(self.faces["F"][2][0][1])
        out.append(self.faces["F"][2][1][1])
        out.append(self.faces["F"][2][2][1])
        return out
    
    def get_b_colors(self):
        out = []
        out.append(self.faces["B"][0][2][1])
        out.append(self.faces["B"][0][1][1])
        out.append(self.faces["B"][0][0][1])
        out.append(self.faces["B"][1][2][1])
        out.append(self.faces["B"][1][1][1])
        out.append(self.faces["B"][1][0][1])
        out.append(self.faces["B"][2][2][1])
        out.append(self.faces["B"][2][1][1])
        out.append(self.faces["B"][2][0][1])
        return out