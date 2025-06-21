# AWS re:Inforce 2025 - Thinking beyond traditional firewalling architectures (NIS303)

**Video Link:** [Watch on YouTube](https://www.youtube.com/watch?v=HSPEq4rZPD8)

## Video Information
- **Author:** AWS Events
- **Duration:** 53.1 minutes
- **Word Count:** 8,670 words
- **Publish Date:** 20250620
- **Video ID:** HSPEq4rZPD8

## Summary
This comprehensive session explores modern network security approaches in AWS, challenging traditional firewall-centric architectures and introducing cloud-native alternatives for various connectivity and security scenarios. The presentation provides practical insights into when to use firewalls and when to leverage alternative AWS services for more efficient and flexible network security.

## Key Points
- **Firewall Considerations**
  - Not about eliminating security, but finding more efficient protection methods
  - AWS offers managed firewall solutions like Network Firewall and Web Application Firewall
  - Different firewall types serve specific purposes (layer 3-7 inspection, web app protection)

- **Internet Ingress Strategies**
  - Use Web Application Firewall (WAF) for web applications
  - Leverage AWS managed services for specialized access needs
  - Utilize CloudFront for content delivery and additional security layers

- **Internet Egress Approaches**
  - Prefer AWS service endpoints over routing all traffic through firewalls
  - Use centralized egress for cost and management efficiency
  - Implement DNS resolver firewall for initial domain validation

- **Workload-to-Workload Communication**
  - Explore VPC Lattice as a cloud-native alternative to traditional network firewalling
  - Support for HTTP/HTTPS, TLS passthrough, and TCP resources
  - Enables application-level connectivity with granular access controls

- **Remote Workforce Connectivity**
  - Consider Amazon Verified Access for secure application access
  - Eliminate traditional VPN requirements
  - Provide real-time, context-aware access policies

## Technical Details
- **Firewall Services**
  - AWS Network Firewall: Layer 3-7 inspection
  - Web Application Firewall: Specialized web app protection
  - VPC Block Public Access: Centralized internet access control

- **Advanced Connectivity Options**
  - VPC Lattice: Application-level networking
  - Service network endpoints
  - Resource gateways for TCP resources

- **Access Control Mechanisms**
  - Granular policy creation
  - Multi-level authorization (service network and service levels)
  - Support for IP version flexibility

**Key Takeaway**: Modern cloud security is about intelligent, granular access control rather than blanket network restrictions. AWS provides sophisticated, flexible tools that enable precise security management while simplifying network architectures.

## Full Transcript

- Hello, everybody. Thank you for coming out so
early on a Wednesday morning after a night out. My name is Tom Adamski. I'm a
principal solution architect. I'm joined today by Ankit, also a principal solution architect. Together we have more than
10 years of experience working with customers,
setting up their networks, and helping them with network security, and the session we have for
you today is around firewalls and when to use them and
maybe when not to use them. So we're gonna ask ourselves when to firewall, when not to firewall, and then we will look
at different use cases where we typically would use firewalls and see if we have some alternatives that might make it easier for you to achieve the same level of security but make it simpler from an
operational point of view or optimize for cost. Every once in a while, we'll
pop these pink rectangles that will give you tips or show you what's important about each slide. So I wanna start off with
different connectivity models that some of which you might
already be familiar with, some of which might be new. So we have two different
network connectivity types, the traditional
network-to-network connectivity, and then the other one is
application networking. So we'll use an example, and
you'll see that there will be a lot of examples throughout the session. We barely use any text.
It's mostly diagrams. On the left-hand side,
we have client VPCs. We have some client, and
on the right-hand side, we have our application VPCs. We have a couple of applications. There's a HTTP application
and some database, and the goal here is to
get the client access to those resources. With traditional networking,
what you would do is you would create some logical network pipe between those VPCs and then set up routing in both directions to
allow traffic to flow, but with that, you're
allowing the client VPC to talk to anything in
the application VPC. You're also allowing the application VPC to initiate connections to
anything in the client VPC. So you would typically start
adding additional restrictions, so security groups which are always there that you have to configure to limit access of what the client can get to, and then very often you would also look at adding some additional
firewalling construct, so either use an AWS managed
next generation firewall or bring a third-party appliance
firewall to put in place. On the application networking, we're looking at a
slightly different model. With application networking, what we're doing is we're making it look as if the application or
database you're trying to get to is actually hosted
inside of the client VPC. So it'll be exposed as
an IP address, a port, and you will expose the
individual application one by one, and then client can connect
to those applications. With that model, you're
already getting a certain level of access control, right? You're not opening up the networks. You're only allowing
the specific resources between the client and the application. We're also allowing for
overlapping address space in this scenario. So you don't really have
to care about routing and IP addresses. It makes that model a
little bit more simpler. If we overlay some of the services that facilitate each type of
those, the connectivity model, for network-to-network connectivity, there will be constructs like the Transit Gateway or Cloud WAN, which are kinda distributed
routing services inside AWS, or VPC peering, which is
probably the simplest one, which actually looks like
that pipe that I showed you. For application networking, we're gonna look at Amazon VPC Lattice as well as AWS PrivateLink. Now, our session is gonna
kinda straddle the line between both of those connectivity models, but if you do want to have a deep dive on each one of those models, some of those sessions already happened. One of those sessions is actually
happening next door to us, but I'll see if you start
switching your headsets to the green color, so stay on blue. So our question today is gonna be, to firewall or not to firewall? And we're not saying not to firewall in terms of don't apply security policies. I actually personally
really like firewalls. My best friends are firewalls, but what we're saying is
firewall when you need to but look at alternatives if
they give you more flexibility or make it easier for
you to deploy things. When we're looking at
firewalling solutions today, we're gonna talk about
AWS Network Firewall and then Web Application Firewall. Both are AWS-managed firewalling solutions that will scale alongside with your load. So you don't have to deal with, you know, patches, updates, scaling. That's all managed, but then there are
differences between them. So Network Firewall
operates at layer three all the way to layer seven, but it's focusing on TCP
and UDP applications, so pretty much any application, any port. It can also cover HTTP, HTTPS, but typically if you have a use case where you're allowing traffic from the outside to your resources, you want to be using a
Web Application Firewall. That's purposely designed
for HTTPS applications, comes with a lot of bells and whistles specializing in protecting
your web application all the way to advanced
things like bot detection and account takeover prevention. Another difference between
those two firewall types is that Network Firewall, you use routing to navigate
traffic to Network Firewall. So you have to be operationally
moving the traffic towards the direction of the
firewall to get it inspected. With Web Application Firewall, with WAF, it natively integrates
with a lot of AWS services, so CloudFront, API Gateway,
Application Load Balancer. So what I wanna start with is give you a reference architecture for how your network would look like if you did firewalling
everywhere, and by firewalling, I mean add additional
third-party firewalls, right, or AWS managed firewalls. You still would do security groups and all the other services, but we'll look at those
additional firewalls here, and we'll look at different use cases, and you see there's a legend there. Different flows will
have different colors, and we'll start with the ingress flow. So ingress is where we have an application that's internet facing and we
have users out on the internet that need to connect to that application. So we would have an
Application Load Balancer, maybe make it public facing, and then deploy Web Application Firewall on top of that Application Load Balancer, and that might be it. Maybe we're done and
we have now protections for users coming to our applications. However, typically with web applications, you would also care about experience. You might wanna do caching. So you would often put
your web application behind a content delivery network. AWS has Amazon CloudFront, which is a content delivery network that also integrates with AWS WAF. It's a single-button integration
on a single API call. So now your users would
be hitting CloudFront closest to where they are. They would get content from cache. They would get inspected
before traffic gets forwarded to our application. Some of the cool features that CloudFront actually
launched recently, they allow you to also connect to an Application Load
Balancer that's private, so you could completely
hide your application, your origin from facing the internet and have all traffic
coming in for CloudFront before it gets to your application. And then as you add
different applications, you would horizontally
scale that environment, add additional VPCs, and each one would be
fronted by CloudFront. We call this model distributed ingress. So every VPC has its own load balancer and it has its own access from CloudFront. Sometimes customers would want
to centralize that ingress. It's not exactly a best practice. Sometimes you just have
to do it, and it's fine, but we tend to recommend
distributed ingress, so have different VPCs,
each one with its own path. That's the most scalable, and that's the more
cost-effective model for ingress. Now, if you want communication
between those VPCs, right, maybe we have hundreds of those VPCs, I'm only showing you two, we can connect those
two routing constructs inside of AWS region. Could be a Transit Gateway.
Could be AWS Cloud WAN. And then we would deploy a
VPC called the inspection VPC with maybe AWS Network Firewall. By the way, we just launched
a native integration between Network Firewall
and Transit Gateway, so you wouldn't even
have to build this VPC to be able to solve this use case. So once we have the firewall,
we will navigate traffic through Transit Gateway or Cloud WAN, push it to the firewall stack, inspect, and then send it to the other VPC. We'll actually show you
a more detailed design on how actually we need to
sorta do it with routing and what are the routing tables
and routes in each layer. Finally, for egress use case,
we could use the same VPC. We could put a NAT gateway in
there and then egress traffic. So traffic that originates
from an EC2 instance or pod or a container would be
sent to the Transit Gateway or Cloud WAN and then sent
out through inspection VPC. So you'll notice for egress, we actually do recommend
centralized egress. That is actually the
more cost-efficient model and allows you to scale better and be more efficient at
using your resources, right? You deploy the NAT
gateway and the firewall, and you can have multiple
VPCs share that layer. The other interesting
thing I wanna call out here is that we now have a different path for traffic coming in from the internet. It hits your workloads
and they respond back to the load balancer then go out back through CloudFront,
but then if an instance on your workload initiates a connection, it will send traffic
to the Transit Gateway and then use egress, use
that centralized egress for getting out. Okay, so if we zoom in
at each firewall layer and kind of understand
what do we see customers do at this layer, so with
AWS WAF for ingress, typically what customers do, they can set up IP addresses
and port-based rules, but they often do things like geoblocking. They add rate limiting, bot control, and a lot of different rules protecting against the OWASP top 10 risks, so SQL injection, cross-site
scripting, what have you. For egress use case, what
we see customers deploy on the Network Firewall is
often would be domain filtering. So you wanna limit the domains that you allow your clients to connect to. We also support geoblocking
so you can limit the countries that you're connecting to. There would be some protocol enforcement, so validating if that HTTP
request that I'm doing is really HTTPS and not some
other protocol pretending to be something else. Traditional IP port-based filtering. JA3 and 4 fingerprinting. So this is super relevant
if you don't plan to decrypt traffic. You can actually fingerprint
the client and the destination and make sure that you're allowing traffic to the legitimate destinations, even if the traffic is encrypted. And then finally optionally,
you can do TLS decryption if that's something that you need to do. So Network Firewall supports that. For the east-west use case, so VPC to VPC, what firewalls typically do is a lot of it would be IP port-based rules. So your VPC would be a security boundary, and then you would set that
up inside of the firewall. Maybe the central security
team is controlling access between different VPCs,
subnets in that VPCs. There will also be some
protocol enforcement as well as domain filtering, so validating the domains
you're connecting to. Now for completeness,
there are also use cases for connecting back to on-premise, right? So maybe you have a corporate data center. You might have a direct connect, which is a pretty much
fiber to our backbone, or use an IPSec VPN. And that traffic can also
hit the Transit Gateway or Cloud WAN and you can
push it up to inspection. So this use case is pretty much the same as the east-west use case. The direct connect or VPN
is just another attachment on the Transit Gateway or Cloud WAN, and the same thing goes
for remote user access. So maybe you have users at home that are connecting using
AWS managed client VPN. The traffic would be brought into a VPC, and then from that VPC, they
can get to all the resources, and again, you can push that
traffic up to inspection, to the inspection VPC
to apply your policies. So we talked about our firewalls, but there's also a lot of
other security services that I'm not gonna mention in the session. We have a DNS firewall, right, where we can filter your
DNS queries at the DNS level rather than before even traffic
gets sent on the data plane to the final destination. We have our network access
control list and security groups, which are always there
and available for you for free inside of the VPC. We have Firewall Manager for managing all of these different constructs, including the firewalls
that we talked about and sent from a central account,
Shield for DDoS protection, and maybe GuardDuty for
threat detection inside a VPC. So there's a lot of things
that you could be deploying inside of the VPC to secure it, but today, we're purely focusing on the
next generation firewalls or Web Application Firewalls. Okay, so let's look at the
different use cases now one by one and talk about
is this the best practice, is this what we would recommend, or is there an alternative
that you can look at to make your life easier? So we'll go back to our
reference architecture, and we'll just focus on the
internet ingress use case, so clients connecting to
the workloads through cloud, CloudFront and Application Load Balancer, and the good news here is, yes, this is the best practice, right? If you have a web application, Web Application Firewall
is what you wanna do. Now, but that is for web applications. What if you have applications
that are not HTTPS, right? What if you have TCP/UDP applications? Maybe you put them behind
the Network Load Balancer or maybe they're directly
facing the internet. What do you do with that traffic? So one option is to deploy security groups on the Network Load Balancer. However, security groups have a limit of how many rules you can configure,
and that number is 1,000. So if you need more than 1,000 entries, security groups are
not gonna be sufficient to limit access to your resources. So you can also use Network Firewall, and this is also a recent launch. So typically prior to this launch, you would have to put the
full-blown Network Firewall inside of that application VPC in front of your Network Load Balancer and then configure routing
to make sure traffic is forwarded correctly. With the recent launch, you
can have the Network Firewall in a different VPC and
create a logical endpoint that can navigate traffic to
that centralized firewall. So the endpoint, think
about it as an extension, a long arm of that firewall
inside of the application VPC. So you still have to set up routing. So that's still always there. So you need to make sure
that as traffic is coming in, you're forwarding it to
the Network Firewall, but then from there, the
Network Firewall endpoint will pass it on to Network Firewall. Network Firewall will apply your policy, decide if traffic is allowed, and then it can continue to the NLB. And then the question here would be, what is your non-web application? And the reason I'm asking
that is there are a lot of AWS managed services
that can replace some of the pain points that you have with having to manage some
of these applications. So if your use case was
exposing an EC2 instance and providing SSH access, we
actually do have a couple of managed services that can allow for you to have this managed
access through the browser or directly through the CLI, where we manage the SSH keys for you, and you can use identity
and access management to provide access. For use cases like FTP, SFTP, we do have AWS Transfer Family,
which is a managed service that can solve that use case for you. And finally, if you have emails, we have a Simple Email Service as well. So we can look at an example of accessing an instance over SSH, right? So if we use Systems
Manager Session Manager, our EC2 instance will do
an outbound connection to the Session Manager service that lives in the same region. So notice, because this
is an outbound connection, you don't have to open any inbound rules. So your security groups could
completely be locked down on the inbound side or
you can have a firewall blocking all the traffic in, but as long as the instance can call out to the Session Manager service, then the users will talk to
the Session Manager service, and Session Manager would stitch
those two sessions together to allow you SSH access to your instance. You don't have to set
up any inbound rules. You don't even have to have
a firewall in front of that. Moving on to internet egress, let's go back to our
reference architecture again and pull on the internet egress use case. We'll show you what the
life of a packet looks like in the internet egress flow. So let's imagine our instance
is trying to get to GitHub to pull some code or do a software update. The first thing it would do
is it would do a DNS lookup. So if you enabled Route
53 DNS Resolver Firewall, you could actually validate if
the domain they're looking up is legitimate or if it's
a domain you wanna allow that traffic to. Say you wanna allow it. GitHub is fine. The next thing you need
to make sure you configure is routing inside that VPC to forward any internet-bound traffic to Transit Gateway or Cloud WAN. On Cloud WAN or Transit Gateway, you would also need to make sure you have routes forwarding the traffic, outbound traffic to the inspection VPC, and then I simplified this
drawing quite heavily. The inspection VPC, inside
of that inspection VPC, each component actually
lives in a different subnet and will have a different
route table associated with it 'cause what we wanna do is, as your traffic arrives
in the inspection VPC, we wanna bump it into
the Network Firewall, do our inspection on Network Firewall, but after that, bump it
into the NAT gateway, and after NAT gateway,
once we NATted the traffic, send it out to the internet. The good news here is the firewall can actually see the original
IP address of the client as well as the destination. So you can apply your policy
just like you would with, you know, on-premise. One side call out here is if
you have an IPv6 use case, you would actually have to put proxies inside of that egress VPC or
do not do centralized egress. If you want to have more
questions on that one, we can chat afterwards,
but just be aware that v6 is a slightly different use case here. So good news also is that doing
Network Firewall for egress is also the best practice. It's a really good
solution for that use case, but what I often see customers
do that's kind of a problem, they use the same path for connecting to AWS managed services. So inside of the region, we might have hundreds
of AWS managed services. I'm showing you only three, S3, which is a storage service,
DynamoDB, a NoSQL database, and then as an example of
all the other services, Elastic Container Registry, ECR. This is where we manage
container images for you. So you can upload container images there or pull container images from there. The reason why I'm showing those is usually those three are
generating a lot of traffic and then pushing a lot of
traffic through Transit Gateway, NAT gateway, Network
Firewall adds latency. You can inspect that
traffic, it will work, but you'll pay more money
and you will add latency. So the best practice to
talk to AWS-based services is to not use your egress stack
but instead use endpoints. So S3 and DynamoDB have two
special types of endpoints. They're unique in that aspect.
They have gateway endpoints. I like to think about those as
wormholes to your VPC, right? And to get traffic out through
that wormhole to the service, you need to make sure you
update your routing tables and say that S3 prefixes should go to the S3 gateway wormhole, and then DynamoDB prefixes
should go to DynamoDB gateway, and you don't have to
manage those prefixes. You don't even need to know what they are. We have a managed prefix list for you that represents all of the S3 ranges or all of the DynamoDB
ranges that you can use. What about all the other services that don't support gateway endpoints? So for those, you would
create interface endpoints. There's no routing required
with interface endpoints. That's one of the application
networking constructs. Interface endpoints are presented locally inside of your VPC as an IP address, and we will update DNS under the hood to redirect your traffic to ECR to go and talk to the endpoint instead of flow through your egress stack. But you can ask, what about security? How do I make sure you know
no one connects to a bucket that's not my corporate bucket or no one connects and downloads an image from somebody else's image repository? Well, you can apply
policies on the endpoints to control data access. Who are you talking to? What destinations you can communicate with through these endpoints. So in this scenario, in this example, we're setting up a policy
on the interface endpoint to say that we're only
allowing to download images from a specific AWS account, and if I try and download a
random image from somebody else, that's not gonna be allowed. I'm also making sure that
the requests are coming from a particular org, and this
is separate to the policies that you'd be setting up on the
resources themselves, right, on the S3 bucket or on ECR itself. This is purely a policy
on the endpoint to control what can you allow to get out. Okay, there's another use
case I want to touch on that we haven't really mentioned earlier, internet airgappped workloads. So this is not really egress or ingress. This is where you want to
deny both of those use cases. So you might have a
workload that you don't want that workload to talk to the internet. So what would you do? What can you do to limit access completely from the internet, so
cut off that workload? Well, you could think you
could do Network Firewall and endpoints and block that traffic. That will technically work, but it's unnecessarily complicated for that specific use case. So the other options, the other things that customers would
do is they would remove an internet gateway from a VPC. That's one option. If the VPC doesn't have
an internet gateway, it's not talking to the internet. The other option would be to use network access control lists or security groups to limit that access. So that's still valid, but
something that we launched earlier this year is your ability to block public access to your VPC, and we called it VPC Block Public Access. So with VPC Block Public Access, you can centrally manage
and declare access controls for a set of VPCs. So you can do that on
the account level, OU, or across all of the organization. Basically you would say,
"I don't want any VPC in my organization or any
VPC in an account or in an OU to have any access to the internet," and you have the ability to
exclude different elements. So you wanna exclude an account, or you apply the policy on an OU level but you wanna exclude an account, or you apply the policy
on an account level, but you want to exclude a VPC or a subnet, that's totally possible, and then you can decide if
you wanna apply blocking on just in both directions
or block only inbound traffic and still allow the outbound traffic, and that still applies on
VPC subnet account level. So the beauty of that
is this is independent from what anybody else
configures inside of that VPC. So even if I mess up
configuration of the VPC and I have an internet gateway, I opened up my security
group, I messed up the NACLs, normally traffic would
just flood into my VPC. If someone enabled Block Public
Access at a central level, so usually a central security team, nobody can get into and out of that VPC. And then finally, you can
use Network Access Analyzer before you enable this
feature just to validate what would be the impact, right? You want to check before
you block public access to all of your VPCs. Okay, so with that, I wanna move on to workload to workload communication and hand off to Ankit to continue. (audience applauding) - Thanks, Tom. So folks, in this next section, we are gonna be talking about workload to workload traffic patterns, inspection architectures
and any alternatives. So firstly, let's look at a workload to workload inspection-based architecture. Your use case is two VPCs. The VPCs can have various flavors of computes inside of them. They're connected to each other using Transit Gateway or Cloud WAN, and your use case is
to punt all the traffic between these two VPCs
through an inspection firewall that is also connected
to the Transit Gateway. Now, earlier you heard Tom mention that you can use routing tables to influence traffic between our VPCs. So in this case, you
would have a static route within your source VPC
that would punt traffic towards Transit Gateway or Cloud WAN. Now, on the Cloud WAN or Transit Gateway, you would need a route that sends traffic to the inspection VPC. Within the inspection VPC,
you would have a route that would send traffic
to the firewall endpoint, firewall does its firewalling, and then you're gonna need a similar route for the return traffic as well. Now, to send traffic
towards the destination VPC, this is where you could
use propagated routes on Cloud WAN or Transit
Gateway and traffic gets sent to the destination VPC and
the reverse direction as well. Now, a pro tip here is you
should use appliance mode on the inspection VPC attachment
for multi-AZ scenarios. That would keep your traffic symmetric. So talking about firewalling,
let's actually take a look at what the firewall does most often. So you could insert a
firewall between two VPCs, which we saw on the previous slide, which basically gives you VPC one's CIDR to VPC two's CIDR kind of a policy. Alternatively, you can
insert a firewall endpoint or a firewall between two
subnets of the same VPC, for example, between two
subnets of a shared VPC. Now, ultimately the policy
that we see customers deploy for east-west inspection or
for VPC to VPC inspection follows the five tuple construct. So basically it's source
IP, destination IP, source port, destination
port, and protocol. Now, since this is mostly based on CIDRs, it really sounds like access control versus deep packet inspection. So with that, let's see
if there is an easier, more cloud-native way of
performing access control between your workloads. This is where we'll start
talking about VPC Lattice. So VPC Lattice is a fully managed service that allows you to securely
connect your workloads, and you get additional
observability related benefits as well by looking at
VPC Lattice access logs. Now let's define the use case again. You have two VPCs and your use case is to provide access control when workloads within these VPCs talk to each other. So this time, you would have
a VPC Lattice service network in the middle. Your VPC Lattice service
network is an aggregation point or a logical grouping of your
services or your applications that require similar
connectivity and security. So the first point to
remember with VPC Lattice is you onboard specific
applications onto VPC Lattice. So from here on, I would
use the words applications and services interchangeably. So the first step you take
here is you create this service called this service-1 on VPC
Lattice, and you say that, okay, this service-1 has a backend target or a target group. That is EKS in the EKS
cluster in your App VPC 1. So from this perspective, your VPC Lattice feels a
lot like a load balancer in that you are onboarding an application and you're providing a
backend target group as well. Now optionally, when
you onboard a service, you can provide custom FQDNs
or vanity domain names as well. Once your application is on Lattice, there's gotta be a consumer. Somebody must want to access it. So this is where you create a service network VPC association. Now, major point to remember here is when we say VPC association,
it means workloads only within that VPC get access to that service. So let's look at the life of
a packet or the traffic flow. The instance is in App VPC 2. When they want to consume this service, they would want to access an FQDN. They try to resolve that. That FQDN resolves to an IP address that puts traffic onto the
VPC Lattice data plane. Another thing to remember
here is this IP address is only available from within the VPC. It's non-routable. Once traffic is on the
VPC Lattice data plane, this is where Lattice understands that this traffic is
destined to service-1, and service-1 lives in the
EKS cluster behind App VPC 1. So from this perspective, your Lattice acts as a
combination of your load balancer that allows you to onboard
specific apps with a target group and also connect your consumers
with service producers. Now let's talk about security. You can optionally provide VPC
Lattice auth policies as well and you can apply these
at two separate levels. Firstly, you can apply the auth policy at the central service network level. This is where you could apply
a very coarse-grained policy, for example, saying
that allow this request as long as the originator of this request was within my AWS org. Now pro tip here is since it's applied on the central service network level, it'll be your central network
or security admin team that would create and apply this policy. Okay, so the policy or the
user request is now approved or allowed at the service network level. The second place where
you could apply a policy is at the actual service level as well, and this is where you
could get really granular with your policy. So in this case, I'm
saying allow the request only if it comes from a
specific AWS principal or a role and at the same time when it's going to only a very specific resource, which is a service within Lattice, and when the principal is
making a GET method request versus something else. So it allows you to get
really, really granular at the service level. Now often enough, it's gonna
be the actual application or service owners that would
have intimate knowledge of how their service should
be consumed by the consumers. So this auth policy on the service level would likely be applied by your
specific app owner accounts. Now another pro tip here is
use sigv4 signed requests for creating really
granular auth policies, for example, matching
on your principal IDs. I'll take a sec here in
case you wanna take a photo. All right. All right, so let's expand your use case. So earlier we saw how you had one service. Let's say another application team wants to onboard their service onto Lattice. So you onboard that service, service-2, onto VPC Lattice service network. From a data path perspective,
everything remains the same. Your instances or your consumers want to access service-2 this time. So they open a TCP connection to port 443. Once traffic gets sent onto
the VPC Lattice data plane, Lattice understands where
this traffic must be sent. So instead of service-1, this time, it's sent to service-2
towards the ECS cluster that's in App VPC 3. So again, the net takeaway here is for your HTTP/HTTPS services, Lattice can act as both a load balancer and a router at the same time. There is another mode in
which you can use VPC Lattice, which is for TLS passthrough. So often customers want to use mutual TLS between client and the actual destination. So the good news with Lattice
is Lattice doesn't break or terminate the connection in the middle. So when you use TLS
passthrough with Lattice, the TLS session is terminated directly between the source and the destination, which gives you true
end-to-end mutual TLS. So now we spoke about your
HTTP/HTTPS applications and TLS passthrough, that
opens up the question of what happens when you have a non-web app, for example, a native TCP
application like a database. So Lattice supports that
connectivity as well. For that, you need a new Lattice construct called resource gateway. When I say new, it was launched
re:Invent of last year. So a resource gateway is your
entry point inside of a VPC. To onboard a TCP resource, you first need to define the
resource in a resource config. So I say that, okay,
this specific database inside of my VPC is my resource. Then you associate the resource config with the resource
gateway, and then finally, you put that onto the service network. So net net what you get is, in addition to your HTTPS services, a TCP resource as well that is
listening on a specific port, port 5432 in this example. For TCP resources, also you
can optionally provide a vanity or a custom FQDN. Now let's look at the traffic
flow in this case again. Your instances, they
send their DNS queries with the response that traffic gets sent onto the VPC Lattice data plane. Now again, since Lattice knows where this traffic must go to, this traffic is sent all the
way to the resource gateway that lives in App VPC 3. A key point to remember here
is your resource gateway gets IP address from the
VPC where it's created, and when the resource
gateway sends traffic to the backend target,
it always performs NAT. So by the time the database
sees the IP packet, the source IP would be that
of the resource gateway in this example. So this is your architecture when your TCP resource lives inside of AWS and your consumer also
lives inside of AWS. If we expand this use
case and if we assume that what happens when your database is sitting on your on-prem data center and you're using a mechanism
like Direct Connect to provide IP connectivity
between your data center and AWS, so assuming you have
provided the resource config and you have associated the
resource with resource gateway, nothing actually changes. So if you look at the
traffic flow, in this case, against the instance
wants to access resource-1 that is onboarded onto VPC Lattice. Traffic gets sent onto
the Lattice data plane Lattice understands this traffic must go to the resource gateway. Now, as long as you have IP connectivity between this resource gateway
and your backend target or which is the TCP resource in this case, Lattice can send that traffic as well. So the pro tip here is when
you define your TCP resource, that can either be an IP address or that can be a fully
qualified domain name. So in this case, if you
provide an IP address of your backend database
that's sitting on prem, this architecture would work. Another thing to keep
in mind is as of today, if you define your resource config with a fully qualified domain name, it must be publicly resolvable. All right, so let's expand
this use case even further. Now let's say you have some resources that are already onboarded onto Lattice, but this time, your consumer
is sitting outside of AWS. The consumer in this case is sitting in an on-prem data center, and again, you're using a mechanism
like Direct Connect to provide IP connectivity
between data center and AWS. So in this case, your usual
VPC association will not work. Why? Because VPC association
with service network only provides access to resources
that live within that VPC. So this is where you need a
different Lattice construct, which is called a
service network endpoint. The service network endpoint
will consume IP addresses, from your Edge VPC in this case, and then you would provide
an endpoint association, which basically is saying that
this endpoint now has access to my Lattice service
network and the applications or the services that are onboarded
onto the service network. Now, every time you onboard a resource or an application with the endpoint, you get routable IP addresses
from within the VPC. Now a lot of you already
know where this is going. You have a routable IP address.
You have IP connectivity. So all your consumers need to do is be able to hit or access
that routable IP address. Once those consumers start
accessing this endpoint or this routable IP address
on the specific port, now the traffic again gets
sent on the Lattice data plane. Once traffic is on Lattice, Lattice knows where to send that traffic and whether to a service
or to a TCP resource. So the pro tip out here is use the service network
endpoint association when your consumers are
sitting outside of AWS. Why? Because this will give you
the routable IP address that your consumers can hit. So now let's talk about how
VPC Lattice would coexist with your traditional
networking deployment, for example, with Cloud
WAN or Transit Gateway with an inspection firewall. So let's say this is the
architecture that you deploy for your pilot or for
your POC with VPC Lattice, and in addition to this, you also have an existing Transit Gateway or Cloud WAN deployment going on. Your Transit Gateway or
Cloud WAN has attachments into the same VPCs and you
also have an inspection VPC connected to Transit Gateway or Cloud WAN. So the good news here is that the laws of VPC routing still apply. So inside of these App VPCs, if let's say you have a
default route pointing to Transit Gateway or Cloud WAN, that route will still be used. The only situation in this
scenario when Lattice is used is when instances in App VPC 2 are trying to access the EKS cluster in App VPC 1. For everything else, you can
continue using Transit Gateway or Cloud WAN. So the major point to
take away from this slide is that let's say you
have an existing Cloud WAN or Transit Gateway deployment and Lattice starts appealing to you. You can spin a pilot or a POC within the same network as well, as in they can all coexist together. So now let's compare the two models. On the left-hand side, we have
Cloud WAN, Transit Gateway, and a Network Firewall,
and on the right-hand side, we have Amazon VPC Lattice. The first point to keep in mind is with Cloud WAN or Transit Gateway, that's a network to network connectivity, and because of that, you
cannot have IP overlaps. Whereas with VPC Lattice, since you onboard specific applications and provide access to
only specific consumers, you can work with IP overlaps as well. Actually, as a matter of fact, your consumers and your producers can be on different IP versions even. Your consumer can be IPv4,
your producer can be IPv6, and vice versa. So the IP version or
overlap doesn't matter in the world of VPC Lattice. Secondly, for auditing or visibility, you can use VPC flow logs
or Transit Gateway flow logs on the left side with Lattice. You can do that with
VPC Lattice access logs. That gives you rich
layer three, layer four, and layer seven information as well, and in addition to that, since you onboard your specific
applications onto Lattice, it becomes very easy for
you to discover a list of all applications that
exist in your network. So it goes beyond traditional
IP addresses and CIDRs. Now this is interesting. When it comes to data processing charges in the Cloud WAN or Transit
Gateway-based model, the data processing charges will apply for Cloud WAN and Transit Gateway or Cloud WAN or Transit Gateway
and your Network Firewall and also your elastic load balancers, for example, any
application load balancers that you may be using to
natively expose your service. On the Lattice side,
data processing charges are on Lattice only. So the major thing to keep in mind is since Lattice also acts
as a load balancer, you can natively expose your
applications onto VPC Lattice. So there may be some
cost savings out there because it allows you to retire one level of your load balancers. Then finally, this comes up often. For a multi-region scenario, Cloud WAN supports that out of
the box with dynamic routing. With Transit Gateway, you can
do Transit Gateway peering and static routes. Now, VPC Lattice as of today
is a regional construct. So if you have a scenario
where your consumers and your producers are
in different AWS regions, you first need to provide IP connectivity, the underlay IP connectivity
across the different regions using mechanisms like
Cloud WAN, Transit Gateway, or VPC peering. Now, once you have the
underlying IP connectivity, once routing is working, all you need is a routable endpoint. Now, how do you get a routable
endpoint with VPC Lattice? That's where the service network endpoint comes into the picture that
we spoke about earlier. So net net, multi-region with
VPC Lattice can also work, just that you need to stitch the underlying IP connectivity separately. All right. All right, so with this, folks, we are going to move into the human to workload traffic pattern. So this is the remote
workforce connectivity. Now, this is the diagram you saw earlier. Your use case is you've
got a remote access user on the bottom right trying to
access some AWS applications on the left side, and in this case, we are gonna be talking
about AWS Client VPN first. So it is basically a
client-based client VPN service. Your client can be an open VPN client or you can use an AWS client. From an authentication perspective, you can use various mechanisms
like Active Directory or SAML or use certificates for
mutual authentication. Now on the authorization
side of the house, with Client VPN, you get
a Client VPN endpoint, and you can apply security
groups over there. Additionally, you can provide
network-based authorization by using authorization
rules on the Client VPN. What that basically says is for some contextual
information about a user that my SAML-based
identity provider provides, give access only to specific networks, so again, network-based authorization. The pro tip here is your Client
VPN-based deployment would work well with your traditional
firewalling architectures. Why? Because the Client VPN
gives you a VPN endpoint inside of a VPC. You can attach that
VPC with your Cloud WAN or Transit Gateway. Once you have that attachment, you can use routes and routing tables to punt traffic through a firewall. So for the same requirement again, let's look at an alternative
with Amazon Verified Access. So your use case remains the same. You have a remote user on the right side trying to access some AWS workloads or applications on the left side. So AVA, or Amazon Verified Access, allows your remote users to
access workloads deployed in AWS without using a VPN. For this, all the user requests
first hit the AVA instance or Verified Access instance. How do you do that? You onboard individual
applications onto AVA. When you onboard your
applications, you get an FQDN. Now, when your users try
to hit that domain name, that's how you attract traffic into AVA. Now, AVA integrates out of the box with IDPs, or identity providers, and optionally enterprise
device managers as well. So when a user request
hits Verified Access, it first goes to an IDP to see if the user is authenticated or not. That part is mandatory. The IDP can send some
contextual information about the user as well, for example, is the user's email ID verified or not? Optionally you can integrate with an enterprise device manager as well to keep an eye on the device posture. Now with AVA, every user request
is evaluated in real time, and it works with both HTTP, HTTPS, and non-web apps as well. For web apps, it's a best
practice to associate WAF with your AVA instance so that
you can provide firewalling or protection for the web apps that Web Application Firewall provides. Now finally, you can apply
fine-grained policies on the applications
that you onboard to AVA, and after the IDP authenticates
all the user requests and after your AVA policy
says the request is good, only after that, AVA sends traffic to the backend application. So from this perspective, it provides an alternative to
a firewalling architecture. Now, we spoke about policies. So let's dive into an AVA policy
and see what it looks like. So first we define the structure. You have to provide an effect,
which is permit the request or forbid or deny the request. Then optionally you can
provide specific value for principal, action and resource, and then there is a condition clause wherein you can provide match statements on the contextual
information about the user. Pro tip here is forbid always
takes precedence over permit. Now here's a sample IP-based policy. We are gonna start super simple. So here I'm saying permit the user request if the user's IP address
is a specific value or a specific range. Now, you would use this only if you know that certain clients
will deterministically always have an IP address. Let's look at a slightly
more involved policy now. So in this case, I'm
saying allow the request only if the user is part of a specific identity provider group. For example, the user might
be a part of an HR group or a finance group defined
within the identity provider. Additionally, allow the request only if the user's email ID is
verified, and on top of that, also ensure that the user's
Jamf risk profile is low. So the net takeaway here
is you can use operators like "and" and "or" to
create really advanced and involved statements. Now, AVA allows you to create and attach these policies
on a per-application basis, but as the number of your
applications grow on AVA, it might become a little cumbersome to manage all those policies. So for that, the best practice
is to club your applications that require similar connectivity and security policies into an AVA group and then apply these policies
on the group directly. So now let's see if
Verified Access can coexist or how it can coexist with your Cloud WAN or Transit Gateway-based deployment. So in this case, let's say AVA starts
fitting your requirements, and you want to cut a POC or a pilot. This is where you start
where a set of remote users are using AVA to access an AWS app. Additionally, you have your Cloud WAN or Transit Gateway-based deployment that has attachment
into your inspection VPC and into your application VPC as well. Now if, let's say, you have
a set of existing users that are using Client VPN, that where the Client VPN VPC attaches into the Cloud WAN or Transit Gateway, that part can continue to coexist with your AVA deployment as well. So again, AVA can coexist
with your Transit Gateway or Cloud WAN-based deployment. Let's again compare the two models. On the left-hand side, we
have the traditional model with Transit Gateway, Cloud
WAN, Client VPN and firewalls. On the right-hand side, we have AVA. So firstly, again with
Transit Gateway or Cloud WAN, you provide access to specific
network, networks or CIDRs. Whereas with AVA, you
onboard specific applications and you provide access
only to those applications. Then the second point is reauthentication. So on the left side with Client VPN, you can use maximum session duration to say that your client should reconnect, for example, after eight
hours or after 12 hours. Whereas with Verified Access, since every request is
evaluated in real time, there is no concept of a reconnect. Then this is interesting. So with Transit Gateway or Cloud WAN and Client VPN-based architecture, you can create slightly
advanced architectures, for example, bringing in
your remote users' traffic into a Client VPN VPC and
then using Transit Gateway or Cloud WAN, sending that
traffic to, let's say, a centralized egress inspection VPC for creating internet egress use cases. Whereas with AVA, you
provide secure access only to AWS workloads. All right, so folks, with this, I'm gonna summarize the entire section. So earlier, you heard Tom talk about internet-based use cases
wherein your users sit on the internet and then they're trying to access workloads within AWS. So the verdict over there is use WAF for your web applications
to provide protection, then use AWS managed
services like Session Manager if you have use cases
like secure CLI access that eliminate the need for opening specific internet ingress
ports, because in this case, your instances would actually open up an external session to
the managed service. And then for everything
else, you have your firewalls that you can use to provide protection. For internet egress, the use
case's traffic originates inside of a VPC and the
traffic is going out to the internet. So for this, the verdict is use endpoints as much as possible. You can apply policies
on the endpoints as well. And then in our experience
working with customers, using inline inspection
firewalls for egress is actually a solid use case. Then we spoke about workload
to workload traffic inspection. So for this, two of your
workloads are talking to each other. I'm showing VPCs, but we
saw that with VPC Lattice, your workloads or consumers
can be outside AWS as well. So for this, the verdict is
consider using VPC Lattice for your HTTP, HTTPS, TLS
passthrough and TCP applications, and if you have UDP applications, that's where you can
continue using firewalls. And then finally, for remote
workforce connectivity or human to workload wherein
you have your remote users trying to access AWS resources, the verdict here is use
Amazon Verified Access. That allows you to talk to your web and non-web apps as well. So folks, with this extremely Egyptian hieroglyphic-style
slide, we are gonna wrap up. We are actually doing great on time. So in case you have any questions,
Tom and I will be around and happy to answer any of your questions. Please, please complete the session survey in the app as well because that tells us if we should continue
running such sessions. Right. Thanks, everyone. (audience applauding)
