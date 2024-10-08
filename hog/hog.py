"""The Game of Hog."""

from dice import six_sided, make_test_dice
from ucb import main, trace, interact

GOAL = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

# 一轮中扔num_rolls次six_sided面骰子，得分为多少
def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome. Defaults to the six sided dice.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    # END PROBLEM 1
#     执行num_roll次循环，返回sow_row规则：有1则本轮得分为1，无1，则得分为总和,即使得分为1，也要把骰子掷完
#   注意：dice()只能执行一次
    sum = 0
    flag = 0
    for i in range(0,num_rolls):
        current_num = dice()
        if current_num == 1:
            flag = 1
        if flag != 1:
            sum += current_num
        else:
            sum = 1

    return sum


# 如果玩家扔出0骰子，该获得多少分
def boar_brawl(player_score, opponent_score):
    """Return the points scored by rolling 0 dice according to Boar Brawl.

    player_score:     The total score of the current player.
    opponent_score:   The total score of the other player.

    """
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    # END PROBLEM 2
#     当玩家掷出0骰子时，返回的分数应该是什么

    player_ones = player_score % 10
    opponent_tens = opponent_score // 10 % 10

    difference_value = abs(opponent_tens - player_ones)

    score = difference_value * 3

    return max(score,1)


# 本轮扔num_rolls次骰子，会获得多少分（不是总分）
def take_turn(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the points scored on a turn rolling NUM_ROLLS dice when the
    player has PLAYER_SCORE points and the opponent has OPPONENT_SCORE points.

    num_rolls:       The number of dice rolls that will be made.
    player_score:    The total score of the current player.
    opponent_score:  The total score of the other player.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    if num_rolls == 0:
        return boar_brawl(player_score, opponent_score)
    else:
        return roll_dice(num_rolls, dice)
    # END PROBLEM 3



# 一轮掷n次骰子后返回的总分数(simple_update的结果)
def simple_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, ignoring Sus Fuss.
    """
    score = player_score + take_turn(num_rolls, player_score, opponent_score, dice)
    return score

# 返回n是否为素数
def is_prime(n):
    """Return whether N is prime."""
    if n == 1:
        return False
    k = 2
    while k < n:
        if n % k == 0:
            return False
        k += 1
    return True

def num_factors(n):
    """Return the number of factors of N, including 1 and N itself."""
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    # 是否为素数，是素数直接返回2
    if is_prime(n):
        return 2
    # 得分为1时返回1个因数,得分为2时返回2个因数
    if n == 1:
        return 1
    if n == 2:
        return 2
    # 不是素数，排除1和n这两个因子外，再计算还有多少个因子
    count = 2
    for i in range(2,n):
        if n % i ==0:
            count += 1
    return count
    # END PROBLEM 4

# 3,4个因数的分数，就加到下一个素数
def sus_points(score):
    """Return the new score of a player taking into account the Sus Fuss rule."""
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    if num_factors(score) == 3 or num_factors(score) == 4:
        while not is_prime(score):
            # print("DEBUG:",score)
            score += 1
    return score
    # END PROBLEM 4

# 将经过sus规则的分数返回
def sus_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, *including* Sus Fuss.
    """
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    un_sus_score = simple_update(num_rolls, player_score, opponent_score, dice)
    return sus_points(un_sus_score)
    # END PROBLEM 4

# print('----',simple_update(9,64,24,make_test_dice(5, 5, 1, 4, 6, 6, 2, 4, 1)))

def always_roll_5(score, opponent_score):
    """A strategy of always rolling 5 dice, regardless of the player's score or
    the opponent's score.
    """
    return 5

# 模拟全流程，返回两个玩家的最终分数
def play(strategy0, strategy1, update,
         score0=0, score1=0, dice=six_sided, goal=GOAL):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first and Player 1's score second.

    E.g., play(always_roll_5, always_roll_5, sus_update) simulates a game in
    which both players always choose to roll 5 dice on every turn and the Sus
    Fuss rule is in effect.

    A strategy function, such as always_roll_5, takes the current player's
    score and their opponent's score and returns the number of dice the current
    player chooses to roll.

    An update function, such as sus_update or simple_update, takes the number
    of dice to roll, the current player's score, the opponent's score, and the
    dice function used to simulate rolling dice. It returns the updated score
    of the current player after they take their turn.

    strategy0: The strategy for player0.
    strategy1: The strategy for player1.
    update:    The update function (used for both players).
    score0:    Starting score for Player 0
    score1:    Starting score for Player 1
    dice:      A function of zero arguments that simulates a dice roll.
    goal:      The game ends and someone wins when this score is reached.
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"

    def update_score(num_rolls, current_score, opponent_score, dice, update_strategy):
        if update_strategy == sus_update:
            return sus_update(num_rolls, current_score, opponent_score, dice)
        else:
            return simple_update(num_rolls, current_score, opponent_score, dice)

    while score0 < goal and score1 < goal:
        if who == 0:
            num_rolls0 = strategy0(score0, score1)
            score0 = update_score(num_rolls0, score0, score1, dice,update)
            who = 1-who
        else:
            num_rolls1 = strategy1(score1, score0)
            score1 = update_score(num_rolls1, score1, score0, dice,update)
            who = 1-who

    # END PROBLEM 5
    return score0, score1

# play(update=sus_update,score0=64,score1=24,goal=88,dice=make_test_dice(5, 5, 1, 4, 6, 6, 2, 4, 1))

#######################
# Phase 2: Strategies #
#######################

# 返回相同的扔骰子次数,不管给定的分数是多少
def always_roll(n):
    """Return a player strategy that always rolls N dice.

    A player strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(3)
    >>> strategy(0, 0)
    3
    >>> strategy(99, 99)
    3
    """
    assert n >= 0 and n <= 10
    # BEGIN PROBLEM 6
    "*** YOUR CODE HERE ***"
    def strategy(score0, score1):
        return n
    return strategy
    # END PROBLEM 6



def catch_up(score, opponent_score):
    """A player strategy that always rolls 5 dice unless the opponent
    has a higher score, in which case 6 dice are rolled.

    >>> catch_up(9, 4)
    5
    >>> strategy(17, 18)
    6
    """
    if score < opponent_score:
        return 6  # Roll one more to catch up
    else:
        return 5

# 检测一个策略 是否总是返回相同数量的骰子,而不管给定的分数是多少
# 就是检测用户自定义的策略是否符合标准：即不论参数是什么，总是返回固定的值，
# 输入n个不同的值来进行检验
def is_always_roll(strategy, goal=GOAL):
    """Return whether STRATEGY always chooses the same number of dice to roll
    given a game that goes to GOAL points.

    >>> is_always_roll(always_roll_5)
    True
    >>> is_always_roll(always_roll(3))
    True
    >>> is_always_roll(catch_up)
    False
    """
    # BEGIN PROBLEM 7
    "*** YOUR CODE HERE ***"
    constant_results = strategy(0,0)
    for score0 in range(goal):
        for score1 in range(goal):
            if strategy(score0,score1) != constant_results:
                return False

    return True
    # END PROBLEM 7

# 返回内部方法，再调用内部方法传参，内部方法的内部使用original_function方法，达成了使用外部方法的参数original_function和samples_count的目的
# 样本数量1000，并不代表同一个骰子扔1000次，而是扔1000个不同的骰子，
def make_averaged(original_function, samples_count=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    called SAMPLES_COUNT times.

    To implement this function, you will have to use *args syntax.
    # 扔40次骰子，每次扔1个骰子，依次出现的骰子数字为4，2，5，1，得出分数总和后求平均值
    # 扔40个不同的骰子，每次只扔1个骰子，
    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 40)
    >>> averaged_dice(1, dice)  # The avg of 10 4's, 10 2's, 10 5's, and 10 1's
    （40+20+50+10）/40= 3.0
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    def averaged_func(*args):
        total = 0
        for i in range(samples_count):
            # 得出本次扔骰子的分数，然后累加上原来的分数
            total +=original_function(*args)
        return total/samples_count
    return averaged_func
    # END PROBLEM 8



# 09的测试用例：
# >>> from hog import *
# >>> dice = make_test_dice(3)   # dice always returns 3
# >>> max_scoring_num_rolls(dice, samples_count=1000)
# 不管samples_count样例有多少个，因为每一个和每一次掷出的骰子面都是3，即使掷10次，所以最高平均分，取决于扔出的次数，扔出越多，平均分越高，最多扔10次，就是扔10次的平均分最高
# 每轮中平均扔多少次（1-10）拿到最高分，如果两轮扔的最高分相同，取最小的那个作为返回值
def max_scoring_num_rolls(dice=six_sided, samples_count=1000):
    """Return the number of dice (1 to 10) that gives the maximum average score for a turn.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    # 最高平均分
    max_average = 0
    # 得到最高平均分的扔骰子次数
    max_rolls = 0
    for i in range(1,11):
        # 进行1000轮重复实验，每轮扔1-10次骰子
        average = make_averaged(roll_dice,samples_count)
        score = average(i,dice)
        if score > max_average:
            max_average = score
            #     第一轮，扔1次，重复实验1000次，最高平均分10，
            #       第二轮，扔2次，最高平均分20
            # 第八轮平均分：扔8次，最高平局分20，
            # 应该返回2
            max_rolls = i
    return max_rolls
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1, sus_update)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    six_sided_max = max_scoring_num_rolls(six_sided)
    print('Max scoring num rolls for six-sided dice:', six_sided_max)

    print('always_roll(6) win rate:', average_win_rate(always_roll(6))) # near 0.5
    print('catch_up win rate:', average_win_rate(catch_up))
    print('always_roll(3) win rate:', average_win_rate(always_roll(3)))
    print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    print('boar_strategy win rate:', average_win_rate(boar_strategy))
    print('sus_strategy win rate:', average_win_rate(sus_strategy))
    print('final_strategy win rate:', average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"

# 返回掷骰子的次数，如果当前情况掷0骰子有利，则掷0骰子，否则就返回对应的num_rolls
# 进一步解释：如果掷0骰子可以至少保证有threshold这个阈值的分数，那么就没必要选择冒更多的风险，直接掷0骰子就好，如果不能，那么可以冒险一把，掷num_rolls次骰子
# 这是保底策略，当前自己和对手的分数是确定的，所以如果掷0骰子能保证自己拿到x分，如果掷骰子就变成了不确定的分数
def boar_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """This strategy returns 0 dice if Boar Brawl gives at least THRESHOLD
    points, and returns NUM_ROLLS otherwise. Ignore score and Sus Fuss.
    """
    # BEGIN PROBLEM 10
    if boar_brawl(score, opponent_score) >= threshold:
        return 0
    return num_rolls  # Remove this line once implemented.
    # END PROBLEM 10

# 如果扔0骰子后的分数经过sus fuss规则后的我的分数-原来我的分数>=阈值，那么就采取扔0骰子,否则扔num_rolls次骰子
def sus_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """This strategy returns 0 dice when your score would increase by at least threshold."""
    # BEGIN PROBLEM 11
    # 如果经过sus fuss规则后的我的分数>=阈值，那么就采取扔0骰子
    if sus_update(0,score,opponent_score) - score >= threshold:
        return 0
    return num_rolls  # Remove this line once implemented.
    # END PROBLEM 11

# 最终策略的胜率要超过基础策略run_experiments,只要投0从的骰子点数,比投6次的骰子点数多,那么就投0次
def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.
    综合考虑Boar Brawl和Sus Fuss规则，以及分数差距，设计策略。
    # 如果即将接近100分,则采取保守策略
    # 如果通过掷0骰子能获胜,则掷0
    # 如果领先对手,则采取保守策略
    # 如果落后对手,则采取进攻策略
    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    if boar_brawl(score, opponent_score) >= 100:
        return 0
    if score + 10 >= 100:
        return 1
    # 如果前面的都不符合,并且当前领先对手,那么采取较保守策略
    if score > opponent_score:
        return 3
    # 否则采取冒进策略
    else:
        return 6  # Remove this line once implemented.
    # END PROBLEM 12


##########################
# Command Line Interface #
##########################

# NOTE: The function in this section does not need to be changed. It uses
# features of Python not yet covered in the course.

# @main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    # args = parser.parse_args()
    #
    # if args.run_experiments:
    #     run_experiments()

    args = parser.parse_args()
    print("Arguments received:", args)  # 输出解析的参数值看是否包括 run_experiments

    if args.run_experiments:
        print("Running experiments")
        run_experiments()
    else:
        print("run_experiments not triggered")  # 如果没有触发，打印提示信息

if __name__ == '__main__':
    run()