from archijson.geometry import Circle
import archijson.geometry as geometry
import json


def test_circle():
    c = Circle(5, 10, properties={'color': 'red'})

    assert c.type == 'Circle'
    print(c.type)
    print(c.data)
    print(c.param)
    print(c.validate)
    assert c.is_valid(c.data)
