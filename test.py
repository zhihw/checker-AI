import random
import time
from collections import defaultdict


class Checkers:
    def __init__(self):
        self.board = self._init_board()
        self.current_player = 1  # Player 1 starts, 1 for white and -1 for black

    def _init_board(self):
        board = [[0] * 8 for _ in range(8)]
        for row in range(3):
            for col in range(row % 2, 8, 2):
                board[row][col] = 1  # Player 1 pieces
        for row in range(5, 8):
            for col in range(row % 2, 8, 2):
                board[row][col] = -1  # Player -1 pieces
        return board

    def get_legal_moves(self, state):
        legal_moves = []
        for r in range(8):
            for c in range(8):
                if state[r][c] == self.current_player:
                    moves = self._get_piece_moves(state, r, c)
                    legal_moves.extend(moves)
        return legal_moves

    def _get_piece_moves(self, state, r, c):
        moves = []
        directions = [(-1, -1), (-1, 1)] if state[r][c] == 1 else [(1, -1), (1, 1)]
        if abs(state[r][c]) == 2:  # King piece moves in all directions
            directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if state[nr][nc] == 0:
                    moves.append(((r, c), (nr, nc)))
                elif state[nr][nc] == -self.current_player:
                    nnr, nnc = nr + dr, nc + dc
                    if 0 <= nnr < 8 and 0 <= nnc < 8 and state[nnr][nnc] == 0:
                        moves.append(((r, c), (nnr, nnc), (nr, nc)))
        return moves

    def apply_move(self, state, move):
        if move is None:
            raise ValueError("Invalid move: None")
        new_state = [row[:] for row in state]
        if len(move) == 2:
            (sr, sc), (er, ec) = move
            new_state[er][ec] = new_state[sr][sc]
            new_state[sr][sc] = 0
        elif len(move) == 3:
            (sr, sc), (er, ec), (cr, cc) = move
            new_state[er][ec] = new_state[sr][sc]
            new_state[sr][sc] = 0
            new_state[cr][cc] = 0
        else:
            raise ValueError(f"Invalid move length: {len(move)}")
        return new_state

    def is_terminal(self, state):
        player_pieces = any(state[r][c] == self.current_player for r in range(8) for c in range(8))
        opponent_pieces = any(state[r][c] == -self.current_player for r in range(8) for c in range(8))
        return not player_pieces or not opponent_pieces

    def evaluate_state(self, state):
        if isinstance(state, tuple):
            state = self.tuple_to_state(state)
        if not isinstance(state, list) or not isinstance(state[0], list):
            raise ValueError("Invalid state format")
        player1_count = sum(1 for r in range(8) for c in range(8) if state[r][c] == 1)
        player2_count = sum(1 for r in range(8) for c in range(8) if state[r][c] == -1)
        return player1_count - player2_count if self.current_player == 1 else player2_count - player1_count

    def switch_player(self):
        self.current_player *= -1

    def initial_state(self):
        return self.board

    def is_win(self, state):
        state = self.state_to_tuple(state)  # Ensure state is in tuple format
        return not any(state[r][c] == self.current_player for r in range(8) for c in range(8))

    def state_to_tuple(self, state):
        if isinstance(state, list):
            return tuple(tuple(row) for row in state)
        return state  # Return as is if already a tuple

    def tuple_to_state(self, state_tuple):
        if isinstance(state_tuple, tuple):
            return [list(row) for row in state_tuple]
        return state_tuple  # Return as is if already a list

    def print_board(self, state):

        representation = {
            1: 'W',  # White pieces
            -1: 'B', # Black pieces
            0: '.'   # Empty squares
        }
        print("  a b c d e f g h")
        print(" +---------------")
        for r in range(8):
            row = f"{8 - r}|"
            for c in range(8):
                row += f" {representation[state[r][c]]}"
            print(row)
        print(" +---------------")


class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.children = {}
        self.visit_count = 0
        self.value_sum = 0
        self.move = move

