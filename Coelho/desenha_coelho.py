from OpenGL.GL import *
import math
def calculaNormal(face,verticeMAP):
    x = 0
    y = 1
    z = 2
    
    v0 = verticeMAP[face[x]]
    v1 = verticeMAP[face[y]]
    v2 = verticeMAP[face[z]]
    
    U = ( v2[x]-v0[x], v2[y]-v0[y], v2[z]-v0[z] )
    V = ( v1[x]-v0[x], v1[y]-v0[y], v1[z]-v0[z] )
    N = ( (U[y]*V[z]-U[z]*V[y]),(U[z]*V[x]-U[x]*V[z]),(U[x]*V[y]-U[y]*V[x]))
    
    NLength = math.sqrt(N[x]*N[x]+N[y]*N[y]+N[z]*N[z])

    return ( N[x]/NLength, N[y]/NLength, N[z]/NLength)
 
def MTL():
    contents = {}
    mtl = None
    for linha in open(filename, "r"):
        if linha.startswith('f'): continue
        if linha.startswith('c'): continue
        if linha.startswith('p'): continue
        if linha.startswith('e'): continue
        values = linha.split()
        if not values: continue
        if values[0] == 'ply':
            mtl = contents[values[1]] = {}
        elif mtl is None:
            print(values[0])
            raise ValueError, "Erro no formato do arquivo"
        else: 
            mtl[values[0]] = map(float, values[1:])
    return contents
 
class OBJ:
    def __init__(self, filename, swapyz=False):
        self.vertices = []
        self.normals = []
        self.normalCalculoArray = []
        self.faces = []
        self.norms = []
 
        material = None
        for linha in open(filename, "r"):
            if linha.startswith('#'): continue
            if linha.startswith('f'): continue
            if linha.startswith('c'): continue
            if linha.startswith('p'): continue
            if linha.startswith('e'): continue
            if linha.startswith('p'): continue       
            values = linha.split()
            if not values: continue
            if values[0] == '3':
                v = map(int, values[1:4])
                self.faces.append(v)
                self.normalCalculoArray.append(calculaNormal(v,self.vertices))
                
            else:
                v = map(float, values[0:3])
                self.vertices.append(v)        
            
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glFrontFace(GL_CCW)

        for i in range(len(self.faces)):
            vertices = self.faces[i]
 
            glBegin(GL_POLYGON)
            
            for k in range(len(vertices)):
                norm = self.normalCalculoArray[i]
                glVertex3fv(self.vertices[int(vertices[k])])  
                glNormal3fv(norm)                
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()