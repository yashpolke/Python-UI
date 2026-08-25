import hou
import re
 
 
def main():
    node = hou.pwd()
    for i in hou.selectedNodes():
        if hou.nodeTypeCategories().keys():
            ### Above function lets you call this function on any context ###
            dir = i.path().split(i.name())[0]
            nodeName = i.path().split('/')[-1]
 
            nodeSel = hou.ui.displayMessage("Which type of node do you want to create?", buttons=('Null', 'Output'))
 
            if nodeSel == 0:
                nodeType = 'null'
            else:
                nodeType = 'output'
 
            # nodeName
            rawOtherName = hou.ui.readInput('Name the node', buttons=('OK', 'CANCEL'), initial_contents='geo')[1]
            # remove white spaces
            #otherName = re.sub(r'\s+', '', rawOtherName)
            # remove special characters
            otherName = 'OUT_'+re.sub(r'\W+', '_', rawOtherName)
            if rawOtherName != "":
                nodeName = otherName
            else:
                nodeName = 'OUT'
            parentNode = hou.node(dir)
 
            new_node = createNode(nodeType, nodeName, parentNode)
 
            new_node_pos = i.position()
            new_node.setColor(hou.Color([0, 0, 0]))
            new_node.setUserData("nodeShape", "circle")
            ### Setting node position ###
            new_node.setPosition(hou.Vector2(new_node_pos[0], new_node_pos[1] - 1))
            new_node.setInput(0, i)
            i.setSelected(False)
            new_node.setSelected(True)
### Setting render and display flags for respective contexts ###
            curContext = i.type().category().name()
            if curContext in ['Dop', 'Chop', 'Pop']:
                new_node.setDisplayFlag(True)
            if curContext in ['Sop', 'Cop2', 'CopNet']:
                new_node.setRenderFlag(True)
                new_node.setDisplayFlag(True)
            if curContext in ['Vop']:
                new_node.setPosition(hou.Vector2(new_node_pos[0] + 1.5, new_node_pos[1]))
                new_node.setInput(0, i)
            ### Match the name of incoming nodes to that of the names of the nodes you have selected
            for aNode in i.outputs():
                x = 0
                for inputs in aNode.inputs():
                    if inputs.name() == i.name():
                        aNode.setInput(x,new_node)
                    else:
                        x += 1
                new_node.setInput(0,i)
def createNode(nodeType, nodeName, parentNode):
 
    new_node = parentNode.createNode(nodeType)
    new_node.setName(nodeName, unique_name=True)
 
    return new_node
