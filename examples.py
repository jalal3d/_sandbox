
#renaming deformer set based from deformer name

import maya.cmds as mc
bends = mc.ls('*_bend', type='nonLinear')


for bend in bends:


    set = mc.listConnections('{0}.message'.format(bend), s=False, d=True, type='objectSet')

    print mc.rename(set, '{0}_set'.format(bend))




#Connect attr "paper_jnt.tweekerVis" to visibility of shape object
import maya.cmds as mc
oSel = mc.ls(selection = True)

for obj in oSel:
    objShape = mc.listRelatives(obj ,s=True ,ni=True)[0]
    mc.connectAttr("paper_jnt.tweekerVis", "{0}.visibility".format(objShape))





import maya.cmds as mc
#within a variable, you can get an exactype from the list)
oSel = mc.ls(selection = True, exactType='transform')
transList = []

for obj in oSel:
    transList.append(obj)
mc.select(transList)




#from selection, select skinCluster and set skin method with dualquaternion
meshList = cmds.ls(sl=True)
for mesh in meshList:
    skCl = mel.eval('findRelatedSkinCluster ' + mesh)
    mc.setAttr('{0}.skinningMethod'.format(skCl), 1)
    mc.setAttr('{0}.dqsSupportNonRigid'.format(skCl), 1)




#From: Alicia Carvalho, Pierre Violanti, Felipe Sanges

#get target from constrained object

constrainedObj = cmds.ls(sl=True)[0]
constraintList = cmds.listConnections('{0}.parentInverseMatrix[0]'.format(constrainedObj), source=True, plugs=False)
targetList = []
for constraintNode in constraintList:
    constraintType = constraintType = cmds.objectType(constraintNode)
    target = getattr(cmds, constraintType)(constraintNode, query=True, targetList=True)
    targetList.append(target[0])

    cmds.select(targetList)
    print 'constrained obj:', constrainedObj, ' constraint:', constraintNode, ' driver:', target

#####find driven object:

#select driver then run the following code
target = cmds.ls(sl=True)[0]
constraintNode = cmds.listConnections(target, type='constraint')[0]
if constraintNode:
driven = cmds.listConnections('{0}.constraintParentInverseMatrix'.format(constraintNode), plugs=False, source=True)
cmds.select(driven)
print(driven)

##########################################################################



#creating a joint within a transform group from selection transform.
import maya.cmds as mc

slt = mc.ls(selection = True)

for obj in slt:
    #create transform and joint node
    createTransform = mc.createNode('transform', n='_orig')
    createJoint = mc.createNode('joint', n='_jnt')
    mc.parent(createJoint, createTransform)
    #get position of selected objects
    posLoc = mc.xform(obj ,q=True ,t=True ,ws=True)
    #set position of selected objects
    setPos = mc.xform(createTransform, t=posLoc, ws=True)






import maya.mel as mel

mesh = cmds.ls(sl=True)
jointList = cmds.skinCluster("body_hi_skClust", q=True, inf=True)

rightJointList = []

#iterate through jointList, replace left side with right side, and append it to the new list
for jointNode in jointList:
    if 'RIG:l_' in jointNode:
        rightJoint = jointNode.replace('RIG:l_', 'RIG:r_')
        rightJointList.append(rightJoint)
        print rightJointList

#iterate through new rightJointList, check if the obejct exists, and if it does add it to the skincluster
for rightJoint in rightJointList:
    if cmds.objExists(rightJoint):
        if not rightJoint in jointList:
            cmds.skinCluster('body_hi_skClust', edit=True, addInfluence=rightJoint, lockWeights=True, weight=0)


#####



jointList = cmds.skinCluster('body_hi_skClust',query=True, influence=True)
cmds.select(jointList)

cmds.skinCluster(jointList, 'bodyHi_skinTemp', toSelectedBones=True, useGeometry=True, maximumInfluences=3, obeyMaxInfluences=False, dropoffRate=4.0)


#######

#---parenting shape node under a joint

slt = mc.ls(sl=True)

### mc.parent(shape , joint , s=True ,r=True)
mc.parent(slt , 'deskCtrl_jnt' , s=True ,r=True)


#######



import maya.cmds as mc
#---parenting shape node under a joint
mc.parent(shape , joint , s=True ,r=True)




import maya.mel as mel

mesh = cmds.ls(sl=True)
jointList = cmds.skinCluster("body_hi_skClust", q=True, inf=True)

rightJointList = []

#iterate through jointList, replace left side with right side, and append it to the new list
for jointNode in jointList:
    if 'RIG:l_' in jointNode:
        rightJoint = jointNode.replace('RIG:l_', 'RIG:r_')
        rightJointList.append(rightJoint)
        print rightJointList

#iterate through new rightJointList, check if the obejct exists, and if it does add it to the skincluster
for rightJoint in rightJointList:
    if cmds.objExists(rightJoint):
        if not rightJoint in jointList:
            cmds.skinCluster('body_hi_skClust', edit=True, addInfluence=rightJoint, lockWeights=True, weight=0)




import maya.cmds as mc
slts = mc.ls(type='transform')

for slt in slts:
    mc.setAttr( '{0}.displayLocalAxis'.format(slt) , 0)




import maya.cmds as mc

locatorGroup = 'matchLocators_grp'
objectSelected = mc.ls(selection = True) or []


#create group to gather all locators into
if not mc.objExists(locatorGroup) :
    locatorGroup = mc.createNode('transform', name=locatorGroup)

#creating for loop to pass through objects in list 1 by 1
for object in objectSelected:
    #replace object name sufix 'manip with 'loc'
    jointName = '{0}_jnt'.format(object)

    #create locator with name specific to 'locatorName' variable
    jointNode = mc.createNode('joint' ,name = jointName ,p=locatorGroup)


    mc.setAttr('{0}.overrideEnabled'.format(jointName), 1)
    mc.setAttr('{0}.overrideColor'.format(jointName), 20)
    mc.parentConstraint(object, jointNode, maintainOffset = False)
    #parent constraint locatorNode to object selected
    mc.delete(mc.parentConstraint(object, jointNode, maintainOffset = False))


sel = mc.ls(selection=True)



import maya.cmds as mc

#Lock attributes

#--- get selections
selectedNodeList = mc.ls(sl=True) or []

