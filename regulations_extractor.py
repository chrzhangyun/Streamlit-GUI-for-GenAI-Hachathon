import re

def extract_points(text):
    # Regex to match patterns like (a), (b), (c) followed by text
    pattern = r'\(([a-z])\)\s*(.*?)\s*(?=\([a-z]\)|$)'
    
    # Find all matches and store them in a dictionary
    points = {match[0]: match[1] for match in re.findall(pattern, text)}
    
    return points

# Example usage
text = "This is (a) first point and then \n(b) next point and lastly \n(c) last point"
points_dict = extract_points(text)
print(points_dict)
