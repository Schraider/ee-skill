import sys
import json
import re

def parse_netlist(netlist_text):

    
    components = {}
    connections = []
    
    lines = netlist_text.strip().split('\n')
    current_component = None
    
    for line in lines:
        line = line.strip()
        
        comp_match = re.match(r'Component\s+(\w+)\s+\(([^)]+)\):', line)
        if comp_match:
            ref = comp_match.group(1)
            value = comp_match.group(2)
            current_component = ref
            components[ref] = {"value": value, "pins": {}}
            continue
        
        if current_component and '->' in line:
            pin_match = re.match(r'Pin\s+(\d+)\s+\(([^)]+)\)\s+->\s+(.+)', line)
            if pin_match:
                pin_num = pin_match.group(1)
                pin_name = pin_match.group(2)
                connection = pin_match.group(3).strip()
                
                components[current_component]["pins"][pin_num] = {
                    "name": pin_name,
                    "connects_to": connection
                }
                
                connections.append({
                    "component": current_component,
                    "pin": pin_num,
                    "pin_name": pin_name,
                    "net": connection
                })
    
    return {
        "components": components,
        "connections": connections,
        "total_components": len(components),
        "total_connections": len(connections)
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python proteus_netlist_parser.py <netlist_file.txt>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r') as f:
            netlist_text = f.read()
    except FileNotFoundError:
        print(f"ERROR: File {filename} not found")
        sys.exit(1)
    
    parsed = parse_netlist(netlist_text)
    
    output_file = filename.replace('.txt', '_parsed.json')
    with open(output_file, 'w') as f:
        json.dump(parsed, f, indent=2)
    
    print(f"Parsed {parsed['total_components']} components, {parsed['total_connections']} connections")
    print(f"Output saved to: {output_file}")

if __name__ == "__main__":
    main()