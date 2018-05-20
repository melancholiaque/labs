Q_NAME, SLOW = 'task_q', False


def work_func(client_prefix, n):
    recur = (lambda f: (lambda x: f(f, x)))
    fact = recur(lambda g, y: y == 0 and 1 or y*g(g, y - 1))
    return f'{client_prefix} {len(str(fact(n % 500)))}'
