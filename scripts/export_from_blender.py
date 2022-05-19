import bpy
import yaml
import os
import copy
#### Argument 


obj = bpy.context.object
#delta = 0.1 # marge pour prendre en compte les objets 

mesh_root_path = "/home/nclerc/Documents/"
root = bpy.data.scenes["Adream"].collection
 #### script

dict_collections = {}
dict_objects = {}

extensions_types = {"OBJ", "STL", "FBX"}







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

def createYamlList(liste_obj):
    dict  =  {}
    for obj in liste_obj:
        c = {'x' : obj.location.x, 'y' : obj.location.y , 'z' : obj.location.z ,'rx' : obj.rotation_euler.x,'ry' : obj.rotation_euler.y, 'rz' : obj.rotation_euler.z}
        name = obj.name
        name = name.replace('.',"_")
        print(type(name))
        print(name)
        dict[name] = c
    print(dict)
#    print(json_string)
#    print(yaml.dump(dict))
    yaml_string = yaml.dump(dict)
    with open(mesh_root_path+"export1.yaml",'w') as outfile :
        outfile.write(yaml_string)

def initTree(list_obj):
    for extension in extensions_types:
        if not os.path.exists(mesh_root_path + extension + "/"):
            os.makedirs(mesh_root_path + extension + "/")        
    for obj in root.objects:
            list_obj.append(obj)
            obj.select_set(True)
            obj.select_set(False)
            print(obj.name)#export object
            print(mesh_root_path+"OBJ/")#lieu
    tree(root.children,"/",list_obj)
    createYamlList(list_obj)

    
def tree(children,collection_path,list_obj):
    for child in children:
        local_collection_path = collection_path + child.name + "/"
        for extension in extensions_types:
            if not os.path.exists(mesh_root_path + extension + local_collection_path):
                os.makedirs(mesh_root_path + extension + local_collection_path)
        if child.name == "furnitures":
            treeFurnitures(child.children,local_collection_path,list_obj)
        else:
            for obj in child.objects:
                list_obj.append(obj)
                obj.select_set(True)
                obj.select_set(False)
                print(obj.name)#export obj bpy.ops.export_mesh.stl()
                print(mesh_root_path + extension + local_collection_path)#lieu
            tree(child.children,local_collection_path,list_obj)

def treeFurnitures(children,collection_path,list_obj):
    for child in children:
        local_collection_path = collection_path + child.name + "/"
        for extension in extensions_types:
            if not os.path.exists(mesh_root_path + extension + local_collection_path):
                os.makedirs(mesh_root_path + extension + local_collection_path)
        for obj in child.objects:
            if not "." in obj.name:
                list_obj.append(obj)
                obj.select_set(True)
                obj.select_set(False)
                print(obj.name)#export 
                print(mesh_root_path + extension + collection_path)#lieu    
        #if len(c.objects) != 0:   
        treeFurnitures(child.children,local_collection_path,list_obj)

if __name__=="__main__":
    for collection in bpy.data.collections:
         print(collection.name)
    print(os.getcwd())
    obj = bpy.context.selected_objects
    list_obj = []
    #createYamlList(obj)
    #initialisation
    initTree(list_obj)
    
    
#   """ initTreeFBX(root.children,path,root.objects) 
 #   initTreeSTL(root.children,path,root.objects)
  #  initTreeOBJ(root.children,path,root.objects)"""
    
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




    
#for ob in bpy.context.selected_objects:
 #   ob.select = False

#C1 = dictObjects["dt_cube_BBRG"]
#C2 = dictObjects["IKEA_RUTBO"]
#overObjectRef(refObject,C2)

#objects_in_collection = bpy.data.collections["My_Collection"].object
