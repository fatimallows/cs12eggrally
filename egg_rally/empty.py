def generate_test_cases() -> None:
    # for n in range(2, 15):
    #     for m in range(n + 1, 15):
    #         print(
    #             f'assert abs(Vector({m ** 2 - n ** 2}, {2*m*n})) == {m ** 2 + n ** 2}')

    print(*(f'assert isclose(Vector({a}, {b}) + Vector({c}, {d}) == Vector({a+b}, {c+d}))'
            for a in {-0.2 - 0.1, 0, 0.1, 0.2}
            for b in {-0.2 - 0.1, 0, 0.1, 0.2}
            for c in {-0.2 - 0.1, 0, 0.1, 0.2}
            for d in {-0.2 - 0.1, 0, 0.1, 0.2}
            ), sep='\n')


generate_test_cases()
