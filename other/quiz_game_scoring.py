def f(t):
    """
    Define point-scoring system

    Formula:

    > f(t) = P * (1 - (t/2T))

    Where:

    - Constant P is max points that can be earnt
    - Constant T is total time for question
    - Variable t is time taken for question
    - Function f(t) is points earnt from question

    t must satisfy the interval [0,T]
    """

    P = 1000
    T = 30

    if not (0 <= t <= T):
        raise ValueError(f"t not in domain [0,{T}], received {t}")

    y = P * (1 - t / (2 * T))

    return y


print(f(40))
