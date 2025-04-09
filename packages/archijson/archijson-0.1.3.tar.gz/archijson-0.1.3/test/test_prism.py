from archijson.geometry import Prism, Segments

def test_prism():

    s = Segments([1, 1, 1, 3, 3, 3], 2, closed=True)
    p = Prism(s, 10, properties={'color': 'blue'})

    assert p.type == 'Prism'
    print(p.type)
    print(p.data)
    print(p.param)
    print(p.validate)
    assert p.is_valid(p.data)

    print(p.data)
