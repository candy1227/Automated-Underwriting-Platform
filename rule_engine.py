from config import Config

class RuleEngine:
    def __init__(self, underwriting_rules=Config.UNDERWRITING_RULES):
        self.rules = underwriting_rules

    def apply_rules(self, features):
        """
        Applies predefined underwriting rules to the extracted features.
        """
        risk_flags = {}
        overall_risk = "LOW_RISK" # Default

        # Example rule application
        roof_condition = features.get("text_roof_condition_classified")
        if roof_condition and roof_condition in self.rules["roof_condition"]:
            risk_flags["roof_risk"] = self.rules["roof_condition"][roof_condition]
            if risk_flags["roof_risk"] == "HIGH_RISK":
                overall_risk = "HIGH_RISK" # Update overall if high risk detected
            elif risk_flags["roof_risk"] == "MEDIUM_RISK" and overall_risk == "LOW_RISK":
                overall_risk = "MEDIUM_RISK"

        foundation_cracks = features.get("text_foundation_cracks_detected")
        if foundation_cracks and foundation_cracks in self.rules["foundation_cracks_detected"]:
            risk_flags["foundation_risk"] = self.rules["foundation_cracks_detected"][foundation_cracks]
            if risk_flags["foundation_risk"] == "HIGH_RISK":
                overall_risk = "HIGH_RISK"

        # Example: Incorporating image-based risk
        image_overall_condition = features.get("image_overall_condition_ai")
        if image_overall_condition == "poor" and overall_risk != "DECLINE":
            risk_flags["image_condition_risk"] = "HIGH_RISK"
            overall_risk = "HIGH_RISK"
        elif image_overall_condition == "fair" and overall_risk == "LOW_RISK":
            risk_flags["image_condition_risk"] = "MEDIUM_RISK"
            overall_risk = "MEDIUM_RISK"

        # Apply more complex rules, e.g., if multiple medium risks, escalate to high
        if overall_risk == "LOW_RISK" and features.get("multimodal_roof_conflict"):
            overall_risk = "REVIEW_REQUIRED" # Conflict flags review

        # Placeholder for final decision based on risk level
        if overall_risk == "HIGH_RISK" or overall_risk == "DECLINE" or overall_risk == "REVIEW_REQUIRED":
            decision = overall_risk
        else:
            decision = "APPROVED" # Or "APPROVED_WITH_CONDITIONS"

        return {"risk_flags": risk_flags, "overall_rule_based_risk": overall_risk, "decision": decision}

# Example Usage:
# rule_engine = RuleEngine()
# rule_results = rule_engine.apply_rules(combined_data)
# print("Rule-based Assessment:", rule_results)