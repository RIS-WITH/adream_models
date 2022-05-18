import bpy
import yaml
import os
#### Argument 


obj = bpy.context.object
delta = 0.1 # marge pour prendre en compte les objets 

path = "/home/nclerc/Documents/blenderpy/"
root = bpy.data.scenes["Scene"].collection
 #### script

dict_collections = {}
dict_objects = {}







#def overObjectRef(objectRef,object):
 #   centerObjectRef = objectRef.location
  #  dimObjectRef = objectRef.dimensions
   # xminObjectRef = centerObjectRef.x - dimObjectRef.x/2 - delta
    #xmaxObjectRef = centerObjectRef.x + dimObjectRef.x/2 + delta
#    yminObjectRef = centerObjectRef.y - dimObjectRef.y/2 - delta
 #   ymaxObjectRef = centerObjectRef.y + dimObjectRef.y/2 + delta
  #  zminObjectRef = centerObjectRef.z + dimObjectRef.z/2 - delta
   # zmaxObjectRef = centerObjectRef.z + dimObjectRef.z/2 + delta
    
 #   centerObject = object.location
  #  dimObject = object.dimensions
   # xminObject = centerObject.x - dimObject.x/2 
#    xmaxObject = centerObject.x + dimObject.x/2 
 #   yminObject = centerObject.y - dimObject.y/2 
  #  ymaxObject = centerObject.y + dimObject.y/2 
   # zminObject = centerObject.z + dimObject.z/2 
    #zmaxObject = centerObject.z + dimObject.z/2 
    
#    if(xminObjectRef<xminObject and xmaxObject<xmaxObjectRef):
        # print('x ok')
 #       if(yminObjectRef<yminObject and ymaxObject<ymaxObjectRef):
            # print('y ok')
  #          if(zminObject > zminObjectRef):
                # print('z ok')
   #             return True
    
    #return False



#def extractObjectCollectionsOverRef(object_ref):
 #   extracted_objects = []
  #  for object_ref in bpy.context.object:
   #         extracted_objects.append(obj)
    #return extracted_objects

def createYaml(liste_obj):
    dict  =  {}
    for obj in liste_obj:
        c = {'x' : obj.location.x, 'y' : obj.location.y , 'z' : obj.location.z , 'rotation' : obj.rotation_euler.z }
        name = obj.name
        name = name.replace('.',"_")
        print(type(name))
        print(name)
        dict[name] = c
    print(dict)
#    print(json_string)
#    print(yaml.dump(dict))
    yaml_string = yaml.dump(dict)
    with open(path+"export1.yaml",'w') as outfile :
        outfile.write(yaml_string)
        
        

def treeFBX(list_c,path2,ext):
    for c in list_c:
        for o in c.objects:
            o.select_set(True)
            o.select_set(False)
            print(o.name)#export l'obj bpy.ops.export_scene.fbx()
            print(path2+c.name+"/"+ext)#lieu
        if not os.path.exists(path2+c.name):    
            os.makedirs(path2+c.name)
        treeFBX(c.children,path2+c.name+"/",ext)
        
def initTreeFBX(list_c,path2,listO):
    if not os.path.exists(path2+"FBX/"):
        os.makedirs(path2+"FBX/")
    for o in bpy.data.scenes["Scene"].collection.objects:
            o.select_set(True)
            o.select_set(False)
            print(o.name)#export l'object bpy.ops.export_scene.fbx()
            print(path)#lieu
    treeFBX(list_c,path2+"FBX/","fbx")

def treeSTL(list_c,path2,ext):
    for c in list_c:
        for o in c.objects:
            o.select_set(True)
            o.select_set(False)
            print(o.name)#export l'obj bpy.ops.export_mesh.stl()
            print(path2+c.name+"/"+ext)#lieu
        if not os.path.exists(path2+c.name):  
                os.makedirs(path2+c.name)
        treeSTL(c.children,path2+c.name+"/",ext)
        
def initTreeSTL(list_c,path2,listO):
    if not os.path.exists(path2+"STL/"):
        os.makedirs(path2+"STL/")
    for o in bpy.data.scenes["Scene"].collection.objects:
            o.select_set(True)
            o.select_set(False)
            print(o.name)#export l'object bpy.ops.export_mesh.stl()
            print(path)#lieu
    treeSTL(list_c,path2+"STL/","stl")
    
def treeOBJ(list_c,path2,ext):
    for c in list_c:
        for o in c.objects:
            o.select_set(True)
            o.select_set(False)
            print(o.name)#export l'obj bpy.ops.export_scene.obj()
            print(path2+c.name+"/"+ext)#lieu
        if not os.path.exists(path2+c.name):  
            os.makedirs(path2+c.name)
        treeOBJ(c.children,path2+c.name+"/",ext)
        
def initTreeOBJ(list_c,path2,listO):
    if not os.path.exists(path2+"OBJ/"):
        os.makedirs(path2+"OBJ/")
    for o in bpy.data.scenes["Scene"].collection.objects:
            o.select_set(True)
            o.select_set(False)
            print(o.name)#export l'object bpy.ops.export_scene.obj()
            print(path)#lieu
    treeOBJ(list_c,path2+"OBJ/","obj")




if __name__=="__main__":
    for collection in bpy.data.collections:
         print(collection.name)
    print(os.getcwd())
    obj = bpy.context.selected_objects
    createYaml(obj)
    #initialisation
    initTreeFBX(root.children,path,root.objects) 
    initTreeSTL(root.children,path,root.objects)
    initTreeOBJ(root.children,path,root.objects)
    
    """for o in bpy.data.scenes["Scene"].collection.objects:
            print(o.name)#export l'object
            print(path)#lieu
    arborescence(bpy.data.scenes["Scene"].collection.children,path+"fbx/","fbx")"""

    
    """    
    for collection in bpy.data.collections:
        dictCollections[collection.name] = collection
        for obj in collection.all_objects:
            dictObjects[obj.name] = obj
   #cubes = extractObjectCollectionsOverRef(refObject,dictCollections[argCollectionCube])
    #print(box)
    truc=extractObjectCollectionsOverRef(obj)

    createYaml(truc)
    """    
    

    

#Cubes = [cube for cube in dictCollections[argCollectionCube].all_objects]
#print(Cubes)
#CubeExtract = []
#for cube in Cubes:
#    if overObjectRef(refObject,cube):
#        CubeExtract.append(cube)

#print(CubeExtract)




    


#C1 = dictObjects["dt_cube_BBRG"]
#C2 = dictObjects["IKEA_RUTBO"]
#overObjectRef(refObject,C2)

#objects_in_collection = bpy.data.collections["My_Collection"].object
