import pytest
import uuid


@pytest.mark.order(1)
def test_voucher_lifecycle(session, base_url, site_id):
    """
    Full voucher workflow:
    1. Create voucher
    2. Fetch details
    3. Delete it
    4. Confirm deletion
    """

    # Step 1: Create a new voucher
    payload = {
        "count": 1,
        "name": f"autotest-{uuid.uuid4()}",
        "authorizedGuestLimit": 1,
        "timeLimitMinutes": 60,
        "dataUsageLimitMBytes": 100,
        "rxRateLimitKbps": 2000,
        "txRateLimitKbps": 2000
    }

    create_resp = session.post(f"{base_url}/v1/sites/{site_id}/hotspot/vouchers", json=payload)
    assert create_resp.status_code == 201, f"Unexpected status: {create_resp.status_code}, body: {create_resp.text}"

    vouchers = create_resp.json().get("vouchers")
    assert vouchers and isinstance(vouchers, list), "Invalid voucher response format"
    voucher_id = vouchers[0].get("id") or vouchers[0].get("_id")
    assert voucher_id, "Voucher ID missing in response"

    # Step 2: Retrieve voucher details
    get_resp = session.get(f"{base_url}/v1/sites/{site_id}/hotspot/vouchers/{voucher_id}")
    assert get_resp.status_code == 200, f"Failed to fetch voucher details: {get_resp.text}"

    details = get_resp.json()
    assert details["name"].startswith("autotest-"), "Voucher name mismatch"
    assert details["timeLimitMinutes"] == 60, "Time limit not applied correctly"

    # Step 3: Delete the voucher
    del_resp = session.delete(f"{base_url}/v1/sites/{site_id}/hotspot/vouchers/{voucher_id}")
    assert del_resp.status_code == 200, f"Failed to delete voucher: {del_resp.text}"

    # Step 4: Confirm it no longer exists
    verify_resp = session.get(f"{base_url}/v1/sites/{site_id}/hotspot/vouchers/{voucher_id}")
    assert verify_resp.status_code in [400, 404], "Expected voucher to be deleted"