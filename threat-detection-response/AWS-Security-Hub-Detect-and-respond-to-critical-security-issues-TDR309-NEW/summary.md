# AWS re:Inforce 2025 - AWS Security Hub: Detect and respond to critical security issues (TDR309-NEW)

**Video Link:** [Watch on YouTube](https://www.youtube.com/watch?v=LLOamLlppkI)

## Video Information
- **Author:** AWS Events
- **Duration:** 42.6 minutes
- **Word Count:** 7,279 words
- **Publish Date:** 20250620
- **Video ID:** LLOamLlppkI

## Summary
This session introduces the **new AWS Security Hub**, redesigned as a unified security service offering advanced threat detection, automated correlation, risk-based prioritization, and integrated response capabilities. It aims to solve key customer pain points like fragmented security signals, limited context, and complex response workflows.

The speakers demonstrate the new hub’s ability to consolidate findings from services like GuardDuty, Inspector, Macie, and the legacy Security Hub (now Security Hub CSPM). Key innovations include “Exposure Findings,” attack path visualization, a security-focused asset inventory, and native ticketing integration with Jira and ServiceNow. The session concludes with a live demo of the console and automation capabilities for large-scale operations.

## Key Points
- **Security Hub is now split into two services:**
  - **Security Hub CSPM** (legacy) continues to focus on compliance checks and finding aggregation.
  - **New Security Hub** (in preview) offers unified detection, correlation, and response.
- **Customer pain points addressed:**
  - Fragmented tools and consoles
  - Manual correlation of findings
  - Lack of business/security context
  - Cumbersome response integration
- **New capabilities:**
  - **Exposure Findings** that correlate vulnerabilities, misconfigurations, sensitive data, network exposure, and IAM relationships
  - **Attack Path Visualization** showing how an attacker could exploit a resource
  - **Security-focused Asset Inventory** across accounts and regions
  - **Native ticketing integrations** with Jira and ServiceNow (no EventBridge setup required)
  - **Region Aggregation** for centralized multi-region view
  - **Automation Rules** to auto-generate tickets or take actions on matched criteria
- **Backed by OCSF schema** for enhanced interoperability with partners and third-party tools
- **Built-in scoring model** for exposure severity, using signals like EPSS, reachability, and AWS internal threat intel (e.g., MadPot)

## Technical Details
- **Exposure Findings** are calculated by aggregating signals from:
  - Amazon Inspector (vulnerabilities)
  - Amazon Macie (sensitive data)
  - GuardDuty (threat detection)
  - Security Hub CSPM (misconfigurations)
  - IAM/resource relationships
  - Automated reasoning for network reachability
- **Severity calculation** includes:
  - Ease of discovery
  - Exploitability (e.g., EPSS score)
  - Threat actor awareness
  - Potential impact
- **Attack Path feature** shows resource interconnectivity, reachable paths, and compromised relationships
- **Security Inventory** supports organization-wide view via AWS Organizations
- **OCSF schema support** improves standardization and partner integrations
- **Automation Rules and Native Integrations** reduce overhead in incident response workflows
- **Region Aggregation** allows centralizing findings from all AWS regions into a single “home” region
- **Preview availability**: Free of charge during preview phase

## Full Transcript

- Good morning all and welcome. I'm Kashish and I have my
colleague, Scott, here with me. And we are from the
Service Teams Security Hub, which is part of the Security
Services Org within AWS. Today we are here to talk
about the new Security Hub that we just introduced yesterday. We'll take a few minutes
to talk about what the, what were the main key customer problems that we heard in over the last few years, which led to building
this new Security Hub. Then we are gonna talk about what are the key capabilities
of the new Security Hub. We are gonna do a demo
and then we will end up with the quick Q and A. We'll do a Q and A on the stage, and then we can also hang out afterwards if you have more questions. So, you know, we are happy
to talk to you after, after the session also. So to start with, let's see what, what the key challenges
that customers were facing that we have heard over the years. And I'm sure most of you, if not all of you, relate to that also. The first one that we
continuously heard was that security is fragmented. Within AWS, we still
have multiple services, different consoles, different
APIs like Amazon GuardDuty, Amazon Inspector, the
existing AWS Security Hub, and we'll talk about what happens to the existing Security
Hub and so and so on. And customers consistently told us, "We want a single place to get security. We don't want to figure out what we need to make our
AWS environment secure." And overall, they just kept telling us, "We don't want that manual
effort that we want to do to manually correlate these findings or results that come out of
individual security services." So disconnected security signals that required manual analysis was the second main thing
that customers told us. The third was limited context. So typically our security services were focused on a resource or were focused on a specific thing. It lagged some of the business context and general context
around the overall risk that presented to an organization. Last year at re:Invent
within Amazon GuardDuty, we did launch extended threat detection that linked together multiple threats that happened within the same timeframe to give you a high confidence,
high confidence results. The third is, or like the fourth one that we heard consistently was that we want to simplify our response. Response could be remediation, response could be just
opening up a ticket. And a lot of the times, one of
the things we did was that we provided building blocks. There was always something to do, but you had to manually system together. For example, if you had
to create a connection, or a ticketing connect, sorry, connection with a ticketing
system like ServiceNow or Jira, you had to manually create
an EventBridge rule. You had to manually create an SCSQ, and then eventually do a lot of the steps to end up setting that,
setting that connection up. So while it's not hard, it's, it is something that customers
can consistently told us. We want a simple way that we
can do, from within the tool. Like we want native integrations. So we talked about, you
know, multiple tools. We talked about manual analysis, context, and delayed response. So what we are doing
now is we are addressing each one of those with a unified solution. We are doing automated
correlation and analysis. We are giving enriched insights into each and every risk that we generate. We also are streamlining our response. This is a preview, so we are starting with some response capabilities like integration with ticketing systems. And we'll cover through,
we'll go over that during our detailed
session in a few minutes, and we will also show that in a demo. So that's very clear how we are doing it within a few clicks. So with that, we are
introducing our preview of our new Security Hub,
which does a bunch of things. And this will be our
unified security solution that will ingest findings from GuardDuty, Inspector Security Hub,
existing Security Hub. It will look at the configurations, even if there are signals
that are not good enough for a misconfiguration finding, there are still configuration
when in relation with multiple other aspects could prove to be harmful. Then there is network exposure,
network exposure to the, to the internet, or it could
be a general reachability from a code execution standpoint. Then sensitive data, then
also resource relationship. How a resource like
EC2 instance can assume an IM role could be very critical. So just understanding the
resource relationships is equally important, equally important to
our security findings. So our vision going forward
with the new Security Hub is that everything that you
need within AWS around security will be available within AWS Security Hub. So what happens with our
existing Security Hub? Our, basically, the vision and
the path we are going forward is that the existing
Security Hub will be renamed to Security Hub CSPM to focus on Cloud Security
Posture Management. Existing Security Hub
did two things mainly. First it provided security
controls or checks against AWS security best practices, and the second was the
aggregation of findings. That will continue to exist. And that product will focus
on building the best checks, the fastest checks to the market for all AWS security
services that we have. And it will continue
to focus on that area, while the new Security Hub
will be truly a Security Hub this time and will give a
unified solution for security that not only means detections, it means automated correlations, it also means risk prioritization, and finally automated response. And the response could
cover across several areas, like ticketing or automated ticketing. So what are the key capabilities
of the new Security Hub? We have introduced a new entity, what we call Exposure findings, and we'll go over details
of Exposure findings with an example in a minute. But Exposure findings is
essentially the toxic combination of things that we identified
in your environment, which could be from resource relationships to findings such as software
vulnerabilities like CVEs. It could be network
exposure, it could be code, it could be in a code execution path, it could be sensitive data, it could be just a configuration. When we generate an exposure finding, we will accompany that with a, with a visual of an potential attack path, which represents that,
how a potential attacker could essentially get
into your environment and exploit that resource. Now, this doesn't have to be
always through the internet. This can be just, you know, ways a attacker could exploit
just getting into your system through back doors and so forth and so on. So there are multiple
ways it could happen. So with this visual,
we are able to present how a potential attacker
could actually exploit your resource and the path it would take. The third is the Asset inventory. Now our approach to asset inventory is very security focused. So we are looking at security
focused resource inventory where you will be able
to see all the resources that exist in your AWS environment
that are being monitored by AWS Security Hub or one
of our detection engines. So when I say detection engines, these are services or
our security capabilities or components like GuardDuty, inspector and so forth and so on. Then finally, we do a lot
of the triage and analysis upfront for you so that
you can automatically do, or take response actions. And this could happen
through automation rules and several automated
actions that you can take. So how this fits into
overall security portfolio? Like I mentioned, Amazon
GuardDuty, Amazon inspector, AWS security of CSPM and Amazon Macie will be the main detection
engines to start with. That will provide signals
to AWS Security Hub. We will also get signals
from, like I mentioned, resource relationships
or configuration itself, but those don't present
as findings in itself. Now our idea is that if you still want to just use building blocks and you know, build a solution on top of it, you will be able to just use
each and individual services that are offered today. So you can still go and
buy AWS Security Hub CSPM, or Inspector, or GuardDuty, and build a solution over it if that's what works best for you. But if you want a unified
solution, a whole unified solution where you can do detection and response, that will be our AWS Security
Hub, the new AWS Security Hub. It is in preview and it will, the new Security Hub itself
will be free of charge during the preview period. Now, I'll have Scott come
and talk about the details of this new product and do a demo. - Thanks Kashish. Morning everybody,
thank you for your time, and thanks for coming out here today. Let's take a little bit
of tour and talk more about the capabilities that
are inside of Security Hub. I'm gonna quickly talk about these. I've got a demo where I'm gonna
dive more deeply into these, but to kind of set the stage for it. The first thing that we focused on with this new Security
Hub is a unified console. We want this to be the singular
place where you can come in and get insight about
your security findings. And so we focused on giving you
this, this summary dashboard to start off with, which
gets you a quick overview of what are the key items
around threats, exposures, your summary of your top
resources with findings, and as well as your security
coverage of all the services that ultimately power Security Hub. We focused on this experience
of giving you more usability, an overall improved user experience, and improved filtering capabilities. We also have the concept
of exposure findings. Kashish touched on that briefly. And so what we're doing
is, we're doing correlation of all of these security findings that are coming into Security Hub, and creating a net new
exposure finding to help you with prioritization around where
you should spend your time, or where you might have the most risk in your environment across your resources. More specifically, let's
just talk about what we view and exposure and how we accomplish generating you an exposure. So there's lots of different ways you could look at an exposure. I like to look at it as
some sort of a weakness that you have in your environment. It's due to some sort
of a misconfiguration, some sort of a security gap or, or some sort of a
vulnerability that exists in your resources or in your environment. The way that we're accomplishing this is we're taking signals from
a lot of different places. So we're taking the network reachability and the vulnerability findings that are coming from Inspector. We're taking the cloud
posture management findings coming out of the Security Hub CSPM, sensitive data findings
coming out of Amazon Macie. And we're taking information that we get around resource configuration
and their relationships. And so we're taking all that
and putting that into an engine and the output of that
is an exposure finding. So this is a net new finding that will exist in Security Hub. And we also focus on giving you, you know, I think you saw in the screenshot we have different severities
for different exposures, from critical, to high, to medium, to low. And so we use some different
pieces of information to help set that severity. So we focused on the ease of discovery. So how easily could an automated tool actually discover this
particular exposure. Ease of exploit, so how simple would it be for a threat actor to
actually be able to exploit this particular vulnerability. The likelihood of the exploit. So focusing on what's the probability based on public information
such as the EPSS score, the exploitability score, as well as internal threat
intelligence that we have. The awareness, so publicly, how aware is the rest of the world and the rest of the community around this particular vulnerability? And then the impact. What would be the potential
harm to your resources, to your environment, to your data if this were to be successfully exploited? Let's talk about an example of an exploit just to help talk a little bit
more about what this means. So there's a, there's
different parts of an exposure. So first we have a vulnerability. So in this case we have an EC2 instance. It has 125 different
vulnerabilities on it, but in the end when you really look at it, there's two vulnerabilities
on that instance that have a high severity and they have a high
likelihood of being exploited. Reachability, so actually identifying that this particular resource is reachable from the internet. Sensitive data, so we're
getting signals from Macie that a particular S3
bucket has sensitive data, and we're also able to determine through the configuration part to determine that particular
resource has permissions to allow it to actually
talk to that bucket where the sensitive data exists. And then things like
misconfiguration, for example, identifying that your EC2
instance is still using IMDSv1, which has some gaps
that might allow somebody to get access to information
about the metadata for your resource, for your instance, or actually get the
credentials for that instance that might allow them to
actually interact with things like that S3 bucket that's
public and has sensitive data. So this is an example of like
the different types of signals and things that we're
pulling out of the findings to arrive at an exposure. What, we'll talk through
some exposures in the demo here in just a minute as well. So what are some of the
benefits of what we're doing from our exposure correlation? So the first one is really we're giving you prioritized findings. We're giving you the
most important resources in your environment that
you should be focusing on, not where we're limiting the
need for you to comb through and go through all these
individual findings, and try to make that decision on your own. Free up some resources to
actually maybe focus on responding to these exposures rather
than trying to find them. That results in low operational overhead. We're the ones who are taking care of running these exposures, coming up with new ways to
identify these exposures, you just get to focus
on remediating them and, and running your environment and, and actually maybe addressing
the root cause of these. We have an intelligent approach to this and what we're really
focusing on best practices. And so we're using our insight
of what's the best way to run and configure a used resources on AWS and applying that to how we're
generating these exposures. When it comes to the vulnerabilities, we're using both external
threat intel, so the, I mentioned the EPSS score,
what's the probability of this vulnerability being exploited, information from our partners
such as recorded future around what's happening with
particular vulnerabilities and, and how are they being exploited? But we're also using our
own internal threat intel. So if you watch the keynote yesterday, you heard Amy mention
MadPot, which is one of our, our internal security
services that we actually use to collect virtual
honeypot information around what are malicious actors
doing against AWS environments. And we actually use some
of that information around how threat actors are exploiting and using certain vulnerabilities to inform our, like our insight, almost the likeliness that this particular
vulnerability would be exploited. And then we're using our
automated reasoning capabilities to actually help identify
network reachability. So automated reasoning as
a discipline that we have within several of our
services here at AWS, that helps us to get to
a binary yes or no answer of, can this particular
resource access the internet looking at all the potential
control plane configurations that could exist for that resource? Other key capabilities. You heard the attack
path mentioned earlier, and so within an exposure we're
giving you a visualization of what is the possible
way that an adversary could actually get access
to the particular resource that this exposure is ultimately for, but also helping you understand what are maybe some of the
other related resources? What are some of the other things that might be at risk if the core resource were to be exposed, for example, storage, or other IAM permissions that are attached to that particular resource,
that somebody might use to even gain further
access to your environment or cause further destruction. We also focus on giving
you a security focused resource inventory, so
giving you that inventory of what are all the resources
that you have deployed that are covered by the security services that power Security Hub. The really cool thing here is that, if you're integrating
with AWS organizations, this is an organization-wide view. So you can now, whether you're looking for security findings or not, come in and get a sense of how much of any particular resource
type do I have deployed? Which ones of them have
security findings against them? What kinds of security
findings do they have? And what's the configuration
of all those resources? And you can get all that
without having to pivot out to another console or to another account to actually go and get that information. Being able to respond to all the findings that you have in Security
Hub is really important. And we wanted to make sure
that we were positioning this, this service so that it
could work with how customers integrate these findings into
their operational workflows. And so we focused on native integration with key ticketing tools. We started out with Jira
Cloud and ServiceNow. And so now customers can
actually configure a connection in Security Hub to their Jira or their ServiceNow environments, and then we will synchronously
create findings into tickets in those particular environments. And so it's a native integration. You don't have to write EventBridge rules to be able to integrate those
with your ticketing tools. Like I mentioned it's synchronous. And so you can go into an
individual finding and choose, create a ticket right there. Or from a scalability perspective, you can actually define automation rules, where you define criteria and say, "When a finding matches this criteria, I'd like you to create a ticket in one of the ticketing
integrations I have." Another key thing with Security Hub, so Security Hub is now a separate service that you enable independent of CSPM. The data store behind that is all based on the open cybersecurity
framework schema. So the old Security Hub CSPM was based on the AWS security findings format. We're now basing this on
OCSF, and so this allows us to have more rich information in all of your security findings. A lot more detail, a lot more information. It also allows you as a customer to, if you're already using OCSF
in some of your other processes or other tools, to
integrate those findings with what you're already doing for OCSF, or if you're gonna use a third party who's already standardized
or a supporting OCSF, to adopt that third party. And on that list we have
a collection of partners who have already committed
to building integrations to consume findings out
of Security Hub and, and make those findings
available and useful to you in their products, as
well as a few partners who have already committed to
offering enablement services for customers who are looking
to adopt Security Hub. So when it comes to operationalization, a couple different ways
that you can look at how you would operationalize the data that's coming into Security Hub. The the first one is the console, which we'll we'll spend
a few minutes on here to just kind of walk through
what you get in the console, but just using the console to be able to look at your findings, all the information that
we've given you there. You can also actually get
a copy of the raw JSON, the OCSF information about
each individual finding if you want it, but you can
use the console to investigate and use that as your first point to be able to make some decisions. We'll also have APIs for
all of the key capabilities of Security Hub, so you can use the APIs. Not only to extract or
to look at information, but also to do things like
maybe update the status of a particular finding,
setting it to closed, or changing the severity,
or adding a comment to that particular finding
so that you can incorporate some of those updates into your workflows. And then Amazon EventBridge integration. So a copy of every single finding that Security Hub generates or updates will be sent to Amazon EventBridge. And so you can write EventBridge rules that will match certain
criteria in those findings, and then you can route those
on to a particular target, which could be an SNS topic, an SQSQ Lambda function to incorporate or do some sort of work on
that particular finding, or you could even incorporate
that with a third party, any of the third party
partners who have onboarded as an EventBridge partner, you
can actually set their system as a target and provide your credentials to be able to send that
finding to their environments. One of the other things
that we've focused on is a simplified onboarding process when it comes to Security Hub. So Security Hub is integrated
with AWS Organizations and so you can get visibility across your entire organization. So to onboard here, it's, you go into your Organizational
Management Account, you turn on Security Hub, you set your delegated
administrator account, and then you get out of that
organizational management account. You don't need to be back in there again. You then go into your
delegated admin account, you enable Security Hub, it's two clicks to enable Security Hub
at your delegated admin. Now at that point you have
your delegated admin account where you're gonna be able
to see all the information for your member accounts that
you've enabled Security Hubs. So what happens if you've
got lots of member accounts? You don't want to go
into each one of those and actually enable Security Hub. You don't want to do some
scripting to call a bunch of APIs to enable Security Hub on
all your member accounts. And you certainly don't
want to have to keep, continue to do that as
you add more accounts to your organizations. So we have a capability where, in the delegated administrator account, you'll go in and you'll define a policy. In that policy you'll go in and say, "Which AWS accounts of all of my members, which accounts do I want enable?" The default is all accounts, but you can choose specific accounts or specific organizational
units in your organization, then you're gonna choose
which AWS regions. So you can choose all regions, or you can choose specific
regions that you operate in. And then once you submit that policy, behind the scenes, we
go and apply that policy to all your member accounts and enable all of the member accounts
with Security Hub. As you add more member accounts, any more member accounts
that match that policy will automatically have
Security Hub enabled as well. Now, many of our customers, probably many people in this room as well operate across multiple AWS regions. So the next challenge is
how do I actually go in and get visibility
across all those regions? So we have a capability
called Region Aggregation. And so you can actually
go into Security Hub, you can define a home
region, whichever region you want to be able to
see all your findings in, and then define which
of your other regions should be linked to that home region. And we will then sync a copy of all those findings
into that home region. And so what you end up with
is you have the ability to go into one single account,
your delegated admin account, and be able to view all
of your organization's security findings across
all accounts and all regions from one delegated home region. So pretty cool from a
visibility perspective. Okay, let's go ahead and
jump into the product. And take you through a
tour of what we have. Okay, so to start off with,
Kashish mentioned earlier, the Security Hub you've
known for the last five years has now been rebranded
as Security Hub CSPM. So if you go into Security Hub CSPM, you'll see a new banner around introducing the new Security Hub, which is in preview. So you can click on that Try Security Hub. That will bring up the brand new console. So if you haven't enabled it yet, you'll go through those enabled steps that I talked about earlier,
but we've got it enabled here. So what do we have here now
that we've come into this? So we have the summary
screen that we talked about. Some more detail about this. We have a Threat Summary,
an Exposure Summary, your Resource Summary, and
your Security Coverage. Threats are focused on GuardDuty. So as soon as you have
Security Hub enabled, if you have GuardDuty enabled, all your GuardDuty findings
will flow into Security Hub. We're organizing those
for you, so that you have clear visibility around
what are all the threats that are happening in my organization? Right there, right on the left. Clearly, clearly easy for
you to be able to see them. Exposures, we talked
about what exposures are. This is a summary of all of the exposures that are currently active, or that we can see in your environment. For each of these, we'll
give you a summary listing of each of the findings of
like the top 10 findings that are tied to this
particular dashboard. And we'll talk about
how you can go see those in more detail in just a moment. This resource summary, this
is actually a top 10 list of all the resources
organized by findings. And so we're prioritizing
the exposure findings, and the extended threat
detection findings of GuardDuty. So if you use GuardDuty or if
you haven't used GuardDuty, extended threat detection
findings are the ones where they're actually correlating multiple GuardDuty findings
into a new finding that's, that's a broader attack sequence that they're seeing in your environment. So we're prioritizing
those prioritized findings because we have a lot more signals that these may be the
ones you want to focus on, and helping using that to organize what are the top resources
with security findings. And then finally the security coverage. So Security Hub is powered
by other AWS services. Inspector, Macie, Security
Hub CSPM, and GuardDuty. So we're giving you visibility around where you might have a coverage gap with those security services, which would imply that you're not getting the full visibility around findings, or exposures, or threats
in your environment. One of the other cool
things that we've done here throughout the product, and I'll show it here in the dashboard, is that we've added a lot
more filtering capabilities. And so I'm gonna just go ahead
and add a quick filter here around resource type. In this case I'm gonna
focus on EC2 instances. Okay, and immediately you'll see that the, the counts on this dashboard change. One of the really cool
things with these filters is, if I've set a filter that I like, I can actually go in and save that filter. And if I want it to, I can set this as my default filter view. And what that means is every
time I come into Security Hub and as I navigate through Security Hub, that will stay as my filter. So if that's something
I really wanna focus on, I can set that and keep it. And I can define as
many filters as I want. So if I have different teams that are coming into Security Hub, and they wanna look at
things different ways based on different attributes, they can choose a filter
that's applicable to them. So we have these filters that
you can live with through, you can use throughout the environment. So building on that, let's
take a look at the threats in a little bit more detail. And so when you click on
any one of those numbers in the summary, it will immediately
bring you to a dashboard that's filtered based
on that severity level that you just chose, so you
can see I'm being brought in to a list of threats
that are just critical, 'cause I clicked on the critical number. One of the things we've done, I talked about the user
experience earlier, is that we have focused on making sure that you can really get value out of all of the finding
information in the console. And so if you ever looked
at a GuardDuty finding in the security of CSPM console, many customers are finding
that they had to pivot back to the GuardDuty console
because all the information was maybe there in the JSON, but it wasn't really relevant
or visible in the console. And so if you look at the
Security Hub console now, a GuardDuty finding and Security Hub looks just like if you were looking
at the finding in GuardDuty. So you have all the full information and, and where you can really see this is the GuardDuty attack sequences, where there's lots of different signals, and lots of different information
that's being presented. So we can see, I've got an attack sequence that's focused on a
compromised cluster in EKS, which GuardDuty just released
a new capabilities yesterday around generating attack
sequences around EKS clusters. So we can see information
about the attack sequence, I can see the different MITRE tactics that GuardDuty is observing,
all the indicators, the endpoints, and the
resources that are tied to that. So really helping you get
information that you need and, and really doubling down on
that unified console experience. So you can just stay in Security Hub to be able to look at
all of your findings. Let's talk about exposures. So in this case, I'm actually gonna go to the exposure specific dashboard. So this is a dashboard that is built specifically for exposures. It's sorting and organizing
it just on exposure findings. And right away what we're giving you here is a summary of key information
about all your exposures. So once again, all the
different severities that we're seeing for your exposures. And what are the top 10 attributes, the different resources, account IDs, and things like that that we're seeing across all of these findings
as well as your top 10 accounts that are in your, that are tied to these
particular exposure findings. So I can click on critical here, and I can see the information
about a particular exposure, or actually wanna show you
something really cool here. We can actually group by the finding title, which
which will then help me understand what are all the
different types of exposures that I have out there. And I can actually then expand this and see the specific resources that are tied to that
particular exposure title. So we're gonna focus on this
critical one here, for example, for this particular EC2 instance. So when I bring this up, we can see an expanded
pane here on the right. I'm actually gonna move
to the expanded view, so that we can see all the information about this particular exposure. So we start off with, by
giving you a quick title to help you understand this. So in this case we have
a potential credential stealing exposure where
we have an EC2 instance that's reachable from the internet, when we talked about internet reachability being one of the key contributors here. And it has an instance profile tied to it, and it has a network exploitable
software vulnerability that's part of that instance. So it's giving it a high
likelihood that this, this resource could be exploited. We've got a more deeper
human readable description about this particular exposure, helping you understand
more of like why did we, why did we generate this
exposure in the first place? And what are some of the key things that exist in this exposure? Then giving you an overview of some key information
about this exposure. So the type of exposure, the
resource that's impacted, the account and the region, and how old is this particular exposure. And then we go into the traits. And so contributing traits
are the key attributes that we extracted out of the findings that we use to correlate this exposure. And these are the things
that ultimately led us to generating this exposure. And I look at these as your
roadmap for remediating or reducing this particular
exposure in your environment. So we have a case where
we have an EC2 instance with a profile, so there's
a potential of credentials or permissions that could be
used off of that resource. The instance is reachable
over the internet, and the instance has a high severity vulnerability tied to it. We then follow up with
remediation guidance. So we give you guidance
on, based on the traits that we saw for this particular exposure, this is links to documentation
about how we recommend you go about remediating
this particular exposure and identifying the things that we found for this particular resource. We also give you a potential attack path. So we talked about the
attack path briefly. I'm gonna go into it a
little bit more here. We use the information we have about that particular
resource to give you, in this case it's an EC2 instance, an overview of what are
the network components and how could a malicious
actor actually get to and interact with this resource? We also have the primary
resource indicated here, which is the resource
that the exposure finding ultimately is for, in this
case it's an EC2 instance. And this little counter over here, is a counter of the number of traits that exist for that particular resource. I can also click on
this particular resource and see more information about
those traits if I wanted to. If there was more than one
resource that had traits that resulted in the exposure, each one of those resources
would have a counter next to it. I can click on any one of these resources and get some key information
about that resource, or pivot to the overall resource details, which I'll show you in just a minute. So we have the attack path
that here help you understand how is this configured, what
are all the related resources tied to this particular item? We also show you another
view of the traits. One of the key things here is that we, we talk about contributing traits. Those are the traits that
actually generated the exposure, but we also give you contextual traits. These are all the other findings that exist there about
this particular resource. They didn't contribute to the exposure, but if you were gonna
go in and try to do more of a broad remediation, or a patch against this particular resource, these are all the other security
issues that are out there that you might want to address as well when you go in and focus on this resource. And then we give you detail
about the primary, you know, the primary resource and
any secondary resources that are associated with
this particular exposure. So in this case it's an EC2 instance. So we've given you a couple
of pieces of information. The type, the ID of the
resource in the region. We give you the tags, which is important so that you can actually understand maybe some configuration
or some ownership. But a lot of customers
need a lot more information to be able to truly understand what's the scope of this resource, how is it configured, is
it configured correctly? And so we talked about that security focused resource inventory. We're actually gonna
give you a full overview of all the configuration information for this particular resource so that you can make a determination of is this actually configured correctly? What are the configuration details? How I might use that as far
as formulating the remediation of this particular exposure. And so we've eliminated the need for you to have to pivot out to another console, or to another account in order to be able to go see that resource information. Okay, so let's talk about, let's go back to exposures. Let's just pick an exposure. So one of the things we
talked about was the ability to have native ticketing integration. So we talked about we have integrations with Jira Cloud and ServiceNow. So you can define a connection to your ticketing environment. When I'm looking at a particular finding, if I decide that, "Hey, this needs to get turned into a ticket." From right here, I can
choose create ticket, I can choose either of
the ticketing providers. So if I've chosen Jira in
this case, I can then choose which of the integrations
or the connections that I've created for Jira. Choose that one, and
right here choose Create. And what's happened is we're
synchronously sending this via the rest APIs to the Jira environment, and we will then add the ticket number or the issue number
directly to that finding. And so now you have a couple things. One, you can actually click on this and it will take you to
the Jira environment, if you wanna look at the ticket in there. But it also gives you
an indicator that, okay, this has already been
created into a ticket. Maybe I don't need to focus on this anyone 'cause it's already in
the hands of the team that is responsible for this. And so a really great way to
just insert these findings into your operational workflows. Now going through and
looking at all these findings one-on-one is probably not
gonna scale pretty easily. And so the other thing that you can do, is we have this feature
called Automation Rules. So I have one defined here, but I can walk you through how this works. So I've got an Automation Rule defined, where I've given it a
criteria where I want to focus on any finding that comes in with a status of critical. I want this to create a ticket. And in this case I've chosen
my ServiceNow integration. And so what's gonna happen
is that every new finding that's created in Security Hub that has a status of critical
will just automatically be sent off to my ServiceNow environment. So there's no need for me to go through and triage every one of these findings. I'm able to get findings
with certain criteria immediately off into the
right place so that the, the operational processes that
are tied to that, can begin. Okay, last thing I want to
talk about real quick is that, oh, let's get back here, is
that security focused inventory. So up to this point I've been talking about specific findings. I was looking at an exposure
for an EC2 instance. So I want to understand
more about like what's, what's up with all the
other EC2 instances, how many do I have out there? Is there a potential that some
of the other EC2 instances might have security findings
against them as well? So this resource focused inventory, this is all the resources
that are deployed across your organization that are covered by our security services. So in this case, I'm
gonna open up compute, I'm gonna focus on EC2 instances. I can see I have 27 EC2 instances that are deployed across my organization. And so I'm gonna go in and I can see, immediately I'll get a list
of all of the instances. I'll also get information
about which ones have findings, and what types of findings
exist about those instances. So right away, I've got
another signal around where might I might spend my time, do I wanna spend focus on
more EC2 instances or not? I'll also see if there's
no findings at all. And so, okay, this one's
out there, it's good. And then if I choose any
one of these instances, just like when we were looking
at the individual finding, I'll have the complete
overview of the configuration of that particular resource. And so I can use that to once
again make some determination of is this resource
configured correctly or, or who do I hand this off to? If depending on the
configuration of that resource, I can also see information
about the particular findings that are tied to that resource. And also if there's been
any exposures created, I can also see the traits of the exposures tied to that resource. So lots of different ways
to get some visibility around the resources, your environment, and help you make some decisions around where you're gonna spend your time or what you should prioritize. Okay, so gonna wrap up here. Some key capabilities that
you want to keep in mind when it comes to Security Hub CSPM versus the new Security Hub. And so first of all,
from a CSPM perspective, Security Hub CSPM focuses
on cloud posture management, configuration compliance and
security finding aggregation, AWS Security Hub focuses
on those three things as well as giving you
automated signal correlation, exposure findings, the
attack path analysis, security focused asset inventory, everything in the OCSF finding format, and a unified configuration console which will be available at GA, where you'll actually be able to configure all those supporting AWS services directly from the Security Hub console. Once we release the slides for
this after the presentation, there'll also be another slide with links to some key documentation
around this service, as well as a couple of customer quotes. I just wanna highlight,
we had some great partners that were part of our preview. So customers ITV and
Asilia gave us some quotes that just highlighted
that how Security Hub was already helping them
to get better insight into their environments
and help to streamline their security operations in
what they're doing on AWS. Lastly, there were a lot of people who made this new service possible. So I'd like to just thank
everybody from an engineering, marketing, a legal standpoint at AWS, who helped to produce this and
provide this service to you. I'd like to thank Kashish for his support and his guidance as well. And I'd like to thank everybody
for coming out here today. So thank you very much for your time. Kashish and I can hang out
here and take some questions for you right here from the
stage if you have any questions, we'll happily take them now. - All right. All right. - We'll be back out
here in a couple minutes if you any other questions, thank you. - Thank you. (audience applauding)
