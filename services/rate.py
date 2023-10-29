import json
import os
from typing import List

current_dir = os.path.dirname(os.path.abspath(__file__))
json_filepath = os.path.join(current_dir, '..', 'data', 'inventory.json')


class RoomType:
    def __init__(self, bookableRate, totalRate, totalRateInclusive, code, currency, roomDescription):
        self.bookableRate = bookableRate
        self.totalRate = totalRate
        self.totalRateInclusive = totalRateInclusive
        self.code = code
        self.currency = currency
        self.roomDescription = roomDescription


class RatePlan:
    def __init__(self, hotelId, code, inDate, outDate, roomType):
        self.hotelId = hotelId
        self.code = code
        self.inDate = inDate
        self.outDate = outDate
        self.roomType = roomType


class Result:
    def __init__(self, ratePlans: List[RatePlan]):
        self.ratePlans = ratePlans


def get_rates(hotelIds: List[str], inDate: str, outDate: str) -> Result:
    with open(json_filepath, 'r') as file:
        data = json.load(file)

    filtered_data = [rate for rate in data if
                     rate['hotelId'] in hotelIds and rate['inDate'] >= inDate and rate['outDate'] <= outDate]
    ratePlans = []
    for rate in filtered_data:
        roomType_data = rate['roomType']
        roomType = RoomType(
            bookableRate=roomType_data['bookableRate'],
            totalRate=roomType_data['totalRate'],
            totalRateInclusive=roomType_data['totalRateInclusive'],
            code=roomType_data['code'],
            currency=roomType_data.get('currency', 'USD'),
            roomDescription=roomType_data.get('description', '')
        )

        ratePlan = RatePlan(
            hotelId=rate['hotelId'],
            code=rate['code'],
            inDate=rate['inDate'],
            outDate=rate['outDate'],
            roomType=roomType
        )

        ratePlans.append(ratePlan)

    result = Result(ratePlans=ratePlans)
    return result