if selectedNodeList :
    stateLock = False

    #--- get current state lock on first attr of first obj
    firstObject = selectedNodeList[0]
    allAttr = mc.listAttr(firstObject , k=True)
    if allAttr :
        firstAttr = allAttr[0]
        stateLock = mc.getAttr(firstObject + "." + firstAttr , l=True)

    #--- reverse lock status
    stateToPut = 1-stateLock

    #---- lock or unlock
    for obj in selectedNodeList :
        allAttr = mc.listAttr(obj , k=True)
        for attr in allAttr :
            attrName = '%s.%s'%(obj , attr)
            mc.setAttr(attrName , l=stateToPut)



#when weighted clusters don't refresh during connection

mc.cluster('MLV_r_roundshoulder_cls', e=True, wn=('r_mlv_fk_col_gor_offset_handle_cls','r_mlv_fk_col_gor_offset_handle_cls'))
mc.connectAttr('r_mlv_fk_col_gor_offset_handle_cls_orig.worldInverseMatrix[0]', 'MLV_r_roundshoulder_cls.bindPreMatrix', f=True)




#To copy over cluster deformers
#mirror deformer
mc.copyDeformerWeights(ss=tempMesh, ds=tempMesh, sd=tempCluster, dd=tempCluster, mirrorInverse=False, mirrorMode='YZ')

#copy deformer
mc.copyDeformerWeights(ss=sourceTempMesh, ds=tempMesh, sd=sourceTempCluster, dd=tempCluster, noMirror=True)



import maya.cmds as mc
#list of current object selected (vertex) fl(flatten) lists
#individual items within the list instead of the group in which
#the item belongs too
vertSelect = mc.ls(selection = True, fl=True)

for verts in vertSelect:

    vertPosition = mc.xform(verts, q=True ,t=True ,ws=True)
    #loc = mc.createNode('transform')
    #locShape = mc.createNode('locator', p=loc)
    locShape = mc.createNode('joint')
    mc.xform(locShape,t=vertPosition ,ws=True)




import maya.cmds as mc

locatorGroup = 'matchLocators_grp'
objectSelected = mc.ls(selection = True) or []

#create group to gather all locators into
if not mc.objExists(locatorGroup) :
    locatorGroup = mc.createNode('transform', name=locatorGroup)

#creating for loop to pass through objects in list 1 by 1
for object in objectSelected:
    #replace object name sufix 'manip with 'loc'
    jointName = '{0}_jnt'.format(object)

    #create locator with name specific to 'locatorName' variable
    jointNode = mc.createNode('joint' ,name = jointName ,p=locatorGroup)


    mc.setAttr('{0}.overrideEnabled'.format(jointName), 1)
    mc.setAttr('{0}.overrideColor'.format(jointName), 20)
    mc.parentConstraint(object, jointNode, maintainOffset = False)
    #parent constraint locatorNode to object selected
#    mc.delete(mc.parentConstraint(object, jointNode, maintainOffset = False))


sel = mc.ls(selection=True)

import kmrt.utils.rivet
surf = 'TTL_shell_hi'
for obj in sel :
    kmrt.utils.rivet.do_rivetClosest(surf , obj )


help(kmrt.utils.rivet.do_rivetClosest)






import maya.cmds as mc

oSel = mc.ls(selection = True)
print oSel

for obj in oSel:
    #---variable that holds the shape of the object selected
    shape = mc.listRelatives(obj ,s=True ,ni=True)[0]
    mc.connectAttr('RIG:openSwivel:jnt.switch', '%s.visibility'%(shape))




#### Select vertices of multiple objects to get center and create transform node
center = 115
aim = 42
up = 9

allPins = mc.ls('attach_*_grp')

for pin in allPins :
    obj = pin.replace('_grp' ,'_hi')

    #--- get vtx number name
    realCenter = '%s.vtx[%d]'%(obj , center)
    realAim = '%s.vtx[%d]'%(obj , aim)
    realUp = '%s.vtx[%d]'%(obj , up)

    #--- create nodes
    objCenter = mc.createNode('transform',n='center')
    objAim = mc.createNode('transform' ,n='aim')
    objUp = mc.createNode('transform',n='up')

    #--- get vertex position
    centerPos = mc.xform(realCenter ,q=True ,t=True ,ws=True)
    aimPos = mc.xform(realAim ,q=True ,t=True ,ws=True)
    upPos = mc.xform(realUp ,q=True ,t=True ,ws=True)

    #--- set position
    mc.xform(objCenter,t=centerPos ,ws=True)
    mc.xform(objAim,t=aimPos ,ws=True)
    mc.xform(objUp,t=upPos ,ws=True)

    #--- orient center obj
    mc.delete(mc.aimConstraint(objAim , objCenter , offset= [0, 0, 0] ,weight=1 , aimVector=[0,0,1] ,upVector=[0, 1, 0] ,worldUpType="object" , worldUpObject=objUp))

    #--- set ctrl name
    name = pin.replace('_grp' ,'_ctrl')
    size = 2
    #--- create control
    ctrl ,orig = kmrt.rig.createCtrl(name ,  shapeInfos=['pinSphere', 17], shapeScale=[size, size, size] ,parentTo ='RIG:origin:traj' ,x=False ,z=True)

    #--- set orig postion
    kmrt.utils.transform.snap(objCenter , [orig])

    #--- delete node for position and orientation
    mc.delete([objCenter , objAim , objUp])

    #--- create constraints
    mc.parentConstraint(ctrl , pin ,mo=True)
    mc.scaleConstraint(ctrl , pin)






#Setting lock state of objects
#--- get selections
selectedNodeList = mc.ls(sl=True) or []

if selectedNodeList :
    stateLock = False

    #--- get current state lock on first attr of first obj
    firstObject = selectedNodeList[0]
    allAttr = mc.listAttr(firstObject , k=True)
    if allAttr :
        firstAttr = allAttr[0]
        stateLock = mc.getAttr(firstObject + "." + firstAttr , l=True)

    #--- reverse lock status
    stateToPut = 1-stateLock

    #---- lock or unlock
    for obj in selectedNodeList :
        allAttr = mc.listAttr(obj , k=True)
        for attr in allAttr :
            attrName = '%s.%s'%(obj , attr)
            mc.setAttr(attrName , l=stateToPut)





selectedNodeList = cmds.ls(sl=True)

axes = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY', 'scaleZ', 'visibility']
for selectedNode in selectedNodeList:
    for axis in axes:
        cmds.setAttr('{0}.{1}'.format(selectedNode, axis), lock=False, keyable=True)





#snap pivots from locator name '_loc' to corresponding object with same name but without '_loc'.
#ex. cube1_loc constraint to cube1
import maya.cmds as mc

