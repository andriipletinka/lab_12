"""Implemention of the Maze ADT using a 2-D array."""
from arrays import Array2D
from lliststack import Stack


class Maze:
    """Define constants to represent contents of the maze cells."""
    MAZE_WALL = "*"
    PATH_TOKEN = "x"
    TRIED_TOKEN = "o"

    def __init__(self, num_rows, num_cols):
        """Creates a maze object with all cells marked as open."""
        self._maze_cells = Array2D(num_rows, num_cols)
        self._start_cell = None
        self._exit_cell = None

    def num_rows(self):
        """Returns the number of rows in the maze."""
        return self._maze_cells.num_rows()

    def num_cols(self):
        """Returns the number of columns in the maze."""
        return self._maze_cells.num_cols()

    def set_wall(self, row, col):
        """Fills the indicated cell with a "wall" marker."""
        assert row >= 0 and row < self.num_rows() and \
               col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._maze_cells[row, col] = self.MAZE_WALL

    def set_start(self, row, col):
        """Sets the starting cell position."""
        assert row >= 0 and row < self.num_rows() and \
               col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._start_cell = _CellPosition(row, col)

    def set_exit(self, row, col):
        """Sets the exit cell position."""
        assert row >= 0 and row < self.num_rows() and \
               col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._exit_cell = _CellPosition(row, col)


    def find_path(self):
        """
        Attempts to solve the maze by finding a path from the starting cell
        to the exit. Returns True if a path is found and False otherwise.
        """
        stack = Stack()
        current_cell = self._start_cell
        while True:
            stack.push(current_cell)
            row = current_cell.row
            col = current_cell.col
            if current_cell == self._exit_cell:
                self._maze_cells.rows[row][col] = "x"
                return True
            if self._valid_move(row-1, col):
                next_cell = _CellPosition(row-1, col)
                self._maze_cells.rows[row][col] = "x"
                current_cell = next_cell
            elif self._valid_move(row, col+1):
                next_cell = _CellPosition(row, col+1)
                self._maze_cells.rows[row][col] = "x"
                current_cell = next_cell
            elif self._valid_move(row+1, col):
                next_cell = _CellPosition(row+1, col)
                self._maze_cells.rows[row][col] = "x"
                current_cell = next_cell
            elif self._valid_move(row, col-1):
                next_cell = _CellPosition(row, col-1)
                self._maze_cells.rows[row][col] = "x"
                current_cell = next_cell
            else:
                self._maze_cells.rows[row][col] = "o"
                current_cell = stack.pop()
                try:
                    current_cell = stack.pop()
                except AssertionError:
                    return False

    def reset(self):
        """Resets the maze by removing all "path" and "tried" tokens."""
        for row in self._maze_cells.rows:
            for col in range(self._maze_cells.num_cols()):
                elem = row[col]
                if elem == "o" or elem == "x":
                    row[col] = None

    def __str__(self):
        """Returns a text-based representation of the maze."""
        text = ""
        for row in self._maze_cells.rows:
            for col in range(self._maze_cells.num_cols()):
                elem = row[col]
                if elem is None:
                    text += "_"
                else:
                    text += str(row[col])
                text += " "
            text += "\n"
        return text.strip("\n")

    def _valid_move(self, row, col):
        """Returns True if the given cell position is a valid move."""
        return row >= 0 and row < self.num_rows() \
               and col >= 0 and col < self.num_cols() \
               and self._maze_cells[row, col] is None

    def _exit_found(self, row, col):
        """Helper method to determine if the exit was found."""
        return row == self._exit_cell.row and col == self._exit_cell.col

    def _mark_tried(self, row, col):
        """Drops a "tried" token at the given cell."""
        self._maze_cells[row, col] = self.TRIED_TOKEN

    def _mark_path(self, row, col):
        """Drops a "path" token at the given cell."""
        self._maze_cells[row, col] = self.PATH_TOKEN


class _CellPosition(object):
    """Private storage class for holding a cell position."""
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __eq__(self, __o: object) -> bool:
        return self.row == __o.row and self.col == __o.col
