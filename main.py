from tkinter import *
import time

def check_win(m, sign):
    zero = 0
    for row in m:
        zero += row.count(0)
        if row.count(sign) == 3:
            return sign
    for col in range(3):
        if m[0][col] == sign and m[1][col] == sign and m[2][col] == sign:
            return sign
    if m[0][0] == sign and m[1][1] == sign and m[2][2] == sign:
        return sign
    if m[0][2] == sign and m[1][1] == sign and m[2][0] == sign:
        return sign
    if zero == 0:
        return "Ничья"
    return False
root = Tk()
root.title('Крестики-нолики')
root.resizable(0, 0)
root.wm_attributes('-topmost', 1)
app_running = True

text = Text()

size_block = 200
m = [[0] * 3 for i in range(3)]

canvas = Canvas(root, width = size_block * 3, height = size_block * 3, highlightthickness=0, bg = "grey")
canvas.pack()
root.update()
query = 0
stop = 0

def getorigin(eventorigin):
    global x, y, query, stop
    x = eventorigin.x
    y = eventorigin.y
    col = x // size_block
    row = y // size_block
    x = col * size_block
    y = row * size_block
    if m[row][col] == 0 and stop == 0:
        if query % 2 == 0:
            m[row][col] = 'x'
            color = 'red'
        else:
            m[row][col] = 'o'
            color = 'green'
        query += 1
    if color == 'red':
        canvas.create_rectangle(x, y, x + size_block, y + size_block, fill = color)
        canvas.create_line(x, y, x + size_block, y + size_block)
        canvas.create_line(x + size_block, y, x, y + size_block)
    if color == 'green':
        canvas.create_rectangle(x, y, x + size_block, y + size_block, fill = color)
        canvas.create_oval(x, y, x + size_block, y + size_block)
    if (query - 1) % 2 == 0:
        game_over = check_win(m, 'x')
    else:
        game_over = check_win(m, 'o')
    if game_over == 'x' or game_over == 'o':
        print(game_over, "выйграл")
        stop = 1
    if game_over == "Ничья":
        print(game_over)
        stop = 1


def draw_table():
    for i in range(0, 4):
        canvas.create_line(0, i * size_block, size_block * 3, i * size_block)
    for i in range(0, 4):
        canvas.create_line(i * size_block, 0, i * size_block, size_block * 3)

draw_table()

root.bind("<Button 1>", getorigin)
root.mainloop()

while 1:
    if app_running:
        root.update_idletasks()
        root.update()
    time.sleep(0.005)
    print(color)

