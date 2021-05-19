import copy

class NoughtsAndCrosses:
    def __init__(self):
        self.board = [[None for _ in range(3)] for i in range(3)]
        self.verbose =[[str(1 + i + n*3) for i in range(3)] for n in range(3)]
        self.turn = True
        self.avaible_positions = list(range(9))
        
    def play(self):
        while True:
            print('Состояние доски')
            self.show_board(self.board)
            if len(self.avaible_positions) == 0:
                break
            is_win = self.check_win(self.board)
            if is_win:
                break
            if self.turn:
                print('Номера позиций')
                self.show_board(self.verbose)
                cross_position = input('Введите позицию для крестика: ')
                while not isinstance(cross_position, int):
                    try:
                        cross_position = int(cross_position) - 1
                    except:
                        cross_position = input('Вы ввели не число. Попробуйте ещё раз: ')
                if cross_position in self.avaible_positions:
                    self.board, self.avaible_positions = self.make_move(True, cross_position, self.board, self.avaible_positions)
                else:
                    print('Эта клетка занята')
                    print('\n\n')
                    continue
                self.turn = False
                print('')
            else:
                print('Ждём компьютер')
                knot_position, _ = self.minmax(copy.deepcopy(self.board), False, copy.deepcopy(self.avaible_positions))
                self.board, self.avaible_positions = self.make_move(False, knot_position, self.board, self.avaible_positions)
                self.turn = True
                print('')
        if is_win:
            print(f'{is_win} выиграл')
        else:
            print('Ничья')    
                
    def make_move(self, is_cross, position, board, avaible_positions):
        row = position // 3
        column = position % 3
        if is_cross:
            board[row][column] = 'X'
        else:
            board[row][column] = 'O'
        for i, position_ in enumerate(avaible_positions):
            if position_ == position:
                avaible_positions.pop(i)
                break
        return (board, avaible_positions)
        
    def show_board(self, board):
        for row in board:
            print('-------')
            symbols = '|'
            for column in row:
                if column != None:
                    symbols += column + '|'
                else:
                    symbols += ' |'
            print(symbols)
        print('-------')
        
    def check_win(self, board):
        for row in board:
            if row == ['X', 'X', 'X']:
                return 'Игрок'
            elif row == ['O', 'O', 'O']:
                return 'Компьютер'
        first, second, third, main, secondary = [], [], [], [], []
        for x in range(3):
            for y in range(3):
                symbol = board[x][y]
                if y == 0:
                    first.append(symbol)
                    if x == 0:
                        main.append(symbol)
                    if x == 2:
                        secondary.append(symbol)
                if y == 1:
                    second.append(symbol)
                    if x == 1:
                        main.append(symbol)
                        secondary.append(symbol)
                if y == 2:
                    third.append(symbol)
                    if x == 0:
                        secondary.append(symbol)
                    if x == 2:
                        main.append(symbol)
        lines = [first, second, third, main, secondary]
        for line in lines:
            if line == ['X', 'X', 'X']:
                 return 'Игрок'
            if line == ['O', 'O', 'O']:
                 return 'Компьютер'
        return False
        
    def versus(self):
        while not self.win:
            print('Состояние доски')
            self.show_board(self.board)
            if len(self.avaible_positions) == 0:
                break
            is_win = self.check_win(self.board)
            if is_win:
                break
            print('Номера позиций')
            self.show_board(self.verbose)
            if self.turn:
                print('Ход крестика')
            else:
                print('Ход нолика')
            position = input('Введите позицию для хода: ')
            while not isinstance(position, int):
                try:
                    position = int(position) - 1
                except:
                    position = input('Вы ввели не число')
            if position in self.avaible_positions:
                self.board, self.avaible_positions = self.make_move(self.turn, position, self.board, self.avaible_positions)
            else:
                print('Эта клетка занята')
                print('\n\n')
                continue
            self.turn = not self.turn
            print('')
        if is_win:
            if is_win == 'Игрок':
                print('Крестики выиграли')
            else:
                print('Нолики выиграли')
        else:
            print('Ничья')
         
    def minmax(self, board, is_cross, avaible):
        turns =[]
        for turn in avaible:
              board_copy, avaible_copy = self.make_move(is_cross, turn, copy.deepcopy(board), copy.deepcopy(avaible))
              is_win = self.check_win(board_copy)
              if is_win:
                  if is_cross:
                      return (turn, -1)
                  else:
                      return (turn, 1)
              elif len(avaible_copy) == 0:
                      turns.append((turn, 0))
              else:
                      if is_cross:
                          new_is_cross = False
                      else:
                          new_is_cross = True
                      best_scenario = self.minmax(board_copy, new_is_cross, avaible_copy)
                      turns.append((turn, best_scenario[1]))
        if is_cross:
              min = (0, 2)
              for scenario in turns:
                  if scenario[1] < min[1]:
                      min = scenario
              return min
        else:
              max = (0, -2)
              for scenario in turns:
                  if scenario[1] > max[1]:
                      max = scenario
              return max
                      
        
if __name__ == '__main__':
    game = NoughtsAndCrosses()
    while True:
        mode = input('Игра против компьютера (введите 0) или против другого человека (введите 1)? ')
        if mode == '0' or mode == '1':
            break
        else:
            print('Неверный ввод')
    mode = int(mode)
    if mode:
        game.versus()
    else:
        game.play()