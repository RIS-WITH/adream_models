import os
import unreal
import yaml

path_base = "/home/nclerc/Documents/FBX"
path_mesh = '/Game/adream/models/meshes'
path_level = '/Game/adream/maps/'

def createWorld() :
	
	unreal.EditorLevelLibrary.new_level(path_level + "Adream")
	unreal.EditorLevelLibrary.load_level(path_level + "Adream")
	world = unreal.EditorLevelLibrary.get_editor_world()
	sub_level_of_world = unreal.EditorLevelUtils.get_levels(world)
	light=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.SkyLight,(0,0,1000),(0,0,0))
	component=unreal.SkyLight()
	hemishphere_color=unreal.LinearColor(1,1,1,1)	
	light.light_component.set_editor_property('lower_hemisphere_color', hemishphere_color)
	light.light_component.set_editor_property('intensity', 10)
	createLevel(sub_level_of_world)

def createLevel(sub_level_of_world) :	
	with open('/home/nclerc/Documents/export1.yaml', 'r') as file :
		yaml_file = yaml.safe_load(file)
	for level_name in yaml_file :
		if str(sub_level_of_world).find(path_level + level_name) != -1 :
			unreal.EditorLevelLibrary.set_current_level_by_name(level_name)
		else :
			streaming_level=unreal.EditorLevelUtils.create_new_streaming_level(unreal.LevelStreamingDynamic , new_level_path = path_level + level_name)
			streaming_level.set_editor_property('initially_loaded',True)
			streaming_level.set_editor_property('initially_visible',True)
		createActors(yaml_file[level_name] , '' , level_name , '')
		unreal.EditorLevelLibrary.save_all_dirty_levels()

def createActors(dic_actor , path_actor_level , actual_dic , path_to_mesh) :
	if 'mesh' in dic_actor :
		if actual_dic == "appartement":
			actor = unreal.EditorLevelLibrary.spawn_actor_from_object(unreal.EditorAssetLibrary.load_asset(path_mesh + path_to_mesh + '/' + dic_actor['mesh'] +'.'+dic_actor['mesh']) 
			, (dic_actor['x'],dic_actor['y'],dic_actor['z']), (dic_actor['ry'],dic_actor['rz'],dic_actor['rx']))
			actor.set_folder_path('/ground_floor/appartement/appartement_vide')
			actor.set_actor_label(actual_dic)
		else:
			actor = unreal.EditorLevelLibrary.spawn_actor_from_object(unreal.EditorAssetLibrary.load_asset(path_mesh + path_to_mesh + '/' + dic_actor['mesh'] +'.'+dic_actor['mesh']) 
			, (dic_actor['x']*100,dic_actor['y']*(-100),dic_actor['z']*100), (dic_actor['ry'],dic_actor['rz'],dic_actor['rx']))
			actor.set_folder_path(path_actor_level)
			actor.set_actor_label(actual_dic)	
			if actual_dic== 'IKEAShelf_mesh_002':
				unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PlayerStart,(520,-670,180),(0,0,0))
		
			
	else :
		for sub_dic in dic_actor :
			if actual_dic == 'appartement' :
				createActors(dic_actor[sub_dic] , "/ground_floor/" + actual_dic + "/appartement_plein", sub_dic , path_to_mesh + "/" + actual_dic)
			elif ('furnitures' in path_actor_level and ('ground_floor' in actual_dic)) :
				createActors(dic_actor[sub_dic] , '/ground_floor' + path_actor_level , sub_dic , path_to_mesh)
			elif ('furnitures' in path_actor_level and ('first_floor' in actual_dic)) :
				createActors(dic_actor[sub_dic] , '/first_floor' + path_actor_level , sub_dic , path_to_mesh)
			else :
				createActors(dic_actor[sub_dic] , path_actor_level + "/" + actual_dic , sub_dic , path_to_mesh + "/" + actual_dic)



if __name__=="__main__":
	createWorld()

