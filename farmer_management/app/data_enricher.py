"""
Data Enricher Module
Applies enrichment rules to farmer data based on country and expertise.
"""


class DataEnricher:
    """
    Enriches farmer data with country-specific rules and additional attributes.
    """

    def enrich(self, data):
        """
        Enriches data based on the farmer's country.

        Args:
            data (dict): Farmer data to enrich.

        Returns:
            dict: Enriched farmer data.
        """
        country = data.get("country")
        if country == "India":
            return self._enrich_india(data)
        elif country == "USA":
            return self._enrich_usa(data)
        elif country == "France":
            return self._enrich_france(data)
        else:
            raise ValueError(f"No enrichment rules defined for country: {country}")

    def _enrich_india(self, data):
        """
        Adds enrichment rules for farmers in India.
        """
        data["subsidy_eligibility"] = data.get("experience_years", 0) > 3
        data["crop_expertise"] = (
            "Rice" if "rice" in data.get("crops", []) else "General"
        )
        return data

    def _enrich_usa(self, data):
        """
        Adds enrichment rules for farmers in the USA.
        """
        data["crop_insurance"] = "Premium Plan"
        data["crop_expertise"] = (
            "Corn" if "corn" in data.get("crops", []) else "General"
        )
        return data

    def _enrich_france(self, data):
        """
        Adds enrichment rules for farmers in France.
        """
        data["farming_guidelines"] = "Follow EU standards"
        data["crop_expertise"] = (
            "Grapes" if "grapes" in data.get("crops", []) else "General"
        )
        return data
