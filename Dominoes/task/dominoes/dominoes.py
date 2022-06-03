import random

stock_pieces = []
computer_pieces = []
player_pieces = []

# array of all dominos
def generate_pieces():
    pieces = []
    for num_left in range(7):
        for num_right in range(num_left, 7):
            pieces.append([num_left, num_right])
    return pieces

# deal pieces randomly to computer and player
def shuffle(stock_pieces):
    domino_stake = []
    player_has_double = [-1, -1]
    computer_has_double = [-1, -1]
    while not domino_stake:
        for selection in range(14):
            piece = random.choice(stock_pieces)
            stock_pieces.remove(piece)
            if selection % 2:
                computer_pieces.append(piece)
                if piece[0] == piece[1]:
                    if piece[0] > computer_has_double[0]:
                        computer_has_double = piece
            else:
                player_pieces.append(piece)
                if piece[0] == piece[1]:
                    if piece[0] > player_has_double[0]:
                        player_has_double = piece
        # if double, pick max and set correct status
        if computer_has_double[0] or player_has_double[0]:
            if computer_has_double[0] > player_has_double[0]:
                domino_stake = [computer_pieces.pop(computer_pieces.index(computer_has_double))]
                status = 'player'
            else:
                domino_stake = [player_pieces.pop(player_pieces.index(player_has_double))]
                status = 'computer'
    return domino_stake, computer_pieces, player_pieces, status

# display all players available dominos
def player_output(dominos):
    print('Your pieces:')
    for index, domino in enumerate(dominos):
        print(f'{index + 1}:{domino}')

# check if move is legal
def legal_move(move, pieces):
    piece = pieces[abs(move) - 1]
    if move < 0:
        piece_stake = domino_stake[0]
        if piece_stake[0] in piece:
            if piece_stake[0] == piece[0]:
                piece.reverse()
            return False
    else:
        piece_stake = domino_stake[-1]
        if piece_stake[1] in piece:
            if piece_stake[1] == piece[1]:
                piece.reverse()
            return False
    return True

# take a turn based of code of -n, place to left or n place to right or 0 get domino from stock
def turn(move, pieces):
    if move == 0:
        if len(stock_pieces) > 0:
            piece = random.choice(stock_pieces)
            pieces.append(piece)
            stock_pieces.remove(piece)
            return False
        else:
            return False
    illegal_move = legal_move(move, pieces)
    if illegal_move:
        return True
    if move < 0:
        domino_stake.insert(0, pieces.pop(abs(move) - 1))
    else:
        domino_stake.append(pieces.pop(move - 1))
    return False

# check to see if anyone has won
def keep_playing():
    if len(player_pieces) < 1:
        print('Status: The game is over. You won!')
        return False
    elif len(computer_pieces) < 1:
        print('Status: The game is over. The computer won!')
        return False
    elif len(domino_stake) > 5 and domino_stake[0][0] == domino_stake[-1][0]:
        if domino_stake.count(domino_stake[0][0]) == 5:
            print("Status: The game is over. It's a draw!")
            return False
    return True

def computer_ai(pieces):
    scores_num = []
    for index in range(7):
        computer_count, stake_count = 0, 0
        for piece in pieces:
            computer_count += piece.count(index)
        for piece in domino_stake:
            stake_count += piece.count(index)
        scores_num.append(computer_count + stake_count)
    scores_piece = []
    for piece in pieces:
        scores_piece.append(scores_num[piece[0]] + scores_num[piece[1]])
    scores_piece, pieces = (list(t) for t in zip(*sorted(zip(scores_piece, pieces), reverse=True)))
    return pieces

# computer takes a turn
def computer_turn(pieces):
    global computer_pieces
    print("Status: Computer is about to make a move. Press Enter to continue...")
    input()
    pick_domino = True
    # while pick_domino:
    pieces = computer_ai(pieces)
    for index, piece in enumerate(pieces):
        move = index + 1
        pick_domino = turn(move, pieces)
        if pick_domino:
            pick_domino = turn(-move, pieces)
        if not pick_domino:
            break
    if pick_domino:
        pick_domino = turn(0, pieces)
    computer_pieces = pieces
    return 'player'

# player takes a turn
def player_turn(pieces):
    print("Status: It's your turn to make a move. Enter your command.")
    ask_for_input = True
    while ask_for_input:
        try:
            move = int(input())
            if abs(move) > len(player_pieces):
                print('Invalid input. Please try again.')
            else:
                ask_for_input = False
                pick_domino = turn(move, pieces)
                if pick_domino:
                    ask_for_input = True
                    print('Illegal move. Please try again.')
        except ValueError:
            print('Invalid input. Please try again.')
    return 'computer'

# display game information
def game_heading():
    print('=' * 70)
    print(f'Stock size: {no_pieces["stock"]}')
    print(f'Computer pieces: {no_pieces["computer"]}')
    if len(domino_stake) > 6:
        print(*domino_stake[:3], end='...')
        print(*domino_stake[-3:])
    else:
        print(*domino_stake)

# initialise main game vaiables
stock_pieces = generate_pieces()
domino_stake, computer_pieces, player_pieces, status = shuffle(stock_pieces)
play_game = True
no_pieces = {}

# main game
while play_game:
    # game ui
    no_pieces['stock'] = len(stock_pieces)
    no_pieces['computer'] = len(computer_pieces)
    no_pieces['player'] = len(player_pieces)
    game_heading()
    player_output(player_pieces)
    # check for a winner
    play_game = keep_playing()
    # if still playing decided who goes next and take turn
    if play_game:
        if status == 'player':
            status = player_turn(player_pieces)
        elif status == 'computer':
            status = computer_turn(computer_pieces)
        if no_pieces['stock'] == 0:
            if no_pieces['computer'] == len(computer_pieces) and no_pieces['player'] == len(player_pieces):
                print("Status: The game is over. It's a draw!")
                play_game = False

