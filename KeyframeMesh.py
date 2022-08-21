import maya.cmds as cmds

def selectMesh( isChecked ):
	
	global obj
	global verts
	
	obj = cmds.ls( selection=True, long=True )[0]
	verts = cmds.polyListComponentConversion( obj, toVertex=True )
	verts = cmds.ls( verts, flatten=True, long=True )

def initializeMesh( isChecked ):
	
	global obj
	
	cmds.addAttr( obj, ln="KeyframeMesh", at="bool", keyable=True )

def storeIniVertPos( isChecked ):
	
	global obj
	global vert_pos
		
	for v in verts:
		pos = cmds.xform( v, query=True, translation=True, worldSpace=False )
		vert_pos.append( pos )

def keyMesh( isChecked ):
	
	global obj
	global verts
	global vert_pos
	
	initial_vert_pos = vert_pos
	
	for i in range( len( verts ) ):
		
		new_vert_pos = cmds.xform( verts[i], query=True, translation=True, worldSpace=False )
		
		result_vert_pos = list()
		
		for j in range( len( new_vert_pos ) ):
			result_vert_pos.append( new_vert_pos[j] - initial_vert_pos[i][j] )
		
		cmds.setKeyframe( verts[i], attribute="pntx", value=result_vert_pos[0] )
		cmds.setKeyframe( verts[i], attribute="pnty", value=result_vert_pos[1] )
		cmds.setKeyframe( verts[i], attribute="pntz", value=result_vert_pos[2] )
	
	cmds.setKeyframe( obj + ".KeyframeMesh", value=True )

def selectObjAndVerts( isChecked ):
	
	global obj
	global verts
	
	selection = list()
	
	selection.append( obj )
	for v in verts:
		selection.append( v )
	
	cmds.select( selection )

def makeUI():

	# UI settings
	win_width = 400
	win_padding = 5
	win_row_spacing = 2
	win_name = 'window_ui'

	# Delete the window ui if it already exists
	if cmds.window( win_name, exists = True ):
		cmds.deleteUI( win_name )

	# Window
	main_window = cmds.window( win_name, title="Keyframe Mesh", iconName='KM', width=win_width, height=10, rtf=True, ret=False )
	main_layout = cmds.columnLayout( adjustableColumn=True, columnAttach=('both', win_padding), columnOffset=('both', 0), rowSpacing=win_row_spacing )
	cmds.text( label='', height=win_padding )
	
	# Buttons
	cmds.button( label='Select Mesh', command=selectMesh, annotation="Adds a custom KeyframeMesh attribute to the selected mesh." )
	cmds.button( label='Add Attribute', command=initializeMesh, annotation="Adds a custom KeyframeMesh attribute to the selected mesh." )
	cmds.button( label='Store Initial Pose', command=storeIniVertPos, annotation="Stores the initial vertex positions of the mesh as a base to compare all modifications." )
	cmds.button( label='Add Keyframe', command=keyMesh, bgc=[0.5, 0.03, 0.03], annotation="Stores the initial vertex positions of the mesh as a base to compare all modifications." )
	cmds.button( label='Edit Keyframes', command=selectObjAndVerts, annotation="Stores the initial vertex positions of the mesh as a base to compare all modifications." )
	
	# Close Button
	cmds.separator( height=( win_padding * 4 ), style='in' )
	cmds.button( label='Close', command=('cmds.deleteUI(\"' + main_window + '\", window=True)') )
	cmds.text( label='', height=win_padding )
	
	# Show Window
	cmds.showWindow( main_window )

# global variables
obj = None
verts = list()
vert_pos = list()

# make UI
makeUI()