from app.enrichment_service import enrich_data


def test_enrich_data_india():
    input_data = {
        "country": "USA",
        "state": "Georgia",
        "crops": ["Corn"],
    }
    enriched_data = enrich_data(input_data)
    assert enriched_data["region"] == "Georgia"
    assert enriched_data["is_enriched"] is True
