from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column

from ul_db_utils.model.base_user_log_model import BaseUserLogModel
from ul_db_utils.model.methods.make_immutable_column import make_immutable_column
from ul_db_utils.modules.postgres_modules.custom_query import CustomQuery
from ul_db_utils.modules.postgres_modules.db import db


class MediaFileDownloadLink(BaseUserLogModel):
    """
      Model for media-storage-service
      git: /unic-lab/libraries/common-services/media-storage

      signature: str, signature of date_expired and media_file_id for purpose of public file download
      date_expired: datetime, date of link expiration
      """
    __tablename__ = 'media_file_download_link'

    media_file_id = mapped_column(UUID(as_uuid=True), db.ForeignKey('media_file.id'), nullable=False)

    signature = mapped_column(db.String, nullable=False)  # not updatable
    date_expired = mapped_column(db.DateTime, nullable=False)  # not updatable

    media_file = relationship(
        'MediaFile',
        foreign_keys=[media_file_id],
        query_class=CustomQuery,
        uselist=False,
        lazy='joined',
    )


make_immutable_column(MediaFileDownloadLink.signature)
make_immutable_column(MediaFileDownloadLink.media_file_id)
make_immutable_column(MediaFileDownloadLink.date_expired)
