from .to_sql_interface import ToSQLInterface


class OurPoint(ToSQLInterface):
    def __init__(self, longitude: float, latitude: float) -> None:
        self.longitude = longitude
        self.latitude = latitude

    # TODO: POINT(%s, %s) with params
    def to_sql(self) -> str:
        return f"POINT ({self.longitude}, {self.latitude})"

    @staticmethod
    def create_select_stmt(column_name: str) -> str:
        return f"ST_X({column_name}), ST_Y({column_name})"

    def __eq__(self, other_point: 'OurPoint') -> bool:
        return (isinstance(other_point, OurPoint) and
                self.longitude == other_point.longitude and
                self.latitude == other_point.latitude)

    def __repr__(self) -> str:
        return f"OurPoint(longitude={self.longitude}, latitude={self.latitude})"


ToSQLInterface.register(OurPoint)
