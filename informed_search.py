from eight_puzzle_state import State


class InformedSearch:
    goal = State([1, 2, 3, 4, 5, 6, 7, 8, 0], 0, 0)

    def __init__(self, current):
        self.current = State(current, 0, 0)
        self.open_list = []
        self.closed_list = []
        self.iter = 0
        self.open_list.append(self.current)

    """
    Check if a state is in open_list or closed_list.
    :param s: A state to compare.
    :return: Returns 3 if in closed_list, 2 if in open_list, and 1 if not found in neither.
    """
    def check_open_closed(self, s):
        if s in self.closed_list:
            return 3

        if s in self.open_list:
            return 2

        return 1

    """
    Walk through the possible moves (left, right, up, and down) and calculate heuristics for each move.
    At the end, sort the open_list and assign current to the first value.
    """
    def state_walk(self):
        self.closed_list.append(self.current)
        self.open_list.remove(self.current)

        walk_state = self.current.tile_seq

        pos = walk_state.index(0)
        row, col = pos // 3, pos % 3

        self.iter += 1

        # Try to move in each direction
        # First state, moving left
        if col - 1 >= 0:
            current_state = self.current.tile_seq
            temp = current_state.copy()

            temp[pos], temp[pos - 1] = temp[pos - 1], temp[pos]

            temp_state = State(temp, self.current.depth + 1, 0, self.current)
            flag = self.check_open_closed(temp_state)
            self.handle_flag(flag, temp_state)

        # Second state, moving right
        if col + 1 <= 2:
            current_state = self.current.tile_seq
            temp = current_state.copy()

            temp[pos], temp[pos + 1] = temp[pos + 1], temp[pos]

            temp_state = State(temp, self.current.depth + 1, 0, self.current)
            flag = self.check_open_closed(temp_state)
            self.handle_flag(flag, temp_state)

        # Third state, moving up
        if row - 1 >= 0:
            current_state = self.current.tile_seq
            temp = current_state.copy()

            temp[pos], temp[pos - 3] = temp[pos - 3], temp[pos]

            temp_state = State(temp, self.current.depth + 1, 0, self.current)
            flag = self.check_open_closed(temp_state)
            self.handle_flag(flag, temp_state)

        # Fourth and final state, moving down
        if row + 1 <= 2:
            current_state = self.current.tile_seq
            temp = current_state.copy()

            temp[pos], temp[pos + 3] = temp[pos + 3], temp[pos]

            temp_state = State(temp, self.current.depth + 1, 0, self.current)
            flag = self.check_open_closed(temp_state)
            self.handle_flag(flag, temp_state)

        self.open_list.sort(key=lambda x: x.weight)
        self.current = self.open_list[0]

    """
    Heuristic search strategies.
    (1) Number of tiles out of place
    (2) Sum of distances out of place
    
    f(n) = g(n) + h(n)
    g(n) = depth of path from start state
    h(n) = (1) + (2) 
    """
    def heuristic_test(self, current):
        curr_seq = current.tile_seq
        goal_seq = self.goal.tile_seq

        # (1) Number of tiles out of place
        h1 = 0
        for i in range(len(curr_seq)):
            if curr_seq[i] != goal_seq[i]:
                h1 += 1

        # (2) Sum of distances out of place
        h2 = 0
        for goal, curr in enumerate(curr_seq):
            if curr:
                score = abs((curr - 1) % 3 - goal % 3) + abs((curr - 1) // 3 - goal // 3)
                h2 += score

        # set the heuristic value for current state
        current.weight = self.current.depth + h1 + h2

    """
    Determine if new state is in open_list or closed_list and update lists accordingly. 
    """
    def handle_flag(self, flag, temp_state):
        # Not in open_list or closed_list
        if flag == 1:
            self.heuristic_test(temp_state)
            self.open_list.append(temp_state)

        # In open_list
        if flag == 2:
            if temp_state.depth < self.current.depth:
                self.open_list.append(temp_state)

        # In closed_list
        if flag == 3:
            if temp_state.depth < self.current.depth:
                self.closed_list.remove(self.current)
                self.open_list.append(temp_state)

    """
    Walks through all possible moves until the goal state is reached. 
    :return: Returns a list in order of the moves to take to reach the goal state.
    """
    def solve(self):
        # List of every state explored during the state walk
        full_path = []
        # The initial state of the board
        first = self.current.tile_seq

        if first == self.goal.tile_seq:
            return []

        while self.current != self.goal:
            self.state_walk()
            full_path.append(self.current)

            if self.iter > 10000:
                return None

        # Backtrack from the goal state and find the states it took to get there
        full_path.reverse()
        current = full_path[0].parent.tile_seq
        path = []

        for state in full_path:
            if current == state.tile_seq:
                path.append(state.tile_seq)
                current = state.parent.tile_seq if state.parent is not None else None

        path.reverse()
        path.insert(0, first)
        path.append(full_path[0].tile_seq)

        # New list with only the numbers being swapped in order to get from initial state to goal state
        moves = []
        for i in range(len(path) - 1):
            for j in range(len(path[i])):
                if path[i][j] != path[i+1][j] and path[i][j] != 0:
                    moves.append(path[i][j])

        return moves