pivotList = mc.listRelatives ('matchLocators_grp',children = True)


for object in pivotList:
    pivotName = object.split('_loc')[0]
    mc.delete(mc.parentConstraint(object, pivotName, maintainOffset = 0))




#Skin transfer

import maya.mel as mel

mesh = cmds.ls(sl=True)[0]
skinClusterNode = mel.eval('findRelatedSkinCluster {0}'.format(mesh))
jointList = cmds.skinCluster("body_hiShape_skClust", q=True, inf=True)

rightJointList = []

#iterate through jointList, replace left side with right side, and append it to the new list
for jointNode in jointList:
    if 'RIG:l_' in jointNode:
        rightJoint = jointNode.replace('RIG:l_', 'RIG:r_')
        rightJointList.append(rightJoint)

#iterate through new rightJointList, check if the obejct exists, and if it does add it to the skincluster
for rightJoint in rightJointList:
    if cmds.objExists(rightJoint):
        if not rightJoint in jointList:
            cmds.skinCluster('body_hiShape_skClust', edit=True, addInfluence=rightJoint, lockWeights=True, weight=0)







import cuRig._sandbox.common
reload(cuRig._sandbox.common)
cuRig._sandbox.common.matchLocators()







import maya.cmds as mc


#making a current selection list and putting it in a variable
objectSelected = mc.ls(selection=True)

def matchLocators(objectSelected=None):

    if objectSelected is None:
        objectSelected = mc.ls(selection=True)

    if not objectSelected:
        raise RuntimeError('Select objects please')

    #create group to gather all locators into
    locatorGroup = mc.group(empty=True, name='matchLocators_grp')
    #creating for loop to cycle through objects in list 1 by 1
    for object in objectSelected:

        #replace object name sufix 'manip with 'loc'
        locatorName = '{0}_loc'.format(object)

        #create locator with name specific to 'locatorName' variable
        locatorNode = mc.spaceLocator(name = locatorName )
        mc.setAttr('{0}.overrideEnabled'.format(locatorName), 1)
        mc.setAttr('{0}.overrideColor'.format(locatorName), 20)

        #parent constraint locatorNode to object selected
        mc.parentConstraint(object, locatorNode, maintainOffset = False)

        #isolate and select constraint type and put it in a variable
        objectConstraint = mc.listConnections(type = 'constraint')

        #delete constraint
        mc.delete(objectConstraint)

        #parent newly created locator to matchLocators group
        mc.parent(locatorNode, 'matchLocators_grp')


matchLocators()




import maya.cmds as mc
import pymel.core as pm

pelterSecA = pm.ls("M_neckPelter_A_CtrlParent_GRP","M_neckPelter_B_CtrlParent_GRP", "M_neckPelter_C_CtrlParent_GRP")
pelterSecB = pm.ls("M_neckPelter_G_CtrlParent_GRP","M_neckPelter_H_CtrlParent_GRP", "M_neckPelter_I_CtrlParent_GRP")

pm.select(pelterSecA)
for oObj in pm.ls(sl = 1):
    pm.parentConstraint("M_neck_CNS",oObj, mo=0)
    pm.scaleConstraint("M_neck_CNS",oObj, mo=0)

pm.select(pelterSecB)
for oObj in pelterSecB:
    pm.parentConstraint("M_head_CNS",oObj, mo=0)
    pm.scaleConstraint("M_head_CNS", oObj, mo=0)
pm.parent("M_neck_GIM","M_neck_CTRL")
pm.parent("M_neck_CNS","M_neck_GIM")



import pymel.core as pm
pm.select(pm.skinCluster(pm.selected()[0], query=True, influence=True))

__________________________________________________________________________________________________________________
#With selected objects, you create 1 locator to match position and rotation using a parentConstraint

import pymel.core as pm
import maya.cmds as mc

oSel = pm.ls(sl = True)

for obj in oSel:
    pm.select(cl = 1)
    mk_jnt = pm.spaceLocator()
    pm.setAttr('%s.overrideEnabled' % mk_jnt, 1)
    pm.setAttr('%s.overrideColor' % mk_jnt, 22)
    pm.parentConstraint(obj, mk_jnt)
    cnsObj = pm.listConnections (type = 'constraint')
    pm.delete(cnsObj)

#Cluster version

import pymel.core as pm
import maya.cmds as mc


oSelect = pm.ls(sl = True)


mk_cluster = pm.cluster(oSelect)
pm.select(cl = 1)
mk_jnt = pm.spaceLocator()
pm.setAttr('%s.overrideEnabled' % mk_jnt, 1)
pm.setAttr('%s.overrideColor' % mk_jnt, 22)
pm.parentConstraint(mk_cluster, mk_jnt)
cnsObj = pm.listConnections (type = 'constraint')
pm.delete(cnsObj)
pm.delete(mk_cluster)
____________________________________________________________________________________________________________________


#VERSOION B A little different from A. Using an index from a selection and associating it with a object
#name to parent constraint then deleting that constraint.
import pymel.core as pm
import maya.cmds as mc

sel = pm.selected()[0:5]
cns_connections = pm.listConnections (type = 'constraint')


def rope_connect():
    pm.pointConstraint(sel[0], 'M_start_CTRL' )
    pm.pointConstraint(sel[1], 'M_end_CTRL' )
    pm.pointConstraint(sel[2], 'M_mid_A_CTRL' )
    pm.pointConstraint(sel[3], 'M_mid_CTRL' )
    pm.pointConstraint(sel[4], 'M_mid_B_CTRL' )

    for obj in sel:
        cns_connections = pm.listConnections (type = 'constraint')
        pm.delete(cns_connections)

rope_connect()


____________________________________________________________________________________________________________________

###MEL script!

