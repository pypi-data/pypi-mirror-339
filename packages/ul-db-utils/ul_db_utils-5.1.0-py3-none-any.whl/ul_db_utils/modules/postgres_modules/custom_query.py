from typing import Dict, Any, Union, TYPE_CHECKING

from flask_sqlalchemy.query import Query

if TYPE_CHECKING:
    from sqlalchemy.orm.mapper import Mapper

from ul_db_utils.modules.postgres_modules.db import db


class CustomQuery(Query):  # type: ignore
    """Overwrite Base Query with additional filters"""

    def __new__(cls, *args: 'Mapper', **kwargs: Union[Any, Dict[str, Any]]) -> 'CustomQuery':
        # get new object Query
        obj = super(CustomQuery, cls).__new__(cls)
        # search arguments and remove from kwargs if found
        with_deleted = kwargs.pop('_with_deleted', False)
        # check args is not None
        if args:
            # initialize object Query
            super(CustomQuery, obj).__init__(*args, **kwargs)
            # filtering
            if hasattr(args[0], 'is_alive') and (not with_deleted):
                # only alive records
                return obj.filter_by(is_alive=True)
            return obj

        # return Query object if args not passed
        return obj

    def join(self, target, *props, **kwargs):  # type: ignore
        """
        Custom kwargs:
            `with_deleted` : filter join with is_alive = True,
            type: bool,
            default: False
        """
        if 'with_deleted' in kwargs and kwargs['with_deleted']:
            kwargs.pop('with_deleted')
            return super(Query, self).join(target, *props, **kwargs)
        elif hasattr(target, "is_alive"):
            return super(Query, self).join(target, *props, **kwargs).filter_by(is_alive=True)
        else:
            return super(Query, self).join(target, *props, **kwargs)

    def __init__(*args: 'Mapper', **kwargs: Union[Any, Dict[str, Any]]) -> None:
        pass

    def with_deleted(self) -> 'CustomQuery':
        """Method for get all records even inactive"""
        # return QueryWithSoftDelete.__new__
        return self.__class__(
            db.class_mapper(self._only_full_mapper_zero(methname='Base').class_),
            session=db.session(),
            _with_deleted=True,
        )
