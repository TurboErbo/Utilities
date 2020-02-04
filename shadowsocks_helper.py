import boto3
import json
import socket

class ProxyServerMgr:
    """Manages the proxy server. For now, only supports AWS EC2 instances"""

    def __init__(self, instance_id='i-0e535d1cb35bea503'):
        self.instance_id = instance_id

    @staticmethod
    def check_http_response(response):
        http_status = response['ResponseMetadata']['HTTPStatusCode']
        return (200 == http_status), http_status

    def change_server_ip(self):
        ec2 = boto3.resource('ec2')
        instance = ec2.Instance(self.instance_id)
        old_ip = instance.public_ip_address
        interface_id = instance.network_interfaces_attribute[0]['NetworkInterfaceId']
        network_interface = ec2.NetworkInterface(interface_id)
        allocation_id = network_interface.association_attribute['AllocationId']
        if not allocation_id:
            print("Failed to retrieve AllocationId of current Elastic IP!")
            return None

        print("Current Ip: %s, AllocationId: %s"%(old_ip, allocation_id))

        client = boto3.client('ec2')
        response = client.allocate_address()
        success, code = self.check_http_response(response)
        ip = response['PublicIp']
        if not success or not ip:
            print("Failed to allocate new ip! HTTP Status: ", code)
            return None

        print("Allocated new Ip: ", ip)

        response = client.associate_address(PublicIp=ip,InstanceId=self.instance_id)
        success, code = self.check_http_response(response)
        if success and response['AssociationId']:
            print("New Ip successfully associated with instance")
        else:
            print("Failed to associate new Ip with Instance! HTTP Status: ", code)
            return None

        response = client.release_address(AllocationId=allocation_id)
        success, code = self.check_http_response(response)
        if success:
            print("Successfully released old Ip address")
        else:
            print("Failed to release old Ip! HTTP Status: ", code)

        return ip


class ProxyClientMgr:

    def __init__(self):
        self.config_file = 'C:\\Users\\erbox\\Downloads\\Shadowsocks-4.1.8.0\\gui-config.json'

    @staticmethod
    def service_reachable(ip, port):
        sock = socket.socket()
        try:
            sock.connect((ip, port))
            return True
        except:
            pass
        return False

    def get_proxy_servers(self):
        f = open(self.config_file, "r")
        contents = f.read()
        data = json.loads(contents)
        servers = [(config['server'], config['server_port']) for config in data['configs']]
        f.close()
        return servers

    def is_proxy_blocked(self):
        for ip, port in self.get_proxy_servers():
            print("Server: %s, Shadowsocks port: %d" %(ip, port))
            ssh_reachable = self.service_reachable(ip, 22)
            print("SSH reachable: ", ssh_reachable)
            if not ssh_reachable:
                continue

            ss_reachable = self.service_reachable(ip, port)
            print("Shadowsocks reachable: ", ss_reachable)

            if not ss_reachable:
                return True
        
        return False

    def update_ip(self, new_ip):
        f = open(self.config_file, "r")
        contents = f.read()
        data = json.loads(contents)
        data['configs'][0]['server'] = new_ip
        contents = json.dumps(data, indent=2)
        f = open(self.config_file, "w")
        f.write(contents)        
        f.close()
    

if __name__ == "__main__":
    client = ProxyClientMgr()
    if client.is_proxy_blocked():
        response = input("Proxy is blocked, change ip? [Y] or n")
        if response in ['', 'Y','y']:
            server = ProxyServerMgr()
            new_ip = server.change_server_ip()
            client.update_ip(new_ip)