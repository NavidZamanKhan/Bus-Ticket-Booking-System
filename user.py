from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Admin:
    username: str
    password: str


class AdminRegistry:
    def __init__(self) -> None:
        self._users: Dict[str, Admin] = {}

    def signup(self, username: str, password: str) -> bool:
        username_key = username.strip().lower()
        if not username_key or not password:
            return False
        if username_key in self._users:
            return False
        self._users[username_key] = Admin(username=username.strip(), password=password)
        return True

    def login(self, username: str, password: str) -> bool:
        username_key = username.strip().lower()
        user: Optional[Admin] = self._users.get(username_key)
        return bool(user and user.password == password)

    def has_any_admin(self) -> bool:
        return len(self._users) > 0


