class SerializerMixin:
    def serialize(self):
        return {column_name.name: getattr(self, column_name.name)for column_name in self.__table__.columns}