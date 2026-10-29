import sys
import json
import math

RULES = {
    "min_component_spacing": 2.0,      
    "min_trace_width_signal": 0.25,    
    "min_trace_width_power": 0.5,      
    "min_clearance": 0.2,              
    "max_crystal_distance": 5.0,       
    "decoupling_max_distance": 2.0,    
}

def check_spacing(components):
    violations = []
    
    comp_list = list(components.items())
    for i in range(len(comp_list)):
        for j in range(i + 1, len(comp_list)):
            ref1, data1 = comp_list[i]
            ref2, data2 = comp_list[j]
            
            dx = data1["x"] - data2["x"]
            dy = data1["y"] - data2["y"]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < RULES["min_component_spacing"]:
                violations.append(
                    f"WARNING: {ref1} and {ref2} too close ({distance:.2f}mm < {RULES['min_component_spacing']}mm)"
                )
    
    return violations

def check_crystal_placement(components):
    """Check if crystal is close enough to MCU"""
    violations = []
    
    mcu = None
    crystal = None
    
    for ref, data in components.items():
        if "STM32" in data.get("value", "") or "MCU" in data.get("value", ""):
            mcu = data
        if "crystal" in data.get("value", "").lower() or "XTAL" in data.get("value", ""):
            crystal = data
    
    if mcu and crystal:
        dx = mcu["x"] - crystal["x"]
        dy = mcu["y"] - crystal["y"]
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > RULES["max_crystal_distance"]:
            violations.append(
                f"CRITICAL: Crystal too far from MCU ({distance:.2f}mm > {RULES['max_crystal_distance']}mm)"
            )
    
    return violations

def check_decap_placement(components):
    """Check if decoupling caps are close to ICs"""
    violations = []
    
    ics = [data for ref, data in components.items() 
           if "STM32" in data.get("value", "") or "IC" in data.get("value", "")]
    
    decaps = [data for ref, data in components.items() 
              if "100nF" in data.get("value", "") or "104" in data.get("value", "")]
    
    for ic in ics:
        closest_decap = None
        min_dist = float('inf')
        
        for decap in decaps:
            dx = ic["x"] - decap["x"]
            dy = ic["y"] - decap["y"]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < min_dist:
                min_dist = distance
                closest_decap = decap
        
        if min_dist > RULES["decoupling_max_distance"]:
            violations.append(
                f"WARNING: Decoupling cap too far from IC ({min_dist:.2f}mm > {RULES['decoupling_max_distance']}mm)"
            )
    
    return violations

def main():
    if len(sys.argv) < 2:
        print("Usage: python drc_checker.py <placement.json>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File {filename} not found")
        sys.exit(1)
    
    components = data.get("components", {})
    
    print("Running DRC checks...\n")
    
    all_violations = []
    
    all_violations.extend(check_spacing(components))
    all_violations.extend(check_crystal_placement(components))
    all_violations.extend(check_decap_placement(components))
    
    if all_violations:
        print(f"Found {len(all_violations)} violations:\n")
        for v in all_violations:
            print(f"  {v}")
    else:
        print("No violations found. Design looks good!")

if __name__ == "__main__":
    main()