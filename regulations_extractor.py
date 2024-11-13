import re

def extract_points(text):
    # Regex to match patterns like (a), (b), (c) followed by text
    pattern = r'\((?![ivxlcIVXLC])([a-z])\)\s*(.*?)(?=\s*\([a-z]\)|\s*\([ivxlcIVXLC]\)|$)'
    
    # List to store points
    points = []
    last_marker = None
    for match in re.finditer(pattern, text):
        marker = match.group(1)
        point = match.group(2).strip()

        # If the marker is a valid letter, store it; otherwise, append it to the previous point
        if marker not in 'ivxlcIVXLC':  # valid alphabetical marker
            if last_marker:
                points.append((last_marker, point))  # Add to previous point
            else:
                points.append((marker, point))
            last_marker = marker

    # Now, handle Roman numeral points and add them to the previous valid marker
    roman_pattern = r'\(([ivxlcIVXLC])\)\s*(.*?)\s*(?=\([a-z]\)|$)'
    for match in re.finditer(roman_pattern, text):
        point = match.group(2).strip()
        if points:
            points[-1] = (points[-1][0], points[-1][1] + " " + point)  # Append to previous valid point

    # Convert list of tuples to a dictionary
    points_dict = {k: v for k, v in points}

    return points_dict

# Example usage
text = "This is (a) first point and then (i) ignored point and lastly (b) next point, and (c) last point"
points_dict = extract_points(text)
print(points_dict)
