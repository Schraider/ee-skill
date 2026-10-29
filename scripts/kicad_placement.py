import pcbnew
placements = {
    "U1": {"x": 100.0, "y": 50.0, "rot": 0, "layer": "F.Cu"},      
    "Y1": {"x": 105.0, "y": 52.0, "rot": 90, "layer": "F.Cu"},     
    "C1": {"x": 95.0, "y": 48.0, "rot": 0, "layer": "F.Cu"},       
    "C2": {"x": 96.0, "y": 48.0, "rot": 0, "layer": "F.Cu"},       
    "C3": {"x": 106.0, "y": 51.0, "rot": 0, "layer": "F.Cu"},      
    "C4": {"x": 106.0, "y": 53.0, "rot": 0, "layer": "F.Cu"},      
    "R1": {"x": 110.0, "y": 50.0, "rot": 0, "layer": "F.Cu"},      
}

def place_components():
    board = pcbnew.GetBoard()
    
    if board is None:
        print("ERROR: No board loaded. Open a PCB file first.")
        return
    
    placed_count = 0
    missing_count = 0
    
    for ref, data in placements.items():
        
        fp = board.FindFootprintByReference(ref)
        
        if fp is None:
            print(f"WARNING: Component {ref} not found in board")
            missing_count += 1
            continue
        
        pos = pcbnew.wxPointMM(data["x"], data["y"])
        fp.SetPosition(pos)
        
        fp.SetOrientation(data["rot"] * 10)
        
        if "layer" in data:
            layer_id = pcbnew.GetLayerID(data["layer"])
            if layer_id != -1:
                fp.SetLayer(layer_id)
        
        print(f"Placed {ref} at ({data['x']}, {data['y']})mm, rot={data['rot']}°")
        placed_count += 1
    
    pcbnew.Refresh()
    
    print(f"\nPlacement complete: {placed_count} placed, {missing_count} missing")

place_components()