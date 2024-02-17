from colorama import Fore, Style


class Board:
    '''hundo p this only exists because of all the fancy highlighting i'd like to do'''

    def __init__(self, values: str):
        self.values = values
        self.cell_highlights = [None]*len(self.values)
        for i in range(len(self.values)):
            if self.values[i] == '?':
                self.cell_highlights[i] = Style.BRIGHT + Fore.BLACK

    def analyze_rows(self):
        values = [*map(int, list(self.values))]
        row_sums = [0]*8
        # LR diagonal
        row_sums[0] = sum(values[0::4])
        # Columns
        for i in range(3):
            row_sums[i+1] = sum(values[i::3])
        # RL Diagonal
        row_sums[4] = sum(values[2:7:2])
        # Rows
        for i in range(3):
            row_sums[i+5] = sum(values[3*i:3*(i+1)])
        return row_sums

    def highlight_row(self, row_id: int, style: str):
        if row_id == 0:
            for i in [0, 4, 8]:
                self.cell_highlights[i] = style
        elif 1 <= row_id <= 3:
            j = row_id-1
            for i in [j, j+3, j+6]:
                self.cell_highlights[i] = style
        elif row_id == 4:
            for i in [2, 4, 6]:
                self.cell_highlights[i] = style
        elif 5 <= row_id <= 7:
            j = (row_id-5)*3
            for i in [j, j+1, j+2]:
                self.cell_highlights[i] = style

    def draw(self, row_captions=None):
        cell_values = list(self.values)
        # Apply highlights
        for i in range(len(cell_values)):
            if self.cell_highlights[i] != None:
                cell_values[i] = f'{self.cell_highlights[i]}{cell_values[i]}{Style.RESET_ALL}'
        # Preformat values to be inserted
        vals = (*row_captions[:6], *cell_values[:3], row_captions[6],
                *cell_values[3:6], row_captions[7], *cell_values[6:])
        print(
            '''\
  {:5}  {:^5} {:^5} {:^5}  {:<5}  
      ↘    ↓     ↓     ↓    ↙
        ┌─────┬─────┬─────┐
{:>5} → │  {}  │  {}  │  {}  │
        ├─────┼─────┼─────┤
{:>5} → │  {}  │  {}  │  {}  │
        ├─────┼─────┼─────┤
{:>5} → │  {}  │  {}  │  {}  │
        └─────┴─────┴─────┘
        '''.format(*vals)
        )
