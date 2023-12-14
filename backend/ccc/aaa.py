# -*- coding: utf-8 -*-
# author: itimor

from godaddypy import Client, Account

if __name__ == '__main__':
    godadd_ac = Account(api_key='gHzap6zE4keX_2NaopMBRt4JRKcczEUbqDw', api_secret='VppHYw5ALkdtzW9XaPb6Ls')
    gd = Client(godadd_ac)
    print("更新godaddy ns")
    zone = 'rga-kl.com'
    update = {
        "nameServers":
            ["ns1.gcorelabs.net", "ns2.gcdn.services"]
    }
    gd.update_domain(zone, **update)
