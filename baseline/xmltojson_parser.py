import json
import xmltodict
import pprint

sample_xml = "baseline/samples/1level-04.xml"

def parse_xml(filename):
    with open(sample_xml) as f:
        xmlString  = f.read()

    jsonString = json.dumps(xmltodict.parse(xmlString))

    with open("sample1.json", 'w') as f:
        f.write(jsonString)

def main():
    parse_xml(sample_xml)

if __name__ == "__main__":
    main()