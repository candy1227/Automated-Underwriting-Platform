import os
from config import Config
from src.document_processing.ocr_parser import OCRParser
from src.document_processing.report_parser import ReportParser
from src.computer_vision.image_analyzer import ImageAnalyzer
from src.multimodal_fusion.data_integrator import DataIntegrator
from src.risk_assessment.rule_engine import RuleEngine
from src.risk_assessment.ml_risk_model import MLRiskModel

def process_underwriting_case(report_path, photo_path):
    print(f"--- Processing Case: {os.path.basename(report_path)} ---")

    # 1. Document Processing
    ocr_parser = OCRParser(Config.TESSERACT_CMD)
    report_parser = ReportParser()

    print("Step 1: Document Processing (Text & Image Extraction)")
    text_content, extracted_images = ocr_parser.extract_text_from_pdf(report_path)
    parsed_text_data = report_parser.parse_text(text_content)
    print("Parsed Text Data:", parsed_text_data)

    # 2. Computer Vision (for primary photo or extracted images)
    image_analyzer = ImageAnalyzer()
    image_analysis_results = {}
    if photo_path and os.path.exists(photo_path):
        image_analysis_results = image_analyzer.analyze_property_image(photo_path)
    elif extracted_images: # Use first extracted image if no primary photo provided
        image_analysis_results = image_analyzer.analyze_property_image(extracted_images[0])
    print("Image Analysis Results:", image_analysis_results)

    # 3. Multimodal Fusion
    data_integrator = DataIntegrator()
    combined_features = data_integrator.integrate_data(parsed_text_data, image_analysis_results)
    print("Combined Features:", combined_features)

    # 4. Risk Assessment (Rule-based)
    rule_engine = RuleEngine()
    rule_based_assessment = rule_engine.apply_rules(combined_features)
    print("Rule-based Assessment:", rule_based_assessment)

    # 5. Risk Assessment (ML Model)
    ml_model = MLRiskModel()
    if not ml_model.load_model():
        print("ML Model not loaded. Skipping ML risk prediction.")
        ml_prediction = {"predicted_label": "N/A", "probabilities": {}}
    else:
        # Preprocess combined_features for the ML model
        # This part needs to be robust: handle missing features, encode categoricals
        # For simplicity, let's assume combined_features has numerical/boolean
        # and ML model handles dummy variables.
        # In a real system, you'd use the same preprocessing (e.g., OneHotEncoder)
        # that was used during training.
        
        # Dummy preprocessing to match expected ML model features
        ml_features_for_prediction = {
            'text_square_footage': float(combined_features.get('text_square_footage', 0).replace(',', '')) if combined_features.get('text_square_footage') else 0,
            'text_year_built': int(combined_features.get('text_year_built', 0)) if combined_features.get('text_year_built') else 0,
            'image_num_defects': combined_features.get('image_num_defects', 0),
            'multimodal_roof_conflict': 1 if combined_features.get('multimodal_roof_conflict') else 0,
            'combined_property_condition_score': combined_features.get('combined_property_condition_score', 0),
            'text_roof_condition_classified_poor': 1 if combined_features.get('text_roof_condition_classified') == 'poor' else 0,
            'text_roof_condition_classified_unknown': 1 if combined_features.get('text_roof_condition_classified') == 'unknown' else 0,
            # Add other dummy-encoded features as per your training data
            'text_roof_condition_classified_good': 1 if combined_features.get('text_roof_condition_classified') == 'good' else 0,
            # If your ML model was trained with 'text_roof_condition_classified_fair' as a feature, include it here.
            # Otherwise, ensure your training strategy accounts for `drop_first=True`
            # For simplicity, if 'good' 'poor' 'unknown' are not set to 1, then 'fair' is implicitly the case when drop_first=True.
        }

        # Filter to only the features the ML model was trained on
        # (This is why self.feature_columns in MLRiskModel is important)
        if ml_model.feature_columns:
            final_ml_input = {k: ml_features_for_prediction.get(k, 0) for k in ml_model.feature_columns}
        else:
            final_ml_input = ml_features_for_prediction # Fallback if feature_columns not set

        ml_prediction = ml_model.predict_risk(final_ml_input)
    print("ML Model Prediction:", ml_prediction)

    print("--- Final Underwriting Decision ---")
    final_decision = rule_based_assessment["decision"]
    if ml_prediction["predicted_label"] == "HIGH_RISK" and final_decision == "APPROVED":
        final_decision = "REVIEW_REQUIRED (ML flag)"
    if ml_prediction["predicted_label"] == "DECLINE" and final_decision != "DECLINE":
        final_decision = "DECLINE (ML override)"

    print(f"Overall Decision: {final_decision}")
    print("-" * 40)
    return final_decision, rule_based_assessment, ml_prediction, combined_features

# To run this:
if __name__ == "__main__":
    # Create dummy data directories and files for testing
    os.makedirs(Config.RAW_DATA_DIR, exist_ok=True)
    os.makedirs(Config.MODELS_DIR, exist_ok=True)

    # Create a dummy PDF (you'll need to create a real one or use existing)
    # For a quick test, you might mock the OCR and parser output
    dummy_pdf_content = """
    Property Appraisal Report
    Property Address: 123 Elm Street, Springfield, IL 62704
    Property Type: Single Family Home
    Year Built: 1985
    Total Living Area: 1850 sq ft
    Roof Condition: Fair, some granular loss.
    Foundation Condition: Solid, no visible cracks.
    """
    with open(os.path.join(Config.RAW_DATA_DIR, "report_001.pdf"), "w") as f: # Not a real PDF, just for text example
         f.write(dummy_pdf_content)
    # You'd typically need a library like reportlab to truly create a PDF
    # Or just use an existing PDF report for testing.

    # Create a dummy image (e.g., a blank image or a photo you have)
    from PIL import Image
    dummy_image = Image.new('RGB', (60, 30), color = 'red')
    dummy_image.save(os.path.join(Config.RAW_DATA_DIR, "property_001.jpg"))

    # --- IMPORTANT: Train and save a dummy ML model first! ---
    # Run the ML model training section in ml_risk_model.py once
    # to generate a dummy model file for this main.py to load.
    # Otherwise, the ML prediction step will be skipped.

    # Example usage:
    process_underwriting_case(
        os.path.join(Config.RAW_DATA_DIR, "report_001.pdf"),
        os.path.join(Config.RAW_DATA_DIR, "property_001.jpg")
    )

    # You could extend this to process multiple files in a loop
    # or build a web API with FastAPI to upload documents.