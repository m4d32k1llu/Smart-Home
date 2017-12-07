# Smart-Home

How to set up.
The simulation is made with for Ubuntu 16.04 servers, running over VirtualBox.
First create one ubuntu 16.04 server.
Install the requierd libraries and other needed software
-Bcrypt
-pycrypto
-Python 2.7
-Github 
-Fail2ban
-iptables-presistent 

After all packeges is installed
-Clone the WM and call them, Client, Lamp and Fridge.
-Change the network adapters for the VMS.
-The Gateway should have 3 adapters enabled.
-Check that there is no conflicts between mac-adresses.
-If you downloaded all required software in the first step, Lamp, Fridge and Client, just need one interface.
-Client, Fridge and Lamps should be attached to an internal network. e.g Frigde and Lamp, intranet, and client, intnet.
-Make sure the Gateway is attached to the same networks + NAT.

Configure network interfaces for Gateway:  vi /etc/network interfaces 
The gateway needs three interfaces
Example of Gateway interface:
#The loopback network interface
auto lo
iface lo inet loopback
#The primary network interface
auto enp0s3
iface enp0s3 inet dhcp

#The secondary network interface
auto enp0s8
iface enp0s8 inet static
adress 192.168.3.1
netmask 255.255.255.0
up route ad -net 192.168.3.0  netmask 255.255.255.0 gw 192.168.3.0

#The Third network interface
auto enp0s9
iface enp0s9 inet static
adress 192.168.2.1
netmask 255.255.255.0
up route ad -net 192.168.2.0  netmask 255.255.255.0 gw 192.168.2.0


For the client: 
auto enp0s3
iface enp0s3 inet static
Adress 192.168.2.100
netmask: 255.255.255.0
Network: 192.168.2.0
broadcast 192.168.2.255
gateway 192.168.2.1
up route ad -net 192.168.2.0  netmask 255.255.255.0 gw 192.168.2.1

For the lamp:
auto enp0s3
iface enp0s3 inet static
Adress 192.168.3.10
netmask: 255.255.255.0
Network: 192.168.3.0
broadcast 192.168.3.255
gateway 192.168.3.1

For the fridge:
auto enp0s3
iface enp0s3 inet static
Adress 192.168.3.100
netmask: 255.255.255.0
Network: 192.168.3.0
broadcast 192.168.3.255
gateway 192.168.3.1


Then deploy code:
To get the database running in the Gateway
Cd to Smart-Home
Run Python createBD.py
To create a user:
run Python insert_user_sqlite.py
Enter superpassword ("1ns3cur3")
Enter username: " "
Enter password: " "

To check that everything is working, -cd to gateway and run Python gateway_server.py
Open the client cd to client and run Python client_console.py
Make sure that you can log inn. 
#Make sure that gateway_server.py is listning on 0.0.0.0 and port 12345.


Run the Fridge and Lamp, cd into devices, and run their respective servers.
-Python server_fridge.py
-Python server_lamp.py


Setting up firewall:
Input rules
iptables - A INPUT -p tcp -m multiport --dports 12345,31414,31415 -j f2b-sshd (<- Fail2ban set up, accepting these TCP ports.)
iptables - A INPUT -p tcp  -s 192.168.2.100 -j --dports 12345 ACCEPT
iptables - A INPUT -p tcp  -s 192.168.3.100 -j --dports 31414 ACCEPT
iptables - A INPUT -p tcp  -s 192.168.3.10 -j --dports 31415 ACCEPT

Output Rules
iptables - A OUTPUT -p tcp  -s 192.168.3.1 -j  ACCEPT
iptables - A OUTPUT -p tcp  -s 192.168.2.1 -j  ACCEPT
iptables - A OUTPUT -p tcp  -s 10.0.2.15 -j  ACCEPT
iptables -A OUTPUT -j DROP

Forward Rules:
iptables -A FORWARD -j DROP




 
