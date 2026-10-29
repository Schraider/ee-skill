import pcbnew

routes = [
    ("VCC", 95.0, 48.0, 100.0, 50.0, 0.5, "F.Cu"),      
    ("GND", 96.0, 48.0, 100.0, 50.0, 0.5, "F.Cu"),      
    ("OSC1", 105.0, 52.0, 106.0, 51.0, 0.25, "F.Cu"),   
    ("OSC2", 105.0, 52.0, 106.0, 53.0, 0.25, "F.Cu"),   
    ("SWDIO", 110.0, 50.0, 115.0, 50.0, 0.25, "F.Cu"),  
]

def create_routes():
    board = pcbnew.GetBoard()
    
    if board is None:
        print("ERROR: No board loaded")
        return
    
    created_count = 0
    
    for net_name, x1, y1, x2, y2, width, layer_name in routes:
        netinfo = board.FindNet(net_name)
        if netinfo is None:
            netinfo = pcbnew.NETINFO_ITEM(board, net_name)
            board.Add(netinfo)
        
        track = pcbnew.PCB_TRACK(board)
        track.SetNet(netinfo)
        
        track.SetStart(pcbnew.wxPointMM(x1, y1))
        track.SetEnd(pcbnew.wxPointMM(x2, y2))
        
        track.SetWidth(pcbnew.FromMM(width))
        
        layer_id = pcbnew.GetLayerID(layer_name)
        if layer_id != -1:
            track.SetLayer(layer_id)
        
        board.Add(track)
        
        print(f"Created track: {net_name} ({x1},{y1}) -> ({x2},{y2}), width={width}mm")
        created_count += 1
    
    pcbnew.Refresh()
    
    print(f"\nRouting complete: {created_count} tracks created")

create_routes()