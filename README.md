# blender-harmonize-vertex-weights
This blender script takes the active object and iterates through each selected object. For each selected object, it then iterates through the vertexes of both the active object and the current selected object. If the two vertexes share the same location in world space, then it copies the vertex weights from the vertex of the active object to the vertex of the current selected object and removes any weights that the active object does not contain.

This script is meant to be used when one is using a rig with multiple body parts, such as a body with different types of head.
