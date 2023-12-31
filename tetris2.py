

import random
import pygame
EMPTY_SPOT = '\033[92m-\033[0m'
BLOCKER_SPOT = '\033[91mX\033[0m'

BROKEN_RULES = False

class Shape:
    def __init__(self, table):
        self.table = table
        self.position = None
        rows, cols = (6, 6)
        self.listt = [[EMPTY_SPOT] * cols for _ in range(rows)]

       

    def print_matrix(self):
        print("    \033[92m0 1 2 3 4 5")
        print("   ------------")
        for row in range(0, 6):
            print(f"\033[92m{row} \033[92m|", end=" ")
            for col in range(0, 6):
                print(self.listt[row][col], end=" ")
            print("")

    


class Puzzle:
    def __init__(self, shape, blocker_locations=None):
        self.shape_instance = Shape(shape)
        self.blocker_locations = blocker_locations or []
        self.color_counter = 0

    
    def draw_square(self, coordinate_x, coordinate_y):
        
        self.color_counter += 1

        if self.color_counter <= 6:
            self.shape_instance.listt[coordinate_x][coordinate_y] = '\033[91m\u25A0\033[0m'

        elif self.color_counter > 6 and self.color_counter <= 12:
            self.shape_instance.listt[coordinate_x][coordinate_y] = '\033[92m\u25A0\033[0m'

        elif self.color_counter > 12 and self.color_counter <= 18:
            self.shape_instance.listt[coordinate_x][coordinate_y] = '\033[93m\u25A0\033[0m'

        elif self.color_counter >18 and self.color_counter <= 24:
            self.shape_instance.listt[coordinate_x][coordinate_y] = '\033[94m\u25A0\033[0m'

        elif self.color_counter > 24 and self.color_counter <= 31:
            self.shape_instance.listt[coordinate_x][coordinate_y] = '\033[95m\u25A0\033[0m'

    def draw(self, locations, current_row):
        
        
        for row in range(len(locations)):
            for col in range(len(locations[0])):
                if locations[row][col] == 1:
                    if current_row < 6:
                        self.shape_instance.listt[row][col] = '\033[91m\u25A0\033[0m'
                    elif current_row > 6 and current_row < 12:
                        self.shape_instance.listt[row][col] = '\033[92m\u25A0\033[0m'

        for blocker_location in self.blocker_locations:
            row, col = blocker_location
            self.shape_instance.listt[row][col] = BLOCKER_SPOT

    def import_matrix(self, locations):
        for location in locations:
            row, col = location
            self.shape_instance.listt[row][col] = '\033[94m\u25A0\033[0m'

    def print_matrix(self):
        self.shape_instance.print_matrix()


def place_traps():
    blocker_locations = set()
    max_traps = 6

    for row in range(6):
        random_col = random.randint(0, 5)
        blocker_locations.add((row, random_col))

    remaining_traps = max_traps - 6  
    while remaining_traps > 0:
        random_location = (random.randint(0, 5), random.randint(0, 5))
        if random_location not in blocker_locations:
            blocker_locations.add(random_location)
            remaining_traps -= 1

    return list(blocker_locations)


def modify_matrix(puzzle_locations, blocker_locations, first_input, current_row):
    global BROKEN_RULES

    
    input_row = int(input("\033[92mInput the row of shape:\033[92m "))
    input_col = int(input("\033[92mInput the column of shape:\033[92m "))
    print("\n")

   

    if first_input and input_row != 0:
        print("\033[91mFirst move must be on row 0.\033[91m")
        print("     \033[91mGAME OVER!\033[91m\n")
        BROKEN_RULES = True

    if not first_input and input_row > current_row:
        print("\033[91myou can't skip rows.\033[91m")
        print("     \033[91mGAME OVER!\033[91m\n")
        BROKEN_RULES = True


    if (input_row, input_col) in blocker_locations:
        print("\033[91mYou hit a blocked spot.\033[91m")
        print("     \033[91mGAME OVER!\033[91m\n")
        BROKEN_RULES = True

    
    puzzle_locations[input_row][input_col] = 1

    return input_row, input_col



def play_again():
    global BROKEN_RULES
    BROKEN_RULES = False

    shape_1 = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0]]

    blocker_locations = place_traps()

    puzzle1 = Puzzle(shape_1, blocker_locations)
    puzzle1.draw(shape_1, 0)
    puzzle1.print_matrix()

    return puzzle1, shape_1, blocker_locations




def main():
    print("\n")
    prompt = input("\033[91mWelcome to the MatriX. Press 'p' to play! \033[91m")
    if prompt == "p":
        shape_1 = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0]]

        blocker_locations = place_traps()

        
        puzzle1 = Puzzle(shape_1, blocker_locations)

        
        puzzle1.draw(shape_1, 0) 
        puzzle1.print_matrix()

        first_input = True
    
        while True:
            
            for current_row in range(30):

                
                x, y = modify_matrix(shape_1, blocker_locations, first_input, current_row)
            
                first_input = False

               
                puzzle1.draw_square(x, y)
                if BROKEN_RULES or prompt == 'q':
                    exit()
                puzzle1.print_matrix()
            pygame.init()
            pygame.mixer.init()
            sound = pygame.mixer.Sound("data/victory.mp3")
            sound.play()
            print("     \033[91mYOU WON!\033[91m\n")
            pygame.time.delay(2000)
            
            play_again_response = input("\033[91mDo you want to play again? (y/n): \033[91m")
            if play_again_response.lower() != 'y':
                break
            else:
                puzzle1, shape_1, blocker_locations = play_again()
                
   
        
if __name__ == "__main__":
    main()
