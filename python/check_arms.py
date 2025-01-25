import json
from collections import defaultdict

def load_json_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def get_body_colors(parts_data):
    body_colors = set()
    for body in parts_data["type"]["body"]:
        color = body.get("color", "")
        if color:
            body_colors.add(color)
    return body_colors

def analyze_arms(parts_data):
    # Get all unique arm names and colors
    arm_names = set()
    colors = set()
    existing_combinations = defaultdict(set)

    # Collect all arms and their colors
    arms_data = parts_data["type"]["arms"]
    for part in arms_data:
        name = part.get("name")
        color = part.get("color", "")
        # Skip arms with empty color value as they are valid for all colors
        if name and color:
            arm_names.add(name)
            colors.add(color)
            existing_combinations[name].add(color)

    # Get body colors and check for unused colors
    body_colors = get_body_colors(parts_data)
    unused_colors = colors - body_colors
    if unused_colors:
        print("\nColors used in arms but not in body section:")
        for color in sorted(unused_colors):
            print(f"  - {color}")

    # Print statistics
    print(f"\nTotal unique arms (excluding universal ones): {len(arm_names)}")
    print(f"Total available colors: {len(colors)}")
    print(f"Theoretical total combinations: {len(arm_names) * len(colors)}")
    
    # Count existing combinations
    total_existing = sum(len(colors_per_arm) for colors_per_arm in existing_combinations.values())
    print(f"Actually existing combinations: {total_existing}")
    
    # Find missing combinations
    missing_found = False
    total_missing = 0
    for arm in sorted(arm_names):
        missing_colors = colors - existing_combinations[arm]
        if missing_colors:
            if not missing_found:
                print("\nArms with missing colors:")
                missing_found = True
            print(f"\n{arm} is missing {len(missing_colors)} colors:", end=" ")
            total_missing += len(missing_colors)
            print(", ".join(sorted(missing_colors)))
    
    if missing_found:
        print(f"\nTotal missing combinations: {total_missing}")

def main():
    try:
        parts_data = load_json_file("../parts.json")
        analyze_arms(parts_data)
    except FileNotFoundError:
        print("Error: parts.json file not found")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in parts.json")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
