import pandas as pd
import pytest

from erp_processminer.io_erp.mappings import apply_mapping


def test_apply_mapping_requires_case_id_column():
    df = pd.DataFrame(
        {
            "WRONG_ID": ["X-1"],
            "CREATION_DATE": pd.to_datetime(["2023-01-01"]),
        }
    )

    config = {
        "case_id": "CASE_ID",
        "tables": {
            "purchase_orders": {
                "entity_id": "CASE_ID",
                "activity": "'Create PO'",
                "timestamp": "CREATION_DATE",
            }
        },
    }

    with pytest.raises(ValueError):
        apply_mapping([df], config)
