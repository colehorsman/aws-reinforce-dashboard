# AWS re:Inforce 2025-Amazon GuardDuty Extended Threat Detection: Identify multi-stage attacks-TDR308

**Video Link:** [Watch on YouTube](https://www.youtube.com/watch?v=hJKIzLe49kE)

## Video Information
- **Author:** AWS Events
- **Duration:** 57.4 minutes
- **Word Count:** 7,914 words
- **Publish Date:** 20250620
- **Video ID:** hJKIzLe49kE

## Summary

This session introduces **GuardDuty Extended Threat Detection**, a new capability designed to detect **multi-stage, multi-vector attacks** in AWS environments. The presenters walk through how this feature correlates telemetry across identity, compute, and data layers using machine learning and threat intelligence. They demonstrate real-world attack detection involving EKS compromise, IAM misuse, and crypto mining behavior, and share best practices for enabling protection plans that feed this advanced correlation engine. This talk also offers insights into the **ML-based ranking model** that powers attack sequence detection, including how GuardDuty prioritizes critical threats and reduces alert fatigue for security teams.

## Key Points

- **Extended Threat Detection** in GuardDuty uses **AI/ML** to correlate multiple low- and high-confidence signals across time and resources into a single "attack sequence" finding.
- These **attack sequences** are labeled with **critical severity (level 9)** and are meant to highlight high-confidence, multi-stage attack behavior like compromised credentials or EKS cluster takeovers.
- Three supported scenarios:
  - **Compromised IAM credentials**
  - **S3 data compromise**
  - **Compromised EKS clusters** (new as of this session)
- GuardDuty consumes telemetry from:
  - CloudTrail, VPC Flow Logs, DNS logs
  - S3 data plane events
  - EKS control plane and runtime
  - RDS login attempts
  - Lambda execution patterns
  - Malware scanning on EC2 and S3
- **No additional cost** to use Extended Threat Detection — enabled automatically once the relevant protection plans are on.
- **Detection accuracy is high**, with only ~2 attack sequence findings per account per quarter.
- Customers can **triage faster** using rich contextual data (e.g., affected resources, MITRE ATT&CK mapping, remediation steps).
- New dashboard shows whether all necessary GuardDuty features are enabled to support these detections.

## Technical Details

### Telemetry Ingestion & Protection Plans

- **Foundational GuardDuty** (IAM + network)
- **S3 Protection** (data exfiltration/destruction)
- **EKS Audit Logs** (control plane)
- **EKS Runtime Monitoring** (host/pod behavior)
- **Lambda Protection** (execution patterns)
- **RDS Login Protection** (brute force, anomalies)
- **Malware Protection** (EC2, EBS, S3 uploads)

### Extended Threat Detection Pipeline

- Ingest and normalize telemetry → extract signals (weak/strong)
- Group related signals by entities (IP, user, cluster, etc.)
- ML ranking model prioritizes threat clusters
- **Findings include**: resource ARNs, IAM roles, container images, processes (e.g., XMRig), DNS queries, MITRE mapping

### ML Techniques

- **Representation learning**: entity behaviors (e.g., usual APIs, IP ranges)
- **Ranking model**: evaluates markers like risky API usage, low-reputation IPs, proxy use
- Uses customer feedback and real-world incident validation to improve accuracy

### Deployment Best Practices

- Enable all protection plans across all accounts and regions for "set-and-forget" coverage
- Alternatively, selectively enable features based on workload types (e.g., S3-heavy vs EKS-heavy)
- Integrate findings into SIEM/SOAR via EventBridge or S3 exports
- Use GuardDuty’s built-in remediation guidance per finding type

## Full Transcript

- Good afternoon, thank you so much for spending your
after-lunch sessions with us. We'll try to be as engaging as possible. So you know, let's call it the tiredness of after lunch will be
offset by the presentation. And my name is Shachar Hirshberg, I'm a product manager at Amazon GuardDuty. I help customers secure
the AWS environment and specifically with a
focus on active threats. - Hey everyone, thanks for joining. I'm Sujay Doshi, and I'm another product
manager with GuardDuty, with the same mission as Shachar said. - So just by a quick show
of hands, just curious, how many of you have heard
about GuardDuty before? All right, so pretty much everyone. Great. - Yeah.
- Who is familiar enough with GuardDuty to come up to the stage and talk instead of us? All right, just joking. How many of you are using
GuardDuty as a customer? Almost everyone. Amazing. And how many of you're using all of GuardDuty's protection plans? Okay. How many of you're
using some of them? Okay. Kind of like majority. And how many of just using base GuardDuty like the core service itself. Okay, so it sounds like all
of you pretty much use a mix of like GuardDuty itself plus the different protection plans. Amazing. So we have a lot
of to talk about today. And thank you, Sujay. And we will talk mainly
about multi-stage attacks that can target your cloud environment and how GuardDuty helps you
detect these kind of scenarios. And to get there, we will
walk through what is GuardDuty and especially the
different protection plans that we have in place to help you understand how GuardDuty
can put it together and detect attacks that
span not only, for example, across identity, but also network
and data plane of services such as S3, control plane
of services such as EKS. Because what you see really
in today's attacks is that they span across multiple dimensions and attack vectors. So a bit about the agenda for today. We'll start with covering
the threat intelligence that powers a lot of the
detection capabilities that we have in GuardDuty. And then continue to speak
about the different options that you have on when to use what. Give a little peek on
the behind the scenes on how we are able to detect detections and do it in an effective manner, and share a new capability
that we released yesterday. It's a major expansion off a capability we released last re:Invent, and I hope many of you
have heard about it before. It's called GuardDuty
Extended Threat Detection, and it's focused primarily on detecting these multi-stage attacks. So starting from the
threat intelligence side. And just to give a quick
intro on GuardDuty. I know many of you are familiar with it, but GuardDuty ts our
threat detection service, is a managed offering that
helps you detect active attacks, threats in your cloud environment. And it's a fully managed
offering from the perspective of getting access to the relevant data and enabling the service itself. Once you enable GuardDuty, and you can do it via the
console or CloudFormation or API with just a few simple steps, GuardDuty automatically gets
the information it needs, which is cloud relevant
telemetry such as CloudTrail logs and other type of logs that
we will cover in a moment. And from that moment, it continuously monitors your cloud
environment for threats and uses multiple techniques including a vast usage
of machine learning. And we'll talk about how
this machine learning works a bit later today,
and as well as stateless and stateful rules to be able to detect threats in
your cloud environment. We also use threat intelligence, both threat intelligence
curated by Amazon as well as threat intelligence shared with us by third party vendors. And from the moment you
enable it, you don't need to update GuardDuty,
maintain it, back sheet, or do anything that
relates to the management of the operation of the service itself. We do it automatically on your behalf. A bit about the scale that we operate. GuardDuty, and I think this room is actually a great
representation of it, is used by tens of thousands of customers across virtually every
industry and geography. We protect millions of AWS accounts, and as a result, millions
of a EC2 instances, S3 buckets, EKS clusters,
and so on and so forth. And this unique vantage point allows us to detect not only common threats but also emerging patterns that we start to see across potentially
a subset of our customers. And then quickly add detection. So if this kind of attack
pattern will become popular, let's put it this way, we'll be able to quickly detect it
across our customer base. We have three sources of threat
intelligence and many more, but this is a sample that we use. The first one is called Mithra. Mithra is one of the largest
neural networks in the world, and it contains billions of nodes and edges that we use to map DNS requests across the visibility that
GuardDuty and really AWS has. And that allows us to detect suspicious and malicious domains, oftentimes weeks before we see them come up from other threat intelligence providers. So very big vantage point, a
lot of visibility, allows us to detect suspicious,
let's call it domains, and other activities early. Another service capability that we have inside of
AWS is called MadPot. MadPot is a global network of honeypots that helps GuardDuty detect activity that can be malicious. If you haven't read
yet the blog on MadPot, I would highly recommend
reading it, it's a great read. If you just google AWS MadPot
blog, you'll probably get it as one of the first resorts. And just to give a bit of sense on the scale GuardDuty operates. Last Prime Day, we analyzed
trillions of events every hour, an increase of 30% from
last year, and we continue to operate in this kind of
scale on a regular basis. And you know for Prime Day,
I know I was responsible for some of this activity,
I bought a lot of things, maybe you guys bought some things as well. But seriously folks, these
scales allows us to operate as a very effective
threat detection service, because we analyze so much activity and have visibility into many things that are happening across
the AWS environment. So a bit about what is this
analysis that we actually do. GuardDuty, and that's
on the left hand side of the screen, process
multiple telemetry sources, that range from CloudTrail, which is basically representation of what happens in the
control plane of the cloud, who did what, where and
when, to network activity such as VPC flow logs and DNS logs, and variety of additional
telemetry sources that helps us get more in-depth protection and detection for
services such as databases and container services. So for example, we process or
able to process S3 data events and detect data exfiltration and data destruction
attempts as a part of it, because we can see all the
get, put, delete requests that are being made. And these attempts to
perform data exfiltration and destruction can be a part of a potential ransomware attack. We just don't call it ransomware, because we don't know if
someone asks for a ransom. In addition to that, we have visibility into runtime activity that is powered by the sensor that we
have, that you can deploy, that gives us visibility
into runtime activity for EKS clusters and EC2 instances and ECS target clusters. And we also have a variety
of other protection plans that we will cover more in depth in the second part of the presentation. But conceptually the way that
GuardDuty works is really ingest all of these flow logs, whether it's the more generalized logs like CloudTrail or VPC flow logs or more service specific
logs such as S3 data events or RDS logging attempts to be able to detect specific threats,
that you would probably want to discover as early as
possible, to respond to. And from your perspective,
all of these processing of telemetry results in over 175 types of findings, ranging from
suspicious IAM activity, to crypto mining, to data
exfiltration, and many more. And these types of
findings can be consumed whether by the GuardDuty console. So you can go into the GuardDuty service and act on them there. You can use Security Hub, which is our CNAPP offering,
and is a part of it, aggregates findings across
accounts and regions so you can respond on them
within the Security Hub console. And you can also use Amazon Detective, which is our investigation service, or send a finding outside and
use, for example, your SIEM or ticketing solution to
work on these findings. And to be able to send findings outside, you can use EventBridge to do a more event driven architecture or export the findings to S3 buckets and pull them from there. And one last thing on
the unique security value that GuardDuty has is that the processing of all these events, all the raw telemetry,
can't be interrupted by an adversary from the outside, because we get this log
sources, whether it's CloudTrail or VPC flow logs, or any of the other ones,
straight from the source, because we are a native
service, which means that even if an attacker comes
in and start, hopefully not, but start compromising your environment, even if they turn off CloudTrail
to try to evade activity, doesn't matter to us, because we always get the
logs straight from the source. Even if they turn off all
the different log sources, we will still get them and report to you on
any malicious activity. So we have all of these things, and it's great, it provides
a very broad coverage for cloud security threats. But what we've been hearing
from customers really over the past year is that they get a lot of alerts from GuardDuty as well as many other security
tools that they have. The one thing I never hear
from a security team is that, you know, I just
don't get enough alerts. I just say, my day is
kind of like half empty, because I just don't
have work to do, right? All of us are overwhelmed with alerts and we get so many different,
so much information from so many different sources. So we wanted to make
it easier for customers to connect the dots between
the different alerts, what we call findings, and help you identify the
most important threats, the most pressing one with
the highest confidence to be true positive. Such that if you only do one
thing when you start your day, you will start by looking
at these findings. And this is why in December, we released GuardDuty
Extended Threat Detection. This capability uses AI and ML to connect the dots
between different signals, whether they are strong
signals which are finding, or weak signals that are events that are potentially suspicious but not suspicious enough for
us to send a finding to you, because we don't want to overwhelm you. And we correlate all of these signals across a 24-hour time window and resources to detect attacks. And we call this, the output of this capability,
attack sequence findings. It's a new type of finding that
we released last re:Invent. And these attack sequences
have critical severity. It's severity, if you are
more familiar with GuardDuty, we had severity up to eight in the past, and this is severity nine, it's critical. And these attack sequences can pass multiple events
organized on a timeline, and we will see a quick
demo of them pretty soon. And the idea is to help you
focus primarily on these type of findings which represent
the most important threats to your cloud environment,
the most pressing ones. Now just a bit about the scale of it. Since we launched this
capability last re:Invent, it's been running successfully, and we worked with many customers to help them if they had
any potential threats to their cloud environments. Over the past three months
we generated 13,000, 13,000 attack sequences
across the millions of AWS accounts that
we protect, which means that if you actually look at the average, it ends up being less than
two findings per account for a period of three months. And we talked about the problem of getting too many findings and not knowing what to do with them. So when you get this type of finding, on average you'll get two
of these every three months. So that translates to
eight of these per year. That's a pretty manageable volume. So when you get one of these,
the recommendation from us, and we strongly recommend
it, is to address them as early as possible. I can say that the true positive rate for these findings is very high, 'cause we validate them
with customers many times. And it's really a managed
approach, it's enabled by default. You don't need to do
anything to enable it. There is no additional
cost, which can be nice, to use to get this capability. The only thing that you do need to enable is the underlying
protection plans. And we'll talk about that in a moment. And we use the broad visibility we have to continuously update the detections powering these findings and
detect emerging threats as well. So what's new? Yesterday we released a major
expansion to this capability, and it now supports EKS clusters as well. And that means that when we see
multiple actions being taken and in relation to an EKS cluster, we will create this critical severity, which would be attack sequence
for compromised EKS cluster. And it will correlate
activities that relate to the EKS cluster automatically
across EKS audit logs, runtime activity, as well
as the cloud control plane. So to translate it to
GuardDuty's protection plans, we will correlate activity
from foundational GuardDuty, because we might see some
discovery activity from CloudTrail that doesn't even relate to EKS yet. But then we start seeing suspicious activity
in EKS control plane and suspicious activity
from EKS runtime monitoring that looks into the
activity on the host itself, and correlate it all
together into a unified story that you can then address. All of these findings are
mapped into MITRE framework, MITRE ATT&CK framework. So we know that again, you
have many security tooling that you use, and MITRE is a good way to understand these type of finding amongst all the hundreds that I have, what does it relate to, what did the attacker did
so far in the attack chain, and assess the importance and the remediation that
you want to do as a result. In terms of the scenarios that we cover, we cover three scenarios now. Compromised credentials, which are the number one
initial attack vector to cloud environments. Compromised data for data residing in S3. And that is most importantly
for many customers, the most important organizational asset. And the one I just mentioned,
compromised EKS cluster. And together it provides
you a pretty wide visibility that supplements the
already coverage you have with GuardDuty across compute,
control plane, and data. Now let's move to the fun part and I'll show you a demo. Okay, if you start, if the text will be too
small, just let me know. Raise your hand or something. So we are now in the GuardDuty console. And as you can see here,
this is the general dashboard that we have in GuardDuty. And within it, you can see
if you have attack sequences. This is specifically a demo account. So you have many attack sequences there, because I generated them on purpose. But typically the ratio that you would see would be
probably one to a thousand. So for each thousand GuardDuty findings, you can expect one attack
sequence give or take, it varies according from
customer to customer. Now you have a dedicated page called Extended Threat Detection, and this page allows you to see, maybe I'll zoom in a bit
more, allows you to see that and validate that you have
the relevant protection plans to get the most out of this capability. So for each part of GuardDuty, we share what scenario is covered and which finding type
corresponds to this scenario. For foundational GuardDuty,
it will cover compromise related to credential misuse, and then, you'll get the IAM compromised
credential attack sequence. Now what is new in this page, if anyone have seen it in the past, we had the related protection plans. And the first protection plan, that was relevant when we
started that re:Invent, was S3 protection for
coverage on compromised data. But now we added EKS protection
and EKS runtime monitoring, and that allows you to detect compromises that relate to your Amazon EKS clusters and get the finding type
of EKS compromised cluster. And let's take a look at this
finding type and learn more. So I'm just sorting by severity to find the attack sequences, and we can go to the first one. This attack sequence covers a potentially
compromised Kubernetes cluster. You can see that it has
a critical severity, and it correlated 13 different signals. So just to go back to
what we discussed earlier, instead of you having to
analyze 13 different findings and understand and analyze how
they relates to each other, we do it on your behalf. And in this case the activity
started around 3:00 PM and ended around 4:00 PM, so
we correlated across an hour. And in real clusters, you'll probably see the activity happening
across multiple hours, even though the velocity of attacks have been
increasing across the industry. When we see new events
happening, we update the finding. So this finding would
be the source of truth as it relates to this specific attack. You don't need to look at other findings, because we update it automatically. And on the left hand side, we provide more of the security intuition
behind why GuardDuty flagged it to such a suspicious activity. So we can see that multiple
MITRE ATT&CK tactics and techniques were used, ranging
from privileged escalation all the way to execution and impact. And GuardDuty also identified
DNS queries being made to crypto mining domains. Now there is a lot of information within the attack sequences, but an easy way to kinda
pivot and understand what or which resources are involved is to go to the Resources tab. And there we group by the events per the resource, AWS resource type. So in this case, you can see that an EKS cluster was compromised. If you click on the different
MITRE techniques, tactics, sorry, you can see the
different GuardDuty findings that relate to this particular cluster. And in this case, we see
privilege escalation, impact execution, very suspicious. And we provide the information about the resources itself as well. So you can see the exact ARN,
you can even see the EC2s that relate and power this cluster, and pivot to the EC2 or EKS console to learn
more about the resource. We can even see that within the cluster, a specific pod was compromised,
and we get information after the container level
of the specific container that was slightly compromised. You can click and see
the different activity that happened associated with container, and even get information such
as the container image used. And that mainly is relevant
for supply chain attacks. And we can also learn that
an access key was involved, and we saw seven different
signals associated with this access key. So we have a likely compromised access key as well as likely compromised EKS cluster. And then we can go and dive deeper on the different signals, which are the timeline that
we build automatically, to learn about the activity that happened. So we can see that a privileged
container was launched on this cluster. We get that visibility
from the EKS control plane. And likely what happened is that someone compromised an access key, whether it was exposed publicly or in another way, launched
this privileged container, and then started performing
crypto mining on it, because we can see that a bitcoin related
domain name was queried, and we can even go and see which specific domain was queried, and it happened as a result of a new binary that was executed. Now we even provide information
on the specific processes that were involved in
this specific attack, because we correlate the activity from both the EKS control plane
and the runtime monitoring, which allows you to get very
high fidelity information that you can then take action with. And in this case, you
can see that an XMRig, which is a popular crypto
mining tool, was executed. So as you work through these findings, you can look at the timeline,
understand the story and how it involved. That's really the right hand side. And on the left hand side,
we provide the context on the MITRE tactics that
were involved in this event as well as the different indicators which are the security intuition on why GuardDuty thought this
is such a suspicious activity. And in this case, you know, the indicators entail multiple MITRE
tactics and techniques that were involved,
crypto mining processes, and you get the exact
processes that were executed. They then communicated
with crypto mining domain. And if you want to learn more, you can see the specific actors from the role that was involved, to the Kubernetes user,
to the different processes that were involved as part of this event. So by using these new attack sequences, you can really focus your effort on the highest priority threats and get very rich contextualization that helps you understand
exactly which entity or identity misused
your cloud environment, the actions they took, how they did it. And then what you can use
is the remediation guidance that we offer. So here on the left hand side,
we have the Remediation tab. And there, we provide
guidance for each finding type on which actions you
should consider taking to respond to and remediate the event. So from the moment you
learn about the finding, all the way down to remediating
it, GuardDuty can help you detect suspicious
activity or malicious one and respond to it effectively. Now I would like to invite
my colleague, Sujay, back to the stage and he
will do the second part. Okay, click again. - Okay, perfect. All right. Thank you Shachar for
your detailed insights into how GuardDuty can help you modernize detecting sophisticated
compromised clusters running in your EKS deployments. Good afternoon and welcome
again, and thanks for joining us. Now for the rest of
this session, we'll talk about some of the patterns and kind of the best practices that we see in the field
from different organizations in terms of GuardDuty adoption of different protection plans
and features that it has. It can become overwhelming
generally to kind of think about what does good look like for me. So hopefully in the next
few slides, we'll try to provide some prescriptive
recommendation based on the patterns that we see
and hopefully that aligns. So really depending on
multiple different options that we'll talk about, the
end goal is to help you determine what really does good look like when it comes to enablement
strategy for GuardDuty and its various protection plans. So the first pattern that we
see is where customers want to enable all the features
in all AWS accounts in all AWS regions where they
have the workloads running. This really is the gold standard for kind of centralized security
administration, truly set and forget model wherein you don't need to worry about getting
protected with GuardDuty as and when you'll have
ephemeral workloads and accounts that are coming
up and decommissioned. There'll be automatic
protection for all the features that GuardDuty today has the
offering to detect threats in. And any new workload that
gets attached to the accounts where you have the features enabled, it automatically protects. And there's a 30-day free
trial for every account, every feature, every region. So that essentially provides a mechanism to evaluate the usage and
also evaluate the efficacy before you go all in and basically go to paid
usage in production. The second pattern or the model that we see
is selective enablement wherein customers would only want to enable different
protection plans in GuardDuty on specific accounts where they have those
targeted workloads running. Now this is also a good
option for customers that have segmented environments and a specific compliance that they need to achieve depending on their
operational requirements. And this kind of helps
strike a fine balance between targeted protection
and cost management, and you don't need to
worry about GuardDuty spend for accounts where you specifically do not require the different protection
plans that GuardDuty has. But the benefits, seamlessness, and ease of use translate
from the first option to here as well where you'd be able
to use 30-day free trial for all, again, accounts where
you have enabled the feature, but every region, and use it to kind of validate the efficacy and
kind of the spend levels. And the third pattern that we see is kind of a better together approach depending upon the workloads that you have, and again kind of different
segmented environments. We also see customers
using GuardDuty findings, because of the virtue of being first party and having native visibility to data for some of these core AWS services, a lot of the customers leverage
the findings from GuardDuty and would integrate it
to their downstream SIEM and SOAR workflows, or
basically any downstream system that can consume data from
let's say, EventBridge. And this makes it seamless for having a holistic threat detection and incident response workflow where GuardDuty findings can contextualize and enrich the data into those systems, and customers can kind of
reduce that mean time to respond essentially by using multiple
different tools facilitated with seamless integration with GuardDuty. So now in this slide,
we'll look around kind of diving slightly deep into
what each protection plan that GuardDuty has to offer, what are the specific
things that we monitor and what are some of the
prerequisites that make sure that you're effectively
able to leverage some of these offerings from
GuardDuty for threat detection. So the first one is foundational sources wherein GuardDuty monitors. By default when you enable an account, with GuardDuty, we are automatically enabling foundational threat
detection, encompassing of monitoring from your
CloudTrail management events, that is the control plane or the API interaction layer for your, for different AWS services that are part of kind of the deployment. And then we'll also be
monitoring the network layer with the VPC flow logs and DNS query logs from your Route 53, essentially giving you visibility into the network based threats and some of the IAM level compromises that GuardDuty can detect
in terms of the anomalies. Then with S3 protection,
very much recommended for when you have workloads where you're storing regulated data or customer data in S3 buckets. And what this entails is monitoring the data plane
API events from CloudTrails, specifically targeted to your S3 buckets, giving you the capability to detect volumetric
exfiltration type scenarios involving S3 and a key source that's part of the attack
sequences that we launched at re:Invent last year
with S3 data compromise. Now moving towards kind
of the workload monitoring with EKS audit logs,
we simplify the ability with which GuardDuty can give
you the compromised scenarios wherein someone is accessing your cluster. So kind of monitoring the control plane of your Kubernetes cluster deployments, you can essentially decide
to enable it on accounts and all the clusters that are existing, or in future when they are
running, GuardDuty automatically, again without any source
service site configuration, you don't need to vend
the logs, you don't need to collect the logs,
we'll ensure that as soon as you enable these
features with a single click and multi account management
using organizations, we'll start collecting the data and then providing you visibility into the threats that we detect. And there's no agents
required for this one. With runtime monitoring on
the other hand, we provided or we built a lightweight
eBPF based agent, so that we can give you visibility into really what's manifesting when let's say, compromise occurs in these container environments. And you can only get,
you can only go so far without getting visibility into the host. So all the way kind of
piecing these signals from when we see in CloudTrail
the control plane interaction to something that we see
with Kubernetes deployments, the control plane activity
when someone creates a cluster, establishes containers,
exploits the misconfiguration of different permissions. Now what really is happening
in those container deployments, that's what runtime monitoring
enables you to do that. There's automated agent management. So, because we use agents
a big pain point generally, GuardDuty provided no
extra cost, the ability to manage those agents and helps you build a unified
threat runtime monitoring or runtime security program
wherein you can use similar, or it's basically the
same eBPF based agent that can be then used
depending on whatever compute or multiple hybrid compute services that you use from GuardDuty
such as EKS on EC2, ECS workloads on EC2, ECS
workloads running on Fargate, and your traditional EC2 workloads. And prerequisites entail,
you know, permissioning, you know in case of EC2, if you want automated agent management, then we recommend checking
SSM-based permissions, 'cause we use that for automation, and you know, generally making sure that you have the agents available for the instances you want. One of the other benefits
generally kind of we hear from the field, and
something that's important to be realized, is, in addition to getting visibility into
the runtime compromise and some of the targeted
protection that we do, just looking at the runtime data, customers also see benefits in
reducing their spend levels. 'Cause depending on the
network architecture, VPC flow logs kind of becomes
a big spend contributor to the GuardDuty bill. So with this runtime agent, whatever instances you
have the agents deploy, GuardDuty will not charge you
for processing the flow logs. We'll still process them,
we'll still generate findings. So kind of, you know, you have, you do not have a single point of failure in cases where the agent stops working, because it's at the maximum capacity. We do not want you to be
regressed with your abilities to detect network-based threats. So we'll still process them
but you would not pay for them, and that's a significantly high benefit, and obviously not
discounting the advancement in capabilities that you
get with different kinds of threats that we detect. Now moving to RDS protection,
this is specifically where again, without
using any agent holistic, a multi account management for
all your existing databases and any new database that you spin up, we'll give you login
anomaly based detection. So giving you visibility in case of misconfigured security groups where your database is running. If you allow public access,
we kind of give visibility into what are kind of the intentions that we see from exit or exit nodes or successful brute force attempts. And then we eventually want
to kind of give or expand this to give other threat scenarios
detection capabilities for data exfiltration and data egress. To date supported for
Aurora and RDS Postgres. And eventually, this will
also be something that we want to provide for other
different RDS engines. With Lambda protection, we help you, again without any configuration or layers that you need to
add to your lambda functions, we give you visibility
into the network based data that we collect from those
function executions, both VPC and non VPC Lambda functions,
so that you can get coverage for threat vectors such as
unintended use of, you know, lambda functions for crypto
mining as an example, or your crypto, or your
supply chain attacks wherein your Lambda function
is now becoming a proxy for C2 communication as the channel. But all of these sources
that we talked about had streaming data or logs that we essentially got
from these services. With malware protection that we launched about two years ago at re:Inforce 2022, well that's three years, we
basically for the first time provided an agent place capability
to scan your EBS volumes that's attached to your EC2 instances and container workloads. So in addition to getting signals from different threat detection
techniques that we have encompassing for all
these different sources, malware protection for
kind of the EBS or the EC2 helps you verify some of the
network anomalies that we see. The way we built it was
to automate the workflows that generally the
analysts would use in case where you see a finding
which indicates communication to outbound, I don't
know, C2 domains, right? You might want to verify
on what really is happening in that workload for this
communication to happen. Is there a malware? And generally before
this feature being GA, what customers did, was to
take a snapshot, and then run with whatever malware scanner
they have at their disposal. And it was a tedious process. We essentially automated the entire thing and additionally added the ability to also initiate on-demand scan so that you can increase the fidelity and improve your investigation workflows or for forensics. Just last year, we
expanded this capability, that is the malware protection or malware scanning capability, to also provide a fully managed offering to protect your untrusted
upload applications that have S3 as the backend. Imagine data that's being sent
from your external vendors to your buckets, or internal users who are uploading data to S3 bucket that will be externally available. In both these cases, if you do not trust the data prominence or you do not trust the entities, there can be a serious risk where organizations can either be accepting malware if
they're not able to verify or be malware distributors if some compromise happens
from internal users and you know, the next
thing you know the image that's uploaded, it's actually a malware, and externally users are
downloading them, right? So this feature kind of
automates this entire process, helps you build secure pipelines
in a fully managed manner. And you can do this enablement
at a bucket by bucket level, 'cause again, not every
S3 bucket qualifies for being an untrusted
upload application bucket. And you can even use
this feature by the way as a standalone feature. Everything else we talked
till now does require you to enable the foundational GuardDuty, so that we can correlate
more such signals. But these are very targeted kind of application developer persona use case, and you know, you can
essentially just use GuardDuty to secure your data pipelines using this malware
protection feature for S3. So now, with the first,
like the few slides that we looked before,
the first one was kind of recommendations and
prescriptive guidance on what does good look like when it comes to enablement strategy. Then we looked and we dove deep into different protection plans that's available in GuardDuty, what each of it entails, and
why is it that you should use with the coverage that you can get. This slide attempts to
provide a mental model or essentially helping you
make a decision process from the workload profile. So depending on whatever kind of the workload profile you
have in your environment, let's say if you're using EC2 and S3, the recommendation is to use Foundational, and then combine that with
malware protection for S3 and the S3 data plane event monitoring. If you're container heavy, there's again control plane monitoring, and kind of within the containers,
with runtime monitoring. So you can basically get
coverage for some of the findings that we generate using
the attack sequences in Extended Threat Detection. And again, remember one
thing, more features that you enable, more
security signals we'll get, and more better the model would be into kind of correlating it. So in case of a real compromise,
we'll have more artifacts to kind of contextualize
the information, ultimately helping you to do targeted remediation, exactly knowing what all are my indicators of compromise and where
all do I see something bad that's happening instead of kind of having to decommission the
entire workload itself. If you have serverless first
strategy, then we'll cover you through, you know,
Foundational, Lambda Protection, and then even for ECS
workloads that run on Fargate, GuardDuty makes it seamless
for you to kind of ensure that every task that's running or that will be running
in your in your workload, we can inject a sidecar to kind of do the runtime monitoring, right? I mean without heavy lifting of having to update the task definition, you just use the task execution role with the right permissions, and any task that's part of that group, you know, will inject the sidecar. And then for kind of data
platforms specifically focused around protecting customer data or involves kind of configurations that you store in databases,
you can use RDS protection, S3 protection malware. And then in general, if
you're kind of in regulated or zero trust, the recommendation
we provides, you know, just enable all, right? That way, at least you
have that peace of mind in everything that GuardDuty has to offer to protect you and secure you. You have that control set enabled. So this was a lot of, you
know, prescriptive guidance and what is it that we see as
patterns in the field talking to all of these different customers. The rest of this session can
either be very interesting or not so interesting, you know, depending on your
inclination on in knowing kind of what the secret sauce
is, how can GuardDuty effectively at the scale that
we just kind of, you know, Shachar mentioned around kind
of 6 trillion logs every hour, imagine the scale at which
kind of you're operating and how it effectively, and
in a sophisticated manner, is able to kind of do some
of these threat detection. While we have a lot of
heuristics and rule base and threat intel based
pattern matching detections, but the ML and AI basically
helps us differentiate between unexpected and abnormal behavior from a not yet seen behavior
but an expected one, 'cause with the scale and
the data volume, with some of these protection plans
that you can imagine, such as flow logs, your
S3 data plane events, your CloudTrail logs, it can easily, if you were to generate atomic findings, we basically will be contributing to the alert fatigue problem, right? And we'll talk about kind
of one class of such model or one ML model that
GuardDuty uses to kind of help gain security
relevant signals out of all of this data set. And we do this primarily
using representation learning. So the goal of representation
learning is essentially to map each entity such as an IP address, the IAM user, the principal ID, all the different data events or the attributes that
we see in these events that represent an entity,
representation learning helps map each entity by encapsulating its
behavioral characteristic into the embedding vector. But think about these
vectors or points as, or points in some unit
dimensional space wherein, as in when we see the
events we ingest the data, establish a normal baseline
for these profiles. And each of these vectors will have kind of the behavioral characteristics. Generally what APIs a user uses, what buckets does it communicate to, what ASN does the user log in from? What are the general instant types we see an account be associated to? These are some of these representations that we encapsulate in vectors, and a primary contributor of
these vectors is essentially give us the ability to differentiate
the unexpected behavior from never seen occurrence, but kind of you know, business as usual. And so let's kind of see how,
in action, this helps, right? Let's take the example, we
see a user Nikki associated with you know, StartInstance API that you see in CloudTrail events, and the ASN VC, the user kind of performing this API is some
Argentine telecom company A. Now from the same user
for the same instance, for the same resource, for the first time we see StopInstance, and it's from a different ASP. Now technically this can be considered as a never seen event for Nikki. And then if you were to generate
kind of atomic indicators or atomic findings, we basically can kind of show this to be an abnormal
or an anomalous behavior in the scope where the
system's kind of running. We never see Nikki to be
using StopInstance API and never see Nikki kind
of performing activities from Argentinian Telecom B. But representation learning
ensures that these vectors, because StartInstance and
StopInstance typically are kind of related APIs, even if
it's on the same resource, generally the system learns
that this is a normal behavior, and in some special region,
you'll also see kind of these ASPs by the virtue of
the geographical context kind of related to each other. And hence with all of this
information, we get a signal that this event's not kind of anomalous. It might be for the
first time we see this, but it certainly is not abnormal, because of some of these vectors that are close points in the space. Now another class of ML
models is actually something that powers the Extended
Threat Detection feature that we talked about. Here we talk how representation learning helps us extract kind of
relevant security signals from this trove of data. But then these security signals
with the singular findings that we generate kind of becomes
a lot of related findings that customers individually
have to investigate. And that's kind of one of
the primary pain points, Extended Threat Detection was created to kind of solve for,
where we combine some of these related security signals to provide a more contextualized and a prescriptive kind
of investigation process, wrapping with all the indicators
of compromise that we see across these 10 different
findings as an example. And we'll kind of try to dive deep into how it does under the hood. So when we think about some of these different security signal groups, like these are nothing but
findings that are generated, and you would kind of be looking before action threat detection, the individual findings were
nothing but security signals. And then we'll group some
of these security signals into security signal groups
that basically can be thought of events you see commonly from a user or from a principal ID or IPs. We'll group all of these
security signals we see on the same entity, and
then we'll do the clustering of kind of these related signals together. But then which cluster is
actually a higher priority finding that something GuardDuty
should generate an output for as an attack sequence. We do this using a ranking
model, ranking ML model, which has encoded the security
engineer's intuition in it. Generally without kind of the ML model, how we see security responders look at any event and triage, they'll basically ask these questions. Like, does it involve high risk API? Is there an unusual instance
type that's involved? Does it have low reputation IP address? Do we see any proxy anonymizer or VPN solutions that are
kind of used as part of this? Is the user agenda among suspicion? And these are some of these questions that typically a security engineer or a security responder would ask in order to kind of effectively triage, whether this is a true
positive or false positive. What we have done is
essentially we encoded all of this security domain expertise, or the security intuition,
into what we call as marker library, which
is basically a series of these encoded functions that every time there's
a security signal group or a cluster that we need to evaluate, the ranking model kind of essentially leverages the questions encoded
as markers in the library. And some of these marker
libraries essentially will have binary decision of yes, no. So in order to kind of get
more prescriptive guidance from the model into which
actually is a sequence that's a higher priority or higher rank, but all these clusters
will be stack ranked. They'll be evaluated
against this marker library with encoded security intuition
package and functions, and then the model will
evaluate on how many of them kind of see yes or no
with some of these markers. And then on top of that, each
of will run another ML model to generate a ranking score. So what really happens in
the ML model for the like, it basically learns how
to aggregate the marker, aggregate the markers disposition from kind of the data that it has. It actually discounts the
contribution of markers that commonly kind of
disagree with each other. So indicating that they
are not of higher efficacy in actually generating
a valid ranking score so that that can be prioritized, 'cause the reason we do this, you know, sophisticated ranking and
clustering is essentially we wanna prioritize those
events of interests, what we call as attack sequences. We actually, this model will automatically reward the markers that tend
to agree with each other. Like, if it's a low risk API
generally seen from an ASN, that's part of let's say a embargo list or something that's not
observed for the organization. Now combine, if all of
these secure signals that we are evaluating
continuous with these markers, agree to the general kind of holistic, then you know the model automatically increases the weightage for these markers. And we'll kind of listen more in order to generate a ranking score. Discounts the contribution
of marker that's always on. One mechanism with which it
locally understands the context of you know, what's really, again maybe abnormal in the general context. But if you localize kind
of the context, it's fine. Business as usual, 'cause it
looks like that's how kind of the workload's operating
in their environment, in a customer's environment. And then we also kind of get incident data with all these different
threat intelligence and the integration we have with internal threat,
intel feed, and IOCs. So we'll reward the
contribution that tends to agree kind of with known incidents. But this is in a nutshell,
things that we have that helps make the detection
capabilities sophisticated for Extended Threat Detection
and attack sequences that we'll generate. All right, I think this is,
we already saw the demo. These are some resources for you to kind of get more detailed
insights into GuardDuty and different offerings. And thank you for your time. (audience claps)