global proc rigSurface(string $surface, int $spansU,int $spansV, int $degU, int $degV ){
    string $shape[]=`ls -sl`;
    int $spans[]=`getAttr ($shape[0]+".spansUV")`;
    int $degre[]=`getAttr ($shape[0]+".degreeUV")`;
    int $ncvu=$spans[0]+ $degre[0] ;
    int $ncvv=$spans[1]+ $degre[1] ;
    print ( $ncvu + "\n");
    print ( $ncvv + "\n");
    string $jgroup=`group -em -n ($surface+"_joint_grp")`;
    string $basejoint[];
    for ($uStart=0;$uStart<$ncvu;$uStart++){
        for ($vStart=0;$vStart<$ncvv;$vStart++){
            float $cvpos[]=`xform -q -ws -t ($surface+".cv["+$uStart+"]["+$vStart+"]")`;
            select -cl;
            string $jt=`joint -p  $cvpos[0]  $cvpos[1]  $cvpos[2] -n ($surface+"_Basejoint_"+$uStart+"_"+$vStart)` ;
            $basejoint[`size( $basejoint)`]=$jt;
            parent $jt $jgroup;
        }
    }
    select -r $basejoint;
    select -add $surface;
    string $sk[]=`newSkinCluster("-tsb")`;
    string $rebuld[]=`rebuildSurface -ch 1 -rpo 0 -rt 0 -end 1 -kr 0 -kcp 0 -kc 1 -su $spansU -du  $degU -sv $spansV -dv  $degV -tol 1e-08 -fr 0  -dir 2  -n ($surface+"_rebuild") $surface`;
    print ("rebuildedSurface =" + $rebuld[0]+"\n");
    rigSecondarySurface( $surface,  $rebuld[0] ,$basejoint);

}

global proc rigSecondarySurface(string $base, string $rebuil, string $rootjoints[]){
    string $shape[]=`listRelatives -s -ni $rebuil`;
    string $baseShape[]=`listRelatives -s -ni $base`;
    int $spans[]=`getAttr ($shape[0]+".spansUV")`;
    int $degre[]=`getAttr ($shape[0]+".degreeUV")`;
    int $ncvu=$spans[0]+ $degre[0] ;
    int $ncvv=$spans[1]+ $degre[1] ;
    print ( $ncvu + "\n");
    print ( $ncvv + "\n");
    string $jgroup=`group -em -n ($rebuil+"_joint_grp")`;
    string $basejoint[];
    for ($uStart=0;$uStart<$ncvu;$uStart++){
        for ($vStart=0;$vStart<$ncvv;$vStart++){

            float $cvpos[]=`xform -q -ws -t ($rebuil+".cv["+$uStart+"]["+$vStart+"]")`;
            select -cl;
            string $jt=`joint -p  $cvpos[0]  $cvpos[1]  $cvpos[2] -n ($rebuil+"_joint_"+$uStart+"_"+$vStart)` ;
            $basejoint[`size( $basejoint)`]=$jt;
            parent $jt $jgroup;
        }
    }
    select -r $basejoint;
    select -add $rebuil ;
    string $sk[]=`newSkinCluster("-tsb")`;
    string $cposi=`createNode closestPointOnSurface`;
    connectAttr ($baseShape[0]+".ws") ($cposi+".inputSurface");
    addAttr -ln displayHighJt -at "bool" -k 1  $rebuil;

    for ($each in $basejoint){
        float $pos[]=`xform -q -ws -t $each`;
        setAttr ($cposi+".inPosition") $pos[0] $pos[1] $pos[2];
        float $u=`getAttr ($cposi+".parameterU")`;
        float $v=`getAttr ($cposi+".parameterV")`;
        string $posi=`createNode pointOnSurfaceInfo -n ($each+"_posi") `;
        connectAttr ($baseShape[0]+".ws") ($posi+".inputSurface");
        setAttr ($posi+".parameterU") $u;
        setAttr ($posi+".parameterV") $v;
        string $matrixNode=`createNode fourByFourMatrix`;
        connectAttr  ($posi+".normalizedNormalX") ($matrixNode+".in00");
        connectAttr  ($posi+".normalizedNormalY") ($matrixNode+".in01");
        connectAttr  ($posi+".normalizedNormalZ") ($matrixNode+".in02");

        connectAttr  ($posi+".normalizedTangentUX") ($matrixNode+".in10");
        connectAttr  ($posi+".normalizedTangentUY") ($matrixNode+".in11");
        connectAttr  ($posi+".normalizedTangentUZ") ($matrixNode+".in12");

        connectAttr  ($posi+".normalizedTangentVX") ($matrixNode+".in20");
        connectAttr  ($posi+".normalizedTangentVY") ($matrixNode+".in21");
        connectAttr  ($posi+".normalizedTangentVZ") ($matrixNode+".in22");

        connectAttr  ($posi+".positionX") ($matrixNode+".in30");
        connectAttr  ($posi+".positionY") ($matrixNode+".in31");
        connectAttr  ($posi+".positionZ") ($matrixNode+".in32");

        string $decomposeMatrix=`createNode decomposeMatrix`;
        connectAttr ( $matrixNode+".output") ($decomposeMatrix+".inputMatrix");
        string $prebindJt[]=`duplicate -n ($each+"_prebind") $each`;
        string $controlJt[]=`duplicate -n ($each+"_control") $each`;
        connectAttr  ($decomposeMatrix+".outputTranslate") ($prebindJt[0]+".translate");

        connectAttr  ($decomposeMatrix+".outputRotate") ($prebindJt[0]+".rotate");
        string $conn[]=`listConnections -p 1 -d 1 ($each+".wm[0]")`;
        string $out=substituteAllString($conn[0],"matrix","bindPreMatrix");

        connectAttr ($prebindJt[0]+".wim") ($out);
        parent $each $controlJt[0];
        string $jigNode=`fred_jiggleNode($each+"_jiggle")`;
        parentConstraint $controlJt[0] $jigNode;
        connectAttr ($jigNode+".x") ($each+".tx");
        connectAttr ($jigNode+".y") ($each+".ty");
        connectAttr ($jigNode+".z") ($each+".tz");
        parent $controlJt[0] $prebindJt[0];
        print ($conn[0]+"\n");
        setAttr ($prebindJt[0]+".drawStyle") 2;
        connectAttr ($rebuil+".displayHighJt") ($controlJt[0]+".v");
        connectAttr ($rebuil+".displayHighJt") ( $jigNode+".v");

    }
    for ($each in $rootjoints){
        string $exp=($each+".v= 1-"+$rebuil+".displayHighJt;") ;
        expression -o $each -s  $exp;
    }
    setAttr ($base+".intermediateObject") 1;




}





