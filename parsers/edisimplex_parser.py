import logging
from dataclasses import dataclass
from typing import List, Optional
from utils.logger import logger

@dataclass
class MessageHeader:
    sender_id: Optional[str]
    recipient_id: Optional[str]
    message_reference_number: Optional[str] = None
    message_type: Optional[str] = "COPARN"  # Default message type

@dataclass
class BeginningOfMessage:
    document_message_number: Optional[str]
    message_function_code: Optional[str]
    message_name_code: Optional[str] = "135"  # Default message name code

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

def get_text_safe(elements, index):
    text = elements[index] if index < len(elements) else None
    return text.strip() if text else text

def parse_edisimplex(edisimplex_message: str) -> dict:
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

    lines = edisimplex_message.strip().split('\n')

    try:
        for line in lines:
            elements = line.split('^')
            tag = elements[0].strip()

            logger.debug(f"Parsing segment: {line}")

            if tag == "ENV001":
                sender_id = get_text_safe(elements, 1)
                recipient_id = get_text_safe(elements, 2)
                parsed_data["message_header"].append(MessageHeader(
                    sender_id=sender_id,
                    recipient_id=recipient_id
                ))
            elif tag == "COPE02000":
                parsed_data["beginning_of_message"].append(BeginningOfMessage(
                    document_message_number=get_text_safe(elements, 1),
                    message_function_code=None
                ))
            elif tag == "COPE02001":
                parsed_data["beginning_of_message"][0].message_name_code = "135"
                parsed_data["beginning_of_message"][0].document_message_number = get_text_safe(elements, 1)
                parsed_data["beginning_of_message"][0].message_function_code = get_text_safe(elements, 2)
            elif tag == "COPE02002":
                parsed_data["date_time_period"].append(DateTimePeriod(
                    qualifier="137",
                    period=get_text_safe(elements, 1)
                ))
            elif tag == "COPE02003":
                parsed_data["free_text"].append(FreeText(
                    qualifier=get_text_safe(elements, 1),
                    text=get_text_safe(elements, 2)
                ))
            elif tag == "COPE02004":
                parsed_data["references"].append(Reference(
                    qualifier=get_text_safe(elements, 1),
                    number=get_text_safe(elements, 2)
                ))
            elif tag == "COPE02005":
                parsed_data["transport_details"].append(TransportDetails(
                    stage_qualifier=get_text_safe(elements, 1),
                    mode_of_transport=get_text_safe(elements, 2),
                    carrier_id=get_text_safe(elements, 3),
                    carrier_name=get_text_safe(elements, 4),
                    transport_id=get_text_safe(elements, 5),
                    transport_name=get_text_safe(elements, 6),
                    transport_nationality=None
                ))
            elif tag == "COPE02006":
                parsed_data["references"].append(Reference(
                    qualifier=get_text_safe(elements, 1),
                    number=get_text_safe(elements, 2)
                ))
                if len(elements) > 3:
                    parsed_data["free_text"].append(FreeText(
                        qualifier=get_text_safe(elements, 1),
                        text=get_text_safe(elements, 3)
                    ))
            elif tag == "COPE02007":
                parsed_data["date_time_period"].append(DateTimePeriod(
                    qualifier="133",
                    period=get_text_safe(elements, 1)
                ))
            elif tag == "COPE02008":
                parsed_data["name_and_address"].append(NameAndAddress(
                    party_qualifier=get_text_safe(elements, 1),
                    party_id=get_text_safe(elements, 2),
                    name=get_text_safe(elements, 3),
                    address=get_text_safe(elements, 4) if len(elements) > 4 else "",
                    city=get_text_safe(elements, 5) if len(elements) > 5 else "",
                    country=get_text_safe(elements, 6) if len(elements) > 6 else ""
                ))
            elif tag == "COPE02010":
                parsed_data["goods_item_details"].append(GoodsItemDetails(
                    item_number=get_text_safe(elements, 1),
                    number_of_packages=get_text_safe(elements, 2),
                    type_of_packages=get_text_safe(elements, 3)
                ))
            elif tag == "COPE02011":
                parsed_data["free_text"].append(FreeText(
                    qualifier=None,
                    text=get_text_safe(elements, 1)
                ))
            elif tag == "COPE02012":
                parsed_data["free_text"].append(FreeText(
                    qualifier=get_text_safe(elements, 1),
                    text=get_text_safe(elements, 2)
                ))
            elif tag == "COPE02013":
                parsed_data["measurements"].append(Measurements(
                    dimension_code=None,
                    value=get_text_safe(elements, 1)
                ))
            elif tag == "COPE02014":
                parsed_data["references"].append(Reference(
                    qualifier=get_text_safe(elements, 1),
                    number=get_text_safe(elements, 2)
                ))
            elif tag == "COPE02017":
                parsed_data["equipment_details"].append(EquipmentDetails(
                    qualifier=get_text_safe(elements, 1),
                    id_number=get_text_safe(elements, 2),
                    size_and_type=get_text_safe(elements, 3)
                ))
            elif tag == "COPE02018":
                parsed_data["references"].append(Reference(
                    qualifier=None,
                    number=get_text_safe(elements, 1)
                ))
            elif tag == "COPE02024":
                # No details provided for COPE02024 in the example
                pass

        logger.info("EDISIMPLEX message parsed successfully")
        return parsed_data
    except Exception as e:
        logger.error(f"Error parsing EDISIMPLEX message: {e}")

    return parsed_data
