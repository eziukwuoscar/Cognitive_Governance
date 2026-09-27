import os
from dataclasses import dataclass

# Mock identities for local development only, not real SSO credentials.
TEST_USERS = {
    "local-test-oscar": {
        "employee_id": "TEST-001",
        "email": "oscar@example.com",
        "identity_type": "human",
        "role": ["Associate"],
        "tenant_id": "none"
    }
}


@dataclass
class IdentityToken:
    employee_id: str
    email: str
    identity_type: str
    role: list[str]
    tenant_id: str
    
    
@dataclass
class Identity:
    token: IdentityToken


def get_caller_identity() -> Identity:
    """Look up a mock caller using the token supplied to the Moko process."""
    token = os.environ.get("MOKO_TEST_TOKEN")
    caller = TEST_USERS.get(token)

    if caller is None:
        raise PermissionError("Missing or invalid test credential")

    identity_token = IdentityToken(
        employee_id=caller["employee_id"],
        email=caller["email"],
        identity_type=caller["identity_type"],
        role=caller["role"].copy(),
        tenant_id=caller["tenant_id"],
    )

    return Identity(token=identity_token)