global proc string fred_jiggleNode(string $namenode)
{
    string $name = `createNode transform -n $namenode`;
    string $expStr;
    string $expression;
    string $shape;
    string $startFrame ;
    addAttr  -sn "sf" -ln "startFrame" -at "long" -dv 1 -k true;
    addAttr  -sn "stiff" -ln "stiffness" -min 0 -max 1 -at "double" -dv 0.2 -k true;
    addAttr  -sn "damp" -ln "damping" -min 0 -max 1 -at "double" -dv 0.2 -k true;
    addAttr  -sn "trans" -ln "translation" -min 0 -max 100 -at "double" -dv 1 -k true;
    addAttr  -sn "rot" -ln "rotation" -min 0 -max 100 -at "double" -dv 1 -k true;
    addAttr  -sn "grav" -ln "gravity" -min -100 -max 100 -at "double" -dv 5 -k true;
    addAttr  -sn "x" -ln "x" -at "double";
    addAttr  -sn "y" -ln "y" -at "double";
    addAttr  -sn "z" -ln "z" -at "double";
    addAttr  -sn "rtx" -ln "rtx" -at "double";
    addAttr  -sn "rty" -ln "rty" -at "double";
    addAttr  -sn "rtz" -ln "rtz" -at "double";
    //addAttr  -sn "twist" -ln "twist" -at "double";
    $shape =`createNode locator -n ($name + "Shape") -p $name`;
    setAttr -k off ".v";
    addAttr  -sn "lastWX" -ln "lastWX" -at "double";
    addAttr  -sn "lastWY" -ln "lastWY" -at "double";
    addAttr  -sn "lastWZ" -ln "lastWZ" -at "double";
    addAttr  -sn "lastVX" -ln "lastVX" -at "double";
    addAttr  -sn "lastVY" -ln "lastVY" -at "double";
    addAttr  -sn "lastVZ" -ln "lastVZ" -at "double";
    addAttr  -sn "lastAX" -ln "lastAX" -at "double";
    addAttr  -sn "lastAY" -ln "lastAY" -at "double";
    addAttr  -sn "lastAZ" -ln "lastAZ" -at "double";
    addAttr  -sn "lastBX" -ln "lastBX" -at "double";
    addAttr  -sn "lastBY" -ln "lastBY" -at "double";
    addAttr  -sn "lastBZ" -ln "lastBZ" -at "double";
    addAttr  -sn "lastT" -ln "lastT" -at "double";
    $expStr = $expStr + (
                    "float $px = " + $name + ".translateX;\n"
                    + "float $py = " + $name + ".translateY;\n"
                    + "float $pz = " + $name + ".translateZ;\n"
                    + "float $wx = " + $shape + ".lastWX;\n"
                    + "float $wy = " + $shape + ".lastWY;\n"
                    + "float $wz = " + $shape + ".lastWZ;\n"
                    + "float $vx = " + $shape + ".lastVX;\n"
                    + "float $vy = " + $shape + ".lastVY;\n"
                    + "float $vz = " + $shape + ".lastVZ;\n"
                    + "int $startFrame = " + $name + ".startFrame;\n"
                    + "float $stiff = " + $name + ".stiffness;\n"
                    + "float $istiff = 1-$stiff;\n"
                    + "float $damp = 1 - " + $name + ".damping;\n"
                    + "float $travel = " + $name + ".translation;\n"
                    + "float $fx = 0; float $fy = 0; float $fz = 0;\n"
                    + "if( frame > " + ($startFrame + 1) + " ){\n"
                    + "     $fx = " + $name + ".x * $istiff + $stiff * ($wx - $px) * $travel + $vx;\n"
                    + "     $fy = " + $name + ".y * $istiff + $stiff * ($wy - $py) * $travel + $vy;\n"
                    + "     $fz = " + $name + ".z * $istiff + $stiff * ($wz - $pz) * $travel + $vz;\n"
                    + "  " + $shape +".lastVX = $vx * $damp -$fx * $stiff;\n"
                    + "  " + $shape +".lastVY = $vy * $damp -$fy * $stiff;\n"
                    + "  " + $shape +".lastVZ = $vz * $damp -$fz * $stiff;\n"
                    + "}else{\n"
                    + "  " + $shape +".lastVX = 0;\n"
                    + "  " + $shape +".lastVY = 0;\n"
                    + "  " + $shape +".lastVZ = 0;\n"
                    + "}\n"
                    + $name + ".x = $fx;\n"
                    + $name + ".y = $fy;\n"
                    + $name + ".z = $fz;\n"
                    + $name +".lastWX = $px;\n"
                    + $name +".lastWY = $py;\n"
                    + $name +".lastWZ = $pz;\n"

                    +"float $rx = " + $name + ".rotateX;\n"
                    + "float $ry = " + $name + ".rotateY;\n"
                    + "float $rz = " + $name + ".rotateZ;\n"
                    + "float $rwx = " + $shape + ".lastAX;\n"
                    + "float $rwy = " + $shape + ".lastAY;\n"
                    + "float $rwz = " + $shape + ".lastAZ;\n"
                    + "float $rvx = " + $shape + ".lastBX;\n"
                    + "float $rvy = " + $shape + ".lastBY;\n"
                    + "float $rvz = " + $shape + ".lastBZ;\n"
                    + "int $startFrame = " + $name + ".startFrame;\n"
                    + "float $stiff = " + $name + ".stiffness;\n"
                    + "float $istiff = 1-$stiff;\n"
                    + "float $damp = 1 - " + $name + ".damping;\n"
                    + "float $travel = " + $name + ".rotation;\n"
                    + "float $gx = 0; float $gy = 0; float $gz = 0;\n"
                    + "if( frame > " + ($startFrame + 1) + " ){\n"
                    + "     $gx = " + $name + ".rtx * $istiff + $stiff * ($rwx - $rx) * $travel + $rvx;\n"
                    + "     $gy = " + $name + ".rty * $istiff + $stiff * ($rwy - $ry) * $travel + $rvy;\n"
                    + "     $gz = " + $name + ".rtz * $istiff + $stiff * ($rwz - $rz) * $travel + $rvz;\n"
                    + "  " + $shape +".lastBX = $rvx * $damp -$gx * $stiff;\n"
                    + "  " + $shape +".lastBY = $rvy * $damp -$gy * $stiff;\n"
                    + "  " + $shape +".lastBZ = $rvz * $damp -$gz * $stiff;\n"
                    + "}else{\n"
                    + "  " + $shape +".lastBX = 0;\n"
                    + "  " + $shape +".lastBY = 0;\n"
                    + "  " + $shape +".lastBZ = 0;\n"
                    + "}\n"
                    + $name + ".rtx = $gx;\n"
                    + $name + ".rty = $gy;\n"
                    + $name + ".rtz = $gz;\n"
                    + $name +".lastAX = $rx;\n"
                    + $name +".lastAY = $ry;\n"
                    + $name +".lastAZ = $rz;\n" );
                expression -s $expStr;
return $name;

}
__________________________________________________________________________________________________________________

import maya.cmds as mc
import pymel.core as pm
import re

