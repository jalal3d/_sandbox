__author__ = 'jtchelebi'



#oSel = mc.ls(sl=True, flatter =True)

#oSel= mc.ls(sl=True, flatten=True)
#mc.pointPosition(oSel, local=True)
#mc.pointPosition(oSel, world=True)


# oSel = cmds.select()[0:1]
# print oSel
#
# cmds.select(1)
#
#
# cmds.select('RIG:l_arm:fk_sldr_offset.cv[*]')
#
# vertex_List = []
#
# for obj in oSel:
#     print obj
#     point_Pos = mc.pointPosition (vertex_List)
#     vertex_List.append(point_Pos)
#     print vertex_List


import maya.cmds as mc

oSel = cmds.ls(sl=True, flatten=True)[0:2]
oSource = cmds.getAttr( oSel[0] +".cv[*]")
oTarget = cmds.getAttr( oSel[1] +".cv[*]")
vertCopy = []

vertCopy.append(oSource)
vertCopy.append(oTarget)
print vertCopy


print oSource
print oTarget





def getVtxPos( shapeNode ) :

	vtxWorldPosition = []    # will contain positions un space of all object vertex

	vtxIndexList = cmds.getAttr( shapeNode+".vrts", multiIndices=True )

	for i in vtxIndexList :
		curPointPosition = cmds.xform( str(shapeNode)+".pnts["+str(i)+"]", query=True, translation=True, worldSpace=True )
		vtxWorldPosition.append( curPointPosition )

	return vtxWorldPosition