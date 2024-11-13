import re

def extract_points(text):
    # Regex to match patterns like (a), (b), (c) followed by text
    pattern = r'\((\w)\)\s*(.*?)\s*(?=\(\w\)|$)'
    
    # Find all matches and store them in a dictionary
    points = {match[0]: match[1] for match in re.findall(pattern, text)}
    
    return points

# Example usage
text = "This is (a) first point and then \n(b) next point and lastly \n(c) last point"
points_dict = extract_points(text)
print(points_dict)


# Input dictionary of points
points = {'a': 'pointa', '1': 'point1', 'i': 'pointi', '2': 'point2', 'b': 'pointb'}

# Initialize result dictionary
formatted_result = {}

# Iterate through the dictionary, segregating points based on keys
for key in points:
    if key.isalpha():  # For alphabetic points (a to z)
        sub_points = []
        for sub_key in points:
            if sub_key.isdigit() or sub_key in ['i', 'v', 'x']:  # For numeric or roman numeral keys
                sub_points.append(f"{sub_key}. {points[sub_key]}")
        formatted_result[key] = f"{points[key]} " + " ".join(sub_points)

# Print the result
print(formatted_result)