for obj in pm.ls(selection=True):
    oFind = re.compile(".+PV|.+_HDL")
    oJnt = re.compile(".+_JNT|.+_Basejoint")
    if oFind.match(obj.name()):
        obj.attr("visibility").set(0)
    if oJnt.match(obj.name()):
        obj.attr("drawStyle").set(2)

 __________________________________________________________________________________________________________________


import maya.cmds as mc
import pymel.core as pm
import re

for obj in pm.ls(selection=True):
    oChild = pm.listRelatives (obj, children = 1)
    SelChildren = pm.select(oChild)
    for sel in pm.ls(sl = 1):
        pm.setAttr('%s.rotation' % sel, 1)
        pm.setAttr('%s.translation' % sel, 1)


___________________________________________________________________________________________________________________

import maya.cmds as mc
import pymel.core as pm

my_list = [
    "CAPE_PRP_BOAT_oldSailShip_001:hirez:MSH_flag_A",
    "CAPE_PRP_BOAT_oldSailShip_001:hirez:MSH_sail_A",
    "CAPE_PRP_BOAT_oldSailShip_001:hirez:MSH_sail_B_2",
    "CAPE_PRP_BOAT_oldSailShip_001:hirez:MSH_sail_C_3",
    "CAPE_PRP_BOAT_oldSailShip_001:hirez:MSH_sail_C_2",
    "CAPE_PRP_BOAT_oldSailShip_001:hirez:MSH_sail_D",
    "CAPE_PRP_BOAT_oldSailShip_001:hirez:MSH_sail_C_1",
    "CAPE_PRP_BOAT_oldSailShip_001:hirez:MSH_sail_B_1",
]

mc.select(my_list)

______________________________________________________________________________________________________________________

import maya.cmds as mc
import pymel.core as pm

pelterSecA = pm.ls("M_neckPelter_A_CtrlParent_GRP","M_neckPelter_B_CtrlParent_GRP", "M_neckPelter_C_CtrlParent_GRP")
pelterSecB = pm.ls("M_neckPelter_G_CtrlParent_GRP","M_neckPelter_H_CtrlParent_GRP", "M_neckPelter_I_CtrlParent_GRP")

pm.select(pelterSecA)
for oObj in pm.ls(sl = 1):
    pm.parentConstraint("M_neck_CNS",oObj, mo=0)
    pm.scaleConstraint("M_neck_CNS",oObj, mo=0)

pm.select(pelterSecB)
for oObj in pelterSecB:
    pm.parentConstraint("M_head_CNS",oObj, mo=0)
    pm.scaleConstraint("M_head_CNS", oObj, mo=0)
pm.parent("M_neck_GIM","M_neck_CTRL" )
pm.parent("M_neck_CNS","M_neck_GIM")



______________________________________________________________________________________________________________________


import maya.cmds as mc
import pymel.core as pm
import re

for n in pm.ls(selection=True, regex='.+(_PV|_HDL|_JNT|)'):
    n.attr("visibility").set(1)

#or

import maya.cmds as mc
import pymel.core as pm
import re

for obj in pm.ls(selection=True):
    oFind = re.compile(".+PV|.+HDL")
    oJnt = re.compile(".+_JNT|.+_Basejoint")
    if oFind.match(obj.name()):
        obj.attr("visibility").set(0)
    if oJnt.match(obj.name()):
        obj.attr("drawStyle").set(2)


##################################################################################


#With selected objects, you create 1 locator to match position and rotation using a parentConstraint

import pymel.core as pm
import maya.cmds as mc

oSel = pm.ls(sl = True)

for obj in oSel:
    pm.select(cl = 1)
    mk_jnt = pm.spaceLocator()
    pm.setAttr('%s.overrideEnabled' % mk_jnt, 1)
    pm.setAttr('%s.overrideColor' % mk_jnt, 22)
    pm.parentConstraint(obj, mk_jnt)
    cnsObj = pm.listConnections (type = 'constraint')
    pm.delete(cnsObj)


#############################################################################
# joint creation                                                            #
#############################################################################
# AUTHOR :            Jalal Tchelebi                                        #
#                                                                           #
#                                                                           #
# CREATION DATE :     23/06/2015                                            #
# UPDATED DATE :	  23/06/2015                                            #
#                                                                           #
# VERSION :		      1.0                                                   #
#                                                                           #
# DESCRIPTION :	      From the list of object selected(locators), a joint   #
#                     is created and then parented.                         #
#                                                                           #
# HOW TO USE :        Select object (locators) in sequence and run script.  #
#############################################################################

# from the list of object selected, a joint is created and then parented.
import pymel.core as pm
import maya.cmds as mc

oSel = pm.selected()
oJntList = []

for obj in oSel:
    pm.select(cl = 1)
    mk_jnt = pm.joint(obj)
    pm.parent(mk_jnt, w = 1)
    oJntList.append(mk_jnt)
pm.parent(oJntList[1], oJntList[0])
pm.parent(oJntList[2], oJntList[1])
pm.parent(oJntList[3], oJntList[2])
pm.parent(oJntList[4], oJntList[3])

#or
#You can for loop through the "range" starting at [0] through the "len"
#of "oJntList" it using "i" as the index. To remember, "len" index start
#at [1] while "range" start at [0] so the -2 is there to make sure we
#the end of the list.
#At each for loop pass, the i+1 acts like an increment
for i in range(0, len(oJntList - 2)):
    pm.parent(oJntList[i + 1], oJntList[i])




# pointOnSurface Tree                                                       #
#############################################################################
# AUTHOR :            Jalal Tchelebi                                        #
#                                                                           #
#                                                                           #
# CREATION DATE :     10/09/2015                                            #
# UPDATED DATE :	  10/09/2015                                            #
#                                                                           #
# VERSION :		      1.0                                                   #
#                                                                           #
# DESCRIPTION :	      Allows quick attribute connection between             #
#                     pointOnSurfaceInfo(current sel), 4by4Matrix and       #
#                     DecomposeMatrix Nodes to oLoc object.                 #
#                                                                           #
# HOW TO USE :        Select pointOnSurfaceInfo Node and run script         #
#                     (don't forget to change oLoc variable since it's the  #
#                     last object in the tree that inherits the transforms) #
#############################################################################

import pymel.core as pm

oSel = pm.ls(sl = 1)



