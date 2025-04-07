from calculadora import soma, subtracao, multiplicacao

def test_soma():
    assert soma(2, 3) == 5
    assert soma(-1, 1) == 0

def test_subtracao():
    assert subtracao(5, 2) == 3
    assert subtracao(3, 5) == -2

def test_multiplicacao():
    assert multiplicacao(2, 3) == 6
    assert multiplicacao(-2, 3) == -6
