import io
from pprint import pprint

from correpy.parsers.brokerage_notes.b3_parser.b3_parser import B3Parser

with open('/Users/thiagosalvatore/Downloads/NotaNegociacao_600655_20220201.pdf', 'rb') as f:
    content = io.BytesIO(f.read())
    content.seek(0)

    brokerage_notes = B3Parser(brokerage_note=content, password="048").parse_brokerage_note()

    for note in brokerage_notes:
        for transaction in note.transactions:
            print(transaction)
            print("############")