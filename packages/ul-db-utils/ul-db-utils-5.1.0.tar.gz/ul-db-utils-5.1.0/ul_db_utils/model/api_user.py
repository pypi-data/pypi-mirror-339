from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import mapped_column


from ul_db_utils.model.base_model import BaseModel
from ul_db_utils.modules.postgres_modules.db import db


class ApiUser(BaseModel):
    __tablename__ = 'api_user'
    __table_args__ = {"comment": "Пользователь API"}

    date_expiration = mapped_column(db.DateTime(), nullable=False, comment="Срок действия доступа")
    name = mapped_column(db.String(255), unique=True, nullable=False, comment="Имя пользователя")
    note = mapped_column(db.Text(), nullable=False, comment="Примечание")
    permissions = mapped_column(ARRAY(db.Integer()), nullable=False, comment="Список разрешений")
