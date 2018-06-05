#Brian Callahan, 1/13/2018
#Updated 6/5/2018

import bpy
import mathutils

def checkIfTypeIsMesh():
    toObjects = bpy.context.selected_editable_objects
    returnToObjects = [r for r in toObjects if r.type == 'MESH' and r != bpy.context.active_object]

    return returnToObjects

def HarmonizeVerts():

    fromObject = bpy.context.active_object

    if fromObject is not None and fromObject.type == 'MESH':

        toObjects = checkIfTypeIsMesh()

        if len(toObjects) > 0:

            fromVGroupNames = set(fromObject.vertex_groups.keys())

            if len(fromVGroupNames) > 0:

                fromData = fromObject.data

                for toObject in toObjects:

                    toVGroupNames = set(toObject.vertex_groups.keys())

                    if len(toVGroupNames) > 0:

                        toData = toObject.data

                        exclusiveNames = toVGroupNames.difference(fromVGroupNames)

                        sharedNames = fromVGroupNames & toVGroupNames

                        for i in sharedNames:
                            print(i, end=" ")

                        for i in exclusiveNames:
                            print(i, end=" . ")

                        if len(sharedNames) > 0:

                            for fromVert in fromData.vertices:
                                for toVert in toData.vertices:

                                    if fromVert.co * fromObject.matrix_world == toVert.co * toObject.matrix_world:

                                        for g in sharedNames:

                                            fromVGroup = fromObject.vertex_groups[g]
                                            toVGroup = toObject.vertex_groups[g]

                                            vert_grp = [g for g in fromVert.groups if g.group == fromVGroup.index]
                                            if len(vert_grp):
                                                toVGroup.add([toVert.index], fromVGroup.weight(fromVert.index), 'REPLACE')

                                        for g in exclusiveNames:

                                            if g in toObject.vertex_groups:

                                                toVGroup.remove([toVert.index])

            else:
                print("The object to copy from has no vertex groups.")
        else:
            print("There are no mesh type selected objects.")
    elif fromObject is None:
        print("No objects is currently active.")
    else:
        print("The object selected is not a mesh.")

def CheckVertexPositonsOnTwoObjectsAndHarmonizeWeights(firstObjectName, secondObjectName):

    firstObject = bpy.data.objects.get(firstObjectName)
    secondObject = bpy.data.objects.get(secondObjectName)

    if firstObject is not None and secondObject is not None:
        if firstObject.type == 'MESH' and secondObject.type == 'MESH':
            print("Both objects are meshes.")
            firstData = firstObject.data
            secondData = secondObject.data

            o1GroupNames = firstObject.vertex_groups.keys()
            o2GroupNames = secondObject.vertex_groups.keys()

            if len(o1GroupNames) > 0 and len(o2GroupNames) > 0:

                sharedNames = list(filter(lambda o: o in o2GroupNames, o1GroupNames))


                if len(sharedNames) > 0:

                    for firstVert in firstData.vertices:
                        for secondVert in secondData.vertices:

                            if mathutils.Vector(firstVert.co) * firstObject.matrix_world == mathutils.Vector(secondVert.co) * secondObject.matrix_world:
                                print("Matching vertex!")
                                for g in sharedNames:

                                    firstVgroup = firstObject.vertex_groups[g]
                                    secondVgroup = secondObject.vertex_groups[g]
                                    #copy from first to second

                                    vert_grp = [g for g in firstVert.groups if g.group == firstVgroup.index]
                                    if len(vert_grp):
                                        print("Weight of first vert: {0}".format(firstVgroup.weight(firstVert.index)))#here's the problem
                                        secondVgroup.add([secondVert.index], firstVgroup.weight(firstVert.index), 'REPLACE')

                else:
                    print("Neither objects have matching vertex groups. You might want to rename a group on one of them.")
            elif len(o1GroupNames) > 0:
                print("The second object has no vetex groups.")
            elif len(o2GroupNames) > 0:
                print("The first object has no vetex groups.")
            else:
                print("Neither objects have any vertex groups.")
        elif firstObject.type == 'MESH':
            print("The second object is not a mesh.")
        elif secondObject.type == 'MESH':
            print("The first object is not a mesh")

        else:
            print("Neither objects are meshes.")
            #print(firstObject.type + " !! " + secondObject.type)
    elif firstObject is None:
        print("The first object does not exist. Check the name.")
    elif secondObject is None:
        print("The second object does not exist. Check the name.")
    else:
        print("Neither objects exist. Check the names.")

HarmonizeVerts()
