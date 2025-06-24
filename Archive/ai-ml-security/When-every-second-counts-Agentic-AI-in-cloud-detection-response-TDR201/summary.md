# AWS re:Inforce 2025 - When every second counts: Agentic AI in cloud detection & response (TDR201)

**Video Link:** [Watch on YouTube](https://www.youtube.com/watch?v=GimWOPIJ4r8)

## Video Information
- **Author:** AWS Events
- **Duration:** 41.2 minutes
- **Word Count:** 6,712 words
- **Publish Date:** 20250620
- **Video ID:** GimWOPIJ4r8

## Summary

This session demonstrates how CrowdStrike's agentic AI capabilities enhance cloud detection and response in an environment where adversaries are moving faster than ever. The presenters reveal that the fastest adversary breakout time has dropped to just 51 seconds, and nearly 80% of attacks are now malware-free, making traditional endpoint security insufficient. The session showcases how adversaries are leveraging AI to improve their attack success rates, with AI-generated phishing emails achieving 4x higher success rates than human-generated ones. Cloud environments are particularly attractive targets due to their expanded attack surface, high-value data, and identity-driven access patterns. The demo illustrates a real-world attack scenario where compromised developer credentials lead to container compromise and lateral movement, demonstrating how CrowdStrike's Charlotte AI can automatically triage incidents, correlate multi-domain telemetry, and generate detailed incident response recommendations within minutes of detection.

## Key Points

- **Adversary Speed**: Fastest breakout time reduced to 51 seconds (down from 2 minutes 7 seconds), requiring defenders to respond faster than ever before
- **Malware-Free Attacks**: 80% of detections are malware-free, using legitimate tools and credentials to blend in with normal user activity
- **AI-Powered Threats**: AI-generated phishing emails show 4x higher success rates, with adversaries leveraging commercial LLMs to scale attacks
- **Cloud-Conscious Adversaries**: Seven officially named cloud-conscious threat actors who specifically target cloud environments and abuse cloud-native features
- **Attack Surface Expansion**: Cloud footprints create expanded, constantly changing attack surfaces with identity-driven access patterns across multiple locations
- **Investigation Challenges**: Traditional security tools create fragmented visibility between cloud control plane and workload levels, making correlation difficult
- **Agentic AI Benefits**: Charlotte AI can automatically triage incidents, correlate cross-domain telemetry, and provide expert-level analysis within minutes
- **Unified Detection**: Cloud detection and response bridges the gap between cloud workload protection and cloud security posture management
- **Expert-Validated AI**: CrowdStrike's AI capabilities developed in collaboration with managed detection response teams for validated expert analysis
- **Threat Intelligence Integration**: Adversary-focused approach studies real threat actors' behaviors, motivations, and potential future tactics

## Technical Details

- **Attack Scenario**: Developer targeted through LinkedIn job scam, malware deployed via coding challenge, credentials scraped from VS Code files, reverse shell injected into Python function
- **Cloud Runtime Protection**: Combines cloud workload protection with cloud detection and response for unified visibility across control plane and workload levels
- **Falcon Platform Integration**: DaemonSet deployment on EKS with image analysis, Kubernetes admission controller, and ASPM relay for application context
- **Charlotte AI Capabilities**: Automated triage, reverse shell analysis, NGSIM query execution, and comprehensive incident reporting with confidence scoring
- **Fusion SOAR Workflows**: Automated workflows triggered by alerts, enriching detection data with Kubernetes context and cloud control plane information
- **Multi-Domain Correlation**: Unified event timelines spanning endpoint, identity, and cloud domains for complete attack visibility
- **Indicators of Attack (IOA)**: Cloud-specific early warning signals designed for legitimate tools used maliciously rather than traditional malware signatures
- **ASPM Integration**: Application Security Posture Management provides service ownership, criticality ratings, and data flow visualization for context
- **Asset Graph Analysis**: Visual representation of compromised instances, running containers, and associated IAM permissions to understand blast radius
- **Automated Response**: Charlotte AI can automatically terminate compromised containers, generate detailed incident reports, and provide specific remediation steps
- **Real-Time Analysis**: Incident analysis and email generation completed within 4 minutes of initial detection with expert-level recommendations

## Full Transcript

- [Karishma] Hello, everyone, and welcome to our presentation today. We're gonna be talking about
cloud detection and response, as well as some of our latest
innovations in agentic AI and how that helps with cloud detection and response outcomes. I'm Karishma, I'm a product
marketer at CrowdStrike. I've been here for about
a little over a year. I've been focusing on cloud security for the past few years of my career. I started off as a penetration tester, and then I did what naturally comes next and moved into marketing. I'll hand it over to Ben
to introduce himself. - [Ben] Hey, guys, my name's Ben. I've been in the space for about 10 years. I'm a senior technical
marketing manager here at CrowdStrike. Been at CrowdStrike about one year, worked previously at Palo
Alto Networks in Cisco. Excited to present to you guys today. - [Karishma] Awesome, thank you. So I'm gonna start off
by painting a picture of what defenders are up against today. According to our latest
global threat report, which released in earlier,
February earlier this year, we found that the fastest
breakout time was 51 seconds. Now, breakout time is the amount of time it takes an adversary to move laterally across a network. Now remember, when an
adversary looks to gain an initial foothold into an environment, their next objective is to break out and move from where they are currently to where the high value assets are. So what breakout time really
determines for a defender is the speed at which a defender must move in order to drastically reduce the costs and damages which are
associated with the breach. Now, if you're looking
at the number right now, this is down from two
minutes and seven seconds from the year prior. So adversaries are only
getting faster and faster, and if we're looking
at less than a minute, right, this could be the amount of time it takes from grabbing your
cup of coffee and sitting down, and an adversary can already be in there escalating privileges
and moving laterally. So let's talk about this
adversary speed a little bit more. Adversaries move faster as
a product of the strategies that they are looking to employ. These are some more notable trends that we found in our global threat report. The first one I think
is really interesting. We found that there is a drastic increase, a 442% increase in
voice phishing activity. Now, what does this tell us? This is very much aligned
with the great advances that we've made in
endpoint security, right? Adversaries are looking
for the next best path or the path of least
resistance for breaking in. And they're very much going after something we've been
saying in the industry for a long time, which is that
humans are the weakest link. And it's been surprisingly effective. We actually had a profile
in our latest report on an adversary group curly spider, and what they do is they
actually pose as it support staff and they'll call targeted
users under the pretext of connectivity issues or security issues, and they gain access in that way. I know this is very real. I've been getting a lot of random text from people who have
been looking to help me. So it's weird how close you can get to these kinds of attacks. Second statistic on the
slide is also aligned with the path of lease resistance, which adversaries are looking for. So we saw a 50% increase in
access broker advertisements. What that tells us is that the access as a service market is booming. Now remember, an access broker is one who is looking to
sell valid credentials on the dark web and facilitate
and criminal activity. So again, if an adversary can get their
hands on valid credentials and not trip any wires while they're executing
on their operation, they will do so, right? And then lastly, when we're
talking about initial access, CrowdStrike found that
just a little over half of the vulnerabilities found
were tied to initial access. So again, along with identity being a popular mode for initial access, vulnerabilities and misconfigurations are very much up there as well. Now, we talked about the breakout time, but this last trend is
very, very interesting. So we found that almost
eight in 10 detections were malware free. Malware free essentially means that an adversary is engaging
in a hands-on keyboard attack or an attack which is meant to blend in with legitimate user activity. And you'll get to see
that a little bit later. Ben will be walking us through a demo. But what this tells us, and honestly, what every single trend
on this slide tells us is that adversaries are
only honing their craft, becoming faster and doing
everything that they can to evade detection, right? And amplifying the problem even further is that AI has become
a popular new addition to the global hacker toolbox. Even at this conference today, you guys have probably
been seeing AI everywhere. Well, it's not just for
the defenders, right? Adversaries can leverage it as well. And something that's interesting is that this relatively easy access to commercial large language models not only helps make adversaries
more productive, right? It helps to shorten their learning curves and their development cycles, but also drastically increases the pace and the scale of their activity. An interesting statistic
that we found around AI is that AI generated phishing emails saw four times the success
rate, success rate meaning, and a victim clicks on
the link in an email than a human-generated phishing email. So this just goes to show that when AI is in the
hands of the adversary, there's a lot of power there, right? Now that we've talked about
the threat landscape at large, I want to talk specifically about cloud. This year alone, this calendar year alone, we've already seen a 45%
increase in cloud intrusions, and this is compared to
the entirety of 2024. Now, something interesting
I wanna note here is that back in 2023, there was a prolific e-crime
adversary, Scattered Spider, and they were kind of the big dogs when it came to cloud intrusions. They made up for about almost a third of cloud-based intrusions. Now, that has gone down to about 13%, not necessarily due to decreased activity, but because there are new adversaries coming onto the scene, right? Like, as you can see up
here, Labyrinth Chollima is one of the newer cloud
conscious adversaries. Now, cloud conscious
means that an attacker is aware of the ability to
compromise a cloud workload and leverages this knowledge to abuse features which
are unique to the cloud. So right now, CrowdStrike has officially
named about seven cloud conscious adversaries, and we're only seeing that
number starting to grow. You'll see that in our reports, which will be coming out later this year. So adversaries are going
after the cloud, but why? Why is it such a popular target? Well, as organizations are
continuing to accelerate their adoption of the cloud,
adversaries are close behind. And the reason for that is because as your cloud
footprint expands, right? A lot of the critical data
starts to migrate that way, which means that there is
now a much higher reward for attackers, higher value reward if they are able to gain
access to a cloud environment. On top of that, as we know,
cloud spans multiple layers of complexity, right? And each of these layers come
with their own unique risks. So now we're looking at this
expanded attack surface. And when we kind of consider
the high deployment velocity and the ephemeral nature
of cloud resources, we not only have an
expanded attack surface, but one which is in a
constant state of flux. And all this gives attackers
just even more room to hide. And lastly, unlike traditional on-premise infrastructure, right? Which is largely enclosed
within defined boundaries, we have cloud activity, which
is largely identity driven. So you have users and services, which are accessing
resources from a variety of different locations, which makes things a lot harder to keep track of as well. So now we've talked about the
threat landscape at large. We've also talked about why
the cloud is a prime target. I'm now going to hand things over to Ben who's gonna walk us through
a real world example. - [Ben] All right, so progress the slide. Okay, cool. So just like Karishma was talking about, we're seeing a lot of malware-free attacks against AWS infrastructure and
cloud footprints in general. So in this example, access broker, or excuse me, access keys were committed to Git Repo commit history. Those keys were then
stolen by an adversary. They had permissions to SSM, they leveraged those permissions in SSM to legitimately access EC2,
opening up a reverse shell to command and control. And from there, further
instructions were given, and ultimately lateral
movement was achieved and data was compromised from S3. Now, there's no malware in this attack. This is effectively like yourself taking your key to your house and leaving it underneath your doormat. If you don't take care of
your keys and your credentials and have good secure GitOps,
this is what can happen. So just wanted to kind of, you know, throw a bone to you there. This is an example of one of those malware-free attacks here. So one of the things I
wanna walk through is like, how would this look like to
investigate this kind of attack? You might want to first look
at the access key exposure. Obviously, if you're
committing access keys into Git repositories and not using, you know, secure secret management, you're gonna be wanting to
at least look at the history of your commits. You're gonna wanna look at that I am role that's associated with that key, right? What are the permissions associated and what were the last use timestamps? From there, a next logical
step might be to investigate any of the AWS API calls that transpired. Good place to look. There would be CloudWatch
or CloudTrail logging. And take a look at the
GoIP of those API calls. And the next thing, you
know, next logical step would actually look at
that EC2 incident itself and provide forensics on that EC2. So things like session activity, what network sockets were open, any processes that were
ran on that machine, and any, you know, subsequent behavior after that reverse shell was open. Outbound traffic logs,
et cetera, and so forth. To achieve that, the next step,
lateral movement detection. This is one of the most challenging things to achieve from an
investigation perspective. VPC flow logs can be helpful to look at the connection
footprint as well as, you know, investigating any
network access control lists that have been updated,
changes to security groups, and rule assumption events. From there, obviously S3 was
impacted, data was compromised. So you're gonna wanna look
at those S3 access logs, any data access patterns
that might be anomalous, and do policy audits of those
buckets themselves, right? Are they over missed? Are they, you know, does this EC2 even need to be able to
read from that bucket or write to that bucket,
et cetera, and so forth? And then ultimately
with any investigation, you're gonna want to do
a timeline correlation. So it's important to understand the steps that the attacker or adversary
took and understanding, you know, how long the dwell time was. We see through our threat
intelligence that some adversaries and e-crime hackers, you know, are trying to
achieve long-term persistence and live off the land as long as they can? So with that said, you
know, the goal is there to piece together different
types of telemetry. Apologies on the overlap there. I swear it didn't look
like that last week. But the two things I
do wanna highlight here is it's really coming down to two buckets, which I've broken down here, which is that service level logging, looking at those, you
know, services themselves, the storage buckets, EBS volumes, you know, identity and access management, and then also understanding what's going on the resource level, understanding what's actually
happening on your containers, your Kubernetes clusters,
and those machines as well. And that's kind of, in
today's cloud tooling, it's a fragmented effort. And oftentimes even in, you
know, the most robust synapse, it provides an incomplete
picture, excuse me. The two main buckets where you see these capabilities fall into is cloud workload protection and CSPM. Workload protection is gonna be looking at those Kubernetes logs, runtime events, as well as anything
that's been running on, you know, any container or workload. The other side of that
coin is the CSPM side. So that's all about your
proactive pruning of risk. That's gonna be the ability
to ingest those cloud logs, look at those misconfigurations. But ultimately, a lot of times, this information is
displayed in different areas, it's hard to correlate, and
it, you know, oftentimes locks that correlated
timeline based investigation. Tools don't speak the same languages. There's limited context on cloud behaviors and ultimately too much
noise and not enough signal. back over to you, Karishma. - [Karishma] All right,
so in order to address many of these gaps, this is kind of where Falcon
Cloud security comes in. We have something called
Cloud Runtime Protection and this includes both
cloud workload protection and cloud detection and
response capabilities. So again, that gap that
Ben was speaking about where you have visibility
at the workload level, and then you also have visibility at the cloud control plane level, but there's this gap
in correlation, right? And understanding the
cloud context to activities that you might be seeing
on the workload level. So that has really given rise to this new sort of category of solution, which is cloud detection and response, and that's something that
we've been really focusing on here at CrowdStrike. There's a few things that I wanna mention. First and foremost, I spoke a lot about this in the beginning, but again, we are
adversary focused, right? And I think that really
is a compelling way to look at threat intelligence because we're not just following CVEs or looking at threats in a generic level. We're really trying to understand who are the real world threat actors, what are their behaviors, and
what are their motivations? Something really cool here actually is, you know, I was speaking with our internal threat hunting team and what they do is not only do they study what these adversaries
have done already, right? How they have gotten
from point A to point B, but also they try and map out even further what that adversary might do. How might that get from point
A to point C or point D? And all of that kind of feeds
into our detection logic, which is really cool. So speaking of our detection logic, that's kind of where our
indicators of attack come in. So indicators of attack,
those are early signals that an attack is
currently unfolding, right? You kind of would like to know before an indicator of
compromise might take place. And again, if you think
back to that example, which Ben showed, right? That was an attack that
included a legitimate access key and legitimate tooling. So when it comes to cloud
attacks, those look very different than what we're used to
seeing on the endpoint. So what's really cool is that
we've built out a repository of cloud specific indicators of attack that look at that cloud
control plane layer. On top of that, of course,
we have our cloud runtime, our workload protection. So this is kind of monitoring and stopping breaches at runtime. But the last two points is something I really wanna
spend some time highlighting. So again, what's really important is the SOC experience as
you're kind of investigating and responding to these attacks. Remember, adversaries are not limited to a specific domain, right? They don't just say, I'm going to attack just the cloud today. As you saw in the example earlier, they leverage an identity
to pivot to the cloud. So attacks can span across
endpoint, identity, and cloud. And the same should go
for how we investigate and respond to these types of attacks. So we have unified graphs and event timelines which
span across all domains in a hybrid cloud environment, and we also have built
in workflow capabilities, which can help a defender
to scale out a response no matter where that
attack had originated from. So again, as I mentioned before, because we are so adversary focused, we continue to innovate by
studying the threat landscape. And something that I mentioned also is that adversaries very much
have AI at their disposal. And so what we wanna do
here is we wanna make sure that we're leveling the playing
field for defenders as well. So what we'll have next for you is a demo on how we are
leveraging Charlotte AI to help with cloud detection
and response outcomes. - [Ben] All right guys, if the demo got smited in front of you, just bear with me. So let me get my
PowerPoint minimized here. You wanna see my screen? Okay, cool. Alright, so... Right, I wanna first start
off by kind of explaining the story behind what we're
about to demonstrate here. And so what I got, you
put together for you guys is kind of talking to our
threat intelligence team. We came together and made
an attack based off of, you know, similar TTPs that
attackers have been using. So here's the story. We had a developer named
Josh, junior developer, makes good money,
doesn't make great money. He was a victim of a phishing
attack that offered him a job. He applied via LinkedIn, they
gave him a first interview, and then they gave him a coding challenge. The developer pulled down
that Git repository repo, which had malware embedded in it. So when he completed the coding challenge, unfortunately, malware was
deployed locally to his machine and cloud credentials are
scraped from his VS code files locally stored. So don't be storing GitHub
personal access tokens in insecure places. Those were compromised and ultimately the
attacker was able to inject code into a Python function,
opening up or reverse shell. From there, the attacker
escalated permissions and then achieved lateral movement. So from there, we'll see in the attack, pulls down a variety of
tooling including AWS CLI, and then, you know, provides
further persistence from there. There's a backdoor user that is created. We often see adversaries
achieve persistence through creating new legitimate users and living off the land. And ultimately, this
attack ends in data theft and data exfiltration. So I'm quickly just gonna
pull up the repository and kind of go through this user service that is compromised. So there was a demo beacon or a reverse shell beacon that was injected in the code base and is actually referenced
in this user service. So what we're gonna be looking at is a Kubernetes application that has a few different
services running on them. One of them is going
to be our user service. When that user service spins up, nested in the main function at
the end of this script here, the demo beacon is opened or that reverse shell is then opened. From there, command and
control instructions are sent and we will walk through
kind of the exercise. So next thing I kind
of wanna show you guys, if I just do a get pods here and just show you what we're looking at, is kind of the architecture in which we're kind of defending
this cluster with Falcon. So what we're using is our
Falcon image analysis at runtime, our computer Kubernetes
emission controller and our Falcon sensor that's
running as a DaemonSet on this EKS cluster. So that's meaning we're
defending each container running on this cluster and
we also have our ASPM relay and Collector to provide
that application context. And so what we were gonna do really quick is kind of jump into the Falcon platform and take a look at what we see. So we're kind of gonna
first do an investigation more from a manual perspective. We're gonna kind of take a
look at some different things. We're gonna look at the process tree, we're gonna kind of try to
follow some of those steps that we mentioned before,
try to get as much context and be realistic as possible as what a cloud defender
would be going through. So we can see that we have
this aggregated detection with adversary association
with Labyrinth Chollima. The way that we make these
associations typically is either from file hashes
that we associate with malware, with an adversary that we've observed, or bad known domains that we know are associated with adversaries. So when we click into
this actual detection, we get a cool little picture
of Labyrinth Chollima. Hopefully, maybe some
of you visited our booth and took a picture with them today. We'll just close the
triage the real quick. But we get a wealth of
information right here just to help defenders understand the adversary context as
Karishma was mentioning earlier. We can see this as a threat actor with origin from North
Korea, and a state sponsored. We get a wealth of information around the process period
of this particular command. We see that we are
associating this initially just from this ping to
this bad known domain. As we go down though, we can see more information
about the cloud asset. And I apologize, I'm kind
of hovering over here. This desk isn't very tall,
so I'm hunching over. But if we look really on this sidebar, we can provide the defender
with a good amount of context. Hey, what account ID is this
instance in, what region? What's the instance ID? Can open up the asset
inventory and learn more. Not gonna jump into that
for this demonstration. We're focused on this detection piece. One of the other areas of information that we layer into the detection is actually the cloud misconfigurations that we've been observed with this EC2. And we can see there's a variety. It's 2025 and we do still see in the wild, I see some people smirking,
Instance Metadata Service v1. If you guys remember the
Capital One breach in 2018, it's 2025. You may have some, you know, you may have like a Uber
dependency to use v1, but highly encourage you
guys to audit your footprints and understand if you are using v1 in any of your environments. We see some other, you
know, misconfigurations here that we flag. You know, we we call them
indicators of misconfiguration. They're not, you know,
necessarily indicators that you're under attack. It's just, hey, this default state that you have configured for this service or this instance, a EC2 could be improved. But ultimately, you know, we will scan your cloud accounts and provide a readout of
anything that we discover. And so when we see a, you
know, an attack against an EC2, we're gonna automatically
pull that cloud context down as Karishma and I myself was
talking about the correlation between endpoint and
the cloud control plane. We also have a tab here for
Kubernetes and containers. And since this attack
is actually exploiting a vulnerable container, we can jump into actual, the
container details themselves. Open that up in a new tab here. And so from here, you
know, our cloud defender can now look into this
particular container. Unfortunately, this details
have expired for some reason. We'll push past that. I don't understand. I guess the gods have
smited me this morning, but apologies for that. But typically, you will see
container information I think. We had, because I'm looking
at an event from two weeks ago that information has timed out. What I wanna do next is open
up this full detection here and jump into the process tree. So when we look at the process tree, this is where we're gonna be
looking at all of the details around what actually
ran on that container. And so we can see that
Python user service.py is the parent process that
opened up this reverse shell. So if we actually open up
the reverse shell here, which is leveraging Bash to
provide the code execution, we can see a variety of commands here pulling down additional tooling, as well as changing permissions, running net stat typically to understand network connections, pulling down AWS CLI, and creating a backdoor user. From there, if we scroll in, we can see additional context
from these AWS commands, ultimately resulting in
theft of data from S3. One of the things I do
wanna also highlight here, as we're in this sidebar
on this process tree, we can actually jump into a
context from the application. So we see the service owner, Josh, the gentleman that was a target
of this particular attack, and he is the service owner. We provide that mapping for defenders. We can see that there's sensitive data associated with this service, and we give it a criticality risk rating. We can also jump into ASPM
directly from this pivot, and we're filtered here
on this user service. One of the things I'd like to do, and this is our ASPM product for you guys. A lot of people don't know that we actually have an ASPM product is from our acquisition of
Bionic about a year ago. But I really like to
use this data flow view and this provides a
context of all the upstream and downstream dependencies
that this server has or this service, excuse me, we can see all the APIs
that it is talking to. So this provides a good deal of context. We've looked at what ran
on the machine itself, we've looked at the
misconfigurations associated with it, and now we've taken a look
at some of the container, I mean, excuse me, the
application context. We can also, if we go back, we can investigate by looking
at a host asset graph, which is easy to kind of visualize. So we're centered on
the instance that was, so this is the node of
the Kubernetes cluster that this container ran on. And we can see all the images that are running on this container, as well as the permissions. So this is the actual
roll that was exploited and the permissions that this role has. And you can see the variety of buckets that this role has access to. So this is helpful for defenders
to gain that clear context of the broader impact of this attack. But as you can see, we provide
a great deal of information on this side panel here. So just want to cover, we
looked at the detection, we manually went through,
looked at the asset graph, looked at information of the
application context itself, and now what we're gonna
do is kind of shift gears and kind of take a look at what it would look like
leveraging Charlotte. So one of the things that Charlotte can do that's actually kind of
cool from this sidebar is if we actually scroll
up on this detection, we can see the reverse
shell that was opened up and we can actually have Charlotte analyze this reverse shell. And all she's doing is just taking a look at
this particular command that was run on that container, and she'll provide a detailed readout, providing context of the entire attack or this command and details
around this command. So we provide a nice
little security evaluation and read out there. We also have the ability to have Charlotte do
a triage of detection. So she will automatically triage any detection that comes in. So she has said that
we should escalate this and that it is a true positive
and provides a nice verdict. So when this detection came
in, this is her interpretation. So the detection was
labeled as a true positive because of this process
that ran a reverse shell. If we look down, she
provides further context of where that came from and she knows that it
was the parent process of that Python service that was running. So the next thing I want to
focus on, as Karishma mentioned, the speed in which AI is moving is how we can leverage workflows. So if we go into Fusion SOAR, which is our native
security orchestration, I can show you guys a Charlotte workflow. Oh, that's not the correct one, excuse me. This is the one. Okay, so what we've done
here is set a trigger to say, "Hey, any alert that comes in, let's go ahead and trigger this action." So any alert that comes in, we're gonna have a Charlotte
go ahead and triage that. The next thing that we're gonna do is actually take the
alert ID from that triage and we're gonna pass it to the next step. The next step is we're gonna use NGSIM. And what I will do is edit this so you guys can actually
see what I'm doing here. And we're actually gonna do
an event query against NGSIM using that alert ID
from the previous step. And if we click into Manage Query, we can see what we're doing. So we're saying any event that comes in, grab that composite ID. We're gonna enrich that information with the Kubernetes context. So all of the container ID information, all of the namespace, the
nodes, et cetera, and so forth, we're gonna pull that
information in and join it. We're gonna grab the APIs and then grab any indicators of attack. And then we're gonna join on
the actual sensor ID as well, provide some context for
Charlotte to rename things, make, you know the naming
convention a little bit cleaner, a little bit nicer, and then
we're gonna group the data. And so when that query
runs, the next thing of, the next step in the chain here is Charlotte is actually gonna
use the cloud latest model and she's gonna be given this prompt. You are a tier one SOC analyst in charge of protecting
a Kubernetes environment. You have received an alert
from CrowdStrike Falcon in regards to one of
your Kubernetes clusters. The data in this detection
can be found below. And again, we're just using this variable and passing the results from
the previous query here. This data consists of
information about the cluster, as well as detections from
the cloud control plane that came from the same host node on that Kubernetes cluster. Some important information, region, cloud, cloud portraying detection
rule, et cetera, and so forth. So we just provide her
a nice little report or a nice little prompt, excuse me, and then ask her to write an email. And so at the end of that phase we say, "Hey, give us your triage verdict, your triage recommendation, your triage confidence, and
your triage explanation." And at the end what we
do is we just, again, take the completion of that LLM call, and then pass that as a
variable for the email. And this is what it looks like. So when this detection ran on June 9th, at about what time is it? Yeah, about three, I
think 40 is when it ran. About four minutes
later, we get this email. Security incident alert,
Kubernetes cluster compromise. Hey, dear security team,
we're writing you a report for critical security incident detected in your Kubernetes
environment or cloud. Falcon platform has
identified suspicious activity classified as command and control using remote access techniques. The detection revealed
the reverse shell attempts from a container that's subsequently used to create a new user and
generate access keys via CLI and your AWS infrastructure,
which are persistent techniques that adversaries use to
maintain unauthorized access. And right here, this is awesome. We provide a ton of context. This is the affected resources. What pod was compromised,
what was the image? Where is that image committed to? We could provide the full registry in which end path for that image. What namespace was that container in? What node was it running on, and what's the cluster ID? The next, she provides the triage details. The verdict is a true positive,
what's the recommendation, what's the confidence, and
what's the explanation? She says, "Hey, this was a detection that was labeled a true positive
because the command line, you know, ran a bash process indicating a reverse shell." From there, the involvement
of the Python processes as a grandparent of the process suggests that the initial compromise
may have occurred through the Python based application. So she can already tell, "Hey,
there's something going on in that Python function, you
guys need to take a look at it, which is very, very cool." Provide a source for
the URL investigation. So you can click here and
go right to that detection, and then she provides incident
response recommendations. She's already taken immediate action by terminating the compromised container to evict the adversary. However, this incident
requires further investigation. Please revoke the access keys,
delete any user accounts, audit the EKS node group roll permissions, investigate the source image,
review the network logs, implement network policies, and consider implementing
runtime security controls. I recommend scheduling an
incident review meeting to discuss with additional
security measures from our Kubernetes environment to ensure we have fully
contained this threat. So as you can see, we can use Charlotte AI and fusion workflows to automate a lot of that tier one work. So that was my demo. Hope you guys enjoyed it. If you guys have any questions, I know Christian's about to
go through a couple slides. I do just wanna go back
to endpoint detections and show you guys that we can actually provide those container details. And that's effectively where she's pulling those
container details from. I'll just go with a detection
that ran on Kron last night as this pulls up, and we can
see all the data is here, the namespace, the region,
what service and container. So when we query NGSIM, this is where NGSIM point
this information from. Hope you guys enjoyed it. Again, if you guys have any questions you guys wanna ask at the end, feel free if you guys want me
to go through anything else, demonstrate anything else, ad hoc, I'm happy, guys, sit
down with any of you guys and deep dive into this stuff. But for now, I think it's time to go back over to Karishma. Is that right? Looks good.
- Yeah. Thank you so much, Ben. - Yeah, absolutely.
- Everyone, give him a hand. That was a great demo. (crowd applauding) Awesome. So just a few slides, and then, you know, we'll have some time for questions, but I really wanted to
double click into agentic AI, which Ben brought up. I know you guys have probably been hearing
about it around a lot, but there's just a few
things I wanna mention. So as I spoke about earlier, right, as organizations continue to
expand their cloud footprints, threat volumes rise and so
do alert volumes, right? Because the cloud has a
very dynamic nature to it, so you're looking at a much larger volume and variety of logs and alerts
to have to sift through. So if you think about that, right, you have the
sharp increase in threats and logs to sift through, but you don't necessarily have that increase in SOC team headcount or manual effort that's scaling
linearly with that, right? And so what's really important to us as we continue to innovate
with the Falcon platform is that we're doing what we can to help bend that labor curve so that you can continue to
move with that same efficiency and speed no matter how out
of proportion these threats or the threat volume or
the alert volume gets. And so that's been an interesting
thing to kind of work on is understand how to increase productivity as we're starting to see adversaries moving faster and faster. That's something that
we spoke about earlier. Another thing is, right? Cloud is a much newer thing to the scene. It's very complex, it's very nuanced, and there's not a lot of
time to try and understand all of its complexities while you might be trying to investigate and respond to an attack. So that's kind of why bringing agentic AI to cloud detection response outcomes was really, really an
important effort for us. I do also wanna speak a
little bit on the difference between generative and agentic AI, especially because
Charlotte AI can be both. She can do both if you need her to. So generative AI is when you
have a very specific question or prompt that you want her to analyze and that can come in handy, right? As we saw in the demo earlier,
we wanted Charlotte AI to kind of pull the cloud
control plane context and maybe query action
send for specific things. But an AI agent is something that can
complete a goal over time and that is something that
becomes increasingly important as it becomes harder to understand. You know, if you get an alert,
what exactly is happening, what is the scope and what do you do next? So it's really cool that
Charlotte AI can kind of guide you through that process and serve as a generative
AI prompt along the way. If you have specific things that you want from her or to ask her. I also wanna speak a little bit about why we even can play
in this AI space, right? I think everyone is doing so, but I wanna speak a bit about
what CrowdStrike has to offer. So when you're looking to
stop breaches with AI, right? It's not just about the
algorithms that you have in place, but it's about the data
that you have to train it. And so it's really cool
is that at CrowdStrike, we actually analyze trillions of security
events a week, right? We have a large established
customer base across the globe. We're monitoring
everything that's happening and we leverage that data to help improve our machine learning algorithms. Additionally, we have an adversary-focused threat intelligence practice, right? So our models don't just understand threats on a generic sense, but they're understanding
adversary stories, what they're doing, how they're behaving, why they're doing what they're doing, and all that helps to make for a sharper understanding of threats. And lastly, I think
this part's really cool. We actually built our
agentic AI capability in strong collaboration with our managed detection response team. So these are expert
analysts that have validated what our agentic AI
capabilities are doing. And so we can kind of go
out there with confidence that we're helping provide
expert analyst support for any defenders that are
using the Falcon platform. And then I'm just gonna close
out here by talking about how we have been recognized
across the industry. I think everybody knows that CrowdStrike is an industry leader when it comes to endpoint and identity, but it's been really cool to
kind of see us get recognized on the cloud side as well. As you can see, our
cloud workload security or workload protection
has been industry leading. We also have recently gained
recognition in the CNAP and cloud detection response space. So definitely check out
these analyst reports if you wanna learn more
about our capabilities and how we stack up. All right, that's it from us. Thank you all for attending, and we'll be happy to take any questions.
