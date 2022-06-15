import bpy
import yaml
import os
import copy
#### Argument 
mesh_root_path = "/home/nclerc/Documents/"
root = bpy.data.scenes["Adream"].collection
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
    
def createNewObjectNode(obj , mesh = ''):
    node = {'x' : 0 if mesh == '' else obj.location.x ,
            'y' : 0 if mesh == '' else obj.location.y ,
            'z' : 0 if mesh == '' else obj.location.z ,
            'rx' : 0 if mesh == '' else obj.rotation_euler.x ,
            'ry' : 0 if mesh == '' else obj.rotation_euler.y ,
            'rz' : 0 if mesh == '' else obj.rotation_euler.z ,
            'mesh' : obj.name.replace('.',"_") if mesh == '' else mesh.replace('.',"_")}
    name = obj.name
    name = name.replace('.',"_")
    return (node, name)

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
            'scale x' : obj.dimensions.x - (bpy.data.objects[mesh].dimensions.x) ,
            'scale y' : obj.dimensions.y - (bpy.data.objects[mesh].dimensions.y) ,
            'scale z' : obj.dimensions.z - (bpy.data.objects[mesh].dimensions.z) ,
            'mesh' : obj.name.replace('.',"_")}
    name = obj.name
    name = name.replace('.',"_")
    return (node , name)
    
def createYamlList(collection_dict):
    yaml_string = yaml.dump(collection_dict)
    with open(mesh_root_path+"export1.yaml",'w') as outfile :
        outfile.write(yaml_string)

def exportObjects():
    createFolderForExtensions(mesh_root_path, "/")
    collection_dict = {}
    collection_dict["objects"] = {} 
    for obj in root.objects:
        exportOneObject(obj, mesh_root_path, "/")
        obj_node, obj_name = createNewObjectNode(obj)
        collection_dict["objects"][obj_name] = obj_node
        
    for child in root.children:
        collection_dict[child.name] = {}
        exportObjectsInCollection(child,"/",collection_dict[child.name],root_visible.children)
    createYamlList(collection_dict)


    
def exportObjectsInCollection(collection , collection_path,objects_dict , visible):
    local_collection_path = collection_path + collection.name + "/"
    createFolderForExtensions(mesh_root_path , local_collection_path)
    if visible[collection.name].is_visible :
        if collection.name == "furnitures" :
            for child in collection.children:
                objects_dict[child.name] = {}
                exportObjectsInFurnitures(child,local_collection_path,objects_dict[child.name],visible[collection.name].children)
        else:
            for obj in collection.objects:
                if not obj.parent :
                    if collection.name == 'env':
                        obj_node, obj_name = createNewLightNode(obj)
                    elif collection.name == 'appartement':
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
