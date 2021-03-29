import json


def json_output(js_date, js_ip, js_type, js_ports, js_timeout, js_results, js_location):
    data = {'date': js_date, 'ip': js_ip, 'type': js_type, 'ports': js_ports, 'timeout': js_timeout,
            'results': js_results}

    with open(js_location, 'a') as outfile:
        json.dump(data, outfile, indent=2)


def write_output(date, wr_ip, wr_type, wr_ports, wr_timeout, wr_results, wr_location, wr_log):
    if wr_log == 'json':
        json_output(date, wr_ip, wr_type,
                    wr_ports, wr_timeout, wr_results, wr_location)
        print(f"Saved log to '{wr_location}'")
    elif wr_log == 'xml':
        print("xml")
    elif wr_log == 'n':
        None
    else:
        print(f"\nError in your log statement. '-l {wr_log} {wr_location}' is not valid.\n"
              f'Examples:\n'
              f"'-l json test.json' saves the log, in JSON, to test.json.\n"
              f"'-l xml tfcop.xml' saves the log, in XML, to tfcop.xml\n"
              )
