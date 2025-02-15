"""
Validation Service Module
Ensures farmer data meets required criteria.
Validates USA, INDIA and FRANCE farmers
"""


def validate_farmer_data(data):
    """
    Validates farmer data to ensure it meets business rules.

    Args:
        data (dict): Farmer data to validate.

    Raises:
        ValueError: If the farmer's data does not meet validation criteria.
    """
    if "name" not in data or not data["name"]:
        raise ValueError("Farmer name is required.")
    if "country" not in data or not data["country"]:
        raise ValueError("Farmer country is required.")
    if "crops" not in data or not isinstance(data["crops"], list) or not data["crops"]:
        raise ValueError("At least one crop must be specified.")
    if data.get("experience_years", 0) < 0:
        raise ValueError("Experience years cannot be negative.")

    # Country-specific validations
    if data["country"] == "India" and not any(
        crop in ["rice", "wheat"] for crop in data["crops"]
    ):
        raise ValueError("Farmers in India must grow either rice or wheat.")
    if data["country"] == "USA" and not any(
        crop in ["corn", "soybeans"] for crop in data["crops"]
    ):
        raise ValueError("Farmers in the USA must grow either corn or soybeans.")
    if data["country"] == "France" and "grapes" not in data["crops"]:
        raise ValueError("Farmers in France must grow grapes.")

    print("Validation successful.")
