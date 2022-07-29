import os
import unreal
import yaml
import math

scene_name = 'camstore'
yaml_path = 'D:/home/nclerc/Documents/export1.yaml'

path_blueprint = '/Game/experiments/' + scene_name + '/blueprints'
path_mesh = '/Game/experiments/' + scene_name + '/models/meshes'
path_level = '/Game/experiments/' + scene_name + '/maps/'
path_hdri = '/Game/experiments/' + scene_name + '/hdri/'

def createWorld() :
	unreal.EditorLevelLibrary.new_level(path_level + scene_name)
	unreal.EditorLevelLibrary.load_level(path_level + scene_name)
	world = unreal.EditorLevelLibrary.get_editor_world()
	sub_level_of_world = unreal.EditorLevelUtils.get_levels(world)
	actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PlayerStart,(20 , 20 , 20))
	actor = unreal.EditorLevelLibrary.spawn_actor_from_object(unreal.EditorAssetLibrary.load_asset(path_hdri + 'Hdri_world_' + scene_name) , (0 , 0 , -50) , (0 , 0 , 0))	
	actor = unreal.EditorLevelLibrary.spawn_actor_from_object(unreal.EditorAssetLibrary.load_asset('/Game/VRTemplate/Blueprints/FirstPersonCharacter.FirstPersonCharacter') , (20 , 20 , 110))		
	actor= unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.LightmassImportanceVolume,(-1001 , -1152 , 388))
	actor.set_actor_relative_scale3d((30 , 32 , 15))
	actor= unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.NavMeshBoundsVolume,(-1001 , -1152 , 388))
	actor.set_actor_relative_scale3d((30 , 32 , 15))
	actor= unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PostProcessVolume,(-1001 , -1152 , 388))
	actor.set_actor_relative_scale3d((30 , 32 , 15))
	createLevel(sub_level_of_world)

def createLevel(sub_level_of_world) :	
	with open(yaml_path , 'r') as file :	
		yaml_file = yaml.safe_load(file)
	for level_name in yaml_file :
		if str(sub_level_of_world).find(path_level + level_name) != -1 :
			unreal.EditorLevelLibrary.set_current_level_by_name(level_name)
		else :
			streaming_level=unreal.EditorLevelUtils.create_new_streaming_level(unreal.LevelStreamingDynamic , '/Game/'+level_name )			
			streaming_level.set_editor_property('initially_loaded' , True)
			streaming_level.set_editor_property('initially_visible' , True)
		createActors(yaml_file[level_name] , '' , level_name , '')
		unreal.EditorLevelLibrary.save_all_dirty_levels()

