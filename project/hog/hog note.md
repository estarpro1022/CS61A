# Project 1：Hog

## 项目内容

Hog是61a的第一个project：两个玩家轮流掷骰子，总点数达到`GOAL`（默认100）就是胜者。每回合可以选择骰子的数量，1-10个任意挑选。看到这，你可能以为每次都选十个不好了，这样点数加的快，实际上还有一条规则：

* sow sad：抛出的骰子中只要有一个点数为1，这回合的点数就是1

正常游戏中，还有两条规则：

* pig tail：如果选择不掷骰子，即骰子的数量为1，这一回合的分数就是`2 * (tens - ones) + 1`，其中`tens`、`ones`分别是对手分数的十位、个位
* square swine：玩家在当前回合加上得分后，如果总得分是完全平方数，即分数可以拆成自然数的平方，则总得分继续加至下一个自然数的平方

## 项目结构

```
.
├── dice.py
├── hog.py
├── hog_ui.py
├── ok
├── proj01.ok
├── __pycache__
│   ├── ...
├── tests
│   ├── ...
└── ucb.py
```

`dice.py` 模拟掷骰子的过程，包括`six_sided` `four_sided`产生fair outcome的方法，还有`make_test_dice`用于控制骰子的点数，方便测试

`hog.py` 是游戏的实现逻辑和策略，模拟玩家对战的过程

`hog_ui.py` 用于输出游戏的界面（显示在控制台的文字游戏），复用了`hog.py`的方法，让学生对逻辑层和显示层分离有了初步的认识。hog的实现方法和显示界面并没有糅合在一起，从而降低了项目的耦合性。

* hog也算个小项目了，光`hog.py`就有400行代码

其余的文件就是关于测试了，采用传统的ok评测，因为我们没有伯克利的邮箱，所以有关ok的命令最后都要加上`--local`。这里附上常见的ok指令

```python 
python ok -q <question_no> -u --local	# 解锁隐藏用例
python ok -q <question_no> --local	# 测试具体问题
python ok --local	# 测试全部用例
python ok --score --local	# 获取项目分数

python ok --help	# ok文档
```

## 项目实现

hog共分了12个小问题，每个问题里都会实现一个方法，组合起来就把项目写完了（组合的框架已经搭好）。~~然而正是框架搭好了，简化了很多步骤，如果start from scratch可能不能从全局角度理解整个项目，这也是很让我头疼的一个点~~。这里我们尽量抽象出基本逻辑， 一些不必要的冗余的代码阐述会摒弃，所以下面给出的函数可能并没有给出完全的代码（具体实现可以到`hog.py`中查看）。这也是John一直强调的abstraction——抽象。减少程序复杂度的方法有很多，函数就是one way to manage complexity

### Problem 0——认识`dice.py`

`dice.py`介绍了两种骰子的类型

* Fair，每次骰子的结果都是等可能的
* Test，给定一个序列，然后骰子的结果就按照序列的顺序，循环反复

`four_sided`和`six_sided`的实现方法非常漂亮，通过高阶函数`make_fair_dice`生成，不需要提供参数

```python
def make_fair_dice(n):
    def dice():
        return randint(1, n)
    return dice
four_sided = make_fair_dice(4)
six_sided = make_fair_dice(6)
```

`make_test_dice`的实现也耐人寻味，使用`*outcomes`表明参数数量不确定，`nonlocal index`确定下一次投掷结果

```python
def make_test_dice(*outcomes):
    index = len(outcomes) - 1	# 预先定义index，后面才能用nonlocal
    def dice():
        nonlocal index
        index = (index + 1) % len(outcomes)
        return outcomes[index]
    return dice
```

### Problem 1——`roll_dice`

```python
def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
```

docstring描述的太清晰了，函数要干什么、参数是什么都说的很清楚，我都想背下来这段话，因为笨人很难有这种口才，老是不能清楚表达自己的意思。

`roll_dice`就是将特定类型的骰子扔`num_roll`次，返回结果的和，如果触发了含1机制，就只能返回0（风险和机遇并存）

### Problem 2——`tail_points`

