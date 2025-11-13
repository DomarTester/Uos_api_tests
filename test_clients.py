import pytest
import uuid


@pytest.mark.order(1)
def test_get_clients_list(session, base_url, site_id):
    """
    Validate that the API returns a paginated list of connected clients.
    """

    response = session.get(f"{base_url}/v1/sites/{site_id}/clients")
    assert response.status_code == 200, f"Unexpected status: {response.status_code}, body: {response.text}"

    data = response.json()
    assert "data" in data, "Response must include 'data' field"
    assert isinstance(data["data"], list), "'data' should be a list"
    assert "offset" in data and "limit" in data, "Pagination fields missing"


@pytest.mark.order(2)
def test_get_single_client_details(session, base_url, site_id):
    """
    Retrieve detailed information about a single connected client.
    If no clients are found, the test will be skipped.
    """

    clients = session.get(f"{base_url}/v1/sites/{site_id}/clients").json().get("data", [])
    if not clients:
        pytest.skip("No clients found to fetch details.")

    client_id = clients[0].get("id") or clients[0].get("_id")
    assert client_id, "Client missing ID field"

    response = session.get(f"{base_url}/v1/sites/{site_id}/clients/{client_id}")
    assert response.status_code == 200, f"Failed to fetch client details: {response.text}"

    details = response.json()
    assert "macAddress" in details, "Client details missing MAC address"
    assert "type" in details, "Client details missing connection type"


@pytest.mark.order(3)
def test_authorize_guest_access(session, base_url, site_id):
    """
    Simulate a client authorization via AUTHORIZE_GUEST_ACCESS.
    A mock client UUID is used, as the endpoint requires a valid format.
    """

    fake_client_id = str(uuid.uuid4())
    payload = {
        "action": "AUTHORIZE_GUEST_ACCESS",
        "timeLimitMinutes": 5,
        "dataUsageLimitMBytes": 10,
        "rxRateLimitKbps": 2000,
        "txRateLimitKbps": 2000
    }

    response = session.post(
        f"{base_url}/v1/sites/{site_id}/clients/{fake_client_id}/actions",
        json=payload
    )

    assert response.status_code in [200, 400, 404], f"Unexpected status: {response.status_code}"

    body = response.json()
    assert isinstance(body, dict), "Response must be JSON object"
    if response.status_code == 200:
        assert body.get("action") == "AUTHORIZE_GUEST_ACCESS", "Action mismatch"


@pytest.mark.order(4)
def test_delete_voucher_by_filter(session, base_url, site_id):
    """
    Demonstrate DELETE with a filter query parameter.
    Removes vouchers with names matching 'autotest*'.
    """

    filter_query = "name.like('autotest*')"
    response = session.delete(f"{base_url}/v1/sites/{site_id}/hotspot/vouchers", params={"filter": filter_query})
    assert response.status_code == 200, f"Unexpected status: {response.status_code}, body: {response.text}"

    result = response.json()
    assert "vouchersDeleted" in result, "Missing 'vouchersDeleted' in response"
    assert isinstance(result["vouchersDeleted"], int), "Invalid response type for 'vouchersDeleted'"
