from archijson.geometry import BasePoint

def test_create():
    p1 = BasePoint(1, 2, 3)
    print(p1)
    assert p1.x == 1
    assert p1.y == 2
    assert p1.z == 3

    p2 = BasePoint([1, 1, 1])
    print(p2)

    p3 = BasePoint({'x': 909.1648356554529, 'y': 51.31071849793332, 'z': 0})
    print(p3)

    assert type(p1) == BasePoint

    p4 = BasePoint(p2)
    assert p4!=p2

