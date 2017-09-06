assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values
    
def cross(A, B):
    return [s+t for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [[rows[i]+cols[i] for i in range(9)], [rows[i]+cols[8 - i] for i in range(9)]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

""""""
def is_values_twins(v1, v2):
    if len(v1) > 0 and len(v1) == len(v2):
        for c in v1:
            if c not in v2:
                return False;
        return True
    return False

def is_twins(box1, box2, values):
    return is_values_twins(values[box1], values[box2])  

def find_twins( unit, values):
    res = []
    for i in range(0, len(unit) - 1):
        if len(values[unit[i]]) != 2:
            continue
        
        for j in range(i+1, len(unit)):
            if len(values[unit[j]]) != 2:
                continue
            if is_twins(unit[i], unit[j], values) == True and values[unit[i]] not in res:
               "print(unit[i] + ' ' + values[unit[i]])"
               res.append(values[unit[i]])
               break
   
    return res
       
def twins_elimination(unit, values):
    twins = find_twins(unit, values)
    for v in twins:
        cnt = 2
        for b in unit:
            if is_values_twins(v, values[b])==True and cnt > 0:
                cnt-=1
                continue
            for char in v:                
                assign_value(values, b, values[b].replace(char,''))
    return values         
        

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    
    for u in unitlist:
        twins_elimination(u, values)

    return values
                

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit,''))
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values == False:
        return False
    "values = naked_twins(values)"
    if values == False:
        return False
    minBox = None
    for box in values:
        if len(values[box]) < 1:
            return False
        if len(values[box]) == 1:
            continue
        
        if minBox is None or len(values[minBox])>len(values[box]):
            minBox = box
        
    if minBox is None :
        return values
    
    for el in values[minBox]:
        copy = dict(values)
        assign_value(copy, minBox, el)        
        res = search(copy)
        if (res != False):
            return res
    

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
		"""
    return search(grid_values(grid))
	
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
