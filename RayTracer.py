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

width = 512
height = 512
r = Raytracer(width,height)
r.glClearColor(0.2, 0.6, 0.8)
r.glClear()

r.envmap = Envmap('animenv.bmp')
r.scene.append(Sphere([-1.01, 0.047, -4.552], 0.5, earthMat))
r.scene.append(Sphere([1.01, 0.047, -4.552], 0.5, lava))
# Lights
#r.pointLights.append( PointLight(position = V3(-4,4,0), intensity = 0.5))

r.dirLight = DirectionalLight(direction = (1, -1, -2), intensity = 0.5)
r.ambientLight = AmbientLight(strength = 0.1)

# Objects
#r.scene.append( Sphere(V3( 0, 0, -8), 2, brick) )


r.scene.append( AABB([0.01, -1.59, -6.04], [6, 0.2, 6] , boxMat ) )
r.scene.append( AABB([3.38, 1.01, -6.12], [0.1, 6.86, 6.86] , wall ) )
r.scene.append( AABB([-3.38, 1.01, -6.12], [0.1, 6.86, 6.86] , wall ) )
r.scene.append( AABB([0, 3.55, -6.03], [7.2, 0.1, 7.2], mirror))
#r.scene.append( AABB([-5, -3, -10], [3, 0.2, 3] , mirror ) )

#r.scene.append( AABB(V3(1.5, 1.5, -5), V3(1, 1, 1) , boxMat ) )
#r.scene.append( Sphere([ 0, 0, -8], 2, earthMat))



r.rtRender()

r.glFinish('output.bmp')





