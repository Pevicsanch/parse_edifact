import xml.etree.ElementTree as ET
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

def get_text_safe(element: Optional[ET.Element]) -> Optional[str]:
    return element.text if element is not None else None

def parse_xml(xml_message: str) -> dict:
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

    try:
        root = ET.fromstring(xml_message)
    except ET.ParseError as e:
        logger.error(f"Error parsing XML: {e}")
        return parsed_data

    try:
        # Parse Message Header
        header = root.find('COPARNE02.HEADER')
        if header is not None:
            interchange_header = header.find('anxs_interchange.header')
            sender_id = get_text_safe(interchange_header.find('anxe_sender.identification'))
            recipient_id = get_text_safe(interchange_header.find('anxe_recipient.identification'))

            message_header = header.find('anxs_message.header')
            if message_header is not None:
                message_reference_number = get_text_safe(message_header.find('anxe_message.reference.number'))
                message_type = get_text_safe(message_header.find('anxe_message.type'))
                version_number = get_text_safe(message_header.find('anxe_message.version.number'))

                parsed_data["message_header"].append(MessageHeader(
                    sender_id=sender_id,
                    recipient_id=recipient_id,
                    message_reference_number=message_reference_number,
                    message_type=message_type,
                    version_number=version_number
                ))

        # Parse Beginning of Message
        beginning_of_message = header.find('trsd_beginning.of.message')
        if beginning_of_message is not None:
            message_name_code = get_text_safe(beginning_of_message.find('tred_document.message.name.coded'))
            document_message_number = get_text_safe(beginning_of_message.find('tred_document.message.number'))
            message_function_code = get_text_safe(beginning_of_message.find('tred_message.function.coded'))

            parsed_data["beginning_of_message"].append(BeginningOfMessage(
                message_name_code=message_name_code,
                document_message_number=document_message_number,
                message_function_code=message_function_code
            ))

        # Parse Date/Time Periods
        for dtm in header.findall('trcd_date.time.period'):
            qualifier = get_text_safe(dtm.find('tred_date.time.period.qualifier'))
            period = get_text_safe(dtm.find('tred_date.time.period'))
            parsed_data["date_time_period"].append(DateTimePeriod(qualifier=qualifier, period=period))

        # Parse Free Texts
        for ftx in header.findall('trsd_free.text'):
            qualifier = get_text_safe(ftx.find('tred_text.subject.qualifier'))
            text = get_text_safe(ftx.find('trcd_text.literal/tred_free.text'))
            parsed_data["free_text"].append(FreeText(qualifier=qualifier, text=text))

        # Parse References
        for group in root.findall('COPARNE02.GROUP1'):
            for rff in group.findall('trcd_reference'):
                qualifier = get_text_safe(rff.find('tred_reference.qualifier'))
                number = get_text_safe(rff.find('tred_reference.number'))
                parsed_data["references"].append(Reference(qualifier=qualifier, number=number))

        # Parse Transport Details
        for group in root.findall('COPARNE02.GROUP2'):
            transport = group.find('trsd_details.of.transport')
            if transport is not None:
                stage_qualifier = get_text_safe(transport.find('tred_transport.stage.qualifier'))
                mode_of_transport = get_text_safe(transport.find('tred_mode.of.transport.coded'))
                carrier = transport.find('trcd_carrier')
                carrier_id = get_text_safe(carrier.find('tred_carrier.identification'))
                carrier_name = get_text_safe(carrier.find('tred_carrier.name'))
                transport_id = get_text_safe(transport.find('trcd_transport.identification/tred_id.of.the.means.of.transport'))
                transport_name = get_text_safe(transport.find('trcd_transport.identification/tred_id.of.means.of.transport.identification'))
                transport_nationality = get_text_safe(transport.find('trcd_transport.identification/tred_nationality.of.means.of.transport.coded'))

                parsed_data["transport_details"].append(TransportDetails(
                    stage_qualifier=stage_qualifier,
                    mode_of_transport=mode_of_transport,
                    carrier_id=carrier_id,
                    carrier_name=carrier_name,
                    transport_id=transport_id,
                    transport_name=transport_name,
                    transport_nationality=transport_nationality
                ))

            for loc in group.findall('trcd_location.identification'):
                place_location_qualifier = get_text_safe(loc.find('tred_place.location.qualifier'))
                place_location_identification = get_text_safe(loc.find('tred_place.location.identification'))
                place_location = get_text_safe(loc.find('tred_place.location'))
                parsed_data["references"].append(Reference(qualifier=place_location_qualifier, number=place_location_identification))
                parsed_data["free_text"].append(FreeText(qualifier=place_location_qualifier, text=place_location))

            for dtm in group.findall('trcd_date.time.period'):
                qualifier = get_text_safe(dtm.find('tred_date.time.period.qualifier'))
                period = get_text_safe(dtm.find('tred_date.time.period'))
                parsed_data["date_time_period"].append(DateTimePeriod(qualifier=qualifier, period=period))

        # Parse Name and Address
        for group in root.findall('COPARNE02.GROUP3'):
            name_and_address = group.find('trsd_name.and.address')
            if name_and_address is not None:
                party_qualifier = get_text_safe(name_and_address.find('tred_party.qualifier'))
                party_id = get_text_safe(name_and_address.find('tred_party.id.identification'))
                name = get_text_safe(name_and_address.find('tred_name.and.address.line'))
                address = get_text_safe(name_and_address.find('tred_street.and.number.p.o.box'))
                city = get_text_safe(name_and_address.find('tred_city.name'))
                country = get_text_safe(name_and_address.find('tred_country.coded'))

                parsed_data["name_and_address"].append(NameAndAddress(
                    party_qualifier=party_qualifier,
                    party_id=party_id,
                    name=name,
                    address=address,
                    city=city,
                    country=country
                ))

        # Parse Goods Item Details
        for group in root.findall('COPARNE02.GROUP5'):
            goods_item = group.find('trsd_goods.item.details')
            if goods_item is not None:
                item_number = get_text_safe(goods_item.find('tred_goods.item.number'))
                number_of_packages = get_text_safe(goods_item.find('tred_number.of.packages'))
                type_of_packages = get_text_safe(goods_item.find('tred_type.of.packages.identification'))

                parsed_data["goods_item_details"].append(GoodsItemDetails(
                    item_number=item_number,
                    number_of_packages=number_of_packages,
                                       type_of_packages=type_of_packages
                ))

            # Parse Measurements
            for mea in group.findall('trsd_measurements'):
                dimension_code = get_text_safe(mea.find('tred_measurement.dimension.coded'))
                value = get_text_safe(mea.find('tred_measurement.value'))
                parsed_data["measurements"].append(Measurements(dimension_code=dimension_code, value=value))

            # Parse Split Goods Placement
            for split_goods in group.findall('COPARNE02.GROUP7/trsd_split.goods.placement'):
                equipment_id = get_text_safe(split_goods.find('tred_equipment.identification.number'))
                num_packages = get_text_safe(split_goods.find('tred_number.of.packages'))
                parsed_data["goods_item_details"].append(GoodsItemDetails(
                    item_number=equipment_id,
                    number_of_packages=num_packages,
                    type_of_packages=""
                ))

        # Parse Equipment Details
        for group in root.findall('COPARNE02.GROUP9'):
            equipment = group.find('trsd_equipment.details')
            if equipment is not None:
                qualifier = get_text_safe(equipment.find('tred_equipment.qualifier'))
                id_number = get_text_safe(equipment.find('tred_equipment.identification.number'))
                size_and_type = get_text_safe(equipment.find('tred_equipment.size.and.type.identification'))

                parsed_data["equipment_details"].append(EquipmentDetails(
                    qualifier=qualifier,
                    id_number=id_number,
                    size_and_type=size_and_type
                ))

            # Parse Equipment Measurements
            for mea in group.findall('trsd_measurements'):
                dimension_code = get_text_safe(mea.find('tred_measurement.dimension.coded'))
                value = get_text_safe(mea.find('tred_measurement.value'))
                parsed_data["measurements"].append(Measurements(dimension_code=dimension_code, value=value))

        logger.info("XML parsed successfully")
        return parsed_data
    except AttributeError as e:
        logger.error(f"Error parsing element: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

    return parsed_data

