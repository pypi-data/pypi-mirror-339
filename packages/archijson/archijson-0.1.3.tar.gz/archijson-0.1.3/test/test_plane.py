from archijson.geometry import Plane

def test():
    c = Plane(5, 10, properties={'color': 'red'})
    print(c)
    print(type(c))
    print(c.data)

    print(c.validate)

    print(Plane.is_valid(c.data))

