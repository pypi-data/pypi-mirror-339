from archijson.geometry.base import BasePoint, BaseGeometry
from archijson.geometry.shape import Cuboid, Cylinder, Plane, Circle, Sphere
from archijson.geometry.mesh import Vertices, Segments, Faces, Mesh, Prism

call = {
    'Cuboid': Cuboid,
    'Cylinder': Cylinder,
    'Plane': Plane,
    'Sphere': Sphere,
    'Circle': Circle,
    'Vertices': Vertices,
    'Segments': Segments,
    'Faces': Faces,
    'Mesh': Mesh,
    'Prism': Prism,
}

