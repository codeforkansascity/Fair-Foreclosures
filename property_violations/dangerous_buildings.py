from dateutil.parser import parse
from sodapy import Socrata

class DangerousBuildingException(Exception):
    """An exception that may bbe raised by the DangerousBuilding class."""
    pass

class Coordinates:
    """A pair of latitude/longitude coordinates."""

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return 'Coordintes: (%s, %s)' % (str(self.lat), str(self.lon))

class DangerousBuilding:
    """A dangerous building record.

    This class represents a single dangerous building record from the KCMO Open
    Data API.

    https://data.kcmo.org/Property/Dangerous-Buildings-List/ax3m-jhxx
    """

    API_DATASET_NAME = 'data.kcmo.org'
    API_RESOURCE_ID = 'rm2v-mbk5'

    # 'Status of Case' constants
    STATUS_DEMOLITION_IN_PROGRESS = 'Demolition By Owner In Progress'
    STATUS_IN_BID_PROCESS = 'In Bid Process'
    STATUS_NOTICE_ISSUED_ASBESTOS = 'Notice to Proceed Issued (Asbestos Removal)'
    STATUS_NOTICE_ISSUED_DEMOLITION = 'Notice to Proceed Issued (Demolition)'
    STATUS_ON_HOLD = 'On Hold'
    STATUS_ONGOING = 'Ongoing Case'
    STATUS_PRE_BID = 'Pre-Bid Process Ongoing'
    STATUS_REHAB_IN_PROGRESS = 'Rehab By Owner In Progress'
    STATUS_REPAIR = 'Repair Case'

    def __init__(self,
                 casenumber=0,
                 address='',
                 zip_code=0,
                 case_opened=None,
                 kivapin=0,
                 statusofcase='',
                 location_city='',
                 location_address='',
                 location_zip='',
                 location_state='',
                 coordinates=None):
        self.casenumber = casenumber
        self.address = address
        self.zip_code = zip_code
        self.case_opened = case_opened
        self.kivapin = kivapin
        self.statusofcase = statusofcase
        self.location_city = location_city
        self.location_address = location_address
        self.location_zip = location_zip
        self.location_state = location_state
        self.coordinates = coordinates

    @staticmethod
    def from_json(json_data):
        """Convert JSON data (obtained from the KCMO Open Data API) to a
        DangerousBuilding object.
        """

        def to_date(value):
            return parse(value) if value else None

        def to_int(value):
            return int(value) if value else 0

        dangerous_building = DangerousBuilding(
            casenumber=to_int(json_data.get('casenumber')),
            address=json_data.get('address'),
            zip_code=to_int(json_data.get('zip_code')),
            case_opened=to_date(json_data.get('case_opened')),
            kivapin=to_int(json_data.get('kivapin')),
            statusofcase=json_data.get('statusofcase'),
            location_city=json_data.get('location_city'),
            location_address=json_data.get('location_address'),
            location_zip=json_data.get('location_zip'),
            location_state=json_data.get('location_state'),
        )

        dangerous_building.coordinates = Coordinates(
            json_data.get('latitude'),
            json_data.get('longitude'),
        )

        return dangerous_building

    @staticmethod
    def fetch(app_token, search_params, limit=5000):
        """Fetch a list of DangerousBuilding objects from the KCMO Open Data
        API. `search_params` is a list of search critera as allowed by the
        Socrata SoQL query language (https://dev.socrata.com/docs/queries/).
        All given parameters will be combined using 'AND' in the query.
        """

        with Socrata(DangerousBuilding.API_DATASET_NAME, app_token) as client:
            where_clause = ' and '.join(search_params)

            # Raises a requests.exceptions.HTTPError if bad criteria is given
            dangerous_buildings = client.get(
                DangerousBuilding.API_RESOURCE_ID,
                where=where_clause,
                limit=limit,
            )

        return [DangerousBuilding.from_json(rec) for rec in dangerous_buildings]

    @staticmethod
    def fetch_by_address(app_token, address):
        """Fetch a list of DangerousBuilding objects from the KCMO Open Data
        API for a single address. Partial addresses can be given, but must
        match the beginning of the street address.
        """

        return DangerousBuilding.fetch(
            app_token,
            ["address like '%s%%'" % address],
        )

    @staticmethod
    def fetch_by_pin(app_token, pin):
        """Fetch a list of DangerousBuilding objects from the KCMO Open Data
        API for a single KIVA pin.
        """

        return DangerousBuilding.fetch(
            app_token,
            ["kivapin = %d" % pin],
        )

    @property
    def as_csv(self):
        """Returns a string containing this object's properties in CSV format."""

        fields = [
            "%d" % self.casenumber,
            '"%s"' % self.address,
            '"%s"' % self.zip_code,
            '"%s"' % self.case_opened.strftime('%Y-%m-%d'),
            "%d" % self.kivapin,
            '"%s"' % self.statusofcase,
            '"%s"' % self.location_city,
            '"%s"' % self.location_address,
            '"%s"' % self.location_zip,
            '"%s"' % self.location_state,
            '%s' % self.coordinates.lat,
            '%s' % self.coordinates.lon,
        ]

        return ','.join(fields)
