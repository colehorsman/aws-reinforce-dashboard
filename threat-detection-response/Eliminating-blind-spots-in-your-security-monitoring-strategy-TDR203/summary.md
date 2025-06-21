# AWS re:Inforce 2025 - Eliminating blind spots in your security monitoring strategy (TDR203)

**Video Link:** [Watch on YouTube](https://www.youtube.com/watch?v=ocB506XpQT0)

## Video Information
- **Author:** AWS Events
- **Duration:** 31.8 minutes
- **Word Count:** 4,993 words
- **Publish Date:** 20250621
- **Video ID:** ocB506XpQT0

## Summary
This talk by Andrew Krug from Datadog explores how security teams can eliminate detection blind spots by combining traditional logging with runtime telemetry, unified data formats, and improved observability pipelines. He walks through the history of detection—from physical security to cloud-native complexity—and advocates for layered telemetry, runtime security, and the Open Cybersecurity Schema Framework (OCSF) as a foundation for scalable, efficient detection and response strategies.

Krug emphasizes the growing value of runtime data from agents, applications, and GenAI systems to detect behaviors that logs alone can’t reveal. He also covers reducing detection engineering toil through data standardization, long-term storage (e.g., Security Lake), and better SIEM cost management.

## Key Points
- **History of Detection:** Evolved from physical/log-based detection → VM complexity → cloud-native → GenAI and Agentic AI threats
- **Modern Detection Challenges:**
  - Too many logs, too diverse in format
  - Multi-account/multi-region AWS makes centralization hard
  - Overwhelmed teams missing alerts despite detections being present
  - Poor context from logs alone (e.g., no syscall or process data)
- **Runtime Context is Critical:**
  - Needed to detect complex attacks (e.g., malware process trees, prompt injection in GenAI)
  - Datadog Workload Protection supports Linux, Windows, Kubernetes, Fargate
  - Application tracing (APM) enables signature matching at the code level
- **Observability Pipelines:**
  - Ingest and normalize data with log routers like Datadog OP
  - Reduce duplication and transform logs into OCSF-compliant events
  - Enable easier migration between SIEMs or tools with less friction
- **Open Cybersecurity Schema Framework (OCSF):**
  - Schema adopted by AWS, Datadog, and major vendors
  - Empowers teams to write detection rules once and apply across all normalized data
  - Supports behavior-based detection (not just signatures)
- **Detection Across Diverse Sources:**
  - Logs (CloudTrail, VPC, S3, identity providers)
  - Runtime agents (syscalls, memory, network activity)
  - App instrumentation (traces, spans)
  - GenAI telemetry (e.g., LLM observability, prompt tracking)
- **Security Lake + Datadog Flex Logs:**
  - Long-term storage up to 7 years with Security Lake (OCSF-native)
  - Archived logs with quick retrieval using Flex Logs for cost-effective retention
- **GenAI and LLM Threat Detection:**
  - LLM Observability uses tracing models to detect:
    - Prompt injection
    - Indirect privilege escalation
    - Hallucinations
    - Toxic output

## Technical Details
- **OCSF Benefits:**
  - Standard format for identity logs, session events, cloud services, etc.
  - Enables simplified detection rule logic across IDPs or log types
  - Reduces vendor lock-in and detection duplication
- **Datadog Runtime Agent:**
  - Captures kernel-level activity and maps parent-child process chains
  - Supports rule activation/deactivation for tuning
- **Datadog APM + Security:**
  - Signature-based detections on traces (e.g., SQLi, SSRF, LFI)
  - Global blocklist from observed attack patterns
- **LLM Observability:**
  - Treats GenAI request/response flows as application spans
  - Detects security and quality issues in real-time
  - Powered by OpenTelemetry extensions for GenAI

## Full Transcript

- Thanks for coming out in the afternoon on the very first day of re:Inforce 2025. I'm Andrew Krug and I have the privilege of leading the Security Advocacy and Research Team at Datadog. We're the team that writes
Datadog Security Labs, the Datadog State of Cloud
Security, State of DevSecOps, and tons of other great content that you see in the
cloud security community. We're around at tons of events like this to hear about how you are
thinking about security. So obviously, if you're here
to learn more about Datadog, I'm here to catch up with
you after the session's over. I can't take any time
for questions on stage, 'cause it's a silent session, but I'm happy to meet you afterwards. So if you got some time to catch up, we can meet here or you can
meet at the Datadog booth in the expo hall where I'll be just briefly
after this is over. So you're here today to hear
about eliminating blind spots and security monitoring. So if you've been in the
security space for a long time, you may have started your
career working in a data center. Does anybody want to admit
to starting their career actually working in a brick
and mortar data center? A few, a few. I actually started my career
working in a data center full of servers, like actual servers that you
could walk up to and touch, running a really old operating
system called Novell NetWare. At the beginning of the
computing revolution in business, things were a lot
simpler than they are now and the biggest problem was figuring out what size of parka to wear
when you walked into the room where the servers were running? A lot of security was physical security. In fact, in the reality
that existed back then, a lot of the identity and
access management was actually, did you have physical access
to the console of that thing? So since then, obviously, things
have significantly evolved. The single-purpose siloed
systems with manual processes evolved into these increasingly complex, intelligent data-driven systems that we're all working with today. Today, especially if you're here, you know observability is
a foundational component driving much of your decision making, whether that's for
performance, cost optimization, and, of course, security. These are all really, really important in complex cloud-native environments. Also, accelerating digital transformation and user experiences. We have to provide these
enhanced feature sets, but also rapidly enable the
business to perform tasks that had previously been performed by entire teams of people. That's a really fancy way of
saying we're doing a lot more, with a lot leaner teams today. So with that complexity
and also innovation, there's always blind spots in the strategy to detect and respond. Some of the blind spots
that we're gonna talk about might surprise you, because they might not be
things that you're aware of. The good news is that blind
spots generally follow a predictable pattern. So I'm a big fan of the notion
that like everything old is pretty much new right now and almost every concern that we have can be addressed by adopting
some old tried and true tactics and just applying them to new technology. So to paraphrase a very old expression, the only lesson we learned from history is that humans don't learn from history. And I think today that is
probably more true than ever. So if you will join me briefly, it's time to hack to the future by taking a quick walk down memory lane. So if you were around for the 1990s and I was around for the 1990s, detection was primarily
focused on networks. We relied really heavily on
signature-based detection. So think file hashes, IP addresses. the incident response
process was very manual, very slow with limited
visibility to help us figure out what were actually false positive. So we worked almost every incident like it was a real incident. Monitoring was fragmented across different layers of the stack. One of the most prominent
blind spots though, was actually the silos that
existed between the teams with each distinct team
having its own tooling and reporting systems. So application security
was a, not even a term that we used back then, but
we had teams of operators that focused on the code that ran. We had network security people
and system security people, and the boundaries around their
knowledge was so different, they almost didn't
speak the same language. In the 2000s, we sort of had
the dawn of observability almost out of necessity. The AWS Cloud actually launched in 2010, 5 years after the creation
of the first SIEM platform. Applications were just
starting to increase in their sprawl and complexity. And if you think about what was going on at this time period, this was kind of the
dawn of virtualization. So prior to this, when you
wanted to have a new thing, you actually had to
like lease a pizza box, put it in a rack, and then run that thing. And with VMs, all of a sudden, we started to be able to run more compute on our extra computes. We had application and server sprawl. The 2010s also brought this era of the very first highly
impactful security incidents. It seemed like almost no company, and I don't mean to shame anybody by putting them on this list. This is for the purpose of demonstrating, regardless of company's size,
no company was really immune to a data breach. On the application side, Kubernetes was released
in this time period and forever changed the surface area for cloud native computing. Datadog was also founded in the 2010s in response to this increasing complexity to help customers address
their gaps in visibility that were present in
so-called modern applications at the time. And we started to see friction here. And this is something that
still really exists today. Anytime that we have brand new technology and technology from the last
era of technical innovation that's gonna have some sharp
edges where we integrate it. I think the most prominent
version of this today is machine to machine
authentication for Agentic AI, but back then it was where
cloud met the data center. We had standards that really didn't work for cloud native computing that did work for us in the data center and any time we saw those
two things intersect, we had issues. So today, we're all running
workloads in the AWS cloud. That's why you're here at AWS re:Inforce. Applications have moved from
static to highly dynamic, from simple to complex
multi-tier architectures, and have changed
fundamentally from generating almost no telemetry to an
explosion of data by default. I would say that most people here are probably actually buried in data but don't necessarily have the systems and the visibility to
analyze and act on that data in a meaningful way 100% of the time. So the truth of that is that
we're all kind of coping with this data problem and we
have data analysis problems, some of which are being
addressed by generative AI, filtering relevant data to cost optimize what data you're ingesting, and acting on from a security
perspective is a challenge. And overwhelm teams that are
inundated with false positives will miss critical security alerts often. One of the most common themes in cloud security incidents today is actually we had detection
mechanisms in place. They detected the problem but no one actually looked
at the alert and triaged it. So if you look back at the
last five to eight years of cloud security incidents, that's an incredibly prominent theme. So in the AWS Cloud today, if you're only ingesting
the common log sources, you probably have at
least five out of box. CloudTrail, data plane
logs from S3 object access, VPC flow logs, and system logs
from compute in the account, and more if you integrate
a third party tool like an identity provider
in that logging strategy. The adoption of generative
AI has also increased logs exponentially in regulated industries and development environments to detect and respond to AI threats. So like just curious from the audience, how many folks are using generative AI? How many people are
using logs as the method by which you detect
threats in generative AI? Almost nobody. Is anybody actually detecting
threats in generative AI? Also, almost nobody. So each one of those logs,
including gen AI logs, comes with its own unique storage format that you have to understand,
transform, store, and ultimately use to alert. So we're dealing with
a volume of data issue and also a diversity of
data issue as an industry that makes detection, response, and triage incredibly challenging. We used to call this the
kitchen sink strategy. You create one way for
service teams to send logs to your aggregator, and in theory, you check the
box and you solve the problem, because then it became the
detection engineers problem. The problem with that is that
in that increase in volume, there's not just an increase
in direct dollar costs, there's also an increased
cost in human time to detect and the confidence and fidelity
of those detections suffers the greater the diversity
of that volume is. So we generally hear
from folks in the market is that they don't extract a lot of value from their detection response solution simply because the existing
solution are too complex, too noisy, and too costly to
cover 100% of their systems. Does anybody identify with that? Like too complex, too noisy, too costly? Yeah, I see some heads nodding. The biggest problem with building a threat detection strategy
on top of SIEM only is that you're missing the
pieces of critical context that doesn't surface in logs. Some examples of that might
be process information, syscalls, kernel activity. In isolation, only logs or
only runtime information is just not enough to provide that high fidelity reliable detection that people can trust 100% of the time. And this is underscored by
the need to observe threats and detect them now today in
these non-deterministic systems like generative AI and Agentic AI. So in summary, everybody's dealing with
collections challenges, log source challenges, cost
challenges, data challenges, investigation issues,
and a lack of context from only having logs or
only having system context. And while they're dealing
with those challenges, they're pressured by the business
to deliver more features, protect intellectual property, and make the safety of
your consumer job zero, which is more important than ever today as we talk about the
rise of generative AI. Quick poll here as well just to see how broad the problem is. How many people in the audience are in a multi-account AWS organization? Almost everyone. So according to our Datadog
State of AWS security, which is notably a
couple of years old now, the most prolific users of organizations use between 10 and 100 total accounts. So the 10 being the lower bound, hundreds of accounts being the upper. Collecting data across multi-account, multi-region is often cumbersome
and difficult to manage. Has anybody ever collected multi-region, multi-account DNS logs,
for example, from route 53? Yeah, then you know it's
like this massive undertaking like multi-month project even just to roll out the collectors, and then get those all
to a central aggregator. So when we talk about that friction in just like getting the
logs into the platform, that impacts our ability
to do investigations, and investigations often
take too long to discover the root cause of the incident. Or worse, if the incident goes
back a long time in history, that creates more friction, because then you have to back load data from a cold index into a hot index. So in almost every incident timeline, this box in the middle of like
what the heck happened here between our desired state, which is that the shiny
new system was working and the system was compromised,
what happened in there? We're always trying to answer that. And that window of uncertainty
can be quite long, right? The longest incident window I
ever worked on was 18 months, and it was a real slog
to load all of that data and analyze it even with today's tools. So that's all to say that
just getting the logs into the aggregator is
kind of a complex problem. The data formats are a problem, but also the pipelines
that we use to plumb logs in these environment. Environments also becomes a problem, because if you're using things
like serverless functions to transform data, all of a sudden, the proliferation of these things becomes something that you
have to actually care and feed. So seemingly simple functions
can have a massive impact on the amount of toil
that your security team goes through just to
transform and ingest logs. So all the standard rules apply here in terms of the care and feeding. So we've identified here
just in this conversation only about logs, a few
modern stack blind spots. We have multi-region,
multi-account, runtime context, and logs that end up in
archives just to name a few. So you may be asking now we've
kind of like done a survey, fly over at a high level of the problem. What do we do about it? I'm a big thing, I'm a big
fan of making things easy. And at a glance, the notion
of that log sync idea, you just throw all your logs at a single thing does sound good to me, 'cause that sounds like what
we call in DevOps paved road. The data transformation
is the biggest issue there and the dollar cost is
almost kind of secondary in the context of the things that we're trying to all secure today. And that's where the Open
Cybersecurity Schema Framework comes into play or OCSF. I don't know if anybody's
heard of OCSF before today. I know it was a big part of
some announcements this week. The OCSF initiative is
state of the art in mapping that glut of formats into
a standardized schema. And I've seen this try to happen
tons of times in my career. This is the most successful
effort I have ever seen in terms of just getting every
major cloud service provider, every vendor to onboard to this, and actually adopt it as
their native storage format, not just for ingest, but also for storage. And I'm not sure as a community, we quite understand what
the impact of that is today. So if you've been around
in the biz for a while, you may be equally dubious that this is not going to
solve all the problems. But unlike the failed
standards that came before this that weren't adopted
broadly, OCSF is a taxonomy. So that taxonomy is adaptable based on the type of data source, and it does not just focus on
signature-based detections, it focuses on tactics,
techniques, and procedures. So we're talking about a schema that was designed for
behavior, not for signatures. And that is what has differentiated this. So OCSF is now part of
the Linux Foundation, and it's a critical part of
how you should be building your modern detection strategy. It's both a format that
is supported by AWS and Datadog as a first class citizen. And what this means for you, if you are doing detection
engineering and like, just show of hands, how many
people are actually doing detection engineering? Quite a few here today. You can write simplified detection rules that will streamline your investigations, because now, your incident responders only need to know one format
that you can correlate across multiple platforms
and data sources. To give an example, here
that's really, really relevant, today, your business might have
multiple identity providers, multiple sources of truth when it comes to federated authentication, 'cause like if you're an
enterprise for example, you might have acquired a
bunch of different companies, and maybe they onboarded with, you know, identity provider one and you
used identity provider two. So all of those logs on ingest are mapped to the standard OCSF format via a product like Datadog
Observability Pipelines or what we just call it OP internally. And because that data now
exists in a standard format, regardless of the solution, it empowers us to write
a single generic rule that now covers all
those identity providers. So like think about things
like account takeover, where you wanna do session
invalidation or phishing attacks. You don't have to go back
and rewrite that rule every time now in order
for it to have value as you onboard more log sources. And that's huge. The concept of log routers, the transform data definitely isn't new, and there's a variety
of solutions in the open and commercial space. The key here though is the ease
of mapping those attributes, those standard attributes
to the OCSF data structure. So we're gonna talk a lot about things that you should be looking
for in the solutions that you're adopting to reduce
frictions for your team. So that's one of the things
that you need to look for is like as I'm onboarding
sources that aren't in OCSF, how easy is it for me and
the platform I use today to actually map those
back to the data structure I'm using to detect. The lower that friction is
for your engineering teams, the more data sources they're
gonna onboard to that pipeline and the more you're going to
increase your threat coverage. An additional bonus of using a log router is the ability to migrate
tools, adopt tools, and filter data easily. That agility allows you
to pick the best tool for the process and you can
move your logs if you choose to even from one SIEM to another
with a ton of agility, which partially addresses
the cost component in successfully implementing
any SIEM solution. So before today, before OCSF, moving out of one SIEM and into another was a multi-year project. And, in fact, sometimes, it would double or triple your cost, because you're replicating data to multiple data sources
while you train your team. And we just don't have to
do that anymore in 2025. Data retention becomes an
additional potential concern. So one example of this is from government, not sure if we have any
public sector folks here. Memorandum M-21-31. It's one we like to talk
about a lot on stage that affects government
contractors and agencies. This requirement dictates
that you have to retain logs for a minimum of 30 months
in a lot of use cases. Can you imagine retaining
30 months worth of logs for your business if
you're not in government for 30 months in a hot index? And what the impact would be to you? Or even just searching all
those logs in the event that you had an incident. So this is where Datadog
and AWS come together to provide a better
long-term retention option. So this is a definite
better together story. AWS Security Lake, if
anybody's familiar with this, was one of the first
partnerships that we launched. We actually launched it at AWS re:Inforce. Security Lake supports OCSF
as the native storage format, and it can be the intake
for events as well. If you fall into that category where you have these very
long data retention windows that are required of your business. Push of a button, up to seven years
retention in Security Lake. Security Lake also makes
it incredibly simple to ingest aggregate store and filter logs before you send them along to Datadog. It's also very, very simple
to onboard multi-account, multi-region to Security Lake if you do fall into that
long term retention use case. So for companies with a little bit shorter retention requirement, Datadog Cloud SIEM now offers this thing called Flex Logs, which is something a
lot of customers ask for for the retention archival of logs as they age out of the system to more cost effective storage tiers. And this is a big deal, right? Because you don't necessarily want to have the logs unavailable or have friction in the event
that you have to reload them, but you do wanna store them
in a little cheaper tier, so that in the event that
you do have an incident, it's easy to recall those, but they're not just
sitting there costing you a ton of money on the shelf. That's just one piece
of the puzzle though. So we've solved like data
ingest, data transformation, storage format, retention
in two use cases. Our additional detection sensors
we're gonna discuss today that I firmly believe
that you can't afford to live without come in the form of what we call
non-traditional security data. So the first is runtime security. And if you see me this year, I'm talking about runtime security a lot, trying to raise awareness for all of the different
types of runtime security, you can have in your environment and how it benefits
your detection strategy. So runtime security can be
really challenging to talk about, because for years, we've
only talked about this as file integrity monitoring. So some people map runtime
security to the concept of an EDR or something like that. And while those things
do do runtime security, runtime context provides
far more visibility than simply changes in files. So we're becoming aware of
this with the rise of gen AI, but before this, we also had
other runtime security sensors. The first of which is the
Datadog Security Agent. So it's a part of the product line that we call cloud
security management now. We call it workload
protection in the UI today. The runtime security agent
collects a variety of data points like process telemetry,
syscall data, network, memory. For example, if a piece of
malware attempts to change a user password on disc, we could easily detect that via logs. However, what we would be missing was the initial access
vector and the knowledge of whether that came through an exploit or what the parent process was
that actually executed that. So we have all this rich
context that we can use to almost reason at the edge
about the criticality of alerts just from changing this one
setting in the Datadog agent. The workload protection
agent detects threats that would otherwise take
incredibly large volumes of logs or context to bring to light
quickly and effectively. It gives you additional
critical insight you can use to open an investigation
or take an action. So that's like a pretty
cool additional value add. One feature you should always look for as you're thinking about runtime security is the ability to activate and deactivate which sensors and rules are firing on that runtime security telemetry. So as we think about
moving beyond simple things like file integrity monitoring to more complex attack
chain style behaviors, we need the ability to kind of be agile and play with that as we
tune it for the business. The Datadog workload
protection agent allows you to do just that using
our supported tooling in a safe and secure manner. Workload security today supports
Windows, Linux, Kubernetes, and Fargate workloads to
give you complete insight regardless of what you're
building in the AWS cloud. All right, so that's two
blind spots we just discussed and solutions. Another potential is actually the data from what is going on in
the application runtime. Depending on the stack, whether
it's pre-compiled byte code, dynamic code, or just in
time like C# or the JVM, something in your stack
has runtime context from the language itself. And this is an area we're actively trying to raise awareness for in
the security community, because for us, this is all built on top of Datadog Application
Performance Monitoring. So is anybody familiar with APM? A lot of security people aren't. So for years, operations
teams have used tracing data to optimize performance. That's simply a span of the information regarding the amount of
time it takes to make calls between services like a database, or a web server, and REST API, turns out a lot of that
data is super, super useful for understanding security context. And today, we're actually as a community, doubling down on that with things like the open telemetry project, which are adding these schemas
to more and more things beyond application runtime
like generative AI. We can use that context to
create security signals. So this is the product family that's called Datadog
App and API Protection, which works by matching
signatures to traces. So it's effectively a set of heuristics that operate on HTTP
headers to detect threats that previously wouldn't
have been detected. Thanks to runtime context, this can reliably identify
things like SQL injection, local file inclusion,
service-side requests forgery, and then it adds that if you
want to a global block list. So the first time this
happens to a single instance from an attacker, that
IP or that user entity is going to go in a global block list that then is blocked
across the entire fleet that's serving that application. And you could decide
whether that's permanent or penalty box. There's a lot of knobs to turn. The more you use a feature like that, the better the benefits, 'cause again, the block list is global. It turns your entire fleet
of public attack surface into a network of sensors
that generate that block list. The interesting thing
about using the concept of tracing here is the tracing concept is extendable to almost anything. So think about it, right? We're detecting the round
trip time between services or the round trip time
in a call to a database. And if we think about a new
technology that we can apply an old method of problem
solving to, it's generative AI, because the reasoning graph for gen AI, actually to us, looks an
awful lot like an APM span. And that's where LLM
observability comes in. It's a Datadog product that
was released last year, seen rapid adoption due to its ability to understand activity in these non-deterministic
systems like LLMs, using the same principles
that we applied to tracing. And actually, what's on
screen here is a gen AI, generative AI generated diagram of how this tactic benefits security. It's not just inside of
Datadog, this is also a standard that's evolving in an
open telemetry community, and it has very real
practical applications in the way that you think about detecting and acting on generative AI threats. So the approach reliably
combines all the pillars that we've been talking about
today, which are safety, security, and performance
to provide visibility into what goes on from the
time a model is prompted to the time that that model
returns its answer or artifact. Today, it can detect things
like prompt injection, indirect privilege escalation, user toxicity, and hallucinations. So this is just one more
example of how runtime security can help you eliminate blind
spots in your organization. And I know the screenshot
here on the slide doesn't do it justice. So if you're interested in seeing this, I would encourage you to
stop by the Datadog booth and have a deep dive into this demo, because the product has
actually evolved a ton just in the last couple weeks and we're really excited
to show it to you. So some key takeaways here
before we wrap the session, and then we go to hallway track for questions and answers and networking. Key takeaway one is observability
has been a foundation for operations teams. It is absolutely a pillar of security and that's something that AWS and Datadog are 100% aligned on. Runtime security is most
definitely on the rise in all the different forms
that you just saw in this deck, plus a few more, and it should definitely be a part of your security strategy today. So if you're looking to reduce toil and increase the signal
and reduce the noise, runtime security is one of the best ways that you can add context to the way that you're assessing the
criticality of an alert. The third is that runtime security does not replace the
logging strategy, right? Logs are still an essential foundation to what you're doing, and
having a great SIEM platform is effectively table stakes now. The thing that you can do to
benefit yourselves the most, of course, in that logging
strategy is just like us, just like AWS really encourage
partners, applications, vendors like us to adopt OCSF, because that just benefits
everyone in the way that we write detection rules. It eliminates things like vendor lock-in, increases log portability, etc. So with that, I'm gonna wrap here. I have a couple of quick QR
links on screen here today. One is to sign up for a
free trial of Datadog, which I'm sure you've
seen the link before. The other is that we just
launched a brand new community focused security newsletter this year, and I'd love to have you subscribe to it. The content, believe it or not, is actually written by a human being. In fact, we're so proud that the content for this newsletter is
written by a human being. We actually put the name
of the human that wrote it at the top of the newsletter. So if you're interested in getting practitioner focused content from my team and the internal research team at Datadog, visit that link on screen and
subscribe to the newsletter. And with that, I thank you for being here on the first day of
re:Inforce in the afternoon and hope to see you in the hall.
