import re
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AddressParser:
    
    @classmethod
    def parse(cls, address):
        address = address.upper()
        address_units = address.split(' AND ')
        if len(address_units) != 2:
            logger.error(f'Invalid address (cannot split into 2 units): {address}')
            return None

        address_unit_one = cls.__parse_address_unit(address_units[0])
        address_unit_two = cls.__parse_address_unit(address_units[1])
        return (
            '/'.join([address_unit_one, address_unit_two]),
            '/'.join([address_unit_two, address_unit_one])
        )

    @classmethod
    def parse_address_unit(cls, address_unit):
        address_unit = address_unit.replace(' ', '').upper()
        return cls.__parse_address_unit(address_unit)

    @classmethod
    def __parse_address_unit(cls, address_unit):
        address_values = address_unit.split(' ')
        address_values_lst = [cls.__parse_address_value(address_value) for address_value in address_values]
        return ' '.join(address_values_lst)

    @classmethod
    def __parse_address_value(cls, address_value):
        # check for ordinal value
        re_result = re.findall(r'\d+', address_value)
        if re_result:
            return re_result[0]

        # check for street_type
        if address_value in AddressParser.street_types:
            return AddressParser.street_types[address_value]

        # assume value is a descriptor
        return address_value

    street_types = {
        'ALLEY' : 'ALY',
        'AVENUE' : 'AV',
        'BOULEVARD' : 'BL',
        'CIRCLE' : 'CIR',
        'COURT' : 'CT',
        'COVE' : 'CV',
        'CANYON' : 'CYN',
        'DRIVE' : 'DR',
        'EAST' : 'E',
        'EXPRESSWAY' : 'EXPY',
        'HIGHWAY' : 'HWY',
        'LANE' : 'LN',
        'NORTH' : 'N',
        'NORTHEAST' : 'NE',
        'NORTHWEST' : 'NW',
        'PARKWAY' : 'PKWY',
        'PLACE' : 'PL',
        'PLAZA' : 'PLZ',
        'POINT' : 'PT',
        'ROAD' : 'RD',
        'SOUTH' : 'S',
        'SOUTHEAST' : 'SE',
        'SOUTHWEST' : 'SW',
        'SQUARE' : 'SQ',
        'STREET' : 'ST',
        'TERRACE' : 'TER',
        'TRAIL' : 'TR',
        'WAY' : 'WY',
        'WEST' : 'W'
    }