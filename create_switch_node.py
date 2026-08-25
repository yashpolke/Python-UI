import hou

def main():
    # Get selected nodes
    selected_nodes = hou.selectedNodes()

    if len(selected_nodes) != 2:
        hou.ui.displayMessage("Please select exactly two nodes (Node A above, Node B below).")
        return

    # Sort nodes vertically by position (higher Y value = Node A, lower Y value = Node B)
    nodes_sorted = sorted(selected_nodes, key=lambda n: n.position().y(), reverse=True)
    node_a, node_b = nodes_sorted[0], nodes_sorted[1]

    # Target parent network where the switch node will be created
    parent = node_a.parent()

    # Create the switchif node
    switch_node = parent.createNode("switchif", "switchif1")

    # Connect Node A -> Switch Input 0, Node B -> Switch Input 1
    switch_node.setInput(0, node_a)
    switch_node.setInput(1, node_b)
    switch_node.parm("expr1").set(0)

    # Helper function to gather valid downstream targets (Nodes & NetworkDots)
    def get_downstream_targets(source_node):
        targets = []
        for connector in source_node.outputConnectors():
            for conn in connector:
                item = conn.outputItem()
                # Exclude internal wiring between selected nodes and the new switch
                if item not in (node_a, node_b, switch_node):
                    targets.append((item, conn.inputIndex(), conn.outputIndex()))
        return targets

    # Determine which node has downstream targets to re-route (check B first, fallback to A)
    downstream_targets = get_downstream_targets(node_b)
    if not downstream_targets:
        downstream_targets = get_downstream_targets(node_a)

    # Re-route the connections to originate from switch_node instead
    for output_item, input_index, output_index in downstream_targets:
        output_item.setInput(input_index, switch_node, output_index)

    # Position the switch node neatly below Node B
    pos_b = node_b.position()
    switch_node.setPosition(hou.Vector2(pos_b.x() - 1.0, pos_b.y() - 1.2))

    # Select the new switch node
    switch_node.setSelected(True, clear_all_selected=True)
