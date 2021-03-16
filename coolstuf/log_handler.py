import json
from datetime import date


def json_output(js_date, js_ip, js_type, js_ports, js_timeout, js_results, js_location):
    data = {}

    data['date'] = js_date
    data['ip'] = js_ip
    data['type'] = js_type
    data['ports'] = js_ports
    data['timeout'] = js_timeout
    data['results'] = js_results

    with open(js_location, 'a') as outfile:
        json.dump(data, outfile, indent=2)


def write_output(wr_ip, wr_type, wr_ports, wr_timeout, wr_results, wr_location, wr_log):
    if wr_log == 'json':
        json_output(date.today().strftime("%d/%m/%Y"), wr_ip, wr_type,
                    wr_ports, wr_timeout, wr_results, wr_location)
        print(f"Saved log to '{wr_location}'")
    elif wr_log == 'xml':
        print("xml")
    elif wr_log == 'n':
        None
    else:
        print(f"Please enter a valid log entry. '-l {wr_log}' is not valid.\n"
              f'Examples:\n'
              f"'-l json test.json' saves the log, in JSON, to test.json.\n"
              f"'-l xml tfcop.xml' saves the log, in XML, to tfcop.xml\n"
              )
