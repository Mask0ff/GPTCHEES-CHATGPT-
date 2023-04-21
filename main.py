import openai

# 初始化棋盘
board = [[' ' for _ in range(15)] for _ in range(15)]

# OpenAI API凭证
openai.api_key = "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"

# 初始化棋盘
board = [[' ' for _ in range(15)] for _ in range(15)]

# 玩家下棋
def player_move(board):
    while True:
        try:
            x, y = map(int, input("请下棋，输入坐标（例如：3 4）：").split())
            if x < 1 or x > 15 or y < 1 or y > 15:
                print("坐标输入错误，请重新输入！")
            elif board[x - 1][y - 1] != ' ':
                print("该位置已经有棋子，请重新输入！")
            else:
                return x - 1, y - 1
        except ValueError:
            print("坐标输入错误，请重新输入！")

# 使用OpenAI API进行对话生成
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].text.strip()

# AI下棋
def get_ai_move(board):
    # 使用对话生成获取电脑下一步的位置
    prompt = "board = " + str(board) + "\n" + "player = ○" + "\n" + "AI = ●" + "\n" + "What is your next move?"
    ai_move_str = generate_response(prompt)
    ai_move = ai_move_str.split()
    try:
        x = int(ai_move[0])
        y = int(ai_move[1])
    except (ValueError, IndexError):
        print("Invalid AI move string:", ai_move_str)
        return get_ai_move(board)

    return x, y


# 打印棋盘
def print_board(board):
    print('   1 2 3 4 5 6 7 8 9 10 11 12 13 14 15')
    for i in range(15):
        print('%2d' % (i + 1), end=' ')
        for j in range(15):
            print(board[i][j], end=' ')
        print()

# 检查是否获胜
def check_win(row, col, player):
    # 检查横向
    count = 0
    for j in range(col - 4, col + 5):
        if j < 0 or j >= 15:
            continue
        if board[row][j] == player:
            count += 1
            if count == 5:
                return True
        else:
            count = 0

    # 检查竖向
    count = 0
    for i in range(row - 4, row + 5):
        if i < 0 or i >= 15:
            continue
        if board[i][col] == player:
            count += 1
            if count == 5:
                return True
        else:
            count = 0

    # 检查正斜向
    count = 0
    for i, j in zip(range(row - 4, row + 5), range(col - 4, col + 5)):
        if i < 0 or i >= 15 or j < 0 or j >= 15:
            continue
        if board[i][j] == player:
            count += 1
            if count == 5:
                return True
        else:
            count = 0

    # 检查反斜向
    count = 0
    for i, j in zip(range(row - 4, row + 5), range(col + 4, col - 5, -1)):
        if i < 0 or i >= 15 or j < 0 or j >= 15:
            continue
        if board[i][j] == player:
            count += 1
            if count == 5:
                return True
        else:
            count = 0

    # 如果没有连成一条线，则返回 False
    return False

def check_draw(board):
    for row in board:
        for piece in row:
            if piece == ' ':
                return False
    return True



# 主循环
def main():
    # 初始化棋盘
    board = [[' ' for _ in range(15)] for _ in range(15)]

    # 打印棋盘
    print_board(board)

    # 循环下棋直到游戏结束
    while True:
        # 玩家下棋
        x, y = player_move(board)
        board[x][y] = '●'
        print_board(board)
        if check_win(x, y, '●'):
            print("恭喜你，你赢了！")
            break
        if check_draw(board):
            print("平局！")
            break

        # AI下棋
        print("电脑正在思考中...")
        x, y = get_ai_move(board)
        board[x][y] = '○'
        print_board(board)
        if check_win(x, y, '○'):
            print("电脑赢了！")
            break
        if check_draw(board):
            print("平局！")
            break



if __name__ == '__main__':
    main()
