from uuid import UUID


class ProfileAlreadyExistsError(Exception):
    def __init__(self, user_id: UUID) -> None:
        super().__init__(f"A profile already exists for user {user_id}")
        self.user_id = user_id


class ProfileNotFoundError(Exception):
    def __init__(self, user_id: UUID) -> None:
        super().__init__(f"No profile found for user {user_id}")
        self.user_id = user_id
