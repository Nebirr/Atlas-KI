from __future__ import annotations
from atlas.atlas_gui.services.settings_service import verify_user, create_user

class AuthService:
    def __init__ (self, seed_user: tuple[str, str] | None = ("admin", "test")):
        if seed_user:
            u, p = seed_user
            try:
                if not verify_user(u, p):
                    create_user(u, p)
            except Exception:
                pass

    def verify(self, username: str, password: str) -> bool:
        return verify_user(username, password)