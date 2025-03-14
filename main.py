from settings import token
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CommandHandler, CallbackQueryHandler
import random
import copy


dict = {
    "將": 1,
    "士": 2,
    "象": 3,
    "車": 4,
    "馬": 5,
    "砲": 6,
    "卒": 7,
    "帥": -1,
    "仕": -2,
    "相": -3,
    "俥": -4,
    "傌": -5,
    "炮": -6,
    "兵": -7
}


def flip_chess(r, c):
    global count
    flipped = random.choice(un_flipped_chess)
    un_flipped_chess.remove(flipped)
    keyboard[r][c] = InlineKeyboardButton(
        flipped, callback_data=f"{r},{c}")
    if count == 0:
        global player_color
        global bot_color
        if flipped in black:
            player_color = copy.copy(black)
            bot_color = copy.copy(red)
            count += 1
        else:
            player_color = copy.copy(red)
            bot_color = copy.copy(black)
            count += 1


def can_eat(attacker, defender):
    if (dict[attacker] > 0 and dict[defender] > 0) or (dict[attacker] < 0 and dict[defender] < 0):
        return False
    elif (attacker == '兵' and defender == '將'):
        return True
    elif (attacker == '卒' and defender == '帥'):
        return True
    elif (attacker == '帥' and defender == '卒'):
        return False
    elif (attacker == '將' and defender == '兵'):
        return False
    elif (abs(dict[attacker]) <= abs(dict[defender])):
        return True
    elif (abs(dict[attacker]) > abs(dict[defender])):
        return False


def can_eat2(r, c):  # 進行砲和炮吃的判斷
    count = 0
    if r == choosed[0]:
        for i in range(min(c, choosed[1])+1, max(c, choosed[1])):
            if keyboard[r][i].text != ' ':
                count += 1
    elif c == choosed[1]:
        for i in range(min(r, choosed[0])+1, max(r, choosed[0])):
            if keyboard[i][c].text != ' ':
                count += 1
    if count == 1 and keyboard[r][c].text in bot_color:
        return True
    else:
        return False


def get_bot_valid_move():
    bot_valid_move = []
    for r in range(8):
        for c in range(4):
            if keyboard[r][c].text in bot_color:
                for r_move in [-1, 0, 1]:
                    for c_move in [-1, 0, 1]:
                        if abs(r_move + c_move) == 1:
                            try:
                                if (keyboard[r+r_move][c+c_move].text == ' ') and (r+r_move >= 0) and (c+c_move >= 0):
                                    bot_valid_move.append(
                                        [r, c, r+r_move, c+c_move])
                            except:
                                continue
    return (bot_valid_move)


def get_bot_valid_eat():
    bot_valid_eat = []
    for r in range(8):
        for c in range(4):
            if (keyboard[r][c].text in bot_color):
                if (keyboard[r][c].text != '砲') and (keyboard[r][c].text != '炮'):
                    for r_move in [-1, 0, 1]:
                        for c_move in [-1, 0, 1]:
                            if abs(r_move + c_move) == 1:
                                try:
                                    if (keyboard[r+r_move][c+c_move].text in player_color) and (r+r_move >= 0) and (c+c_move >= 0):
                                        if can_eat(keyboard[r][c].text, keyboard[r+r_move][c+c_move].text) == True:
                                            bot_valid_eat.append(
                                                [r, c, r+r_move, c+c_move])
                                except:
                                    continue
                elif (keyboard[r][c].text == '砲') or (keyboard[r][c].text == '炮'):
                    count = 0
                    for r2 in range(r-1, -1, -1):  # 從砲或炮的位置開始，往上尋找可以吃的棋是什麼
                        if keyboard[r2][c].text != ' ':
                            count += 1
                        if count == 2:
                            if keyboard[r2][c].text in player_color:
                                bot_valid_eat.append([r, c, r2, c])
                                break
                            break
                    count = 0
                    for r2 in range(r+1, 8, 1):  # 從砲或炮的位置開始，往下尋找可以吃的棋是什麼
                        if keyboard[r2][c].text != ' ':
                            count += 1
                        if count == 2:
                            if keyboard[r2][c].text in player_color:
                                bot_valid_eat.append([r, c, r2, c])
                                break
                            break
                    count = 0
                    for c2 in range(c+1, 4, 1):  # 從砲或炮的位置開始，往右尋找可以吃的棋是什麼
                        if keyboard[r][c2].text != ' ':
                            count += 1
                        if count == 2:
                            if keyboard[r][c2].text in player_color:
                                bot_valid_eat.append([r, c, r, c2])
                                break
                            break
                    count = 0
                    for c2 in range(c-1, -1, -1):  # 從砲或炮的位置開始，往左尋找可以吃的棋是什麼
                        if keyboard[r][c2].text != ' ':
                            count += 1
                        if count == 2:
                            if keyboard[r][c2].text in player_color:
                                bot_valid_eat.append([r, c, r, c2])
                                break
                            break
    return bot_valid_eat


