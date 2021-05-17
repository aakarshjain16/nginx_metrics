import schedule
import requests
import bernhard
import time
from configparser import ConfigParser

file='/var/nginx_metrics/code/metrics_config.ini'
config = ConfigParser()
config.read(file)
ip= config['api_config']['ip']
port=config['api_config']['port']
api_version = config['api_config']['api_version']
riemann_host=config['riemann']['host']
riemann_port= config['riemann']['port']
url="http://"+ip+":"+port+"/api/"+api_version
c = bernhard.Client(host = riemann_host , port = riemann_port)

def connections():

        response = requests.get("http://10.57.11.218:3000/api/6/connections")
        json_response = response.json()
        c.send({'service': 'connections' , 'attributes':json_response})

def ssl():

        response = requests.get(url+"/ssl")
        json_response = response.json()
        c.send({'service': 'ssl' , 'attributes':json_response})

def requests_data():

        response = requests.get(url+"/http/requests")
        json_response = response.json()
        c.send({'service': 'requests_data' , 'attributes':json_response})

def upstreams():

        response = requests.get(url+"/http/upstreams")
        json_response = response.json()
        for upstream_name in json_response:
               server_num = len(json_response[upstream_name]['peers'])
               response_total = [0,0,0,0,0]
               requests_total = total_sent = total_received = total_fails = total_unavail = total_downtime = total_weight = total_active = total_hchecks = total_hfails = total_unhealthy = total_header = total_response= 0 

               for server in range(server_num):
                        request = (json_response[upstream_name]['peers'][server]['requests'])
                        requests_total += request

                        response_1xx = (json_response[upstream_name]['peers'][server]['responses']['1xx'])
                        response_total[0] += response_1xx

                        response_2xx = (json_response[upstream_name]['peers'][server]['responses']['2xx'])
                        response_total[1] += response_2xx

                        response_3xx = (json_response[upstream_name]['peers'][server]['responses']['3xx'])
                        response_total[2] += response_3xx

                        response_4xx = (json_response[upstream_name]['peers'][server]['responses']['4xx'])
                        response_total[3] += response_4xx

                        response_5xx= (json_response[upstream_name]['peers'][server]['responses']['5xx'])
                        response_total[4] += response_5xx

                        sent = (json_response[upstream_name]['peers'][server]['sent'])
                        total_sent += sent

                        received = (json_response[upstream_name]['peers'][server]['received'])
                        total_received += received

                        fails=(json_response[upstream_name]['peers'][server]['fails'])
                        total_fails += fails

                        unavail= (json_response[upstream_name]['peers'][server]['unavail'])
                        total_unavail += unavail

                        downtime=(json_response[upstream_name]['peers'][server]['downtime'])
                        total_downtime+= downtime

                        weight=(json_response[upstream_name]['peers'][server]['weight'])
                        total_weight+=weight

                        active=(json_response[upstream_name]['peers'][server]['active'])
                        total_active+=active

                        hchecks=(json_response[upstream_name]['peers'][server]['health_checks']['checks'])
                        total_hchecks+=hchecks

                        hfails=(json_response[upstream_name]['peers'][server]['health_checks']['fails'])
                        total_hfails+=hfails

                        unhealthy=(json_response[upstream_name]['peers'][server]['health_checks']['unhealthy'])
                        total_unhealthy+=unhealthy

                        try:

                                header=(json_response[upstream_name]['peers'][server]['header_time'])
                                response_time=(json_response[upstream_name]['peers'][server]['response_time'])
                                total_header+=header
                                total_response+=response_time
                        except:
                                total_header=0
                                total_response=0

               upstream_response = {'upstream':upstream_name , 'REQUESTS': requests_total ,'SERVERS': server_num, '1xx': response_total[0] , '2xx': response_total[1]  , '3xx': response_total[2] ,'4xx': response_total[3] ,'5xx': response_total[4], 'Sent':total_sent ,'Received':total_received ,  'Fails':total_fails,'Unavail':total_unavail,'Downtime':total_downtime , 'Weight':total_weight ,'Active Conns':total_active ,'Checks':total_hchecks,'fail':total_hfails,'Unhealthy':total_unhealthy ,'Header':total_header,'Response':total_response}
               c.send({'service': upstream_name+'_upstream'  , 'attributes':upstream_response})

