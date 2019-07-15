import xml, json
from pprint import pprint
from json_writer import JsonWriter

def parse_xml(filename):

    with open(filename) as f:
        xml_file = xml.load(f)
    
    world = xml_file["world"]

    # TODO: implement here

    construct_json(world_infos, filename)

def construct_json(world_infos, filename):
    json_writer = JsonWriter("baseline/sample.json")

def main():
    sample_xml = "baseline/xmls/sample.xml"
    parse_xml(samle_xml)

if __name__ == "__main__":
    main()