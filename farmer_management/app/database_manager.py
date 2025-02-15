"""
Database Manager Module
Simulates database operations for storing and retrieving farmer data.
"""


class DatabaseManager:
    """
    Manages database operations for farmer data.
    """

    def __init__(self):
        self.database = {}  # Simulating an in-memory database

    def save_farmer(self, farmer_id, data):
        """
        Saves farmer data to the database.

        Args:
            farmer_id (str): Farmer's unique ID.
            data (dict): Farmer's data to save.
        """
        self.database[farmer_id] = data
        print(f"Farmer {farmer_id} saved to database.")

    def get_farmer(self, farmer_id):
        """
        Retrieves farmer data from the database.

        Args:
            farmer_id (str): Farmer's unique ID.

        Returns:
            dict: Farmer's data.
        """
        return self.database.get(farmer_id, {})

    def delete(self, farmer_id: int) -> None:
        """
        Deletes farmer data from the database.

        Args:
            farmer_id (int): ID of the farmer to delete.
        """
        print(f"Deleting from DB: Farmer ID {farmer_id}")
