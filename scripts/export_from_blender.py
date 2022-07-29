import bpy
import yaml
import os
import copy
#### Argument 
mesh_root_path = "/home/nclerc/Documents/"
root = bpy.data.scenes["Scene"].collection
root_visible = bpy.context.view_layer.layer_collection
#### script
 
extensions_types = {"OBJ" , "STL" , "FBX"}

def createFolderForExtensions(path_before , path_after):
    for extension in extensions_types:
        if not os.path.exists(path_before + extension + path_after):
            os.makedirs(path_before + extension + path_after)
    
def exportOneObject(obj, export_path_before , export_path_after):
    obj.select_set(True)
    for obj_child in obj.children:
        obj_child.select_set(True)
    if obj.animation_data :
        bpy.ops.object.duplicate()
        bpy.ops.anim.keyframe_clear_v3d()
    bpy.ops.export_mesh.stl(filepath = export_path_before + "STL" + export_path_after + obj.name + ".stl" ,  check_existing=False, 
    use_selection = True , axis_forward = 'X' , axis_up = 'Z')
    bpy.ops.export_scene.obj(filepath = export_path_before + "OBJ" + export_path_after + obj.name + ".obj" ,  check_existing=False, 
    use_selection = True , axis_forward = 'X' , axis_up = 'Z')
    bpy.ops.export_scene.fbx(filepath = export_path_before + "FBX" + export_path_after + obj.name + ".fbx" ,  check_existing=False, 
    use_selection = True , mesh_smooth_type = 'FACE' , axis_forward = 'X' , axis_up = 'Z' , bake_anim=False)
    if obj.animation_data :
        bpy.ops.object.delete()
    obj.select_set(False)
    for obj_child in obj.children:
        obj_child.select_set(False)

def exportOneObjectDoor(obj , export_path_before , export_path_after):
    obj.select_set(True)
    if obj.animation_data :
        bpy.ops.object.duplicate()
        bpy.ops.anim.keyframe_clear_v3d()
    bpy.ops.export_mesh.stl(filepath = export_path_before + "STL" + export_path_after + obj.name + ".stl" ,  check_existing=False, 
    use_selection = True , axis_forward = 'X' , axis_up = 'Z')
    bpy.ops.export_scene.obj(filepath = export_path_before + "OBJ" + export_path_after + obj.name + ".obj" ,  check_existing=False, 
    use_selection = True , axis_forward = 'X' , axis_up = 'Z')
    bpy.ops.export_scene.fbx(filepath = export_path_before + "FBX" + export_path_after + obj.name + ".fbx" ,  check_existing=False, 
    use_selection = True , mesh_smooth_type = 'FACE' , axis_forward = 'X' , axis_up = 'Z' , bake_anim=False)
    if obj.animation_data :
        bpy.ops.object.delete()
    obj.select_set(False)
    
def createNewObjectNode(obj , mesh = ''):
    node = {'x' : 0 if mesh == '' else obj.location.x ,
            'y' : 0 if mesh == '' else obj.location.y ,
            'z' : 0 if mesh == '' else obj.location.z ,
            'rx' : 0 if mesh == '' else obj.rotation_euler.x ,
            'ry' : 0 if mesh == '' else obj.rotation_euler.y ,
            'rz' : 0 if mesh == '' else obj.rotation_euler.z ,
            'mesh' : obj.name.replace('.' , "_") if mesh == '' else mesh.replace('.' , "_")}
    name = obj.name
    name = name.replace('.',"_")
    return (node , name)

