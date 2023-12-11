try:
    from classes.Block import Block
    from classes.Board import Board
    from classes.Player import Player
    from classes.AIPlayer import AIPlayer
except:
    from Block import Block
    from Board import Board
    from Player import Player
    from AIPlayer import AIPlayer
import time

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
                    #print(f"\nPlayer {player.color}'s turn\n\nRemaining blocks:")
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
                                #print("Move not valid!")
                                turn_active = True

                    elif action == "rotate":
                        block_idx = int(input("Choose Block\n"))
                        player.blocks[block_idx].rotate()
                        turn_active = True
                    elif action == "reflect":
                        block_idx = int(input("Choose Block\n"))
                        player.blocks[block_idx].reflect()
                        turn_active = True
                    
                    if len(player.blocks) == 0:
                        print(f"{player} wins the game")
                        exit = True

                if action == "exit":
                    exit = True
                    break
            round_one = False
            
#PlayerA = Player("red", None)
#Players = [PlayerA] 
#game = Game(Players)
#game.start_new_game()

class AI_Game():

    def __init__(self, players: list[AIPlayer], board: Board) -> None:
        self.players = players
        self.board = board
        self.active_player = players[0]
        pass

    def play_new_game(self):
        self.board = Board()
        round_one = True
        for player in self.players:
            player.board = self.board

        while True:
            for player in self.players:
                #print(len(player.blocks))
                time.sleep(1)
                if round_one:
                    player.set_first_block()
                else:
                    player.set_block()
                #print("test")
                #time.sleep(1)
                self.board.show_board()
            round_one = False


    def play_game(self, round_one):
        if round_one:
            self.active_player.set_first_block()
        else:
            self.active_player.set_block()
        return self.board


    def init_game(self):
        self.board = Board()
        for player in self.players:
            player.board = self.board
        return self.board

    def get_next_active_player(self):
        idx = self.players.index(self.active_player)
        next_idx = idx + 1
        if next_idx > len(self.players) - 1:
            next_idx = 0

        self.active_player = self.players[next_idx]

    
    def calculate_points(self):
        for player in self.players:
            best_value = 1000
            negative_points = 0
            for block in player.blocks:
                for i in len(block.matrix):
                    for j in len(block.matrix[0]):
                        if block.matrix[i][j]:
                            negative_points += 1
            if negative_points <= best_value:
                winner = player.color
                best_value = negative_points
        return winner
            
                

    


aia = AIPlayer("red", None)
aib = AIPlayer("blue", None)
aic = AIPlayer("green", None)
new_board = Board()
game = AI_Game([aia, aib, aic], new_board)
#game.play_game()