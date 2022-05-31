import os
import unreal
import yaml

path_base = "/home/nclerc/Documents/FBX"
mesh = '/Game/adream/models/meshes'
material='/Game/adream/models/material'
path_level='/Game/adream/maps/'


"""
print(os.getcwd())"""




"""import sys
my_libs_path = os.getenv("ENV_VARIABLE_NAME")
if "/home/nclerc/Documents/UE/ProjectAdream/Content/Python" is not None and "/home/nclerc/Documents/UE/ProjectAdream/Content/Python" not in sys.path:
    sys.path.append("/home/nclerc/Documents/UE/ProjectAdream/Content/Python")

"""



def createWorld():
	unreal.EditorLevelLibrary.new_level(path_level+"Adream")
	unreal.EditorLevelLibrary.load_level(path_level+"Adream")
	a=unreal.EditorLevelLibrary.get_editor_world()
	b=unreal.EditorLevelUtils.get_levels(a)
	for folder_path in unreal.EditorAssetLibrary.list_assets(mesh,False,True):
		folder_name=str(folder_path).replace(mesh,'')
		if str(b).find(path_level+folder_name.replace('/',''))!=-1:
			unreal.EditorLevelLibrary.set_current_level_by_name(folder_name.replace('/',''))
		else :
			unreal.EditorLevelUtils.create_new_streaming_level(unreal.LevelStreamingDynamic, new_level_path=path_level+folder_name.replace('/',''))
		unreal.EditorLevelLibrary.save_all_dirty_levels()
		c=unreal.EditorLevelLibrary.spawn_actor_from_object(unreal.EditorAssetLibrary.load_asset(mesh+"/appartement/IKEA_chair_PELLO.IKEA_chair_PELLO"),(0,0,0))
		c.set_folder_path('test/oui/non/style')
		#parcours le yaml, prend actorifie tous les objets qui ont folder_name.replace('/','') dans leur nom, les mets bonne coordone rotation (vector/rotator)
		#set_folder_path('path yml'(modification possible pour les exceptions))

		

if __name__=="__main__":

	with open('/home/nclerc/Documents/export1.yaml', 'r') as file:
		z=yaml.safe_load(file)

	for x in [string for string in z if 'appartement' in string]:
		print(z[x]['name'])
	b="salut le monde"
	print(b.replace("chat",'chien'))
	#createWorld()
