import schema, math
from archijson.geometry import BaseGeometry


class Cuboid(BaseGeometry):
    def __init__(self, length=1, width=1, height=1, **kwargs):
        if('type' in kwargs):
            del kwargs['type']
        super(Cuboid, self).__init__('Cuboid', **kwargs)
        self.__length = length
        self.__width = width
        self.__height = height
        self.matrix[0] = float(length)
        self.matrix[5] = float(width)
        self.matrix[10] = float(height)

    @property
    def length(self):
        return self.__length

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @length.setter
    def length(self, length):
        m = self.matrix[0]
        self.matrix[0] = m*length/self.length
        self.__w = length

    @width.setter
    def width(self, width):
        m = self.matrix[5]
        self.matrix[5] = m*width/self.width
        self.__width = width

    @height.setter
    def height(self, height):
        m = self.matrix[10]
        self.matrix[10] = m*height/self.height
        self.__height = height

    @property
    def param(self):
        return {
            'length': self.length,
            'width': self.width,
            'height': self.height
        }

    @property
    def data(self):
        return {
            **super(Cuboid, self).data,
            **self.param
        }

    def DATASCHEMA():
        return schema.Schema({
            'type': 'Cuboid',
            'length': schema.And(schema.Or(float, int), lambda x: x > 0),
            'width': schema.And(schema.Or(float, int), lambda x: x > 0),
            'height': schema.And(schema.Or(float, int), lambda x: x > 0),
        }, ignore_extra_keys=True)

    @property
    def validate(self):
        a = super(Cuboid, self).validate()
        b = Cuboid.DATASCHEMA().validate(self.data)
        return {
            **a,
            **b
        }

    def is_valid(obj):
        return BaseGeometry.DATASCHEMA().is_valid(obj) & Cuboid.DATASCHEMA().is_valid(obj)


class Plane(BaseGeometry):

    def __init__(self, length=1, width=1, **kwargs):
        if('type' in kwargs):
            del kwargs['type']
        super(Plane, self).__init__('Plane', **kwargs)
        self.__length = length
        self.__width = width
        self.matrix[0] = float(length)
        self.matrix[5] = float(width)

    @property
    def length(self):
        return self.__length
    
    @property
    def width(self):
        return self.__width
    
    @length.setter
    def length(self, length):
        m = self.matrix[0]
        self.matrix[0] = m*length/self.length
        self.__length = length
    
    @width.setter
    def width(self, width):
        m = self.matrix[5]
        self.matrix[5] = m*width/self.width
        self.__width = width
    
    @property
    def param(self):
        return {
            'length': self.length,
            'width': self.width
        }

    @property
    def data(self):
        return {
            **super(Plane, self).data,
            **self.param
        }
    
    def DATASCHEMA():
        return schema.Schema({
            'type':'Plane',
            'length': schema.And(schema.Or(float, int), lambda x: x > 0),
            'width': schema.And(schema.Or(float, int), lambda x: x > 0)
        }, ignore_extra_keys=True)
    
    @property
    def validate(self):
        return {
            **super(Plane, self).validate(),
            **Plane.DATASCHEMA().validate(self.data)
        }
    
    def is_valid(obj):
        return BaseGeometry.DATASCHEMA().is_valid(obj) & Plane.DATASCHEMA().is_valid(obj)




