from gl import color 
import ops as op
from numpy import arccos, arctan2

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2
PI = 3.14159265
WHITE = color(1,1,1)

class AmbientLight(object):
    def __init__(self, strength = 0, _color = WHITE):
        self.strength = strength
        self.color = _color

class DirectionalLight(object):
    def __init__(self, direction = (0,-1,0), _color = WHITE, intensity = 1):
        self.direction = op.divide(direction , op.norm(direction))
        self.intensity = intensity
        self.color = _color

class PointLight(object):
    def __init__(self, position = (0,0,0), _color = WHITE, intensity = 1):
        self.position = position
        self.intensity = intensity
        self.color = _color
class Material(object):
    def __init__(self, diffuse = WHITE, spec = 0, ior = 1, texture = None, matType = OPAQUE):
        self.diffuse = diffuse
        self.spec = spec

        self.matType = matType
        self.ior = ior

        self.texture = texture

class Intersect(object):
    def __init__(self, distance, point, normal, texCoords, sceneObject):
        self.distance = distance
        self.point = point
        self.normal = normal

        self.texCoords = texCoords

        self.sceneObject = sceneObject
#import numpy as gp
class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dir):
        L = op.subtract(self.center, orig)
        tca = op.dot(L, dir)
        l = op.norm(L) # magnitud de L
        d = (l**2 - tca**2) ** 0.5
        if d > self.radius:
            return None

        # thc es la distancia de P1 al punto perpendicular al centro
        thc = (self.radius ** 2 - d**2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc
        if t0 < 0:
            t0 = t1

        if t0 < 0: # t0 tiene el valor de t1
            return None

        # P = O + tD
        hit = op.add(orig, op.mtxmul(t0,  dir))
        norm = op.subtract( hit, self.center )
        norm = op.divide(norm , op.norm(norm))

        u = 1 - (arctan2( norm[2], norm[0]) / (2 * PI) + 0.5)
        v =  arccos(-norm[1]) / PI

        uvs = [u, v]


        return Intersect(distance = t0,
                         point = hit,
                         normal = norm,
                         texCoords = uvs,
                         sceneObject = self)

class Plane(object):
    def __init__(self, position, normal, material):
        self.position = position
        self.normal = op.divide(normal , op.norm(normal))
        self.material = material

    def ray_intersect(self, orig, dir):
        # t = (( position - origRayo) dot normal) / (dirRayo dot normal)

        denom = op.dot(dir, self.normal)

        if abs(denom) > 0.0001:
            t = op.dot(self.normal, op.subtract(self.position, orig)) / denom
            if t > 0:
                # P = O + tD
                hit = op.add(orig,op.mtxmul(t ,  dir))

                return Intersect(distance = t,
                                 point = hit,
                                 normal = self.normal,
                                 texCoords = None,
                                 sceneObject = self)

        return None

# Cubos
# AA Bounding Box: axis adjacent Bounding Box
class AABB(object):
    def __init__(self, position, size, material):
        self.position = position
        self.size = size
        self.material = material
        self.planes = []

        halfSizeX = size[0] / 2
        halfSizeY = size[1] / 2
        halfSizeZ = size[2] / 2


        self.planes.append( Plane( op.add(position, (halfSizeX,0,0)), (1,0,0), material))
        self.planes.append( Plane( op.add(position, (-halfSizeX,0,0)), (-1,0,0), material))

        self.planes.append( Plane( op.add(position, (0,halfSizeY,0)), (0,1,0), material))
        self.planes.append( Plane( op.add(position, (0,-halfSizeY,0)), (0,-1,0), material))

        self.planes.append( Plane( op.add(position, (0,0,halfSizeZ)), (0,0,1), material))
        self.planes.append( Plane( op.add(position, (0,0,-halfSizeZ)), (0,0,-1), material))


    def ray_intersect(self, orig, dir):

        epsilon = 0.001

        boundsMin = [0,0,0]
        boundsMax = [0,0,0]

        for i in range(3):
            boundsMin[i] = self.position[i] - (epsilon + self.size[i] / 2)
            boundsMax[i] = self.position[i] + (epsilon + self.size[i] / 2)

        t = float('inf')
        intersect = None

        uvs = None

        for plane in self.planes:
            planeInter = plane.ray_intersect(orig, dir)

            if planeInter is not None:

                # Si estoy dentro del bounding box
                if planeInter.point[0] >= boundsMin[0] and planeInter.point[0] <= boundsMax[0]:
                    if planeInter.point[1] >= boundsMin[1] and planeInter.point[1] <= boundsMax[1]:
                        if planeInter.point[2] >= boundsMin[2] and planeInter.point[2] <= boundsMax[2]:
                            if planeInter.distance < t:
                                t = planeInter.distance
                                intersect = planeInter

                                if abs(plane.normal[0]) > 0:
                                    # mapear uvs para eje x. Uso coordenadas en Y y Z.
                                    u = (planeInter.point [1] - boundsMin[1]) / (boundsMax[1] - boundsMin[1])
                                    v = (planeInter.point [2] - boundsMin[2]) / (boundsMax[2] - boundsMin[2])

                                elif abs(plane.normal[1]) > 0:
                                    # mapear uvs para eje y. Uso coordenadas en X y Z.
                                    u = (planeInter.point [0] - boundsMin[0]) / (boundsMax[0] - boundsMin[0])
                                    v = (planeInter.point [2] - boundsMin[2]) / (boundsMax[2] - boundsMin[2])

                                elif abs(plane.normal[2]) > 0:
                                    # mapear uvs para eje Z. Uso coordenadas en X y Y.
                                    u = (planeInter.point [0] - boundsMin[0]) / (boundsMax[0] - boundsMin[0])
                                    v = (planeInter.point [1] - boundsMin[1]) / (boundsMax[1] - boundsMin[1])

                                uvs = [u, v]

        if intersect is None:
            return None

        return Intersect(distance = intersect.distance,
                         point = intersect.point,
                         normal = intersect.normal,
                         texCoords = uvs,
                         sceneObject = self)