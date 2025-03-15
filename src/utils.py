from xml.etree.ElementTree import Element, SubElement, tostring


def json_to_xml(json_data):
    root = Element("metadata")

    for index, item in enumerate(json_data, start=1):
        image = SubElement(root, "image", name=f"image{index}")

        for obj in item.get("objects", []):
            SubElement(image, "object").text = obj

        SubElement(image, "text").text = item.get("text", "")
        SubElement(image, "description").text = item.get("description", "")

    xml_str = tostring(root, encoding="utf-8", method="xml").decode("utf-8")
    xml_str = '<?xml version="1.0" encoding="utf-8"?>\n' + xml_str

    return xml_str
