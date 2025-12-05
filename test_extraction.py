
def extract_severity(text_content):
    severity = "Unknown"
    if "Severity Level:" in text_content:
        try:
            parts = text_content.split("Severity Level:")
            if len(parts) > 1:
                # The part after "Severity Level:" contains the level and the rest of the text
                # We need to isolate the level (first line)
                rest_of_text = parts[1].strip()
                severity_line = rest_of_text.split("\n")[0]
                
                severity_part = severity_line.replace("*", "").replace("[", "").replace("]", "").strip()
                if "Low" in severity_part: severity = "Low"
                elif "Moderate" in severity_part: severity = "Moderate"
                elif "High" in severity_part: severity = "High"
                
                # Remove the Severity line from the text content to avoid duplication/clutter
                # We reconstruct the text without the "Severity Level: ..." line
                text_content = text_content.replace(f"Severity Level: {severity_line}", "").strip()
        except:
            pass
    return severity, text_content

# Test Cases
test_1 = """Severity Level: Moderate

### 1. Probable Conditions:
* **Flu:** ..."""

test_2 = """Severity Level: [High]

### 1. Probable Conditions:
..."""

test_3 = """Severity Level: Low
### 1. Probable Conditions:
..."""

print(f"Test 1: {extract_severity(test_1)}")
print(f"Test 2: {extract_severity(test_2)}")
print(f"Test 3: {extract_severity(test_3)}")
