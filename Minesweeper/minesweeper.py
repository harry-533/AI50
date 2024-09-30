import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # if the length of the sentence is equal to amount of mines, they are all mines, ignored if there are no mines
        if len(self.cells) == self.count and self.count != 0:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # if there are no mines then all the cells are safe
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # if the mine cell that is passed to the function is in the sentence, remove it and decrease mine coutn as it is known to be a mine
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # if the cell passed to the function is in the sentence, remove it as its known to be safe
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        # adds the mine to the mine set, and then loops through the sentences in knowledge and removes it
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        # adds the safe cell to the safe set, then loops through removing it from all sentences in knowledge
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # adds the cell to the moves made
        self.moves_made.add(cell)

        # adds the cell to the safe set and removes it from all sentences
        self.mark_safe(cell)

        # keep track of the cells the ai does not know the value of and the amount of mines in neighbouring cells
        undetermined_cells = []
        mine_count = 0

        # loop through the cells to the left, middle and right
        for i in range(cell[0] - 1, cell[0] + 2):
            # loops through the cells to the top middle and bottom
            for j in range(cell[1] - 1, cell[1] + 2):
                # if the current cell is a known mine, add 1 to mine count
                if (i, j) in self.mines:
                    mine_count += 1
                # if the cell is on the board 
                if 0 <= i < self.height and 0 <= j < self.width:
                    # if the cell is not a known mine or safe cell, add it to undertermined cells
                    if (i, j) not in self.safes and (i, j) not in self.mines:
                        undetermined_cells.append((i, j))

        # makes a new sentence with the undertermined cells, and the mine count is the initial count - the mines we already know
        new_sentence = Sentence(undetermined_cells, count - mine_count)

        # adds the sentence to the knowledge
        self.knowledge.append(new_sentence)

        # loops through the sentences in the knowledge
        for sentence in self.knowledge:
            # if the sentence is all mines
            if sentence.known_mines():
                # loops through the sentence (copy) and marks each cell as a mine, and removes it from the sentence
                for cell in sentence.known_mines().copy():
                    self.mark_mine(cell)
            # if the sentence is all safe cells
            if sentence.known_safes():
                # loops throught the sentence (copy) and marks each cell as safe and removes it from the sentence
                for cell in sentence.known_safes().copy():
                    self.mark_safe(cell)

        # loops through the sentences in the knowledge
        for sentence in self.knowledge:
            # if the new sentence is a subset of an existing sentence and bot sentences have mines atleast one mine
            if new_sentence.cells.issubset(sentence.cells) and sentence.count > 0 and new_sentence.count > 0:
                # if the two sentences are not the same
                if new_sentence != sentence:
                    # new subset is the difference between the two sentences
                    new_subset = sentence.cells.difference(new_sentence.cells)
                    # adds the subset as a new sentence
                    new_sentence_subset = Sentence(
                        list(new_subset), sentence.count - new_sentence.count)
                    self.knowledge.append(new_sentence_subset)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # loops through the safe cells and picks one that has not already been moved to
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = []

        # loops through the board
        for i in range(self.height):
            for j in range(self.width):
                # if the cell is not a made move and not a mine appends to possiblem oves
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    possible_moves.append((i, j))

        # if there is a move to make it makes a random move
        if len(possible_moves) != 0:
            return random.choice(possible_moves)
        else:
            return None