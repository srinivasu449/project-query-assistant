from app.country_api_manager import CountryAPIManager
from app.data_enricher import DataEnricher
from app.database_manager import DatabaseManager
from app.event_handler import EventHandler
from app.validation_service import validate_farmer_data


def main():
    # Initialize components
    country_api_manager = CountryAPIManager()
    data_enricher = DataEnricher()
    database_manager = DatabaseManager()
    event_handler = EventHandler(data_enricher, country_api_manager, database_manager)

    # Example farmer data
    farmer_data = {
        "name": "John Doe",
        "country": "USA",
        "crops": ["corn", "wheat"],
        "experience_years": 5,
    }

    try:
        # Validate data
        validate_farmer_data(farmer_data)

        # Process and send data
        farmer_id = "farmer_123"
        response = event_handler.process_farmer_data(farmer_id, farmer_data)
        print("Response:", response)
    except ValueError as e:
        print("Validation Error:", e)


if __name__ == "__main__":
    main()
