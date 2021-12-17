from tortoise import fields, models


class AutomaticComment(models.Model):
    url = fields.TextField()
    automatic_comment = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.url
