import random
from collections import defaultdict

class QLearningAgent:
    def __init__(self, checkers_game, alpha=0.1, gamma=0.9, epsilon=0.1):
        self._checkers_game = checkers_game
        self._alpha = alpha
        self._gamma = gamma
        self._epsilon = epsilon
        self._q_table = defaultdict(lambda: defaultdict(float))

    def choose_action(self, state):
        state = self._checkers_game.state_to_tuple(state)  # Ensure state is in tuple format
        legal_moves = self._checkers_game.get_legal_moves(state)
        if not legal_moves:
            return None
        if random.random() < self._epsilon:
            return random.choice(legal_moves)
        else:
            return max(legal_moves, key=lambda move: self._q_table[state][move])

    def update_q_table(self, state, move, reward, next_state):
        state = self._checkers_game.state_to_tuple(state)  # Ensure state is in tuple format
        next_state = self._checkers_game.state_to_tuple(next_state)
        legal_moves = self._checkers_game.get_legal_moves(next_state)

        if legal_moves:
            best_next_move = max(legal_moves, key=lambda m: self._q_table[next_state][m])
            td_target = reward + self._gamma * self._q_table[next_state][best_next_move]
        else:
            td_target = reward
        td_error = td_target - self._q_table[state][move]
        self._q_table[state][move] += self._alpha * td_error

    def train(self, num_episodes):
        for _ in range(num_episodes):
            state = self._checkers_game.initial_state()
            state = self._checkers_game.state_to_tuple(state)  # Ensure state is in tuple format

            while not self._checkers_game.is_terminal(state):
                move = self.choose_action(state)
                if move is None:
                    break
                next_state = self._checkers_game.apply_move(state, move)
                next_state = self._checkers_game.state_to_tuple(next_state)
                reward = self._checkers_game.evaluate_state(next_state)
                self.update_q_table(state, move, reward, next_state)
                state = next_state