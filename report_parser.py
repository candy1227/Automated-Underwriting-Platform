import re
import pandas as pd

class ReportParser:
    def __init__(self):
        # Define regex patterns for common appraisal fields
        self.patterns = {
            "property_address": r"(?i)property\s+address[:\s]*(.*?)(?:\n|$)",
            "property_type": r"(?i)property\s+type[:\s]*(.*?)(?:\n|$)",
            "square_footage": r"(?i)(?:total|gross)\s+living\s+area[:\s]*([\d,\.]+)\s*(?:sq\s*ft|sf|sq\.ft\.)",
            "year_built": r"(?i)year\s+built[:\s]*(\d{4})",
            "roof_condition_text": r"(?i)roof\s+condition[:\s]*(.*?)(?:\n|$)",
            "foundation_condition_text": r"(?i)foundation\s+condition[:\s]*(.*?)(?:\n|$)"
        }

    def parse_text(self, text):
        extracted_data = {}
        for key, pattern in self.patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                extracted_data[key] = match.group(1).strip()
            else:
                extracted_data[key] = None
        
        # Example: Simple classification based on keywords
        roof_condition = extracted_data.get("roof_condition_text", "").lower()
        if "good" in roof_condition or "new" in roof_condition:
            extracted_data["roof_condition_classified"] = "good"
        elif "fair" in roof_condition or "average" in roof_condition:
            extracted_data["roof_condition_classified"] = "fair"
        elif "poor" in roof_condition or "damaged" in roof_condition or "leaking" in roof_condition:
            extracted_data["roof_condition_classified"] = "poor"
        else:
            extracted_data["roof_condition_classified"] = "unknown"

        foundation_condition = extracted_data.get("foundation_condition_text", "").lower()
        extracted_data["foundation_cracks_detected"] = "yes" if "crack" in foundation_condition else "no"

        return extracted_data

# Example Usage:
# parser = ReportParser()
# sample_text = "Property Address: 123 Main St, Anytown. Year Built: 1980. Roof Condition: Fair, some wear. Foundation Condition: Solid."
# parsed_info = parser.parse_text(sample_text)
# print("Parsed Info:", parsed_info)