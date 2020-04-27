from .. import address_parser

def test_street_and_avenue():
    address = '31st street and 20th avenue'
    parsed_address = address_parser.AddressParser.parse(address)
    expected_result = ['31 ST/20 AV', '20 AV/31 ST']
    assert parsed_address[0] == expected_result[0]
    assert parsed_address[1] == expected_result[1]

def test_directions():
    directions = ['north', 'northeast', 'east', 'south east', 'south', 'south west', 
    'west', 'northwest']
    expected_result = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

    for index, direction in enumerate(directions):
        assert address_parser.AddressParser.parse_address_unit(direction) == expected_result[index]