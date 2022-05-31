import os
import unreal

path_mesh = '/Game/adream/models/meshes'
path_material='/Game/adream/models/material'
path_level='/Game/adream/maps/'

separate_asset_classes = {"Material","Texture2D","Texture3D"}

def importTree(fbx_path, path_end):
	list = os.listdir(fbx_path + path_end)
	for elements in list:
		if not ".fbx" in elements:
			if not unreal.EditorAssetLibrary.does_directory_exist(path_mesh + path_end + elements):
				unreal.EditorAssetLibrary.make_directory(path_mesh + path_end + elements)
			importTree(path_end + elements + "/")
		else:
			importMyAssets(fbx_path + path_end + elements,path_mesh + path_end)

def buildStaticMeshImportOptions():
	options = unreal.FbxImportUI()

	options.set_editor_property('import_mesh', True)
	options.set_editor_property('import_textures', False)
	options.set_editor_property('import_materials', True)
	options.set_editor_property('import_as_skeletal', False)

	options.static_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)	
	options.static_mesh_import_data.set_editor_property('combine_meshes', True)
	options.static_mesh_import_data.set_editor_property('generate_lightmap_u_vs', True)
	options.static_mesh_import_data.set_editor_property('auto_generate_collision', False)
	options.texture_import_data.set_editor_property('material_search_location', unreal.MaterialSearchLocation.ALL_ASSETS)
	return options

def buildImportTask(filename,destination_path,options=None):
	task=unreal.AssetImportTask()
	task.set_editor_property('automated', True)
	task.set_editor_property('destination_name', '')
	task.set_editor_property('destination_path', destination_path)
	task.set_editor_property('filename', filename)
	task.set_editor_property('replace_existing', True)
	task.set_editor_property('save', True)
	options=buildStaticMeshImportOptions()
	task.set_editor_property('options', options)
	return task

def executeImportTasks(tasks=[]):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)


def importMyAssets(file_name_and_path,destination_path):
	static_mesh_task = buildImportTask(file_name_and_path, destination_path)
	executeImportTasks([static_mesh_task])


def separateMaterialFromMesh():
	unreal.EditorAssetLibrary.make_directory(path_material)
	list_assets_path=unreal.EditorAssetLibrary.list_assets(path_mesh)
	for asset_path in list_assets_path:
		asset=unreal.EditorAssetLibrary.find_asset_data(asset_path)
		if asset.asset_class in separate_asset_classes:
			unreal.EditorAssetLibrary.rename_asset(asset_path,path_material + "/" + str(asset.asset_name))

def importAssets(fbx_path, path):
	if not unreal.EditorAssetLibrary.does_directory_exist(path_mesh):
		unreal.EditorAssetLibrary.make_directory(path_mesh)
	importTree(fbx_path, '/')
	materialsMouv()