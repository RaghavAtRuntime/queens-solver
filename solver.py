class Solver:
    def solve(self, board, regions, index=0, x_positions=set()):
        """Backtracking solver to place Xs while following the rules."""
        region_keys = list(regions.keys())
        if index == len(region_keys):
            return x_positions  # Solution found

        region = region_keys[index]
        for r, c in regions[region]:
            if self.is_valid(board, x_positions, r, c, len(board)):
                new_positions = x_positions | {(r, c)}  # Add X
                result = self.solve(board, regions, index + 1, new_positions)
                if result:
                    return result  # Found a valid solution

        return None  # No solution found

    def is_valid(self, board, x_positions, r, c, n):
        """Checks if placing an X at (r, c) is valid."""
        for x_r, x_c in x_positions:
            if x_r == r or x_c == c:  # Same row or column
                return False
            if abs(x_r - r) == 1 and abs(x_c - c) == 1:  # Diagonal adjacency
                return False
        return True
