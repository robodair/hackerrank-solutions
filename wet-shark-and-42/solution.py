GAIN_SQUARE_THRESHOLD = 42
MOD = 1000000007

def main():
    tests = int(raw_input())
    for i in range(tests):
        print get_squares(int(raw_input())) 


def get_squares(strength):
    raw_squares = 2 * strength
    bonus_squares = get_bonus(raw_squares)
    squares = (raw_squares + bonus_squares) % MOD
    return squares

def get_bonus(squares):
    if squares < GAIN_SQUARE_THRESHOLD:
        return 0
    leftover_squares = squares % GAIN_SQUARE_THRESHOLD
    extra_squares = (squares // GAIN_SQUARE_THRESHOLD) * 2
    extra_squares += get_bonus(extra_squares + leftover_squares)

    return extra_squares

if __name__ == "__main__":
    main()
