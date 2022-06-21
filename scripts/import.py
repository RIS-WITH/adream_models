import os
import unreal
import yaml
import math

path_base = "/home/nclerc/Documents/FBX"
path_mesh = '/Game/adream/models/meshes'
path_level = '/Game/adream/maps/'

def createWorld() :
	unreal.EditorLevelLibrary.new_level(path_level + "Adream")
	unreal.EditorLevelLibrary.load_level(path_level + "Adream")
	world = unreal.EditorLevelLibrary.get_editor_world()
	sub_level_of_world = unreal.EditorLevelUtils.get_levels(world)
	actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.EditorAssetLibrary.load_blueprint_class('/Game/Hdri_world') , (0 , 0 , -50) , (0 , 0 , 0))								
	createLevel(sub_level_of_world)

def createLevel(sub_level_of_world) :	
	with open('/home/nclerc/Documents/export1.yaml', 'r') as file :
		yaml_file = yaml.safe_load(file)
	for level_name in yaml_file :
		if str(sub_level_of_world).find(path_level + level_name) != -1 :
			unreal.EditorLevelLibrary.set_current_level_by_name(level_name)
		else :
			streaming_level=unreal.EditorLevelUtils.create_new_streaming_level(unreal.LevelStreamingDynamic , new_level_path = path_level + level_name)
			streaming_level.set_editor_property('initially_loaded' , True)
			streaming_level.set_editor_property('initially_visible' , True)
		createActors(yaml_file[level_name] , '' , level_name , '')
		unreal.EditorLevelLibrary.save_all_dirty_levels()

