from app.models.tortoise import AutomaticComment
from typing import Union


async def get(id: int) -> Union[dict, None]:
    comment = await AutomaticComment.filter(id=id).first().values()
    if comment:
        return comment[0]
    return None
