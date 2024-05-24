# EDI Message Parser

## Project Description

The **EDI Message Parser** project is designed to process and convert messages in various EDI (Electronic Data Interchange) formats such as EDIFACT, EDISIMPLEX, and XML into structured JSON files.


## Project Structure

- `main.py`: Main script that coordinates reading input files, processing messages, and writing results to JSON files.
- `parsers/`: Directory containing parsers for different EDI message formats.
    - `edifact_parser.py`: Parser for EDIFACT format messages.
    - `edisimplex_parser.py`: Parser for EDISIMPLEX format messages.
    - `xml_parser.py`: Parser for XML format messages.
- `utils/`: Directory containing additional utilities.
    - `logger.py`: Logger configuration for event logging.
- `data/`: Directory containing input CSV files.
- `output/`: Directory where output JSON files are saved.
- `log/`: Directory where log files are saved.

## Input File Format

The input file must be a CSV file with two columns:
- `FORMAT`: Indicates the message format (can be `EDIFACT`, `EDIXML`, or `EDISIMPLEX`).
- `CONTENIDO`: Contains the complete EDI message.

### Example of Input CSV File

```csv
FORMAT,CONTENIDO
EDIFACT,UNB+UNOA:2+ESA83728279+ESA08139404+240508:0809+JKO9708641++COPARN'UNH+2400007284240+COPARN:D:99A:UN:FT9922'BGM+135+7487202400007284240+5'DTM+137:202405080809:203'...
EDIXML,<COPARNE02><HEADER><anxs_interchange.header><anxe_sender.identification>ESA83728279</anxe_sender.identification><anxe_recipient.identification>ESA08139404</anxe_recipient.identification>...
EDISIMPLEX,ENV001^ESB85173821^ESA08707887^COPE02000^202410136639^COPE02001^B85173821202410136639^9^COPE02002^202405081311^COPE02003^ZSE^DONOTREPLY@MAERSK.COM^...
```
### Requirements

- Python 3.8 or higher
- Packages specified in requirements.txt

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your_username/edi-message-parser.git
```
2. Navigate to the project directory:

```bash
cd edi-message-parser
```
3. Install the required packages:

```bash
pip install -r requirements.txt
```

### Usage

1. Place the input CSV file in the `data/` directory.
2. Run the main script:

```bash
python main.py
```
3. Check the `output/` directory for the generated JSON files.
The generated JSON files will be saved in the output directory.

#### Example of JSON Output


```json 
{
    "message_header": [
        {
            "sender_id": "ESA83728279",
            "recipient_id": "ESA08139404",
            "message_reference_number": "2400007284240",
            "message_type": "COPARN"
        }
    ],
    "beginning_of_message": [
        {
            "document_message_number": "7487202400007284240",
            "message_function_code": "5",
            "message_name_code": "135"
        }
    ],
    "date_time_period": [
        {
            "qualifier": "137",
            "period": "202405080809"
        }
    ],
    "free_text": [
        {
            "qualifier": "ACB",
            "text": "BOOKING CONTACT?: VALERIIA MOISEEVA"
        }
    ],
    "references": [
        {
            "qualifier": "ACA",
            "number": "RTM1416246C100050"
        }
    ],
    "transport_details": [
        {
            "stage_qualifier": "20",
            "mode_of_transport": "1",
            "carrier_id": "AP02174",
            "carrier_name": "CMA-CGM IBERICA",
            "transport_id": "9454395",
            "transport_name": "CMA CGM AMERIGO VESPUCCI",
            "transport_nationality": "MT"
        }
    ],
    "name_and_address": [
        {
            "party_qualifier": "TR",
            "party_id": "A58898487",
            "name": "BARCELONA EUROPE SOUTH TER BEST",
            "address": "",
            "city": "",
            "country": ""
        }
    ],
    "goods_item_details": [
        {
            "item_number": "1",
            "number_of_packages": "1",
            "type_of_packages": "PK"
        }
    ],
    "measurements": [
        {
            "dimension_code": "WT",
            "value": "25121"
        }
    ],
    "equipment_details": [
        {
            "qualifier": "CN",
            "id_number": "TCLU4328296",
            "size_and_type": "42G1"
        }
    ]
}
```