for obj in oSel:

    oNodeMatrix = pm.createNode( 'fourByFourMatrix' )
    oNodeDecMatrix = pm.createNode( 'decomposeMatrix' )

    oLoc = 'positionCtrl_B_LOC'


    pm.connectAttr( obj.name() + '.result.normal.normalX', oNodeMatrix.name() + '.in00' )
    pm.connectAttr( obj.name() + '.result.normal.normalY', oNodeMatrix.name() + '.in01' )
    pm.connectAttr( obj.name() + '.result.normal.normalZ', oNodeMatrix.name() + '.in02' )

    pm.connectAttr( obj.name() + '.result.tangentU.tangentUx', oNodeMatrix.name() + '.in10' )
    pm.connectAttr( obj.name() + '.result.tangentU.tangentUy', oNodeMatrix.name() + '.in11' )
    pm.connectAttr( obj.name() + '.result.tangentU.tangentUz', oNodeMatrix.name() + '.in12' )

    pm.connectAttr( obj.name() + '.result.tangentV.tangentVx', oNodeMatrix.name() + '.in20' )
    pm.connectAttr( obj.name() + '.result.tangentV.tangentVy', oNodeMatrix.name() + '.in21' )
    pm.connectAttr( obj.name() + '.result.tangentV.tangentVz', oNodeMatrix.name() + '.in22' )

    pm.connectAttr( obj.name() + '.result.position.positionX', oNodeMatrix.name() + '.in30' )
    pm.connectAttr( obj.name() + '.result.position.positionY', oNodeMatrix.name() + '.in31' )
    pm.connectAttr( obj.name() + '.result.position.positionZ', oNodeMatrix.name() + '.in32' )

    pm.connectAttr( oNodeMatrix.name() + '.output', oNodeDecMatrix.name() + '.inputMatrix ')

    pm.connectAttr( oNodeDecMatrix.name() + '.outputTranslateX', oLoc + '.translate.translateX' )
    pm.connectAttr( oNodeDecMatrix.name() + '.outputTranslateY', oLoc + '.translate.translateY' )
    pm.connectAttr( oNodeDecMatrix.name() + '.outputTranslateZ', oLoc + '.translate.translateZ' )

    pm.connectAttr( oNodeDecMatrix.name() + '.outputRotateX', oLoc + '.rotate.rotateX' )
    pm.connectAttr( oNodeDecMatrix.name() + '.outputRotateY', oLoc + '.rotate.rotateY' )
    pm.connectAttr( oNodeDecMatrix.name() + '.outputRotateZ', oLoc + '.rotate.rotateZ' )


#####################################################################################################

#With selected objects, you create 1 joint child of each selection

import pymel.core as pm
import maya.cmds as mc

sel = pm.ls(sl = True)

for obj in sel:
    pm.select(cl = 1)
    mk_joint = pm.joint()
    pos = pm.xform(obj, q = 1, t = 1, ws = 1 )
    pm.xform(mk_joint, ws = 1, t = pos)
    pm.parent(mk_joint, obj)
    sel_child = pm.listRelatives(children=True)
    pm.rename(sel_child, '%sJNT' % obj.name().split('FLC')[0])


#####################################################################################################

#VERSION A: Match transforms using parent constraint from a sequence selection.
#example: 5 locatos and 5 spheres. Select 5 locators is sequence, then the spheres in sequence...run script.
import pymel.core as pm
import maya.cmds as mc

obj_sel = pm.ls(sl = 1)

half_sel = len(obj_sel) / 2

cns_connection = pm.listConnections(type = 'constraint')

for obj in range(half_sel):
    pm.parentConstraint(obj_sel[obj], obj_sel[half_sel + obj])
    pm.delete(cns_connection)

#####################################################################################################

#VERSOION B A little different from A. Using an index from a selection and associating it with a object
#name to parent constraint then deleting that constraint.
import pymel.core as pm
import maya.cmds as mc

sel = pm.selected()[0:5]
cns_connections = pm.listConnections (type = 'constraint')


def rope_connect():
    pm.parentConstraint(sel[0], 'M_start_CTRL', sr = ['x', 'y', 'z'] )
    pm.parentConstraint(sel[1], 'M_mid_A_CTRL', sr = ['x', 'y', 'z'] )
    pm.parentConstraint(sel[2], 'M_mid_CTRL', sr = ['x', 'y', 'z'] )
    pm.parentConstraint(sel[3], 'M_mid_B_CTRL', sr = ['x', 'y', 'z'] )
    pm.parentConstraint(sel[4], 'M_end_CTRL', sr = ['x', 'y', 'z'] )
    for obj in sel:
        cns_connections = pm.listConnections (type = 'constraint')
        pm.delete(cns_connections)

rope_connect()


#####################################################################################################
# CONSTRAINT DELETE                                                         #
#############################################################################
# AUTHOR :            Jalal Tchelebi                                        #
#                                                                           #
#                                                                           #
# CREATION DATE :     23/06/2015                                            #
# UPDATED DATE :	  23/06/2015                                            #
#                                                                           #
# VERSION :		      1.0                                                   #
#                                                                           #
# DESCRIPTION :	      Deleting constraints from 1 or many selected objects  #
#                                                                           #
# HOW TO USE :        Select object that have constraints and run script.   #
#############################################################################


import maya.cmds as mc
import pymel.core as pm

#variable holding selection list
obj_sel = pm.ls(selection = True)


#defining the function.
def cns_del():
    #Takes current objects selected and puts them in a list.
    for obj in obj_sel:
        #creating a variable to hold the listed connections of constraints using the for loops that passes through each object.
        obj_cns = set(pm.listConnections(type = "constraint", destination = False))
        #deleting the constraint as it filters through each object within the list.
        pm.delete(obj_cns)

#if statement confirming selection to run function
if obj_sel:
    cns_del()
#alternative to if statement if fails
else:
    error ("NO OBJECT(S) SELECTED")

cns_del()

########################################################################################################################

#CONSTRAINING MESH TO TARGET
import maya.cmds as mc
import pymel.core as pm

for oObj in pm.ls(selection=True):
        pm.parentConstraint ("locator1", oObj, mo=0)
        pm.scaleConstraint ("locator1", oObj, mo=0)

#####################################################################################################

#Select object with specific name and delete constraints, if not found, delete constraints of the current object selected
import maya.cmds as mc
import pymel.core as pm

oFind = pm.ls(selection=True, regex='.+CtrlOffset')


for oObj in oFind:
    pm.select(oObj)
    for oCns in oObj:
        constraintList = pm.listConnections(t='constraint')
#        pm.select(constraintList)
        pm.delete(constraintList)


    else:
        for oObj in pm.ls(selection=True):
            pm.pointConstraint(remove=True)


