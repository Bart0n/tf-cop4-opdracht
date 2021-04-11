import json
import xml.etree.ElementTree as ET
from coolstuf import color as c


# Writes output depending on wr_log value. If none matches, return an error.
def write_output(date, wr_ip, wr_type, wr_ports, wr_timeout, wr_open_port, wr_closed_port, wr_location, wr_log):
    if wr_log == 'json':
        json_output(date, wr_ip, wr_type, wr_ports, wr_timeout, wr_open_port, wr_closed_port, wr_location)
        return True, f"{c.C.YELLOW}[✓]{c.C.END} Saved log to {c.C.UNDERLINE}{c.C.GREEN}'{wr_location}'"
    elif wr_log == 'xml':
        xml_output(date, wr_ip, wr_type, wr_ports, wr_timeout, wr_open_port, wr_closed_port, wr_location)
        return True, f"{c.C.YELLOW}[✓]{c.C.END} Saved log to {c.C.UNDERLINE}{c.C.GREEN}'{wr_location}'"
    elif wr_log == 'n':
        None
    else:
        return False, (
            f"\n{c.C.RED}[✖]{c.C.END} Error in your log statement. '-l {wr_log} {wr_location}' is not valid.\n"
            f'Examples:\n'
            f"'-l json test.json' saves the log, in JSON, to test.json.\n"
            f"'-l xml test.xml' saves the log, in XML, to test.xml\n"
            )


# Creates an json file
def json_output(js_date, js_ip, js_type, js_ports, js_timeout, js_open_port, js_closed_port, js_location):
    data = {'date': js_date, 'ip': js_ip, 'type': js_type, 'ports': js_ports, 'timeout': js_timeout,
            'open_ports': js_open_port, 'closed_ports': js_closed_port}

    with open(js_location, 'a') as outfile:
        json.dump(data, outfile, indent=2)


# Creates an xml file
def xml_output(xml_date, xml_ip, xml_type, xml_ports, xml_timeout, xml_open_port, xml_closed_port, xml_location):
    try:  # Check if the XML file exist, if so, use that file and append to it
        tree = ET.parse(xml_location)
        root = tree.getroot()

    except FileNotFoundError:  # If the file does not exist, make a new XML root element
        root = ET.Element("root")

    host = ET.SubElement(root, "host", {"ip": xml_ip})

    date = ET.SubElement(host, "Date")
    date.text = xml_date

    scan_type = ET.SubElement(host, "ScanType")
    scan_type.text = xml_type

    ports = ET.SubElement(host, "PortRange")
    ports.text = xml_ports

    timeout = ET.SubElement(host, "Timeout")
    timeout.text = str(xml_timeout)

    open_port = ET.SubElement(host, "OpenPorts")
    open_port.text = str(xml_open_port)

    closed_port = ET.SubElement(host, "ClosedPorts")
    closed_port.text = str(xml_closed_port)

    ET.ElementTree(root).write(xml_location)