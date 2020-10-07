
	Azure Express Route Setup Quick Guide


#### Table of contents

1. [Purpose](#Purpose)
2. [Network Diagram](#Network Diagram)
3. [Stakeholders](#Stakeholders)
    - [Company IT](#Company IT)
    - [Cloud (Azure) Engineer](#Cloud Azure Engineer)
	- [Azure support](#Azure support)
4. [Costs](#Costs)
5. [Annexure](#Annexure)
    - [Q&A for connection by ISP](#Q&A for connection by ISP)
    - [Secure Connect Service Brochure by ISP](#Secure Connect Service Brochure by ISP)
	- [ExpressRoute Docs:](#ExpressRoute Docs:)
	- [Azure Costs:](#Azure Costss:)

##Purpose:

This document is a quick guide intended to provide setup instructions for establishing a dedicated interconnection between organization’s on-premise network and Azure network using Azure Express route

This guide can help serve your customers who are completely new to the concept and may seek any organization to provide information.

Note: The below details are presented taking an example of what it will take for an organization to setup Express Route connection to Azure Cloud platform via Tata as the ISP.

##Network Diagram:


		 Figure 1: Connectivity of Customer n/w to Microsoft n/w
Ref: https://docs.microsoft.com/en-us/azure/expressroute/expressroute-troubleshooting-expressroute-overview





		Figure 2: Another Connectivity of Customer n/w to Microsoft n/w


*Note 01*: In the above diagrams, the connection that has been shown has 2 options. 
First is a simple connection for connectivity between both side network. 
Second kind of setup is on customer request they will also provide connection to Microsoft Office365 data center too.
2nd option is complex and takes more time.
*Note 02*: This document, at the moment, only talks about the first approach.




Figure 3: Specifics during Connectivity of Customer(On-Prem) to Azure n/w

*Note*: VPN Gateway here to be read as Express Route Gateway
Stakeholders:

This section explains the key stakeholders and their roles. 
####ISP 
- Examples  in India are Tata, Airtel, etc.
- Examples in the US are Equinix, Centrinox, etc.
- The ISP team will place a physical channel (FibreOptics) between source and destination location. They will set up this channel and configure it as per bandwidth requirements. Charges will be based on Bandwidth requirement and subscription to this service is annually calculated. 
Takes ~ 15 days for ISP. May depend on ISP to ISP
Why 15 days when the understanding is that a physical channel should have been already existing and only job remaining is to allot for the specific ask?
_Answer_ :  In between locations, ISPs have the Fiber Channel but they still need to set up a secure pipe (as they commonly call it) in two places. One is from ISP nearest local center  to Company and from ISP Main center (nearest to MS DC area)  to Microsoft EDGE data center.

####Company IT 
Company IT team will take care of connection provided by this ISP setup at on-premise networking devices. Team will need to do some networking setup such as BGP routing configurations and provide VM infrastructure under one VLAN setup. Also they need to configure private ranged ASN to this routing setup.

####Cloud (Azure) Engineer
Azure Cloud Engineer responsibility is to get all details from the IT team related to network setup after ISP work gets done.Then provide those details to Azure support team and track if they complete our setup at azure side. Finally we need to check if on-prem network resources can be accessed by Azure Vnet resources successfully or not.


####Azure support
Azure Support Team can support Azure side configurations for the Cloud Engineer. They will request all sorts of on-premise networking information 
(VLAN ID, ASN, Local Network Range) to setup connectivity to Azure Infrastructure. 

Costs
Cost to ISP
ISP itself charges 2 fold i.e. as below: MPLS Secure connect(ISP - Azure) + MPLS(GL - ISP)


A/C NAME
SERVICE
BW
ANNUAL RENTAL
OTC
LOCKING
<Orga>
MPLS SECURE CONNECT (AZURE PRABHADEVI)
50 MBPS
960000
15000
12 MONTHS
MPLS
50 MBPS
440000
15000
12 MONTHS
MPLS
50 MBPS
400000
150000
24 MONTHS
MPLS
50 MBPS
360000
15000
36 MONTHS
GST EXTRA AS APPLICABLE…..

So Total Costs for GL looks like as follows:

Cost To ISP
ISP itself charges 2 fold i.e. as below
    MPLS Secure connect(ISP - Azure) + MPLS(GL - ISP)
    This costs ~15 lacs INR or 20K $ for 50MPBS
    Breakup : 960000 + 440000


####Cost To Azure
Subscription
    $55 for 50MBPS + $0.025 /GB Data charges

####Conclusion:
While Costs to Azure is nominal, the investment in ISP subscription is high.

Test Latency on VMS
Though Direct connectivity is a known concept to give better performance, if we still want to test the latency. This is how it can be done.

There is no specific from/to server requirement.  The goal is to test latency w/ and w/o Express route connections so as to finalize our application architecture.
One way can be to test latency between VMs as in below diagram.




###How to Test:
While ping/trace route are okay to test with,  they do not provide accurate information. In case it is possible to test with tools like SockPerf (for Linux) and latte.exe (for Windows), that would be preferable. More details here -
https://docs.microsoft.com/en-us/azure/virtual-network/virtual-network-test-latency


# ##Annexure
Q&A for connection by ISP
https://drive.google.com/file/d/12WhOkuh3o5ionoGkJdjxohTnud_sNBZu/view?usp=sharing
Secure Connect Service Brochure by ISP:
https://docs.google.com/document/d/1l5hIgACdVTtFIR9UWp9o9e6MSbPuy8GzayEzbUBHjX8/edit?usp=sharing
ExpressRoute Docs:
https://docs.microsoft.com/en-us/azure/expressroute/expressroute-introduction

ExpressRoute Setup Docs & Videos:
https://channel9.msdn.com/Blogs/bfrank/Hybrid-Network-ExpressRoute-interxion-Azure
Azure Costs
https://azure.microsoft.com/en-in/pricing/details/expressroute/
Zones https://azure.microsoft.com/en-in/resources/knowledge-center/which-regions-correspond-to-zone-1-zone-2/