```python
from operator import mul

def tail_points(opponent_score):
    """Return the points scored by rolling 0 dice according to Pig Tail.
    
    opponent_score:   The total score of the other player.
    """
```

实现 *pig tail* 规则，当前玩家选择不掷骰子，从对手分数里加分

写起来还好，`%10`获得个位数字，`//10`再`%10`获得十位数字。这里整了个花活，用了`mul`函数，看起来清晰一点

### Problem 3——`take_turn`

```python
def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Return the points scored on a turn rolling NUM_ROLLS dice.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the other player.
    dice:            A function that simulates a single dice roll outcome.
    """
```

这里特判一下扔骰子的次数，如果为0，就触发`tail_points`，如果不为0，则正常扔骰子，并返回总点数

### Problem 4——`square_update`

```python
def square_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, *including* Square Swine.
    """
    # code
    
def simple_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, ignoring Square Swine.
    """
    return player_score + take_turn(num_rolls, opponent_score, dice)
```

更新玩家的分数，抽象出`update`函数，前面是扔骰子的过程，这时候就是更新玩家分数。其实这里可以将`update`和`take_turn`合并起来，但是这样又把过程杂糅起来了，将不同方法分开写更清晰点（老是担心如果自己从零写能不能想起来这点）

还需要添加`perfect_square`和`next_perfect_square`两个函数，用于处理完全平方数，我自己实现的比较丑，之后==可以参照下别人的处理方式==（waiting to be coped with)

### Problem 5——`play`

```python
def play(strategy0, strategy1, update,
         score0=0, score1=0, dice=six_sided, goal=GOAL):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first and Player 1's score second.

    E.g., play(always_roll_5, always_roll_5, square_update) simulates a game in
    which both players always choose to roll 5 dice on every turn and the Square
    Swine rule is in effect.

    A strategy function, such as always_roll_5, takes the current player's
    score and their opponent's score and returns the number of dice the current
    player chooses to roll.

    An update function, such as square_update or simple_update, takes the number
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
```

`play`模拟一整局的游戏，这里需要玩家掷骰子的策略，并提供玩家分数和对手分数，如`always_roll(6)`，不管分数如何每次掷6个骰子。也要实现回合转变，在player0扔完骰子并计算完分数后，要切换到player1，这里使用`who`来判断当前是哪个玩家，用`who = 1 - who`实现玩家切换

#### User Interface

`python hog_ui.py -n 1`可实现玩家和电脑对战

`python hog_ui.py -n 2` 实现玩家与玩家的对战

### Problem 6——`always_roll`

```python
def always_roll(n):
    """Return a player strategy that always rolls N dice.

    A player strategy is a function that takes two total scores as arguments (the current player's score, and the opponent's score), and returns a number of dice that the current player will roll this turn.
```

高阶函数，返回值是函数，这个函数总是返回n

### Problem 7——`is_always_roll`

```python
def is_always_roll(strategy, goal=GOAL):
    """Return whether strategy always chooses the same number of dice to roll.
```

将当前玩家的score和对手的score全部遍历一遍，看看strategy是不是每次返回的结果都相同

### Problem 8——`make_averaged`

```python
def make_averaged(original_function, total_samples=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION called TOTAL_SAMPLES times.

    To implement this function, you will have to use *args syntax.
```

返回函数，此函数接受参数后返回`original_function`被调用`total_samples`次后返回值的平均值

### Problem 9——`max_scoring_num_rolls`

```python
def max_scoring_num_rolls(dice=six_sided, total_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn score by calling roll_dice with the provided DICE a total of TOTAL_SAMPLES times. Assume that the dice always return positive outcomes.
```

这段比较难懂，大体意思就是判断扔多少个骰子得到的平均分数更高。这里借用上面的`average = make_averaged(roll_dice, total_samples)`，然后遍历1-10，`average(num, dice)`，看哪个结果最大就好了

### Problem 10、11——strategy

这里引入新的函数`winner`和`average_win_rate`

`winner`用于判断一轮游戏中谁是胜者，`average_win_rate`就是判断两个策略相比谁的胜率更高喽

`python hog.py -r`可以查看不同策略和`always_roll(6)`相比的优胜率
