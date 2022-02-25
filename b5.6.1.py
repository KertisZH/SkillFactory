DIVIDER = '-----------------------'


def greet():
    print(DIVIDER)
    print('Приветствуем вас в игре')
    print('    крестики-нолики')
    print('   Формат ввода: x y')
    print('   x - номер строки')
    print('   y - номер столбца')
    print(DIVIDER)

    
def show():
    print('')
    print(DIVIDER)
    print('    |  0  |  1  |  2  |')
    print(DIVIDER)
    for i, row in enumerate(fields):
        print(f'  {i} |  {"  |  ".join(row)}  |')
        print(DIVIDER)
        

def ask():
    while True:
        user_input = input('Введите 2 координаты: ')
        coords = user_input.split()
        
        if len(coords) < 2:
            print('Введите 2 координаты')
            continue
        
        x, y = coords
        
        if not x.isdigit() or not y.isdigit():
            print('Координаты должны быть цифрами')
            continue
            
        x, y = int(x), int(y)
        
        if not 0 <= x <= 2 or not 0 <= y <= 2:
            print('Координаты должны быть в диапазоне [0, 2]')
            continue
            
        if fields[x][y] != ' ':
            print('Клетка занята!')
            continue
            
        return x, y


def check_win_conditions():
    wins_coords = (
        ((0, 0), (0, 1), (0, 2)),  # Первая строка
        ((1, 0), (1, 1), (1, 2)),  # Вторая строка
        ((2, 0), (2, 1), (2, 2)),  # Третья строка
        ((0, 0), (1, 0), (2, 0)),  # Первый столбец
        ((0, 1), (1, 1), (2, 1)),  # Второй столбец
        ((0, 2), (1, 2), (2, 2)),  # Третий столбец
        ((0, 0), (1, 1), (2, 2)),  # Первая диагональ
        ((0, 2), (1, 1), (2, 0)),  # Вторая диагональ
    )
    
    for win_coord in wins_coords:
        symbols = []

        for position in win_coord:
            symbols.append(fields[position[0]][position[1]])

        if symbols == ['X', 'X', 'X']:
            print('Победил X!')
            return True

        if symbols == ['O', 'O', 'O']:
            print('Победил O!')
            return True        
    
    return False

        
greet()

fields = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]

count = 0
while count < 9:
    count += 1
    show()
    
    if count % 2 == 1:
        print('Ходит X')
        x, y = ask()
        fields[x][y] = 'X'
    else:
        print('Ходит O')
        x, y = ask()
        fields[x][y] = 'O'
    
    if check_win_conditions():
        show()  # Показать последнее состояние полей
        break
else:
    show()  # Показать последнее состояние полей
    print('Ничья!')
