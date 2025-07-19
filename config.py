import os

class Config:
    # Directories
    RAW_DATA_DIR = os.path.join("data", "raw_appraisals")
    PROCESSED_TEXT_DIR = os.path.join("data", "processed_text")
    PROCESSED_IMAGES_DIR = os.path.join("data", "processed_images")
    MODELS_DIR = "models"

    # OCR Settings
    TESSERACT_CMD = r'/usr/local/bin/tesseract' # Adjust path as needed for your OS

    # Image Analysis Settings (Dummy values)
    IMAGE_MODEL_PATH = os.path.join(MODELS_DIR, "defect_detector_model.pth")
    DEFECT_THRESHOLD = 0.7

    # Risk Assessment Settings
    RISK_MODEL_PATH = os.path.join(MODELS_DIR, "risk_scorer_model.pkl")
    # Example underwriting rules (can be more complex, e.g., in a JSON file)
    UNDERWRITING_RULES = {
        "roof_condition": {"poor": "HIGH_RISK", "fair": "MEDIUM_RISK", "good": "LOW_RISK"},
        "foundation_cracks_detected": {"yes": "HIGH_RISK", "no": "LOW_RISK"},
        "property_age": {"gt_50_years": "MEDIUM_RISK", "lt_10_years": "LOW_RISK"},
        "flood_zone": {"high": "DECLINE", "medium": "ADDITIONAL_PREMIUM", "low": "STANDARD"},
        # Add more rules as needed
    }