from aiogram.types import User as TgUser
from aiogram.utils.web_app import WebAppUser
from tortoise.fields import BigIntField, BooleanField, CharField, IntEnumField
from x_model.models import Model
from x_model.types import BaseUpd

from x_auth.enums import Lang, Role
from x_auth.types import AuthUser


class UserTg(Model):
    id: int = BigIntField(True, description="tg id")
    username: str | None = CharField(63, unique=True, null=True)
    first_name: str | None = CharField(63)
    last_name: str | None = CharField(31, null=True)
    blocked: bool = BooleanField(default=False)
    lang: Lang | None = IntEnumField(Lang, default=Lang.ru, null=True)
    role: Role = IntEnumField(Role, default=Role.READER)

    def get_auth(self) -> AuthUser:
        return AuthUser.model_validate(self, from_attributes=True)

    @classmethod
    async def tg2in(cls, u: TgUser | WebAppUser, blocked: bool = None) -> BaseUpd:
        user = cls.validate(
            {**u.model_dump(), "username": u.username or u.id, "lang": u.language_code and Lang[u.language_code]}
        )
        if blocked is not None:
            user.blocked = blocked
        return user

    @classmethod
    async def is_blocked(cls, sid: str) -> bool:
        return (await cls[int(sid)]).blocked

    class Meta:
        abstract = True