def createActors(dic_actor , path_actor_level , actual_dic , path_to_mesh) :
	if 'mesh' in dic_actor :
		if actual_dic == "appartement":
			actor = unreal.EditorLevelLibrary.spawn_actor_from_object(unreal.EditorAssetLibrary.load_asset(path_mesh + path_to_mesh + '/' + dic_actor['mesh'] + '.' + dic_actor['mesh']) 
			, (dic_actor['x']*100 , dic_actor['y']*(-100) , dic_actor['z']*100) , (dic_actor['ry']*(-180/math.pi) , dic_actor['rz']*(-180/math.pi) , dic_actor['rx']*(180/math.pi)))
			actor.set_folder_path('/ground_floor/appartement/appartement_vide')
			actor.set_actor_label(actual_dic)		
		elif "env" in path_actor_level:
			if dic_actor['type']=='AREA':
				rectlight=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.RectLight , (dic_actor['x']*100 , dic_actor['y']*(-100)
				, dic_actor['z']*100-60) , (dic_actor['rx']*(-180/math.pi)-90 , dic_actor['rz']*(-180/math.pi)-90 , dic_actor['ry']*(180/math.pi)))
				rectlight.root_component.set_editor_property('mobility' , unreal.ComponentMobility.STATIC)
				rectlight.root_component.set_editor_property('intensity' , dic_actor['power'])
				rectlight.set_folder_path(path_actor_level)
				rectlight.set_actor_label(actual_dic)
			elif dic_actor['type']=='POINT':
				pointlight=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PointLight,(dic_actor['x']*100 , dic_actor['y']*(-100) , dic_actor['z']*100)
				, (dic_actor['rx']*(-180/math.pi) , dic_actor['rz']*(-180/math.pi) , dic_actor['ry']*(180/math.pi)))
				pointlight.root_component.set_editor_property('mobility' , unreal.ComponentMobility.STATIC)
				pointlight.root_component.set_editor_property('intensity' , dic_actor['power'])
				pointlight.set_folder_path(path_actor_level)
				pointlight.set_actor_label(path_actor_level)
		elif "grapable" in path_actor_level:
			actor=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.EditorAssetLibrary.load_blueprint_class('/Game/experiments/blueprints/BP_grapable_Free.BP_grapable_Free'), 
			(dic_actor['x']*100 , dic_actor['y']*(-100) , dic_actor['z']*100) , (dic_actor['ry']*(-180/math.pi) , dic_actor['rz']*(-180/math.pi) , dic_actor['rx']*(180/math.pi)))
			actor.set_folder_path(path_actor_level)
			actor.set_actor_label(actual_dic)
			actor.root_component.set_editor_property('relative_scale3d' , (dic_actor['scale x'] , dic_actor['scale y'] , dic_actor['scale z']))
			all_actors = unreal.EditorLevelLibrary.get_all_level_actors_components()
			for blueprint_component in all_actors:
				actor_owner=blueprint_component.get_owner()
				if actor_owner:	
					if actual_dic == actor_owner.get_actor_label():
						blueprint_component.set_editor_property("static_mesh",unreal.EditorAssetLibrary.load_asset(path_mesh + path_to_mesh+ "/" + dic_actor['mesh']))	
		elif "furnitures" in path_actor_level:
			actor = unreal.EditorLevelLibrary.spawn_actor_from_object(unreal.EditorAssetLibrary.load_asset(path_mesh + path_to_mesh + '/' + dic_actor['mesh'] + '.' + dic_actor['mesh']) 
			, (dic_actor['x']*100 , dic_actor['y']*(-100) , dic_actor['z']*100) , (dic_actor['ry']*(-180/math.pi) , dic_actor['rz']*(-180/math.pi) , dic_actor['rx']*(180/math.pi) ))			
			actor.set_folder_path(path_actor_level)
			actor.set_actor_label(actual_dic)
			actor.root_component.set_editor_property('relative_scale3d' , (dic_actor['scale x'] , dic_actor['scale y'] , dic_actor['scale z']))
		else:
			actor = unreal.EditorLevelLibrary.spawn_actor_from_object(unreal.EditorAssetLibrary.load_asset(path_mesh + path_to_mesh + '/' + dic_actor['mesh'] + '.' + dic_actor['mesh']) 
			, (dic_actor['x']*100 , dic_actor['y']*(-100) , dic_actor['z']*100) , (dic_actor['ry']*(-180/math.pi) , dic_actor['rz']*(-180/math.pi) , dic_actor['rx']*(180/math.pi) ))
			actor.set_folder_path(path_actor_level)
			actor.set_actor_label(actual_dic)	


	elif 'right_door' in dic_actor :
		actor=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.EditorAssetLibrary.load_blueprint_class('/Game/experiments/blueprints/BP_door_interactive.BP_door_interactive') , 
		(dic_actor['right_door']['x']*100 , dic_actor['right_door']['y']*(-100) , dic_actor['right_door']['z']*100) , (dic_actor['right_door']['ry']*(-180/math.pi) , dic_actor['right_door']['rz']*(-180/math.pi) , dic_actor['right_door']['rx']*(180/math.pi) ))								
		actor.set_folder_path(path_actor_level)
		actor.set_actor_label(actual_dic)
		list = []
		i = 0
		while i == 0:
			i = 1
			all_actors = unreal.EditorLevelLibrary.get_all_level_actors_components()
			for blueprint_component in all_actors:
				actor_owner=blueprint_component.get_owner()
				if actor_owner:	
					if actual_dic == actor_owner.get_actor_label() and ('StaticMesh' in str(blueprint_component) or 'ChildActor' in str(blueprint_component)):
						check_list=str(blueprint_component).split('PersistentLevel.BP_door_interactive_C')[1]
						check_list=str(check_list).split(".")[1]
						check_list=str(check_list).split("'")[0]
						if check_list not in list :
							i=0
							element_list=str(blueprint_component).split('PersistentLevel.BP_door_interactive_C')[1]
							element_list=str(element_list).split(".")[1]
							element_list=str(element_list).split("'")[0]
							list.append(element_list)					
							if 'Handle' in str(blueprint_component) and 'handle' in dic_actor:
								blueprint_component.set_editor_property("child_actor_class",unreal.EditorAssetLibrary.load_blueprint_class(path_blueprint + "/BP_" + dic_actor["handle"]["mesh"] + "_movable_" + scene_name))			
							elif 'Lock' in str(blueprint_component) and 'lock' in dic_actor:
								blueprint_component.set_editor_property("static_mesh",unreal.EditorAssetLibrary.load_asset(path_mesh + "/furnitures/door/" + dic_actor['lock']['mesh']))
							elif 'Wrist' in str(blueprint_component) and 'wrist' in dic_actor:
								blueprint_component.set_editor_property("child_actor_class",unreal.EditorAssetLibrary.load_blueprint_class(path_blueprint + "/BP_" + dic_actor["wrist"]["mesh"] + "_nonmovable_" + scene_name))			
							elif 'door_left' in str(blueprint_component) and 'left_door' in dic_actor:	
								blueprint_component.set_editor_property("static_mesh",unreal.EditorAssetLibrary.load_asset(path_mesh + "/furnitures/door/" + dic_actor['left_door']['mesh']))
							elif 'door_right' in str(blueprint_component) and 'right_door' in dic_actor:	
								blueprint_component.set_editor_property("static_mesh",unreal.EditorAssetLibrary.load_asset(path_mesh + "/furnitures/door/" + dic_actor['right_door']['mesh']))
							elif 'Double' in str(blueprint_component) and 'frame' in dic_actor:
								blueprint_component.set_editor_property("static_mesh",unreal.EditorAssetLibrary.load_asset(path_mesh + "/furnitures/door/" + dic_actor['frame']['mesh']))
			unreal.EditorLevelLibrary.save_all_dirty_levels()


	elif 'elevator' == actual_dic:
		actor=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.EditorAssetLibrary.load_blueprint_class('/Game/experiments/blueprints/elevator.elevator') , 
		(dic_actor['gf_elevator']['x']*100 , dic_actor['gf_elevator']['y']*(-100) , dic_actor['gf_elevator']['z']*100) , (dic_actor['gf_elevator']['ry']*(-180/math.pi) , dic_actor['gf_elevator']['rz']*(-180/math.pi) , dic_actor['gf_elevator']['rx']*(180/math.pi) ))								
		actor.set_folder_path(path_actor_level)
		actor.set_actor_label(actual_dic)
		list = []
		i = 0
		while i == 0:
			i = 1
			all_actors = unreal.EditorLevelLibrary.get_all_level_actors_components()		
			for blueprint_component in all_actors:
				actor_owner = blueprint_component.get_owner()				
				if actor_owner:
					if actual_dic in actor_owner.get_actor_label() and 'StaticMesh' in str(blueprint_component):
						check_list = str(blueprint_component).split('PersistentLevel.elevator_C')[1]
						check_list = str(check_list).split(".")[1]
						check_list = str(check_list).split("'")[0]						
						if check_list not in list:							
							i=0
							element_list = str(blueprint_component).split('PersistentLevel.elevator_C')[1]
							element_list = str(element_list).split(".")[1]
							element_list = str(element_list).split("'")[0]
							list.append(element_list)
							if 'interior' in str(blueprint_component):
								blueprint_component.set_editor_property("static_mesh",unreal.EditorAssetLibrary.load_asset(path_mesh + "/elevator/" + dic_actor['interior']['mesh']))			
							elif 'top door half 1' in str(blueprint_component):
								blueprint_component.set_editor_property("static_mesh",unreal.EditorAssetLibrary.load_asset(path_mesh + "/elevator/" + dic_actor['door_exterior_top_001']['mesh']))	
							elif 'top door half' in str(blueprint_component):
								blueprint_component.set_editor_property("static_mesh",unreal.EditorAssetLibrary.load_asset(path_mesh + "/elevator/" + dic_actor['door_exterior_top']['mesh']))	
							elif 'door bot in 1' in str(blueprint_component):
								blueprint_component.set_editor_property("static_mesh",unreal.EditorAssetLibrary.load_asset(path_mesh + "/elevator/" + dic_actor['door_interior_botom_001']['mesh']))	
							elif 'door bot in' in str(blueprint_component):
								blueprint_component.set_editor_property("static_mesh",unreal.EditorAssetLibrary.load_asset(path_mesh + "/elevator/" + dic_actor['door_interior_botom']['mesh']))	
							elif 'door top in 1' in str(blueprint_component):
								blueprint_component.set_editor_property("static_mesh",unreal.EditorAssetLibrary.load_asset(path_mesh + "/elevator/" + dic_actor['door_interior_top_001']['mesh']))	
							elif 'door top in' in str(blueprint_component):
								blueprint_component.set_editor_property("static_mesh",unreal.EditorAssetLibrary.load_asset(path_mesh + "/elevator/" + dic_actor['door_interior_top']['mesh']))	
							elif 'bot door' in str(blueprint_component):
								blueprint_component.set_editor_property("static_mesh",unreal.EditorAssetLibrary.load_asset(path_mesh + "/elevator/" + dic_actor['gf_elevator']['mesh']))	
							elif 'botom door half 1' in str(blueprint_component):
								blueprint_component.set_editor_property("static_mesh",unreal.EditorAssetLibrary.load_asset(path_mesh + "/elevator/" + dic_actor['exterior_door_botom_001']['mesh']))	
							elif 'botom door half' in str(blueprint_component):
								blueprint_component.set_editor_property("static_mesh",unreal.EditorAssetLibrary.load_asset(path_mesh + "/elevator/" + dic_actor['exterior_door_botom']['mesh']))								
			unreal.EditorLevelLibrary.save_all_dirty_levels()


	else :
		for sub_dic in dic_actor :
			if actual_dic == 'appartement' :
				createActors(dic_actor[sub_dic] , "/ground_floor/" + actual_dic + "/appartement_plein", sub_dic , path_to_mesh + "/" + actual_dic)
			elif ('furnitures' in path_actor_level and ('ground_floor' in actual_dic)) :
				createActors(dic_actor[sub_dic] , '/ground_floor' + path_actor_level , sub_dic , path_to_mesh)
			elif ('furnitures' in path_actor_level and ('first_floor' in actual_dic)) :
				createActors(dic_actor[sub_dic] , '/first_floor' + path_actor_level , sub_dic , path_to_mesh)
			elif (('furnitures' in path_actor_level or 'grapable' in path_actor_level)and 'mesh'in dic_actor[sub_dic]) :
				createActors(dic_actor[sub_dic] , path_actor_level , sub_dic , path_to_mesh)
			else :
				createActors(dic_actor[sub_dic] , path_actor_level + "/" + actual_dic , sub_dic , path_to_mesh + "/" + actual_dic)



if __name__=="__main__":
	createWorld()