def mcts(root_state, checkers_game, iter_max=1000):
    root_node = MCTSNode(root_state)

    for _ in range(iter_max):
        node = root_node
        state = root_state

        while node.children and not checkers_game.is_terminal(state):
            if node.visit_count == 0:
                break
            node = max(node.children.values(), key=lambda n: n.value_sum / n.visit_count)
            state = checkers_game.apply_move(state, node.move)

        if not checkers_game.is_terminal(state):
            legal_moves = checkers_game.get_legal_moves(state)
            for move in legal_moves:
                if move not in node.children:
                    new_state = checkers_game.apply_move(state, move)
                    new_state = checkers_game.state_to_tuple(new_state)
                    node.children[move] = MCTSNode(new_state, parent=node, move=move)

        if not checkers_game.is_terminal(state):
            value = simulate_random_game(state, checkers_game)
        else:
            value = checkers_game.evaluate_state(state)

        # Backpropagation
        while node is not None:
            node.visit_count += 1
            node.value_sum += value
            node = node.parent

    # Choose the move with the highest visit_count
    if root_node.children:
        best_move = max(root_node.children.values(), key=lambda n: n.visit_count).move
        return best_move
    return None

def simulate_random_game(state, checkers_game):
    state = checkers_game.state_to_tuple(state)
    while not checkers_game.is_terminal(state):
        legal_moves = checkers_game.get_legal_moves(state)
        if not legal_moves:
            break
        move = random.choice(legal_moves)
        state = checkers_game.apply_move(state, move)
        state = checkers_game.state_to_tuple(state)
    return checkers_game.evaluate_state(state)

class QLearningAgent:
    def __init__(self, checkers_game, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.checkers_game = checkers_game
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = defaultdict(lambda: defaultdict(float))

    def choose_action(self, state):
        state = self.checkers_game.state_to_tuple(state)
        legal_moves = self.checkers_game.get_legal_moves(state)
        if not legal_moves:
            return None
        if random.random() < self.epsilon:
            return random.choice(legal_moves)
        else:
            return max(legal_moves, key=lambda move: self.q_table[state][move])

    def update_q_table(self, state, move, reward, next_state):
        state = self.checkers_game.state_to_tuple(state)
        next_state = self.checkers_game.state_to_tuple(next_state)
        legal_moves = self.checkers_game.get_legal_moves(next_state)

        if legal_moves:
            best_next_move = max(legal_moves, key=lambda m: self.q_table[next_state][m])
            td_target = reward + self.gamma * self.q_table[next_state][best_next_move]
        else:
            td_target = reward
        td_error = td_target - self.q_table[state][move]
        self.q_table[state][move] += self.alpha * td_error

    def train(self, num_episodes):
        for _ in range(num_episodes):
            state = self.checkers_game.initial_state()
            state = self.checkers_game.state_to_tuple(state)

            while not self.checkers_game.is_terminal(state):
                move = self.choose_action(state)
                if move is None:
                    break
                next_state = self.checkers_game.apply_move(state, move)
                next_state = self.checkers_game.state_to_tuple(next_state)
                reward = self.checkers_game.evaluate_state(next_state)
                self.update_q_table(state, move, reward, next_state)
                state = next_state

def compare_algorithms(checkers_game):
    mcts_time = 0
    ql_time = 0
    mcts_wins = 0
    num_games = 1000

    ### MCTS Test ###
    for _ in range(num_games):
        start_time = time.time()
        state = checkers_game.initial_state()
        state = checkers_game.state_to_tuple(state)

        while not checkers_game.is_terminal(state):
            move = mcts(state, checkers_game)
            if move is None:
                break
            state = checkers_game.apply_move(state, move)
            checkers_game.switch_player()
        end_time = time.time()
        mcts_time += (end_time - start_time)
        if checkers_game.is_win(state):
            mcts_wins += 1

    ### Q-Learning Test ###
    start_time = time.time()
    ql_agent = QLearningAgent(checkers_game)
    ql_agent.train(1000)
    ql_wins = 0

    for _ in range(num_games):

        state = checkers_game.initial_state()
        state = checkers_game.state_to_tuple(state)

        while not checkers_game.is_terminal(state):
            move = ql_agent.choose_action(state)
            if move is None:
                break
            state = checkers_game.apply_move(state, move)
            checkers_game.switch_player()
        end_time = time.time()
        ql_time += (end_time - start_time)
        if checkers_game.is_win(state):
            ql_wins += 1

    print(f"MCTS Time: {mcts_time:.2f} seconds")
    # print(f"MCTS Wins: {mcts_wins}/{num_games} games")
    print(f"QL Time: {ql_time:.2f} seconds")
    # print(f"QL Wins: {ql_wins}/{num_games} games")


### Main Program ###
if __name__ == "__main__":
    checkers_game = Checkers()
    checkers_game.print_board(checkers_game.initial_state())
    compare_algorithms(checkers_game)
