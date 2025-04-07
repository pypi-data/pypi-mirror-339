import px


def test_id():
    ret = px.hello()
    print(f"ret: {ret}")

    px.generate_id_digit()

    for i in range(100):
        print(f"{px.generate_id_digit()}, {px.generate_id_str()}")


def test_benchmark():
    import timeit

    ret = timeit.timeit(
        "px.generate_id_digit()",
        setup="import px",
        number=100000,
    )

    print(f"timeit: {ret}")
    ret = timeit.timeit(
        "px.generate_id_str()",
        setup="import px",
        number=100000,
    )

    print(f"timeit: {ret}")

    # for i in range(100):
    #     px.generate_id_digit()

    # for i in range(100):
    #     px.generate_id_str()
