import logging
from dataclasses import dataclass
from typing import Optional
from utils.logger import logger

@dataclass
class MessageHeader:
    sender_id: Optional[str]
    recipient_id: Optional[str]
    message_reference_number: Optional[str]
    message_type: Optional[str]
    version_number: Optional[str]

@dataclass
class BeginningOfMessage:
    message_name_code: Optional[str]
    document_message_number: Optional[str]
    message_function_code: Optional[str]

@dataclass
class DateTimePeriod:
    qualifier: Optional[str]
    period: Optional[str]

@dataclass
class FreeText:
    qualifier: Optional[str]
    text: Optional[str]

@dataclass
class Reference:
    qualifier: Optional[str]
    number: Optional[str]

@dataclass
class TransportDetails:
    stage_qualifier: Optional[str]
    mode_of_transport: Optional[str]
    carrier_id: Optional[str]
    carrier_name: Optional[str]
    transport_id: Optional[str]
    transport_name: Optional[str]
    transport_nationality: Optional[str]

@dataclass
class NameAndAddress:
    party_qualifier: Optional[str]
    party_id: Optional[str]
    name: Optional[str]
    address: Optional[str]
    city: Optional[str]
    country: Optional[str]

@dataclass
class GoodsItemDetails:
    item_number: Optional[str]
    number_of_packages: Optional[str]
    type_of_packages: Optional[str]

@dataclass
class Measurements:
    dimension_code: Optional[str]
    value: Optional[str]

@dataclass
class EquipmentDetails:
    qualifier: Optional[str]
    id_number: Optional[str]
    size_and_type: Optional[str]

def parse_edifact(edifact_message: str) -> dict:
    parsed_data = {
        "message_header": [],
        "beginning_of_message": [],
        "date_time_period": [],
        "free_text": [],
        "references": [],
        "transport_details": [],
        "name_and_address": [],
        "goods_item_details": [],
        "measurements": [],
        "equipment_details": []
    }

    def get_text_safe(elements, index):
        return elements[index] if index < len(elements) else None

    try:
        segments = edifact_message.strip().split("'")
        sender_id, recipient_id = None, None

        for segment in segments:
            elements = segment.split("+")
            tag = elements[0].split(":")[0].strip()

            logger.debug(f"Parsing segment: {segment}")

            if tag == "UNB":
                sender_id = get_text_safe(elements[2].split(":"), 0)
                recipient_id = get_text_safe(elements[3].split(":"), 0)
            elif tag == "UNH":
                parsed_data["message_header"].append(MessageHeader(
                    sender_id=sender_id,
                    recipient_id=recipient_id,
                    message_reference_number=get_text_safe(elements, 1),
                    message_type=get_text_safe(elements[2].split(":"), 0),
                    version_number=get_text_safe(elements[2].split(":"), 1)
                ))
            elif tag == "BGM":
                parsed_data["beginning_of_message"].append(BeginningOfMessage(
                    message_name_code=get_text_safe(elements, 1),
                    document_message_number=get_text_safe(elements, 2),
                    message_function_code=get_text_safe(elements, 3)
                ))
            elif tag == "DTM":
                date_time_info = get_text_safe(elements, 1).split(":")
                parsed_data["date_time_period"].append(DateTimePeriod(
                    qualifier=get_text_safe(date_time_info, 0),
                    period=get_text_safe(date_time_info, 1)
                ))
            elif tag == "FTX":
                parsed_data["free_text"].append(FreeText(
                    qualifier=get_text_safe(elements, 1),
                    text=get_text_safe(elements, 4)
                ))
            elif tag == "RFF":
                reference_info = get_text_safe(elements, 1).split(":")
                parsed_data["references"].append(Reference(
                    qualifier=get_text_safe(reference_info, 0),
                    number=get_text_safe(reference_info, 1)
                ))
            elif tag == "TDT":
                transport_info = get_text_safe(elements, 8).split(":::") if len(elements) > 8 else ["", "", ""]
                transport_name = transport_info[0]
                transport_nationality = None
                if ":" in transport_name:
                    transport_name, transport_nationality = transport_name.rsplit(":", 1)

                parsed_data["transport_details"].append(TransportDetails(
                    stage_qualifier=get_text_safe(elements, 1),
                    mode_of_transport=get_text_safe(elements, 3),
                    carrier_id=get_text_safe(elements[5].split(":::") if len(elements) > 5 else [""], 0),
                    carrier_name=get_text_safe(elements[5].split(":::") if len(elements) > 5 else [""], 1),
                    transport_id=transport_info[0],
                    transport_name=transport_name,
                    transport_nationality=transport_nationality
                ))
            elif tag == "LOC":
                loc_info = elements[2].split(":")
                loc_name = ":".join(loc_info[3:]) if len(loc_info) > 3 else None
                parsed_data["references"].append(Reference(
                    qualifier=get_text_safe(elements, 1),
                    number=get_text_safe(loc_info, 0)
                ))
                parsed_data["free_text"].append(FreeText(
                    qualifier=get_text_safe(elements, 1),
                    text=loc_name
                ))
            elif tag == "NAD":
                party_qualifier = get_text_safe(elements, 1)
                party_id = get_text_safe(elements, 2).split(":")[0]
                name = get_text_safe(elements, 3)
                address = get_text_safe(elements, 5)  # address está en la posición 5
                city = get_text_safe(elements, 6)    # city está en la posición 6
                country = get_text_safe(elements, 9) # country está en la posición 9

                parsed_data["name_and_address"].append(NameAndAddress(
                    party_qualifier=party_qualifier,
                    party_id=party_id,
                    name=name,
                    address=address if address else "",
                    city=city if city else "",
                    country=country if country else ""
                ))
            elif tag == "GID":
                parsed_data["goods_item_details"].append(GoodsItemDetails(
                    item_number=get_text_safe(elements, 1),
                    number_of_packages=get_text_safe(elements, 2).split(":")[0] if get_text_safe(elements, 2) else None,
                    type_of_packages=get_text_safe(elements, 2).split(":")[1] if get_text_safe(elements, 2) and ":" in get_text_safe(elements, 2) else None
                ))
            elif tag == "MEA":
                measurement_info = get_text_safe(elements, 3).split(":")
                parsed_data["measurements"].append(Measurements(
                    dimension_code=get_text_safe(elements, 2),
                    value=get_text_safe(measurement_info, 1) if len(measurement_info) > 1 else None
                ))
            elif tag == "EQD":
                parsed_data["equipment_details"].append(EquipmentDetails(
                    qualifier=get_text_safe(elements, 1),
                    id_number=get_text_safe(elements, 2),
                    size_and_type=get_text_safe(elements, 3)
                ))

        logger.info("EDIFACT message parsed successfully")
        return parsed_data
    except Exception as e:
        logger.error(f"Error parsing EDIFACT message: {e}")

    return parsed_data