def shared_zones():

        response = requests.get(url+"/slabs")
        json_response = response.json()

        for zone_name in json_response:
                pages_used = json_response[zone_name]['pages']['used']
                pages_free = json_response[zone_name]['pages']['free']
                pages_total = pages_used + pages_free
                memory_usage=(pages_used/pages_total)*100
                zone_response={'zone':zone_name ,'pages_used':pages_used,'pages_total':pages_total,'memory_usage':memory_usage}
                c.send({'service': zone_name+'_shared_zone'  , 'attributes':zone_response})

def server_zones():

        response = requests.get(url+"/http/server_zones")
        json_response = response.json()

        for zone_name in json_response:

                response_1xx= json_response[zone_name]['responses']['1xx']
                response_2xx= json_response[zone_name]['responses']['2xx']
                response_3xx= json_response[zone_name]['responses']['3xx']
                response_4xx= json_response[zone_name]['responses']['4xx']
                response_5xx= json_response[zone_name]['responses']['5xx']
                sent = json_response[zone_name]['sent']
                received=  json_response[zone_name]['received']
                total_requests=json_response[zone_name]['requests']
                zone_response={'zone':zone_name ,'1xx':response_1xx ,'2xx':response_2xx , '3xx':response_3xx , '4xx':response_4xx ,'5xx':response_5xx ,'sent': sent,'received':received,'total_requests':total_requests}
                c.send({'service': zone_name+'_server_zone' , 'attributes':zone_response})

def location_zones():

        response = requests.get(url+"/http/location_zones")
        json_response = response.json()


        for zone_name in json_response:

                response_1xx= json_response[zone_name]['responses']['1xx']
                response_2xx= json_response[zone_name]['responses']['2xx']
                response_3xx= json_response[zone_name]['responses']['3xx']
                response_4xx= json_response[zone_name]['responses']['4xx']
                response_5xx= json_response[zone_name]['responses']['5xx']
                sent = json_response[zone_name]['sent']
                received=  json_response[zone_name]['received']
                total_requests=json_response[zone_name]['requests']
                zone_response={'zone':zone_name ,'1xx':response_1xx ,'2xx':response_2xx , '3xx':response_3xx , '4xx':response_4xx ,'5xx':response_5xx ,'sent': sent, 'received':received , 'total_requests':total_requests}
                c.send({'service': zone_name+'_location_zone' , 'attributes':zone_response})

def limit_reqs():

        response = requests.get(url+"/http/limit_reqs")
        json_response = response.json()

        for zone_name in json_response:

                passed= json_response[zone_name]['passed']
                delayed=json_response[zone_name]['delayed']
                rejected=json_response[zone_name]['rejected']
                delayed_dry_run=json_response[zone_name]['delayed_dry_run']
                rejected_dry_run=json_response[zone_name]['rejected_dry_run']
                zone_response={'zone':zone_name , 'passed':passed ,'delayed':delayed , 'rejected':rejected,'delayed_dry_run':delayed_dry_run,'rejected_dry_run':rejected_dry_run}
                c.send({'service':zone_name+'_limit_reqs' , 'attributes':zone_response})


schedule.every(1).seconds.do(connections)
schedule.every(1).seconds.do(ssl)
schedule.every(1).seconds.do(requests_data)
schedule.every(1).seconds.do(upstreams)
schedule.every(1).seconds.do(server_zones)
schedule.every(1).seconds.do(location_zones)
schedule.every(1).seconds.do(shared_zones)
schedule.every(1).seconds.do(limit_reqs)

while True:
    schedule.run_pending()
    time.sleep(1)
