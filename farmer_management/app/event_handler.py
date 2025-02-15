"""
Event Handler Module
Orchestrates data validation, enrichment, database storage, and API communication.
"""


class EventHandler:
    """
    Handles events related to farmer data.
    """

    def __init__(self, data_enricher, country_api_manager, database_manager):
        self.data_enricher = data_enricher
        self.country_api_manager = country_api_manager
        self.database_manager = database_manager

    def process_farmer_data(self, farmer_id, data):
        """
        Processes and enriches farmer data, then sends it to the country's API.

        Args:
            farmer_id (str): Farmer's unique ID.
            data (dict): Farmer's original data.

        Returns:
            dict: Response from the country's API.
        """
        enriched_data = self.data_enricher.enrich(data)
        self.database_manager.save_farmer(farmer_id, enriched_data)
        return self.country_api_manager.send_to_country_api(enriched_data)
