from Block import Block
from Board import Board
from Player import Player

class Game():

    def __init__(self, players: list[Player], board = None) -> None:
        self.players = players
        self.board = board 
    
    def start_new_game(self):
        exit = False
        self.board = Board()
        round_one = True
        for player in self.players:
            player.board = self.board
        
        while not exit:
            for player in self.players:
                turn_active = True
                while turn_active:
                    turn_active = False
                    print(f"\nPlayer {player.color}'s turn\n\nRemaining blocks:")
                    player.show_remaining_blocks()
                    self.board.show_board()
                    action = input("\nChoose Action   (insert, rotate, reflect, exit)\n")
                    if action == "insert":
                        block_idx = int(input("Choose Block\n"))
                        row =  int(input("Choose row\n"))
                        col = int(input("Choose Col\n"))
                        if round_one:
                            player.player_insert(block_idx, row, col)
                        else:
                            valid = self.board.is_move_valid(row, col, player.get_block(block_idx))
                            if valid:
                                player.player_insert(block_idx, row, col)
                            else: 
                                print("Move not valid!")
                                turn_active = True

                    elif action == "rotate":
                        block_idx = int(input("Choose Block\n"))
                        player.blocks[block_idx].rotate()
                        turn_active = True
                    elif action == "reflect":
                        block_idx = int(input("Choose Block\n"))
                        player.blocks[block_idx].reflect()
                        turn_active = True
                if action == "exit":
                    exit = True
                    break
            round_one = False
            
PlayerA = Player("red", None)
PlayerB = Player("blue", None)
PlayerC = Player("green", None)

Players = [PlayerA] + [PlayerB] + [PlayerC] 

game = Game(Players)
game.start_new_game()