def createActors(dic_actor , path_actor_level , actual_dic , path_to_mesh) :
	if 'mesh' in dic_actor :
		if actual_dic == "appartement":
			actor = unreal.EditorLevelLibrary.spawn_actor_from_object(unreal.EditorAssetLibrary.load_asset(path_mesh + path_to_mesh + '/' + dic_actor['mesh'] + '.' + dic_actor['mesh']) 
			, (dic_actor['x']*100 , dic_actor['y']*(-100) , dic_actor['z']*100) , (dic_actor['ry']*(-180/math.pi) , dic_actor['rz']*(-180/math.pi) , dic_actor['rx']*(-180/math.pi)))
			actor.set_folder_path('/ground_floor/appartement/appartement_vide')
			actor.set_actor_label(actual_dic)
		elif "env" in path_actor_level:
			if dic_actor['type']=='AREA':
				rectlight=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.RectLight , (dic_actor['x']*100 , dic_actor['y']*(-100)
				, dic_actor['z']*100) , (-90 ,dic_actor['rz']*(-180/math.pi) , dic_actor['rx']*(-180/math.pi)))
				rectlight.root_component.set_editor_property('mobility' , unreal.ComponentMobility.STATIC)
				rectlight.root_component.set_editor_property('intensity' , dic_actor['power'])
				rectlight.set_folder_path(path_actor_level)
				rectlight.set_actor_label(actual_dic)
			elif dic_actor['type']=='POINT':
				pointlight=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PointLight,(dic_actor['x']*100 , dic_actor['y']*(-100),dic_actor['z']*100)
				,(dic_actor['ry']*(-180/math.pi) , dic_actor['rz']*(-180/math.pi) , dic_actor['rx']*(-180/math.pi)))
				pointlight.root_component.set_editor_property('mobility' , unreal.ComponentMobility.STATIC)
				pointlight.root_component.set_editor_property('intensity' , dic_actor['power'])
				pointlight.set_folder_path(path_actor_level)
				pointlight.set_actor_label(path_actor_level)
		elif "furnitures" in path_actor_level:
			actor = unreal.EditorLevelLibrary.spawn_actor_from_object(unreal.EditorAssetLibrary.load_asset(path_mesh + path_to_mesh + '/' + dic_actor['mesh'] + '.' + dic_actor['mesh']) 
			, (dic_actor['x']*100 , dic_actor['y']*(-100) , dic_actor['z']*100) , (dic_actor['ry']*(-180/math.pi) , dic_actor['rz']*(-180/math.pi) , dic_actor['rx']*(-180/math.pi) ))
			print(path_actor_level)
			print('____________________')
			print(actual_dic)
			print('_____________')
			actor.set_folder_path(path_actor_level)
			actor.set_actor_label(actual_dic)
			actor.root_component.set_editor_property('relative_scale3d' , (dic_actor['scale x'] , dic_actor['scale y'] , dic_actor['scale z']))
		else:
			actor = unreal.EditorLevelLibrary.spawn_actor_from_object(unreal.EditorAssetLibrary.load_asset(path_mesh + path_to_mesh + '/' + dic_actor['mesh'] + '.' + dic_actor['mesh']) 
			, (dic_actor['x']*100 , dic_actor['y']*(-100) , dic_actor['z']*100) , (dic_actor['ry']*(-180/math.pi) , dic_actor['rz']*(-180/math.pi) , dic_actor['rx']*(-180/math.pi) ))
			print(path_actor_level)
			print('____________________')
			print(actual_dic)
			print('_____________')
			actor.set_folder_path(path_actor_level)
			actor.set_actor_label(actual_dic)	


	elif 'right_door' in dic_actor :
		actor=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.EditorAssetLibrary.load_blueprint_class('/Game/adream/blueprint/DoubleDoorOpenBP_Skylight.DoubleDoorOpenBP_Skylight') , 
		(dic_actor['right_door']['x']*100 , dic_actor['right_door']['y']*(-100) , dic_actor['right_door']['z']*100) , (dic_actor['right_door']['ry']*(-180/math.pi) , dic_actor['right_door']['rz']*(-180/math.pi) , dic_actor['right_door']['rx']*(-180/math.pi) ))								
		actor.set_folder_path(path_actor_level)
		actor.set_actor_label(actual_dic)
		list = []
		i=0
		while i == 0:
			i=1
			all_actors = unreal.EditorLevelLibrary.get_all_level_actors_components()
			for blueprint_component in all_actors:
				if actual_dic in str(blueprint_component) and actual_dic+'_' not in str(blueprint_component) and 'StaticMesh' in str(blueprint_component) :
					print(blueprint_component)
					print(actual_dic)
					print(str(blueprint_component).split('PersistentLevel.')[1])
					check_list=str(blueprint_component).split('PersistentLevel.'+actual_dic+'.')[1]
					print(check_list)
					check_list=str(check_list).split("'")[0]
					print(check_list)
					if check_list not in list :
						i=0
						element_list=str(blueprint_component).split('PersistentLevel.'+actual_dic+'.')[1]
						element_list=str(element_list).split("'")[0]
						list.append(element_list)
						if 'Handle' in str(blueprint_component) and 'handle' in dic_actor:
						
							blueprint_component.set_editor_property("static_mesh",unreal.EditorAssetLibrary.load_asset("/Game/adream/models/meshes/furnitures/door/"+dic_actor['handle']['mesh']))			
						elif 'Lock' in str(blueprint_component) and 'lock' in dic_actor:
						
							blueprint_component.set_editor_property("static_mesh",unreal.EditorAssetLibrary.load_asset("/Game/adream/models/meshes/furnitures/door/"+dic_actor['lock']['mesh']))
						elif 'door_left' in str(blueprint_component) and 'left_door' in dic_actor:
						
							blueprint_component.set_editor_property("static_mesh",unreal.EditorAssetLibrary.load_asset("/Game/adream/models/meshes/furnitures/door/"+dic_actor['left_door']['mesh']))
						elif 'door_right' in str(blueprint_component) and 'right_door' in dic_actor:
						
							blueprint_component.set_editor_property("static_mesh",unreal.EditorAssetLibrary.load_asset("/Game/adream/models/meshes/furnitures/door/"+dic_actor['right_door']['mesh']))
						elif 'Double' in str(blueprint_component) and 'frame' in dic_actor:
						
							blueprint_component.set_editor_property("static_mesh",unreal.EditorAssetLibrary.load_asset("/Game/adream/models/meshes/furnitures/door/"+dic_actor['frame']['mesh']))
			unreal.EditorLevelLibrary.save_all_dirty_levels()
			
			


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