def createNewDoorNode(obj , l_door , lock , handle , frame , wrist ):
    rnode={'x' : obj.location.x ,
            'y' : obj.location.y ,
            'z' : obj.location.z ,
            'rx' : obj.rotation_euler.x ,
            'ry' : obj.rotation_euler.y ,
            'rz' : obj.rotation_euler.z ,
            'mesh' : obj.name.split('.', 1)[0]}
    lnode={'x' : 0 if l_door == '' else l_door.location.x ,
            'y' : 0 if l_door == '' else l_door.location.y ,
            'z' : 0 if l_door == '' else l_door.location.z ,
            'rx' :0 if l_door == '' else  l_door.rotation_euler.x ,
            'ry' :0 if l_door == '' else  l_door.rotation_euler.y ,
            'rz' :0 if l_door == '' else  l_door.rotation_euler.z ,
            'mesh' : 0 if l_door == '' else l_door.name.split('.', 1)[0]} 
    locknode={'x' : 0 if lock == '' else lock.location.x ,
            'y' : 0 if lock == '' else lock.location.y ,
            'z' : 0 if lock == '' else lock.location.z ,
            'rx' : 0 if lock == '' else lock.rotation_euler.x ,
            'ry' :0 if lock == '' else  lock.rotation_euler.y ,
            'rz' :0 if lock == '' else  lock.rotation_euler.z ,
            'mesh' :0 if lock == '' else  lock.name.split('.', 1)[0]}
    wristnode={'x' : 0 if wrist == '' else wrist.location.x ,
            'y' : 0 if wrist == '' else wrist.location.y ,
            'z' : 0 if wrist == '' else wrist.location.z ,
            'rx' : 0 if wrist == '' else wrist.rotation_euler.x ,
            'ry' :0 if wrist == '' else  wrist.rotation_euler.y ,
            'rz' :0 if wrist == '' else  wrist.rotation_euler.z ,
            'mesh' :0 if wrist == '' else  wrist.name.split('.', 1)[0]}
    handlenode={'x' :0 if handle == '' else handle.location.x ,
            'y' : 0 if handle == '' else handle.location.y ,
            'z' : 0 if handle == '' else handle.location.z ,
            'rx' : 0 if handle == '' else handle.rotation_euler.x ,
            'ry' : 0 if handle == '' else handle.rotation_euler.y ,
            'rz' : 0 if handle == '' else handle.rotation_euler.z ,
            'mesh' : 0 if handle == '' else handle.name.split('.', 1)[0]}
    framenode={'x' : 0 if frame == '' else frame.location.x ,
            'y' : 0 if frame == '' else frame.location.y ,
            'z' : 0 if frame == '' else frame.location.z ,
            'rx' : 0 if frame == '' else frame.rotation_euler.x ,
            'ry' : 0 if frame == '' else frame.rotation_euler.y ,
            'rz' :0 if frame == '' else  frame.rotation_euler.z ,
            'mesh' : 0 if frame == '' else frame.name.split('.', 1)[0]}

    node = {'right_door' : rnode}
    if(l_door != '') :
        node['left_door'] = lnode
    if(handle != ''):
        node['handle'] = handlenode
    if(lock != '') :
        node['lock'] = locknode
    if(frame != ''):
        node['frame'] = framenode
    if(wrist != ''):
        node['wrist'] = wristnode
    name = obj.name
    name = name.replace('.',"_")
    return(node , name)


def createNewLightNode(obj):
    node = {'x' : obj.location.x ,
            'y' : obj.location.y ,
            'z' : obj.location.z ,
            'rx' : obj.rotation_euler.x ,
            'ry' : obj.rotation_euler.y ,
            'rz' : obj.rotation_euler.z ,
            'scale x' : obj.scale.x ,
            'scale y' : obj.scale.y ,
            'scale z' : obj.scale.z ,
            'type' : obj.data.type ,
            'power' : obj.data.node_tree.nodes["Emission"].inputs["Strength"].default_value ,
            'mesh' : obj.name.replace('.',"_")}
    name = obj.name
    name = name.replace('.',"_")
    return (node , name)

def createNewFurnituresNode(obj , mesh):
    node = {'x' : obj.location.x ,
            'y' : obj.location.y ,
            'z' : obj.location.z ,
            'rx' : obj.rotation_euler.x ,
            'ry' : obj.rotation_euler.y ,
            'rz' : obj.rotation_euler.z ,
            'scale x' : obj.dimensions.x / (bpy.data.objects[mesh].dimensions.x) ,
            'scale y' : obj.dimensions.y / (bpy.data.objects[mesh].dimensions.y) ,
            'scale z' : obj.dimensions.z / (bpy.data.objects[mesh].dimensions.z) ,
            'mesh' : mesh.replace('.',"_")}
    name = obj.name
    name = name.replace('.',"_")
    return (node , name)
  
def createYamlList(collection_dict):
    yaml_string = yaml.dump(collection_dict)
    with open(mesh_root_path+"export1.yaml" , 'w') as outfile :
        outfile.write(yaml_string)

def exportObjects():
    createFolderForExtensions(mesh_root_path , "/")
    collection_dict = {}
    collection_dict["objects"] = {} 
    for obj in root.objects:
        exportOneObject(obj , mesh_root_path , "/")
        obj_node , obj_name = createNewObjectNode(obj)
        collection_dict["objects"][obj_name] = obj_node
        
    for child in root.children:
        collection_dict[child.name] = {}
        exportObjectsInCollection(child , "/" , collection_dict[child.name] , root_visible.children)
    createYamlList(collection_dict)


    
