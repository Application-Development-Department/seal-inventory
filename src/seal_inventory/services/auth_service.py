from ldap3 import Server, Connection
import os


class AuthService:

    def authenticate(self, username: str, password: str) -> bool:
        server = Server(os.getenv("LDAP_SERVER"))

        # Try both formats dynamically
        possible_users = [
            f"{username}@Mects.local",   # UPN
            f"MECTS\\{username}",        # DOMAIN\user
        ]

        for user in possible_users:
            try:
                Connection(server, user=user, password=password, auto_bind=True)
                return True
            except Exception:
                continue

        return False