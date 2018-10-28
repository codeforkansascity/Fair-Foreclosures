from datetime import datetime
from dateutil.parser import parse
from sodapy import Socrata

class ServiceRequestCallException(Exception):
    """An exception that may be raised by the ServiceRequestCall class."""
    pass

class Coordinates:
    """A pair of latitude/longitude coordinates."""

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return 'Coordintes: (%s, %s)' % (str(self.lat), str(self.lon))

class ServiceRequestCall:
    """A service request call, also known as a 311 call.

    This class represents a record from the KCMO 311 Call Center Service
    Requests dataset. This call center fields various service requests from
    KCMO residents.

    https://data.kcmo.org/311/311-Call-Center-Service-Requests/7at3-sxhp
    """

    API_DATASET_NAME = 'data.kcmo.org'
    API_RESOURCE_ID = 'cyqf-nban'

    DAYS_OPEN_0_TO_30 = 0
    DAYS_OPEN_31_TO_60 = 30
    DAYS_OPEN_61_TO_90 = 60
    DAYS_OPEN_90_PLUS = 90

    def __init__(self,
                 case_id=0,
                 source='',
                 department='',
                 work_group='',
                 request_type='',
                 category='',
                 type='',
                 detail='',
                 creation_date_time=None,
                 exceeded_est_timeframe=False,
                 closed_date=None,
                 days_to_close=0,
                 street_address='',
                 zip_code=0,
                 neighborhood='',
                 county='',
                 council_district=0,
                 police_district='',
                 parcel_id=0,
                 coordinates=None,
                 case_url='',
                 days_open=0):
        self.case_id = case_id
        self.source = source
        self.department = department
        self.work_group = work_group
        self.request_type = request_type
        self.category = category
        self.type = type
        self.detail = detail
        self.creation_date_time = creation_date_time
        self.exceeded_est_timeframe = exceeded_est_timeframe
        self.closed_date = closed_date
        self.days_to_close = days_to_close
        self.street_address = street_address
        self.zip_code = zip_code
        self.neighborhood = neighborhood
        self.county = county
        self.council_district = council_district
        self.police_district = police_district
        self.parcel_id = parcel_id
        self.coordinates = coordinates
        self.case_url = case_url
        self.days_open = days_open

    @staticmethod
    def from_json(json_data):
        """Convert JSON data (obtained from the KCMO Open Data API) to a
        ServiceRequestCall object.
        """

        def to_bool(value):
            return value == 'Y'

        def to_date(value):
            return parse(value) if value else None

        def to_time(value):
            return parse(value).time() if value else None

        def to_int(value):
            return int(value) if value else 0

        service_request = ServiceRequestCall(
             case_id=to_int(json_data.get('case_id')),
             source=json_data.get('source'),
             department=json_data.get('department'),
             work_group=json_data.get('work_group'),
             request_type=json_data.get('request_type'),
             category=json_data.get('category'),
             type=json_data.get('type'),
             detail=json_data.get('detail'),
             exceeded_est_timeframe=to_bool(json_data.get('exceeded_est_timeframe')),
             closed_date=to_date(json_data.get('closed_date')),
             days_to_close=to_int(json_data.get('days_to_close')),
             street_address=json_data.get('street_address'),
             zip_code=to_int(json_data.get('zip_code')),
             neighborhood=json_data.get('neighborhood'),
             county=json_data.get('county'),
             council_district=to_int(json_data.get('council_district')),
             police_district=json_data.get('police_district'),
             parcel_id=to_int(json_data.get('parcel_id_no')),
             coordinates=None,
             case_url=json_data.get('case_url'),
             days_open=to_int(json_data.get('days_open')),
        )

        creation_date = to_date(json_data.get('creation_date'))
        creation_time = to_time(json_data.get('creation_time'))
        if creation_date and creation_time:
            creation_date_time = datetime.combine(creation_date, creation_time)
        else:
            creation_date_time = None
        service_request.creation_date_time = creation_date_time

        service_request.coordinates = Coordinates(
            json_data.get('latitude'),
            json_data.get('longitude'),
        )

        days_open = json_data.get('days_open')
        service_request.days_open = None if days_open is None else to_int(days_open)

        return service_request

    @staticmethod
    def fetch(app_token, search_params, limit=5000):
        """Fetch a list of ServiceRequestCall objects from the KCMO Open Data
        API. `search_params` is a list of search critera as allowed by the
        Socrata SoQL query language (https://dev.socrata.com/docs/queries/).
        All given parameters will be combined using 'AND' in the query.
        By default, we limit the results to 5000 records but you can specify
        a different limit with the `limit` parameter.
        """

        with Socrata(ServiceRequestCall.API_DATASET_NAME, app_token) as client:
            where_clause = ' and '.join(search_params)

            # Raises a requests.exceptions.HTTPError if bad criteria is given
            service_requests = client.get(
                ServiceRequestCall.API_RESOURCE_ID,
                where=where_clause,
                limit=limit,
            )

        return [ServiceRequestCall.from_json(rec) for rec in service_requests]

    @staticmethod
    def fetch_by_address(app_token, address):
        """Fetch a list of ServiceRequestCall objects from the KCMO Open Data
        API for a single address. Partial addresses can be given, but must
        match the beginning of the street address.
        """

        return ServiceRequestCall.fetch(
            app_token,
            ["street_address like '%s%%'" % address.upper()],
        )

    @property
    def is_open(self):
        return self.closed_date is None

    @property
    def is_closed(self):
        return not self.is_open
