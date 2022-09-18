import logging

from app.dtos.user import Avatar, UserIn, UserOut

logger = logging.getLogger(__name__)


def retrieve_user_by_email(email: str):
    return UserOut(
        email=email,
        avatar=Avatar(background="#ff0000", emoji="stork"),
        streak=91,
    )


def create_user(user_data: UserIn, hashed_password: str):
    logger.info(hashed_password)
    return UserOut(
        email=user_data.email,
        avatar=Avatar(background="#ff0000", emoji="stork"),
        streak=91,
    )
