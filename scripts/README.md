# PCB Automation Scripts
Automation scripts for KiCad and Proteus PCB design workflows.

## Scripts

### kicad_placement.py
Auto-places components in KiCad based on AI-generated coordinates

**Usage:**
1. Open KiCad PCB Editor
2. Tools > Scripting Console
3. Copy-paste the script
4. Modify the `placements` dictionary with your AI output
5. Run

### kicad_routing.py
Creates basic tracks in KiCad from AI-generated netlist

**Usage:**
1. Open KiCad PCB Editor
2. Tools > Scripting Console
3. Copy-paste the script
4. Modify the `routes` list with your AI output
5. Run

### proteus_netlist_parser.py
Parses AI-generated netlist text into structured JSON

**Usage:**
```bash
python proteus_netlist_parser.py netlist.txt