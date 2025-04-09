import requests
from datetime import datetime
from enum import StrEnum


class AliasMode(StrEnum):
    UUID = "uuid"
    WORD = "word"


class SimpleLoginClient:
    BASE_URL: str = "https://app.simplelogin.io"

    def __init__(self, key: str):
        self.key: str = key

    def _headers(self) -> dict:
        return {"Authentication": self.key, "Content-Type": "application/json"}

    def _format_datetime(self, ts: str | None) -> str:
        if not ts:
            return "N/A"
        try:
            dt = datetime.fromisoformat(
                ts.replace("Z", "+00:00").replace("+00:00", "+0000")
            )
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return ts

    def list_aliases(
        self,
        page: int = 0,
        pinned: bool = False,
        disabled: bool = False,
        enabled: bool = False,
        query: str | None = None,
    ) -> list[dict] | None:
        params: dict = {"page_id": page}
        if pinned:
            params["pinned"] = True
        elif disabled:
            params["disabled"] = True
        elif enabled:
            params["enabled"] = True

        data: dict | None = {"query": query} if query else None

        try:
            r = requests.get(
                f"{self.BASE_URL}/api/v2/aliases",
                headers=self._headers(),
                params=params,
                json=data,
                timeout=10,
            )
        except requests.RequestException:
            return None

        if r.status_code != 200:
            return None

        aliases: list[dict] = r.json().get("aliases", [])
        result: list[dict] = []

        for alias in aliases:
            latest: dict = alias.get("latest_activity") or {}
            activity: str = (
                f"{latest.get('action', 'N/A')} ({self._format_datetime(latest.get('timestamp'))})"
                if latest
                else "N/A"
            )
            mailbox: str = (
                alias.get("mailboxes")[0]["email"] if alias.get("mailboxes") else "N/A"
            )
            result.append(
                {
                    "id": alias.get("id"),
                    "email": alias.get("email"),
                    "name": alias.get("name", ""),
                    "enabled": alias.get("enabled"),
                    "pinned": alias.get("pinned", False),
                    "mailbox": mailbox,
                    "latest_activity": activity,
                    "stats": {
                        "forwarded": alias.get("nb_forward", 0),
                        "replied": alias.get("nb_reply", 0),
                        "blocked": alias.get("nb_block", 0),
                    },
                    "note": alias.get("note", ""),
                }
            )
        return result

    def list_mailboxes(self) -> list[dict] | None:
        try:
            r = requests.get(
                f"{self.BASE_URL}/api/v2/mailboxes", headers=self._headers(), timeout=10
            )
        except requests.RequestException:
            return None

        if r.status_code != 200:
            return None

        return r.json().get("mailboxes", [])

    def _get_alias_options(self) -> dict | None:
        try:
            r = requests.get(
                f"{self.BASE_URL}/api/v5/alias/options",
                headers=self._headers(),
                timeout=10,
            )
        except requests.RequestException:
            return None

        if r.status_code != 200:
            return None

        return r.json()

    def create_custom_alias(
        self,
        prefix: str,
        mailbox_ids: list[int] = [],
        note: str = None,
        name: str = None,
        suffix: str = None,
    ) -> dict | None:
        options: dict | None = self._get_alias_options()
        if options is None:
            return None

        if not options.get("can_create", False):
            return None

        suffixes: list = options.get("suffixes", [])
        if not suffixes:
            return None

        suffix_ids: dict = {s["suffix"]: s["signed_suffix"] for s in suffixes}

        if suffix is None:
            suffix = list(suffix_ids.keys())[0]
        elif suffix not in suffix_ids:
            alt_suffix = suffix.lstrip("@")
            found = False
            for key in suffix_ids:
                if key.lstrip("@") == alt_suffix:
                    suffix = key
                    found = True
                    break
            if not found:
                return None

        data: dict = {"alias_prefix": prefix, "signed_suffix": suffix_ids[suffix]}
        if not mailbox_ids:
            mailboxes: list[dict] = self.list_mailboxes() or []
            if mailboxes:
                mailbox_ids = [m["id"] for m in mailboxes]
        if mailbox_ids:
            data["mailbox_ids"] = mailbox_ids
        if note:
            data["note"] = note
        if name:
            data["name"] = name

        try:
            r = requests.post(
                f"{self.BASE_URL}/api/v3/alias/custom/new",
                headers=self._headers(),
                json=data,
                timeout=10,
            )
        except requests.RequestException:
            return None

        if not r.ok:
            return None

        return r.json()

    def create_random_alias(self, mode=AliasMode.WORD, note: str = None) -> dict | None:
        params: dict = {}
        if mode:
            params["mode"] = mode.value

        data: dict = {}
        if note:
            data["note"] = note

        try:
            r = requests.post(
                f"{self.BASE_URL}/api/alias/random/new",
                headers=self._headers(),
                json=data,
                params=params,
                timeout=10,
            )
        except requests.RequestException:
            return None

        if not r.ok:
            return None

        return r.json()