class Cylinder(BaseGeometry):
    def __init__(self, radius=1, height=1, **kwargs):
        if('type' in kwargs):
            del kwargs['type']
        super(Cylinder, self).__init__('Cylinder', **kwargs)

        self.__radius = radius
        self.__height = height
        self.matrix[0] = float(radius)
        self.matrix[5] = float(radius)
        self.matrix[10] = float(height)

    @property
    def radius(self):
        return self.__radius

    @property
    def height(self):
        return self.__height

    @radius.setter
    def radius(self, radius):
        m = self.matrix[0]
        self.matrix[0] = m*radius/self.radius
        self.matrix[5] = m*radius/self.radius
        self.__r = radius

    @height.setter
    def height(self, height):
        m = self.matrix[10]
        self.matrix[10] = m*height/self.height
        self.__height = height

    @property
    def param(self):
        return {
            'radius': self.radius,
            'height': self.height
        }

    @property
    def data(self):
        return {
            **super(Cylinder, self).data,
            **self.param
        }

    
    def DATASCHEMA():
        return schema.Schema({
            'type': 'Cylinder',
            'radius': schema.And(schema.Or(float, int), lambda x: x > 0),
            'height': schema.And(schema.Or(float, int), lambda x: x > 0)
        }, ignore_extra_keys=True)

    @property
    def validate(self):
        return {
            **super(Cylinder, self).validate(),
            **Cylinder.DATASCHEMA().validate(self.data)
        }
    
    def is_valid(obj):
        return BaseGeometry.DATASCHEMA().is_valid(obj) & Cylinder.DATASCHEMA().is_valid(obj)


class Circle(BaseGeometry):
    def __init__(self, radius=1, theta=math.pi, **kwargs):
        if('type' in kwargs):
            del kwargs['type']
        super(Circle, self).__init__('Circle', **kwargs)
        self.__radius = radius
        self.__theta = theta
        self.matrix[0] = float(radius)
        self.matrix[5] = float(radius)

    def __str__(self):
        return ("Circle: radius = {}, theta = {}".format(self.radius, self.theta))

    @property
    def radius(self):
        return self.__radius

    @property
    def theta(self):
        return self.__theta

    @radius.setter
    def radius(self, radius):
        m = self.matrix[0]
        self.matrix[0] = m*radius/self.radius
        self.__radius = radius

    @theta.setter
    def theta(self, theta):
        m = self.matrix[5]
        self.matrix[5] = m*theta/self.theta
        self.__theta = theta

    @property
    def param(self):
        return {
            'radius': self.radius,
            'theta': self.theta
        }

    @property
    def data(self):
        return {
            **super(Circle, self).data,
            **self.param
        }

    def DATASCHEMA():
        return schema.Schema({
            'type': 'Circle',
            'radius': schema.And(schema.Or(float, int), lambda x: x > 0),
            'theta': schema.And(schema.Or(float, int), lambda x: x > 0)
        }, ignore_extra_keys=True)

    @property
    def validate(self):
        return {
            **super(Circle, self).validate(),
            **Circle.DATASCHEMA().validate(self.data)
        }

    @staticmethod
    def is_valid(obj):
        return BaseGeometry.DATASCHEMA().is_valid(obj) & Circle.DATASCHEMA().is_valid(obj)


class Sphere(BaseGeometry):
    def __init__(self, radius=1, **kwargs):
        if('type' in kwargs):
            del kwargs['type']
        super(Sphere, self).__init__('Sphere', **kwargs)
        self.__radius = radius
        self.matrix[0] = float(radius)
        self.matrix[5] = float(radius)
        self.matrix[10] = float(radius)

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, radius):
        m = self.matrix[0]
        self.matrix[0] = m*radius/self.radius
        self.matrix[5] = m*radius/self.radius
        self.matrix[10] = m*radius/self.radius
        self.__radius = radius

    @property
    def param(self):
        return {
            'radius': self.radius
        }

    @property
    def data(self):
        return {
            **super(Sphere, self).data,
            **self.param
        }

    def DATASCHEMA():
        return schema.Schema({
            'type': 'Sphere',
            'radius': schema.And(schema.Or(float, int), lambda x: x > 0)
        }, ignore_extra_keys=True)

    @property
    def validate(self):
        return {
            **super(Sphere, self).validate(),
            **Sphere.DATASCHEMA().validate(self.data)
        }

    @staticmethod
    def is_valid(obj):
        return BaseGeometry.DATASCHEMA().is_valid(obj) & Sphere.DATASCHEMA().is_valid(obj)