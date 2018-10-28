class CityOrdinance:
    """A Kansas City city ordinance.

    This class includes constants and methods for working with city ordinances.

    More info can be found here:
    https://library.municode.com/mo/kansas_city/codes/code_of_ordinances
    """

    CHAPTER_GENERAL = 1
    CHAPTER_ADMINISTRATION = 2
    CHAPTER_CONTRACTS = 3
    CHAPTER_ADVERTISING = 4
    CHAPTER_AVIATION = 6
    CHAPTER_AIR_QUALITY = 8
    CHAPTER_ALCOHOLIC_BEVERAGES = 10
    CHAPTER_AMUSEMENTS = 12
    CHAPTER_ANIMALS = 14
    CHAPTER_AUCTIONS = 16
    CHAPTER_BUILDINGS = 18
    CHAPTER_CABLE = 19
    CHAPTER_CIGARETTES = 20
    CHAPTER_CONDEMNATION_PROPERTY = 22
    CHAPTER_DRIVER_TRAINING = 24
    CHAPTER_FIRE_PREVENTION = 26
    CHAPTER_FENCE = 27
    CHAPTER_FLOODPLAIN = 28
    CHAPTER_FOOD = 30
    CHAPTER_GAS = 32
    CHAPTER_GEOGRAPHICAL = 33
    CHAPTER_HEALTH = 34
    CHAPTER_HOSPITALS = 36
    CHAPTER_HUMAN_RELATIONS = 38
    CHAPTER_ARTERIAL_STREET = 39
    CHAPTER_LICENSES = 40
    CHAPTER_DAY_LABOR = 41
    CHAPTER_MASSAGE = 42
    CHAPTER_SHORT_TERM_LOAN = 43
    CHAPTER_CORRECTIONS = 44
    CHAPTER_NOISE_CONTROL = 46
    CHAPTER_NUISANCE = 48
    CHAPTER_OFFENSES = 50
    CHAPTER_PARKS = 53
    CHAPTER_PAWNBROKERS = 54
    CHAPTER_PROPERTY_MAINTENANCE = 56
    CHAPTER_RAILROADS = 58
    CHAPTER_SEWER = 60
    CHAPTER_STORMWATER = 61
    CHAPTER_SOLID_WASTE = 62
    CHAPTER_EROSION = 63
    CHAPTER_STREET = 64
    CHAPTER_SURETY = 67
    CHAPTER_TAXATION = 68
    CHAPTER_TRAFFIC = 70
    CHAPTER_MOBILE_HOMES = 72
    CHAPTER_REDEVELOPMENT = 74
    CHAPTER_EASEMENTS = 75
    CHAPTER_VEHICLES_FOR_HIRE = 76
    CHAPTER_WATER = 78
    CHAPTER_ZONING = 88

    CHAPTER_TITLES = {
        CHAPTER_GENERAL: 'General Provisions',
        CHAPTER_ADMINISTRATION: 'Administration',
        CHAPTER_CONTRACTS: 'Contracts and Leases',
        CHAPTER_ADVERTISING: 'Advertising',
        CHAPTER_AVIATION: 'Airports and Aviation',
        CHAPTER_AIR_QUALITY: 'Air Quality',
        CHAPTER_ALCOHOLIC_BEVERAGES: 'Alcoholic Beverages',
        CHAPTER_AMUSEMENTS: 'Amusements and Commercial Recreation',
        CHAPTER_ANIMALS: 'Animals',
        CHAPTER_AUCTIONS: 'Auctions and Special Sales',
        CHAPTER_BUILDINGS: 'Buildings and Building Regulations',
        CHAPTER_CABLE: 'Cable Television',
        CHAPTER_CIGARETTES: '  Cigarettes',
        CHAPTER_CONDEMNATION_PROPERTY: 'Condemnation of Property',
        CHAPTER_DRIVER_TRAINING: 'Driver Training Schools and Instructors',
        CHAPTER_FIRE_PREVENTION: 'Fire Prevention and Protection',
        CHAPTER_FENCE: 'Fences and Walls',
        CHAPTER_FLOODPLAIN: 'Floodplain Management',
        CHAPTER_FOOD: 'Food and Food Products',
        CHAPTER_GAS: 'Gas and Oil',
        CHAPTER_GEOGRAPHICAL: 'Geographical Information System',
        CHAPTER_HEALTH: 'Health and Sanitation',
        CHAPTER_HOSPITALS: 'Hospitals and Similar Institutions',
        CHAPTER_HUMAN_RELATIONS: 'Human Relations',
        CHAPTER_ARTERIAL_STREET: 'Arterial Street Impact Fees',
        CHAPTER_LICENSES: 'Licenses And Miscellaneous Business Regulations',
        CHAPTER_DAY_LABOR: 'Day Labor Business',
        CHAPTER_MASSAGE: 'Massage Shops, Nude Modeling Studios and Body Painting Artists',
        CHAPTER_SHORT_TERM_LOAN: 'Short Term Loan Establishments',
        CHAPTER_CORRECTIONS: 'Corrections',
        CHAPTER_NOISE_CONTROL: 'Noise Control',
        CHAPTER_NUISANCE: 'Nuisances',
        CHAPTER_OFFENSES: 'Offenses and Miscellaneous Provisions',
        CHAPTER_PARKS: 'Parks, Recreation and Boulevards',
        CHAPTER_PAWNBROKERS: 'Pawnbrokers, Junk Dealers and Secondhand Dealers',
        CHAPTER_PROPERTY_MAINTENANCE: 'Property Maintenance Code',
        CHAPTER_RAILROADS: 'Railroads',
        CHAPTER_SEWER: 'Sewers and Sewage Disposal',
        CHAPTER_STORMWATER: 'Stormwater',
        CHAPTER_SOLID_WASTE: 'Solid Waste',
        CHAPTER_EROSION: 'Erosion and Sediment Control',
        CHAPTER_STREET: 'Streets, Sidewalks and Public Places',
        CHAPTER_SURETY: 'Surety Recovery Agents',
        CHAPTER_TAXATION: 'Taxation',
        CHAPTER_TRAFFIC: 'Traffic and Vehicles',
        CHAPTER_MOBILE_HOMES: 'Mobile Homes and Recreational Vehicles',
        CHAPTER_REDEVELOPMENT: 'Kansas City Redevelopment Ordinance',
        CHAPTER_EASEMENTS: 'Release of Easements',
        CHAPTER_VEHICLES_FOR_HIRE: 'Vehicles for Hire',
        CHAPTER_WATER: 'Water',
        CHAPTER_ZONING: 'Zoning and Development Code',
    }

    def __init__(self, chapter, ordinance):
        self.chapter = chapter
        self.ordinance = ordinance

    @property
    def chapter_title(self):
        title = CityOrdinance.CHAPTER_TITLES.get(self.chapter)

        if not title:
            title = '(Unknown Chapter)'

        return title

    def __str__(self):
        return 'Ordinance: %s (%s)' % (self.chapter, self.ordinance)
