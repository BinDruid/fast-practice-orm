from __future__ import annotations

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

from src.database.mixin_models import TimeStampedModel


class Post(TimeStampedModel, Model):
    id = fields.IntField(primary_key=True)
    author = fields.ForeignKeyField('models.User', related_name='posts')
    content = fields.TextField()

    def __str__(self):
        return f'{self.author}#{self.id}'


PostPydanticIn = pydantic_model_creator(Post, name='PostIn', include=('content',))
PostPydanticOut = pydantic_model_creator(Post, name='PostOut', include=('id', 'author', 'content'))