def move_or_eat(r1, c1, r2, c2):
    keyboard[r2][c2] = InlineKeyboardButton(
        keyboard[r1][c1].text, callback_data=f"{r2},{c2}")
    keyboard[r1][c1] = InlineKeyboardButton(
        ' ', callback_data=f"{r1},{c1}")


def get_bot_valid_flip():
    bot_valid_flip = []
    for r in range(8):
        for c in range(4):
            if keyboard[r][c].text == '●':
                bot_valid_flip.append([r, c])
    return bot_valid_flip


def bot_run():
    bot_move = []
    bot_eat = []
    bot_flip = []
    bot_move = get_bot_valid_move()
    bot_eat = get_bot_valid_eat()
    bot_flip = get_bot_valid_flip()
    while True:
        try:
            if len(bot_eat) != 0:
                bot_do = random.choice(bot_eat)
                break
            else:
                bot_do = random.choice(random.choice(
                    [bot_move, bot_eat, bot_flip]))
                break
        except:
            continue
    if len(bot_do) == 4:  # 吃或移動
        if keyboard[bot_do[2]][bot_do[3]].text == ' ':  # 移動
            keyboard[bot_do[2]][bot_do[3]] = InlineKeyboardButton(
                keyboard[bot_do[0]][bot_do[1]].text, callback_data=f"{bot_do[2]},{bot_do[3]}")
            keyboard[bot_do[0]][bot_do[1]] = InlineKeyboardButton(
                ' ', callback_data=f"{bot_do[0]},{bot_do[1]}")
            return (bot_do[2], bot_do[3])
        else:  # 吃
            keyboard[bot_do[2]][bot_do[3]] = InlineKeyboardButton(
                keyboard[bot_do[0]][bot_do[1]].text, callback_data=f"{bot_do[2]},{bot_do[3]}")
            keyboard[bot_do[0]][bot_do[1]] = InlineKeyboardButton(
                ' ', callback_data=f"{bot_do[0]},{bot_do[1]}")
            global player_eaten_count
            player_eaten_count += 1
            return (bot_do[2], bot_do[3])
    else:  # 翻棋
        flipped = random.choice(un_flipped_chess)
        un_flipped_chess.remove(flipped)
        keyboard[bot_do[0]][bot_do[1]] = InlineKeyboardButton(
            flipped, callback_data=f"{bot_do[0]},{bot_do[1]}")
        return (bot_do[0], bot_do[1])


