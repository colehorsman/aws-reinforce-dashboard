# AWS re:Inforce 2025 - AWS Network Firewall: Latest features and deployment options (NIS201-NEW)

**Video Link:** [Watch on YouTube](https://www.youtube.com/watch?v=nauTd9uOtsU)

## Video Information
- **Author:** AWS Events
- **Duration:** 29.1 minutes
- **Word Count:** 3,441 words
- **Publish Date:** 20250621
- **Video ID:** nauTd9uOtsU

## Summary

This session dives into the latest innovations in **AWS Network Firewall**, with a strong emphasis on **simplifying deployment**, **enhancing visibility**, and **improving defenses**. New features include **native AWS Transit Gateway attachment**, **multi-VPC endpoint support**, **automated domain analysis**, and the launch of an **Active Threat Defense managed rule group** powered by Amazon's internal threat intel (MadPot). These updates aim to reduce operational complexity while increasing protection for workloads, especially in hybrid cloud and multi-account environments.

## Key Points

- **Transit Gateway native attachment** now allows direct integration without inspection VPCs, significantly reducing routing complexity.
- **Support for multiple VPCs per firewall** lowers cost and simplifies deployment by sharing a single firewall across up to 50 VPCs.
- **Automated domain list** analysis allows customers to convert observed domain traffic into allowlists with a single click.
- **New monitoring dashboard** provides real-time visibility into top talkers, blocked sessions, rejected flows, and long-lived connections.
- **Active Threat Defense managed rule group** leverages Amazon’s honeypot-based threat intelligence (MadPot) to automatically block malicious traffic.
- **Collective defense model** allows customers to opt-in to share anonymized threat indicators to improve detection across AWS.
- All new features are available in all commercial regions, including GovCloud and China.

## Technical Details

### Deployment Enhancements

- **Transit Gateway Integration**:
  - Attach AWS Network Firewall directly to a TGW.
  - Eliminates the need for inspection VPCs and complex routing.
  - Reduces setup time and simplifies security policy enforcement across accounts and AZs.

- **Multi-VPC Firewall Endpoints**:
  - Attach up to **50 VPCs** to one shared firewall.
  - Each additional VPC uses a **secondary endpoint** (lower cost).
  - Traffic scales automatically to **100 Gbps per AZ**.

### Visibility & Monitoring

- **Automated Domain List Analysis**:
  - Enables "Traffic Analysis Mode" to inspect HTTP(S) traffic.
  - Shows most accessed domains, unique sources, and frequency.
  - Data can be converted to actionable allowlists in minutes.

- **Detailed Monitoring Dashboard**:
  - Real-time visibility into:
    - Active connections
    - Blocked and rejected flows
    - Long-lived TCP sessions
    - TLS SNI matches
    - Top talkers (by IP or VPC)
  - Uses CloudWatch or S3 logs (no added charge from Network Firewall).

### Advanced Threat Protection

- **Active Threat Defense Managed Rule Group** (AMR):
  - Continuously updated with real-time threat intel from MadPot.
  - Blocks:
    - Command-and-control domains
    - Malicious IPs, domains, URLs
    - Known malware communication patterns
  - Integrated with GuardDuty findings (attributed to threat infrastructure).
  - Opt-in for **Collective Defense**: enriches rules using insights from peer activity.
  - Three-step deployment in console under Stateful Rule Groups.

### Use Cases Addressed

- Centralized and simplified **East-West and egress filtering**.
- **Threat-driven policy updates** with minimal manual tuning.
- Support for hybrid and multi-account architectures.
- Enhanced **SOC operations** via integrated dashboards and shared telemetry.

## Full Transcript

- All right, good morning everyone. Welcome to our session
on AWS Network firewall. I would like to start with
the quote from Einstein. He once said, "Everything must be made
as simple as possible, but not simpler." This isn't just clever, but it's very critical
for network security. One missed rule and your network is vulnerable. Our customers face this challenge daily. You ask for simpler security without compromising on protections. We listened and work backwards from there. And today we are launching new
AWS network firewall features that will strip away the complexity and make it easy for you
to secure your networks. My name is Amish Shah. I'm the product manager for AWS Network Firewall Service. I'm joined by my
colleague Prashanth Kalika and in this session we will talk about all the new innovations that will help you simplify your network security and give you the
protections that you need. So what's new with AWS Network Firewall? We have focused our
innovations in three key areas that matters most to you. Number one, deploy. Where we are simplifying firewall setup
with native integrations. Number two, discover. Where we are enhancing visibility
so you can stay secure. And finally, defend. Where we are using advanced threat intelligence
to give you the protections that you need for your cloud workloads. So throughout this session you'll see how all the innovations that
we have launched recently helps you strike that balance of simplicity without
creating security gaps. Let's look at some of the
innovations that we launched that helps you with the deployment. So our customers tell us that securing VPC architectures
can be a complex task. It often requires
deploying inspection VPCs and creating multiple route tables, which means now you have to
manage all those route tables. It can increase chances
of misconfigurations. It can also increase
overhead of your operations, and these type of pain points
can slow down your deployment, which means there is a higher risk, because as you don't move
your protections faster, there is a chance someone can act and break into your network. So how do we prevent and help you with
features that enables you to onboard your firewalls quickly? And what if you can completely eliminate that inspection VPC and still get those centralized egress controls that you need? That's exactly what we are launching with our latest announcement. I'm extremely excited to announce that AWS Network Firewall
now offers native attachment for AWS transit gateway. This game changing innovation simplifies your network architecture and strengthens your security posture. By eliminating the need for
creating those inspection VPCs, we make it easy for you to deploy firewalls in a
centralized deployment model and you don't have to now
manage the routing tables for those inspection VPC. Next, you can quickly spin up firewalls and configure them easily, which means now there is
reduced time to protections. Also, this integration allows you to consistently apply security policies across availability zones. So overall resiliency is improved. And as you have more VPCs that
are, you know, coming over, you can consistently
apply the same security policies for those new VPCs that are being inspected by this firewall. So here I'm showing a sample architecture where the requirement was to
do East-West traffic filtering, say for example, VPC to VPC filtering, and this can be within a same account or it can be across accounts. There was a need to use a
transit gateway to route traffic between these PCs. With the new native attachment feature, the network firewall and the connectivity between
the route transit gateway and network firewall is
automatically done for you and you don't have to worry
about the inspection VPC. So the things that you see on the left side here, on my left side, where you have a network
firewall and the transit gateway, that is all installed
automatically for you and you don't have to
about the connectivity. So now when you go and create a new network firewall, there is an option for you to
select the transit gateway. You want to attach this
network firewall too. You can select the availability
zone where you want to deploy this network firewall. You can add multiple
availability zones here if you want high availability. Once you do this, on your
firewall details page, you will see that this particular
firewall is now attached to transit gateway. There is an attachment ID
that you can see over there as well as the availability zone where this firewall was installed. So this makes it super
simple for you to deploy that centralized inspection model. Isn't it exciting? Now let's look at some other innovations that will help you with deployment as well as bring down the overall cost of firewall endpoints. We started supporting multiple VPCs for AWS network firewall
earlier this year. How many of you are familiar with distributed firewall deployments where you deploy one
endpoint in each VPCs? There are a few of you. Yeah, so customers use a
distributed firewall deployment, which where where you need
isolations for your workloads or if you want to reduce a blast radius and apply specific policies to
those workloads in that VPC. So that is still supported and relevant for some use cases, but as your network scales, so does the cost of your firewall endpoint because the more number of VPCs, the more number of firewall endpoints that you have to deploy. With multiple VPC endpoints per firewall, you can now attach up to 50 VPCs to a single shared firewall, thereby bringing down the overall cost of your firewall endpoints. The rules that are now configured on a single primary firewall can be shared with all these 50 VPCs and your traffic bandwidth will
automatically scale, right? Your firewall bandwidth
will automatically scale based on your traffic volume, up to a hundred GPS per availability zone. So let's look at a visual
representation on what it used to be before multi VPC per end, multi VPC endpoint per firewall. So previously, you could only have one endpoint firewall in A VPC, which means behind the scene if you know there is like a gateway
load balancer endpoint that is assigned to a firewall and you also have a
fleet of EC2 instances, which automatically scales as your network traffic volume grows. So there are certain
thresholds that we monitor, such as active connections,
number of packets, etcetera, and we automatically scale the firewall to support your traffic volume. So again, as you add more
VPCs in that architecture for every VPC you had in your
specific network firewall, which increases cost,
increases complexity. With multi VPC, you can attach all these VPCs to a single shared firewall. Now how would you do it? So say in this deployment
you are the owner of a primary firewall where you create a firewall in your VPCA in availability zone one and you want to share this
firewall with different VPCs and these VPCs can be in same account or different account as long as they are in same availability zone. So you will share this
firewall with VPCB and VPCC. Now, the owners of VPCB and VPCC will create VPC endpoint association and associate this, that VPC, to the primary shared firewall. When you do that VPC endpoint
association, by the way, this VPC association
is a new resource type that we are launching with
this multi endpoint feature. So here is how actually
you will configure that. So when you go to your management console
under network firewall, you will now see VPC Endpoint Association. This is where you will go and select your primary firewall. You will select the VPC
that you want to attach to this firewall and
specify other parameters. And once you do it, we will deploy that secondary firewall
endpoint in that VPC that you have defined. And you can see all the mappings
here in the VPC endpoint association mapping table. Again, you can share primary
firewall with up to 50 VPCs and the way we bring down
the cost is instead of paying for the primary firewall
endpoint in each of those VPCs, you are only paying for
primary firewall for one VPC and secondary endpoints which are deployed in each of those VPCs. There is like a much reduced price on the endpoint of our cost, thereby bringing down the
overall cost of your deployment. Now let's look at some of
the things that we are doing to help you get additional
visibility about your traffic. Traditionally, firewalls
require customers to create and maintain their own list of allowed or block domains and there are several
challenges with this approach. By the way, anyone here maintains their own set of allow
list to only send traffic to trusted domains, right? A lot of customers when they start, they start with just an alert mode, because they don't know
what should be allowed or what should be denied. So the challenge is that we
have heard from customer is, you know, they spend hours
every week analyzing logs to figure out which
destinations should be allowed from their workloads. This manual approach
is very time consuming and it is also prone to error, right? Think about it. Effectively managing this manual list at scale in a large organization, it takes a lot of time and you have to keep on repeating this because things constantly change. Also, there is a possibility that because you didn't update
that allow list frequently, your rules can be outdated or ineffective, which means sometimes you
have very permissive set of allow list which can
increase security risk, or your list is too restrictive, which can actually
block legitimate traffic and that's where security teams are constantly under pressure
to maintain tighter security and remain compliant with business or regulatory requirements, but also ensure that business operations are not disrupted because of the policy. With AWS network firewall, you can easily build that allow list. So things that previously
used to take weeks can now be done in minutes. We introduced a feature
called automated domain list and here is a sample report of the domain based insights that you get from AWS network firewall. To use this feature, all you have to do is
enable the analysis mode, the traffic analysis mode, checkbox. Once you do that, network firewall will
start inspecting HCDP and HCDP's traffic that is
going through your firewall. And you can see a detailed
view of the number of domains that were
accessed through a firewall. And the frequency on how
often they were accessed. Also number of unique sources
that were trying to reach to those destinations. With 30 days of historical
data in this report, you now have real insight on
where your traffic is going to, which can be used to update
your firewall policy. And what is powerful here is, it's not just giving you
this insight with one click. You can convert this insight
into real security policies and deploy them on your firewall rules. So instead of, you know,
maintaining manual list, you now have real data of what's
going through your traffic, going through a firewall and you can convert them into
policy using the real data that is very specific to your deployment. This feature is available
in all AWS regions where AWS network firewall is available, including GovCloud
region and China regions. So you can now go and generate report and see all the domains that
are going through a firewall. To further improve visibility, we recently announced a native
new monitoring dashboard on network firewall. Visibility has always been one of the top asks from our customers. They want to see what's
going through my firewall, not just to monitor, but it also helps them troubleshoot certain issues that are
relevant to their configuration. So with this new detailed
monitoring dashboard, you can get a high level
summary of active connections, how many connections were
blocked by my firewall, etcetera. But you also get detailed
insights about top talkers. Again, top talkers has been one of the key asks from customers. Like we had a large customer who started seeing a significant
increase in their traffic processing volume from firewall and they wanted to understand which of my workloads are
generating most traffic. Using top talkers inside, you can easily filter traffic based on say source IP address to identify which VPCs or which sources are
generating the most traffic and sending them through firewall so that I can now either optimize my rules or charge back to the account owner. Besides that, there
are additional insights that are available from this dashboard. So you can here see, these are all the domains or the destinations that
were blocked by the rules that I have in my firewall policy. Similarly, I can also see which
destinations were rejected. So these are the traffic flows that are matching my reject action rules. I also have visibility into
my long-lived TCP sessions, so there's a lot more
details that is now available to you directly on the dashboard, instead of you going
to say CloudWatch logs and running your own queries or doing your own log analysis. Additional insights such
as if you want to see what are all the TLS SNI that are matching my policy or my security rules. All this top X analysis is available directly on the dashboard. And again, this dashboard
is available in all regions. If you go to the monitoring
page of the network firewall, you'll see a new checkbox to
enable detailed monitoring. Once you do that, you'll
start seeing all this insights on your dashboard. Question. - [Speaker] is there a charge for it? - Yeah, so the question was, is there a charge for this dashboard? So there is no incremental charge from network firewall for this dashboard. All you need to do is as
you have enabled logging, you can send these logs
to CloudWatch and S3. So whatever logging charge that you pay on CloudWatch or Amazon S3, that would still continue to apply, but there's no additional
charge to build this dashboard. All right, so now I'll pass it to my colleague Prashanth Kalika to take you through the
rest of this session. - Moving on to the defend theme, I'm excited to announce that AWS Network Firewall
now offers active threat defense managed rule group. This rule group leverages
Amazon threat intelligence to protect your VPC workloads
against active threats targeting workloads on AWS. Before we dive into the
feature and use cases, let's look at various pain points customers
are facing on this front. We heard from customers, especially customers who
deploy hybrid cloud models, they have challenges with active threat protect protections, especially in four areas. As attack surface widens, they have to constantly
deal with threat landscape, evolving threat landscape from various types of network based threats, cloud native threats and zero days to. Two. They have to use multiple tools to detect active threats today from third party threat feeds, to vulnerability management, to SIEM and SOAR and monitoring tools. Third, most of these third party security tools don't have visibility
into AWS infrastructure, making it challenging to identify active threats accurately. From constrained access
to various AWS resources and entities and network traffic to limitations in log data
and quality of alerts. Fourth, they also have sometimes have to deal with delayed threat response
due to analysis bottleneck caused by multiple dashboards, time taken to create complex custom rules and managing consistent
compensating controls across multiple enforcement points. To address these challenges, AWS has invested heavily on
building its own global honeypot infrastructure called Mad Pot, where we have deployed millions of low interaction
to high interaction honeypots and decoys to capture attack TTPs of bad actors targeting workloads on AWS. This real time data, threat data, is further curated into IOCs and IOA's, such as attack infrastructure, IP's, domains, URLs, and threat signatures from
various malware communication and known exploit attempts on
the any part infrastructure. AWS uses this contextual and real time actionable intelligence to power various firewalls to support active threat
protection use cases. To address these challenges, we just launched active threat
defense manageable group on AWS Network firewall
addressing use cases that protect VPC workloads
against active threats. Anybody has used managed rule groups on network firewall so far? Awesome. This new AWS manageable group, in short, AMR's, address
four key use cases for AWS network firewall customers. First, threat protection. By configuring this AMR within
network firewall policy, you can now automatically
block malicious traffic and protect your VPC workloads
against active threats. In other words, this AMR will
block various active attack infrastructure indicators such as command and control C2's,
endpoints, embedded URLs, and malicious domains. The second use case is rapid protection. This AMR will continuously
be updated with new rules as and when new threats are discovered, providing immediate protection
against active threats. Three, streamlined security operations. Security findings on GuardDuty attributed to active threat defense
as a threat source, can now be automatically blocked by using this AMR on network firewall. Fourth, collective defense. By configuring this AMR, you enable deep threat
inspection by default, which enriches the existing threat data with additional TTPs from
blocked traffic logs. In other words, the
rules are now augmented with precise indicators
such as threat signatures and artifacts based on evidence seen within the customer network logs. This allows for sharing
threat intelligence from one active threat defense customer to all active threat defense customers. Also, you can opt out of this capability if you
don't want this feature to actually process your network logs. Also, this feature is not fully supported as part of this release, but will be available in
the next release update. So now let's look a visual
representation of the console or how to get started. So this is the console
network, firewall console. You just have to start
with creating a policy or updating the policy to add this AMR. Within the policy, within the policy under
the stateful rule group, You can click on action and you can drop down to
add manage rule groups. Within that, you will see
active threat defense rule group show up with a rule rule group called attack infrastructure rules. Just check mark that. This rule group is set to default by drop. You can toggle to alert if you wish. Finally, you can add this policy to the network firewall policy. This rule to the network firewall policy. Pretty much three steps
and you can add this AMR. Now, there is an additional
capability that we have brought to bear as part of this feature is visibility of these rules. Within the network firewall console, you can click on the rule group and that will provide
you additional details and search options. This is a visual representation of the console showing active threat defense rule group details
such as you can see total rule capacity consumed by this rule group. And also you can see
the last updated time. You can also look up the threat names and the indicators you
are protected against. With this, we end the presentation. Just to recap, we covered features related to deployments such as
transit gateway integration and multiple VPC endpoint support. As part of visibility, we
covered automated domain list and new dashboard for monitoring. And finally, as part of Defend team, we covered active threat
defense, manage rule group. All of these new rule
groups, all of these, sorry, all of these new features
address various aspects of simplification that are delivering, that are being delivered
based on customer feedback. And we will continue
to evolve this feature based on your feedback as
you adopt these features. Here are some of call, here are some of the call to actions that you can take advantage of. There's an upcoming workshop
on securing egress controls to defend against zero days and ransomware where we
cover some of these features. You can also look up the
firewall deployment guide. There's a QR code here that you can, it takes you to the deployment
guide so you can actually get that details as well. And for those who are new
to AWS Network firewall, please talk to your account team about network firewall POC credits, or you can reach out to us at this email.
