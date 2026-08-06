import hou
def main():

    # Get selected nodes in selection order
    selected = hou.selectedNodes()

    if len(selected) != 2:
        hou.ui.displayMessage(
            "Please select exactly TWO nodes in order:\n"
            "1. Source node (Original Pyro Solver)\n"
            "2. Target node (New Pyro Solver)",
            severity=hou.severityType.Warning
        )
    else:
        src_node = selected[0]
        dst_node = selected[1]

        # Group into a single Undo operation
        with hou.undos.group(f"Copy Parms from {src_node.name()} to {dst_node.name()}"):
            copied_count = 0
            
            for src_parm in src_node.parms():
                parm_name = src_parm.name()
                dst_parm = dst_node.parm(parm_name)
                
                # Skip if destination doesn't have the parm or if it's locked
                if dst_parm is None or dst_parm.isLocked():
                    continue
                
                try:
                    # Copy keyframes or expressions if present
                    keyframes = src_parm.keyframes()
                    if keyframes:
                        dst_parm.setKeyframes(keyframes)
                    # Copy string parameters without forcing evaluation where possible
                    elif src_parm.parmTemplate().type() == hou.parmTemplateType.String:
                        dst_parm.set(src_parm.rawValue())
                    # Copy standard numeric/toggle values
                    else:
                        dst_parm.set(src_parm.eval())
                        
                    copied_count += 1
                except Exception as e:
                    print(f"Skipped parameter '{parm_name}': {e}")

        print(f"Done! Copied {copied_count} parameter values from '{src_node.name()}' to '{dst_node.name()}'.")
