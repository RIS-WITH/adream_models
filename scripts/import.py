import os
import unreal
path = "/home/nclerc/Documents/FBX"
end = '/Game/meshes'
matirial='/Game/material'

def importTree(path_fin):
	list = os.listdir(path+path_fin)
	for elements in list:
		if not ".fbx" in elements:
			if not unreal.EditorAssetLibrary.does_directory_exist(end+path_fin+elements):
				unreal.EditorAssetLibrary.make_directory(end+path_fin+elements)
			importTree(path_fin+elements+"/")
		else:
			importMyAssets(path+path_fin+elements,end+path_fin)

def buildStaticMeshImportOptions():
	options=unreal.FbxImportUI()
	options.set_editor_property('import_mesh',True)
	options.set_editor_property('import_textures',False)
	options.set_editor_property('import_materials',True)
	options.set_editor_property('import_as_skeletal',False)
	options.static_mesh_import_data.set_editor_property('import_uniform_scale',1.0)	
	options.static_mesh_import_data.set_editor_property('combine_meshes',True)
	options.static_mesh_import_data.set_editor_property('generate_lightmap_u_vs',True)
	options.static_mesh_import_data.set_editor_property('auto_generate_collision',False)
	options.texture_import_data.set_editor_property('material_search_location',unreal.MaterialSearchLocation.ALL_ASSETS)
	return options

def buildImportTask(filename,destination_path,options=None):
	task=unreal.AssetImportTask()
	task.set_editor_property('automated',True)
	task.set_editor_property('destination_name','')
	task.set_editor_property('destination_path',destination_path)
	task.set_editor_property('filename',filename)
	task.set_editor_property('replace_existing',True)
	task.set_editor_property('save',True)
	options=buildStaticMeshImportOptions()
	task.set_editor_property('options',options)
	return task

def executeImportTasks(tasks=[]):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    """imported_asset_paths = []
                for task in tasks:
                    for path in task.get_editor_property('imported_object_paths'):
                        imported_asset_paths.append(path)
                return imported_asset_paths"""


def importMyAssets(file_name_and_path,destination_path):
	static_mesh_task = buildImportTask(file_name_and_path, destination_path)
	executeImportTasks([static_mesh_task])


def materialsMouv():
	unreal.EditorAssetLibrary.make_directory(matirial)
	list_assets_path=unreal.EditorAssetLibrary.list_assets(end)
	for asset_path in list_assets_path:
		asset=unreal.EditorAssetLibrary.find_asset_data(asset_path)
		if asset.asset_class=='Material':
			unreal.EditorAssetLibrary.rename_asset(asset_path,matirial+"/"+str(asset.asset_name))

if __name__=="__main__":
	if not unreal.EditorAssetLibrary.does_directory_exist(end):
		unreal.EditorAssetLibrary.make_directory(end)
	importTree('/')
	materialsMouv()
			
