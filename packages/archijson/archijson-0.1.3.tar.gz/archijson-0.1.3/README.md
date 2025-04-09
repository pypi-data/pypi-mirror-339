ArchiJSON is a [JSON-based](https://www.json.org/json-en.html) protocol for exchanging architectural design data and parameters. 

The purpose of ArchiJSON is to design readable and compact data interaction formats to make data exchange between front and back ends easier. It integrates perfectly with [ArchiWeb](https://web.archialgo.com) and provides data visualization and manipulation.

This is the python implementation, providing a socket-io server and convert tool to [COMPAS](https://compas.dev) geometries.

### Installation
``` bash
pip install archijson
```

### Documentation
The documentation is intergrated with [ArchiWeb Docs](https://docs.web.archialgo.com). 
### Geometry Primitive
- shape
  - Cuboid
  - Plane
  - Cylinder
- mesh
  - Vertices
  - Segments
  - Faces
  - Mesh
### Usage
#### ArchiServer
For more help, check out the documentation.
``` py
from archijson import ArchiServer, ArchiJSON

server = ArchiServer(URL, TOKEN, IDENTITY)


def on_connect():
    print('exchanging')
    server.send('client', {'msg': 'hello'})


def on_receive(id, body):
    print(id)
    print(body)

    archijson = ArchiJSON(body)
    for geom in archijson.geometries:
        print(geom)


server.on_connect = on_connect
server.on_receive = on_receive
```
