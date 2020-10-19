from gl import Raytracer, color
from obj import Obj, Texture, Envmap
from sphere import *
import random



brick = Material(diffuse = color(0.8, 0.25, 0.25 ), spec = 16)
stone = Material(diffuse = color(0.4, 0.4, 0.4 ), spec = 32)
mirror = Material(spec = 64, matType = 1)
glass = Material(spec = 64, ior = 1.5, matType= 2) 

boxMat = Material(texture = Texture('mwood.bmp'))
lava = Material(texture = Texture('lava.bmp'))
earthMat = Material(texture = Texture('energy.bmp'))
wall =Material(texture = Texture('mbrick.bmp'))

#size
width = 112
height = 112
r = Raytracer(width,height)
r.glClearColor(0.2, 0.6, 0.8)
r.glClear()

#env map
r.envmap = Envmap('animenv.bmp')

#spheres
print("trabajando en esferas")
r.scene.append(Sphere([-1.01, 0.047, -4.552], 0.4, earthMat))
r.scene.append(Sphere([1.01, 0.047, -4.552], 0.4, lava))
r.scene.append(Sphere([0.01, 1.01, -5.552], 0.4, glass))
r.scene.append(Sphere([0.01, 0.01, -3.552], 0.4, glass))

# Lights
print("trabajando en luces")
r.dirLight = DirectionalLight(direction = (1, -1, -2), intensity = 0.5)
r.pointLights.append(PointLight(intensity=0.1, position=(0, 2.5, 0)))
r.ambientLight = AmbientLight(strength = 0.1)

# Objects
print("trabajando en cajas")
r.scene.append( AABB((0.01, -1.59, -6.04), [6, 0.2, 6] , boxMat ) )
r.scene.append( AABB((3.38, 1.01, -6.12), [0.1, 6.86, 6.86] , wall ) )
r.scene.append( AABB((-3.38, 1.01, -6.12), [0.1, 6.86, 6.86] , wall ) )
r.scene.append( AABB((0.35, 0.01, -6.00), [0.3, 0.3, 0.3], stone))
r.scene.append( AABB((-0.35, 0.01, -6.00), [0.3, 0.3, 0.3], brick))
r.scene.append( AABB([0.01, 3.6, -5.98], [6.86, 0.2, 6.86] , mirror ) )



r.rtRender()

r.glFinish('output.bmp')





