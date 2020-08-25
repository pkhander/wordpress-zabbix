#! /usr/bin/python3

"""Gets Active triggers and posts them to the wordpress website"""

from zabbix_methods import ZabbixConnection
from helper import load_config, config
from api_helper import notify


class ZabbixConnectionTrigger(ZabbixConnection):

    def get_triggers_description(self, priority=3):
        """Get dictionary of trigger ID and description for triggers with priority >= 3"""

        load_config()
        HOST_NAME = config['zabbix_api']['HOST_IN_ZABBIX']

        results = self.session.do_request(
            "trigger.get", {
                "filter":
                {"host": [HOST_NAME]}, "only_true": True
            })["result"]
        if results == []:
            return None

        trigger_dict = {}
        for item in results:
            # TODO: Add more filters example - if int(item['priority']) >= priority and item['prop_name']) = priority  :
            if int(item['priority']) >= priority:
                trigger_dict[item['triggerid']] = item['comments']
        return trigger_dict


def get_triggers():
    """ Filtering trigger info to get desired output"""

    load_config()
    USER = config['zabbix_api']['USER']
    PASSWORD = config['zabbix_api']['PASSWORD']
    ZABBIX_SERVER = config['zabbix_api']['ZABBIX_SERVER']

    with ZabbixConnectionTrigger(USER, "https://" + ZABBIX_SERVER, PASSWORD) as conn:
        conn.login(USER, "https://" + ZABBIX_SERVER, PASSWORD)
        trigger_dict = conn.get_triggers_description()
        # print(trigger_dict)
        return trigger_dict


if __name__ == "__main__":

    trigger_data = get_triggers()
    if trigger_data is None:
        content = ''
        #print("No triggers!")
        notify(content)
    else:
        val = []
        html_table = '<table>'
        for k, v in trigger_data.items():
            if len(v) >= 1:
                html_table += '<tr>'
                html_table += '<td>' + v
                html_table += '</td> </tr>'

        html_table += '</table>'
        # print(html_table)
        notify(html_table)
