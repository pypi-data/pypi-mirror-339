from typing import Optional, TypedDict

HowToResolve = TypedDict("HowToResolve", {"ENGLISH": str, "SIMPLIFIED_CHINESE": str})


class KebleException(Exception):
    def __init__(
        self,
        *,
        # internal, server side
        alert_admin: bool = False,
        function_identifier: Optional[str] = None,
        admin_note: Optional[str] = None,
        # client side, for end user
        status_code: int = 400,
        how_to_resolve: Optional[HowToResolve] = None,
    ):
        self.status_code = status_code
        self.alert_admin = alert_admin
        self.how_to_resolve = how_to_resolve
        self.function_identifier = function_identifier
        self.admin_note = admin_note

    def __str__(self):
        base_message = f"[{self.__class__.__name__}] "
        metadata = []

        if self.function_identifier:
            metadata.append(f"Function: {self.function_identifier}")
        if self.admin_note:
            metadata.append(f"Admin Note: {self.admin_note}")
        if self.alert_admin:
            metadata.append("Alert Admin: True")

        return base_message + (f" | {' | '.join(metadata)}" if metadata else "")

    @property
    def exception_name(self):
        return self.__class__.__name__