def exportObjectsInCollection(collection , collection_path,objects_dict , visible):
    local_collection_path = collection_path + collection.name + "/"
    createFolderForExtensions(mesh_root_path , local_collection_path)
    if visible[collection.name].is_visible :
        if collection.name == "furnitures" or collection.name == "grapable" :
            for child in collection.children:
                objects_dict[child.name] = {}
                exportObjectsInFurnitures(child , local_collection_path , objects_dict[child.name] , visible[collection.name].children)
        else:
            for obj in collection.objects:
               
                if 'door' in collection.name:
                    if not '.' in obj.name:
                        createFolderForExtensions(mesh_root_path, '/furnitures/')
                        createFolderForExtensions(mesh_root_path, '/furnitures/door/')
                        exportFromOriginDoor(obj , mesh_root_path , '/furnitures/door/')
                    if not obj.parent :
                        l_door = ''
                        lock = ''
                        handle = ''
                        frame = ''
                        wrist = ''
                        for sub_mesh in obj.children :
                            if 'half' in sub_mesh.name or 'left' in sub_mesh.name:
                                l_door = sub_mesh
                            elif 'wrist' in sub_mesh.name :
                                wrist = sub_mesh
                            elif 'lock' in sub_mesh.name:
                                lock = sub_mesh
                            elif 'handle' in sub_mesh.name :
                                handle = sub_mesh
                            elif 'frame' in sub_mesh.name:
                                frame = sub_mesh
                        obj_node , obj_name = createNewDoorNode(obj , l_door , lock , handle , frame , wrist)
                        objects_dict[obj_name] = obj_node
                elif not obj.parent :
                    if collection.name == 'env':
                        obj_node, obj_name = createNewLightNode(obj)
                    elif collection.name == 'appartement' or collection.name == 'elevator':
                        exportFromOrigin(obj , mesh_root_path , local_collection_path)  
                        obj_node , obj_name = createNewObjectNode(obj,obj.name)
                    else :
                        exportOneObject(obj , mesh_root_path , local_collection_path)  
                        obj_node , obj_name = createNewObjectNode(obj)

                    objects_dict[obj_name] = obj_node
            for child in collection.children:
                objects_dict[child.name] = {}
                exportObjectsInCollection(child , local_collection_path , objects_dict[child.name] , visible[collection.name].children)

def exportFromOrigin(obj , mesh_root_path , collection_path):
    x = obj.location.x
    y = obj.location.y
    z = obj.location.z
    rx = obj.rotation_euler.x
    ry = obj.rotation_euler.y
    rz = obj.rotation_euler.z
    obj.location.x = 0
    obj.location.y = 0
    obj.location.z = 0
    obj.rotation_euler.x = 0 
    obj.rotation_euler.y = 0
    obj.rotation_euler.z = 0
    exportOneObject(obj , mesh_root_path , collection_path)
    obj.location.x = x
    obj.location.y = y
    obj.location.z = z
    obj.rotation_euler.x = rx
    obj.rotation_euler.y = ry
    obj.rotation_euler.z = rz


def exportFromOriginDoor(obj , mesh_root_path , collection_path):
    obj_tmp = obj
    if obj.parent and not 'handle' in obj.name:
        obj_tmp = obj.parent
        dad = obj.parent
        x = dad.location.x
        y = dad.location.y
        z = dad.location.z
        rx = dad.rotation_euler.x
        ry = dad.rotation_euler.y
        rz = dad.rotation_euler.z
        dad.location.x = 0
        dad.location.y = 0
        dad.location.z = 0
        dad.rotation_euler.x = 0 
        dad.rotation_euler.y = 0
        dad.rotation_euler.z = 0
        exportOneObjectDoor(obj , mesh_root_path , collection_path)
        dad.location.x = x
        dad.location.y = y
        dad.location.z = z
        dad.rotation_euler.x = rx
        dad.rotation_euler.y = ry
        dad.rotation_euler.z = rz
    else :
        x = obj.location.x
        y = obj.location.y
        z = obj.location.z
        rx = obj.rotation_euler.x
        ry = obj.rotation_euler.y
        rz = obj.rotation_euler.z
        obj.location.x = 0
        obj.location.y = 0
        obj.location.z = 0
        obj.rotation_euler.x = 0 
        obj.rotation_euler.y = 0
        obj.rotation_euler.z = 0
        exportOneObjectDoor(obj , mesh_root_path , collection_path)
        obj.location.x = x
        obj.location.y = y
        obj.location.z = z
        obj.rotation_euler.x = rx
        obj.rotation_euler.y = ry
        obj.rotation_euler.z = rz

def exportObjectsInFurnitures(collection , collection_path , objects_dict,visible):
    local_collection_path = collection_path + collection.name + "/"
    createFolderForExtensions(mesh_root_path , local_collection_path)
    if visible[collection.name].is_visible:
        for obj in collection.objects:
            if not obj.parent :
                if not "." in obj.name:
                    exportFromOrigin(obj, mesh_root_path , collection_path)
                obj_node, obj_name = createNewFurnituresNode(obj, obj.name.split('.', 1)[0])  
                objects_dict[obj_name] = obj_node
        for child in collection.children:
            objects_dict[child.name] = {}
            exportObjectsInFurnitures(child , local_collection_path, objects_dict[child.name] , visible[collection.name].children)


if __name__=="__main__":
    for ob in bpy.context.selected_objects:
        ob.select_set(False)
    exportObjects()
    print('export end well')