async def func(update, context):
    global bot_eaten_count
    row, col = [int(x) for x in update.callback_query.data.split(',')]
    if len(choosed) == 0:  # 如果沒有選棋子
        if keyboard[row][col].text == '●':  # 如果格子裡的字是空白，則表示要翻棋
            flip_chess(row, col)
            await context.bot.edit_message_text(f'你的棋子有:{player_color}\n你翻了{row+1}, {col+1}，請等待bot下棋',
                                                reply_markup=InlineKeyboardMarkup(
                                                    keyboard),
                                                chat_id=update.callback_query.message.chat_id,
                                                message_id=update.callback_query.message.message_id)
            bot_row, bot_col = bot_run()
            await context.bot.edit_message_text(f'你的棋子有:{player_color}\nbot下了({bot_row+1}, {bot_col+1})，換你下囉!',
                                                reply_markup=InlineKeyboardMarkup(
                                                    keyboard),
                                                chat_id=update.callback_query.message.chat_id,
                                                message_id=update.callback_query.message.message_id)
        elif keyboard[row][col].text == ' ':
            await context.bot.answer_callback_query(update.callback_query.id, '不合理的選擇!')
            await context.bot.edit_message_text(f'你的棋子有:{player_color}\n請重新選擇!',
                                                reply_markup=InlineKeyboardMarkup(
                                                    keyboard),
                                                chat_id=update.callback_query.message.chat_id,
                                                message_id=update.callback_query.message.message_id)
        else:  # 即將吃棋或移動 先選擇棋子
            if keyboard[row][col].text in player_color:
                choosed.append(row)
                choosed.append(col)
                await context.bot.edit_message_text(f'你的棋子有:{player_color}\n請選擇從{row+1}, {col+1}移動到哪格',
                                                    reply_markup=InlineKeyboardMarkup(
                                                        keyboard),
                                                    chat_id=update.callback_query.message.chat_id,
                                                    message_id=update.callback_query.message.message_id)
            else:  # 如果選錯顏色
                await context.bot.answer_callback_query(update.callback_query.id, '不合理的選擇!')
                await context.bot.edit_message_text(f'你的棋子有:{player_color}\n請重新選擇!',
                                                    reply_markup=InlineKeyboardMarkup(
                                                        keyboard),
                                                    chat_id=update.callback_query.message.chat_id,
                                                    message_id=update.callback_query.message.message_id)
    else:  # 前面已經選過棋子 現在進行移動或吃
        if abs(choosed[0]+choosed[1]-row-col) == 1:
            if keyboard[row][col].text == ' ':  # 如果格子裡的字是空白，則表示要移動
                keyboard[row][col] = InlineKeyboardButton(
                    keyboard[choosed[0]][choosed[1]].text, callback_data=f"{row},{col}")
                keyboard[choosed[0]][choosed[1]] = InlineKeyboardButton(
                    ' ', callback_data=f"{choosed[0]},{choosed[1]}")
                choosed.clear()
                await context.bot.edit_message_text(f'你的棋子有:{player_color}\n你移動了({row+1}, {col+1}，請等待bot下棋)',
                                                    reply_markup=InlineKeyboardMarkup(
                                                        keyboard),
                                                    chat_id=update.callback_query.message.chat_id,
                                                    message_id=update.callback_query.message.message_id)
                bot_row, bot_col = bot_run()
                await context.bot.edit_message_text(f'你的棋子有:{player_color}\nbot下了({bot_row+1}, {bot_col+1})，換你下囉!',
                                                    reply_markup=InlineKeyboardMarkup(
                                                        keyboard),
                                                    chat_id=update.callback_query.message.chat_id,
                                                    message_id=update.callback_query.message.message_id)
            elif keyboard[row][col].text == '●':
                await context.bot.answer_callback_query(update.callback_query.id, '不合理的選擇!')
                await context.bot.edit_message_text(f'你的棋子有:{player_color}\n請重新選擇!',
                                                    reply_markup=InlineKeyboardMarkup(
                                                        keyboard),
                                                    chat_id=update.callback_query.message.chat_id,
                                                    message_id=update.callback_query.message.message_id)
                choosed.clear()
            else:  # 吃棋
                if (can_eat(keyboard[choosed[0]][choosed[1]].text,  keyboard[row][col].text) == True) and (keyboard[choosed[0]][choosed[1]].text != '砲') and (keyboard[choosed[0]][choosed[1]].text != '炮'):
                    bot_eaten_count += 1
                    move_or_eat(choosed[0], choosed[1], row, col)
                    await context.bot.edit_message_text(f'你的棋子有:{player_color}\n你吃了棋{row+1}, {col+1},請等待bot下棋',
                                                        reply_markup=InlineKeyboardMarkup(
                                                            keyboard),
                                                        chat_id=update.callback_query.message.chat_id,
                                                        message_id=update.callback_query.message.message_id)
                    choosed.clear()
                    if (player_eaten_count != 16) and (bot_eaten_count != 16):
                        bot_row, bot_col = bot_run()
                        await context.bot.edit_message_text(f'你的棋子有:{player_color}\nbot下了({bot_row+1}, {bot_col+1})，換你下囉!',
                                                            reply_markup=InlineKeyboardMarkup(
                                                                keyboard),
                                                            chat_id=update.callback_query.message.chat_id,
                                                            message_id=update.callback_query.message.message_id)

                else:
                    await context.bot.answer_callback_query(update.callback_query.id, '不合理的選擇!')
                    await context.bot.edit_message_text(f'你的棋子有:{player_color}\n請重新選擇!',
                                                        reply_markup=InlineKeyboardMarkup(
                                                            keyboard),
                                                        chat_id=update.callback_query.message.chat_id,
                                                        message_id=update.callback_query.message.message_id)
                    choosed.clear()
        elif (keyboard[choosed[0]][choosed[1]].text == '砲') or (keyboard[choosed[0]][choosed[1]].text == '炮'):  # 進行砲或炮的吃
            if can_eat2(row, col) == True:
                bot_eaten_count += 1
                move_or_eat(choosed[0], choosed[1], row, col)
                choosed.clear()
                await context.bot.edit_message_text(f'你的棋子有:{player_color}\n你吃了棋{row+1}, {col+1},請等待bot下棋',
                                                    reply_markup=InlineKeyboardMarkup(
                                                        keyboard),
                                                    chat_id=update.callback_query.message.chat_id,
                                                    message_id=update.callback_query.message.message_id)
                if (player_eaten_count != 16) and (bot_eaten_count != 16):
                    bot_row, bot_col = bot_run()
                    await context.bot.edit_message_text(f'你的棋子有:{player_color}\nbot下了({bot_row+1}, {bot_col+1})，換你下囉!',
                                                        reply_markup=InlineKeyboardMarkup(
                                                            keyboard),
                                                        chat_id=update.callback_query.message.chat_id,
                                                        message_id=update.callback_query.message.message_id)
            else:
                await context.bot.answer_callback_query(update.callback_query.id, '不合理的選擇!')
                await context.bot.edit_message_text(f'你的棋子有:{player_color}\n請重新選擇!',
                                                    reply_markup=InlineKeyboardMarkup(
                                                        keyboard),
                                                    chat_id=update.callback_query.message.chat_id,
                                                    message_id=update.callback_query.message.message_id)
                choosed.clear()
        else:
            await context.bot.answer_callback_query(update.callback_query.id, '不合理的選擇!')
            await context.bot.edit_message_text(f'你的棋子有:{player_color}\n請重新選擇!',
                                                reply_markup=InlineKeyboardMarkup(
                                                    keyboard),
                                                chat_id=update.callback_query.message.chat_id,
                                                message_id=update.callback_query.message.message_id)
            choosed.clear()
    if player_eaten_count == 16:
        await context.bot.edit_message_text(f'你的棋子有:{player_color}\n你沒有棋子可以下了，輸爛了呵',
                                            reply_markup=InlineKeyboardMarkup(
                                                keyboard),
                                            chat_id=update.callback_query.message.chat_id,
                                            message_id=update.callback_query.message.message_id)
    elif bot_eaten_count == 16:
        await context.bot.edit_message_text(f'你的棋子有:{player_color}\nbot沒有棋子可以下了，你贏麻了',
                                            reply_markup=InlineKeyboardMarkup(
                                                keyboard),
                                            chat_id=update.callback_query.message.chat_id,
                                            message_id=update.callback_query.message.message_id)


async def start(update, context):
    global keyboard, un_flipped_chess, count, player_eaten_count, bot_eaten_count
    un_flipped_chess = ["將", "士", "士", "象", "象", "車", "車", "馬", "馬", "砲", "砲", "卒", "卒", "卒", "卒", "卒",
                        "帥", "仕", "仕", "相", "相", "俥", "俥", "傌", "傌", "炮", "炮", "兵", "兵", "兵", "兵", "兵"]
    random.shuffle(un_flipped_chess)
    player_color.clear()
    bot_color.clear()
    count = 0
    player_eaten_count = 0
    bot_eaten_count = 0
    keyboard = [[InlineKeyboardButton('●', callback_data=f"{row},{
                                      col}") for col in range(4)] for row in range(8)]
    await update.message.reply_text('開始遊戲，由你開始下', reply_markup=InlineKeyboardMarkup(keyboard))


def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    application.add_handler(CallbackQueryHandler(func))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    black = ["將", "士", "象", "車", "馬", "砲", "卒"]
    red = ["帥", "仕", "相", "俥", "傌", "炮", "兵"]
    keyboard = []
    choosed = []
    player_color = []
    bot_color = []
    count = 0
    player_eaten_count = 0
    bot_eaten_count = 0
    main()