#####################################################################################################

import maya.cmds as mc
import pymel.core as pm

for obj in pm.ls(selection=True):
    pm.setAttr('%s.overrideEnabled' % obj, 1)
#    pm.setAttr('%s.overrideDisplayType' % obj, 2)
    pm.setAttr('%s.overrideColor' % obj, 6)
#    pm.setAttr('%s.inheritsTransform' % obj, 0)

#(6 Blue 13 Red 22 yellow)

#####################################################################################################


import pymel.core as pm
from pymel.core import *

sel = pm.selected()

for oObj in pm.ls(selection=True):
    cst_connections = pm.listConnections(type="constraint", source=False, connections=True, plugs=True)
    print cst_connections

    for cst_conn in cst_connections:
        #print cst_conn
        cst_targets = pm.nodetypes.parentConstraint(cst_conn, getTargetList)
        print cst_targets

#print sel[0]

#####################################################################################################

import maya.cmds as mc
import pymel.core as pm

#Prints the number of object selected
selection = pm.ls(sl=1)
print len(selection)

#####################################################################################################

#Node Tree for controllers version A
import pymel.core as pm
import maya cmds as mc

#Create and empty(em)group node with L_objectName_CNS name
pm.group(em=True, name='L_objectName_CNS')

#Create and group node L_objectName_CTRL and adds it to 'L_onjectName_CNS'
pm.group('L_objectName_CNS', name='L_objectName_CTRL')

#Create a group node 'L_objectNameCtrlOffset' and adds it to L_objectName_CNS
pm.group('L_objectName_CTRL', name='L_objectNameCtrlOffset')

#Create a group node 'L_objectNameCtrlParent_GRP' and adds it to 'L_objectNameCtrlOffset'
pm.group('L_objectNameCtrlOffset', name='L_objectNameCtrlParent_GRP')

#Create a group node L_objectNameCtrlRoot_GRP and adds it to L_objectNameCtrlParent_GRP
pm.group('L_objectNameCtrlParent_GRP', name='L_objectNameCtrlRoot_GRP')

######################################################################################################


#Node Tree for controllers version B

#############################################################################
# Controller Maker                                                          #
#############################################################################
# AUTHOR :            Jalal Tchelebi                                        #
#                                                                           #
#                                                                           #
# CREATION DATE :     23/01/2015                                            #
# UPDATED DATE :      30/06/2015                                            #
#                                                                           #
# VERSION :	      1.0                                                   #
#                                                                           #
# DESCRIPTION :	      With a controller selected, groups parented in a      #
#                     conform structure.                                    #
#                                                                           #
# HOW TO USE :        Select a control curve and Run script.                #
#############################################################################

import pymel.core as pm
import maya.cmds as mc

#defining the function.
def ctrl_mk(obj_list):
    #If "obj_list" is not a list in the given argument...
    if not isinstance(obj_list, list):
        #then make a list out of it in an "obj_list" variable.
        obj_list = [obj_list]
    gp = pm.group(empty=True, name='L_objectName_CNS')
    pm.parent(gp,obj_list)
    #Create a group node L_objectNameCtrlRoot_GRP and adds it to L_objectNameCtrlParent_GRP
    gp_offset = pm.group(obj_list, name='L_objectNameCtrlOffset')
    gp_parent = pm.group(gp_offset, name='L_objectNameCtrlParent_GRP')
    pm.group(gp_parent, name='L_objectNameCtrlRoot_GRP')

def main():
    obj_sel = pm.ls(selection = True)

    if obj_sel:
        ctrl_mk(obj_list)

    else:
        error("NO OBJECT(S) SELECTED")


#####################################################################################################


import maya.cmds as mc

nodes = cmds.allNodeTypes()

for all in nodes:
    print all

#####################################################################################################


from pymel import core as pm

sel = pm.selected()

for node in sel:
    all_history_nodes = node.listHistory()
    poly_tweak = None
    poly_map = None

    for history_node in all_history_nodes:

        if history_node.nodeType() == 'polyMapDel':
            poly_map = history_node

            if not poly_tweak:
                continue
            else:
                break


        if history_node.nodeType() == 'polyTweakUV':
            poly_tweak = history_node

            if not poly_map:
                continue
            else:
                break



    if poly_map:
        pm.delete(poly_map.node())

    if poly_tweak:
        pm.delete(poly_tweak.node())

#####################################################################################################


#looks through current selection and recursively selects object with specific target name
 from pymel import core as pm

target_name = 'pSphere4'
sel = pm.selected()
found_nodes = []

def search_by_name(target, name):
    match_nodes = []
    list_children = target.listRelatives(children=True)

    if name in target.nodeName():
        match_nodes.append(target)

    for child in list_children:
        match_nodes += search_by_name(child, name)

    return match_nodes

for node in sel:
    found_nodes += search_by_name(node, target_name)

for found_node in found_nodes:
    print found_node

#####################################################################################################

# Print deformers associated with selected object skinCluster

import maya.cmds as mc
import pymel.core as pm

oInfluence = pm.skinCluster("skinCluster2", q=True, inf=True)


for inf in oInfluence:
    print 'select("%s", add=True)' % inf

#####################################################################################################

#find the skincluster related to the mesh 
meshList = cmds.ls(sl=True)
for mesh in meshList:
    skCl = mel.eval('findRelatedSkinCluster ' + mesh)
    print(skCl)
    cmds.select (skCl)
    
#find deformers related to the mesh
meshList = cmds.ls(sl=True)
for mesh in meshList:
    deformers = mel.eval('findRelatedDeformer ' + mesh)
    print(deformers)

#itereate through the deformers and find and print the object type (type of deformer)
for deformer_node in deformers:
    deformer_type = cmds.objectType(deformer_node)
    print(deformer_node, deformer_type)
    

   ####################################################################################################
import maya.cmds as cmds
curve_point_list = cmds.ls(selection=True, flatten=True)

point_position_list = []
for curve_point in curve_point_list:
    point_position = cmds.pointPosition(curve_point)
    point_position_list.append(point_position)
    
cmds.curve(p=point_position_list)
    
#########################################################################################################
#rivet commands in python and mel

import maya.mel as mel
mel.eval('Rivet;')

import maya.internal.nodes.uvpin.node_interface
maya.internal.nodes.uvpin.node_interface.createRivet()

#you can make it shorter for example:
import maya.internal.nodes.uvpin.node_interface as xyz
xyz.createRivet()

#########################################################################################################
