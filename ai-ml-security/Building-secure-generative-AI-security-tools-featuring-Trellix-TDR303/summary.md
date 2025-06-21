# AWS re:Inforce 2025 - Building secure generative AI security tools, featuring Trellix (TDR303)

**Video Link:** [Watch on YouTube](https://www.youtube.com/watch?v=5waghmr6_38)

## Video Information
- **Author:** AWS Events
- **Duration:** 60.2 minutes
- **Word Count:** 11,573 words
- **Publish Date:** 20250620
- **Video ID:** 5waghmr6_38

## Summary
This session explores how to securely build and operationalize generative AI tools for cybersecurity, highlighting both AWS strategies and a real-world case study from Trellix. The speakers walk through the **generative AI maturity matrix**—ranging from simple retrieval-augmented generation (RAG) to fully autonomous multi-agent systems—and demonstrate how these models apply to security operations.

Key AWS speakers introduce best practices for adopting generative AI responsibly, integrating traditional ML and agentic AI for improved detection, triage, and automation. Trellix shares a powerful live example of applying agentic AI in production to automate alert analysis, context gathering, and security decision-making using LLMs. The talk concludes with implementation patterns, model selection tips, and how to balance cost, performance, and explainability in generative security tooling.

## Key Points
- **Three security-focused dimensions of generative AI:**
  - *Security of GenAI* – securing the models and infrastructure
  - *GenAI for Security* – applying AI to security objectives (main topic)
  - *Security from GenAI* – protecting assets from misuse of GenAI
- **GenAI maturity matrix (L1–L4):**
  - L1: Search (RAG, Q&A)
  - L2: Workflow automation (LLMs guide predefined steps)
  - L3: Orchestration (multi-agent planning with tool access)
  - L4: Autonomy (dynamic planning, execution, and self-healing)
- **Security use cases across the NIST framework:**
  - Alert enrichment, threat triage, log analysis, vulnerability management
  - Generative remediation suggestions (e.g., for Lambda functions)
  - Agentic SOC orchestration, proactive threat hunting
- **Agent architecture design:**
  - Core agent loop: LLM (brain) + tools + memory + goal context
  - Model Context Protocol (MCP) helps agents reason over tools/APIs
- **Best practices for GenAI security tools:**
  - Start with L1 (search) and progress incrementally
  - Avoid hallucinations via controlled outputs and human-in-the-loop
  - Tier models by cost/performance (e.g., Nova Micro vs. Claude Sonnet)
  - Use multi-model orchestration (e.g., one for classification, one for decision-making)
  - Tune with prompts and real-world QA benchmarks, not just synthetic tests
- **Trellix use case:**
  - Live example of an LLM-powered SOC using multiple AWS services
  - Agentic AI responds to alerts using internal/external data (Security Hub, GuardDuty, custom intel, verified access)
  - Rich explanations and remediation steps generated automatically
  - Adaptive model behavior based on organizational context and case notes

## Technical Details
- **Model orchestration strategy:**
  - Uses Amazon Bedrock for multi-model orchestration (e.g., Nova for classification, Claude Sonnet for decisioning)
  - Tiered evaluation strategy to balance cost/performance
  - Agent “prompt” architecture includes structured goals, tools, return format, and guidance
- **Data sources used in agents:**
  - AWS security services (Security Hub, GuardDuty, Inspector, Verified Access, Security Lake)
  - Trellix services (XDR, telemetry, threat intelligence)
  - External sources like Tenable, CrowdStrike, Okta, etc.
- **Tool integrations:**
  - Agents select tools based on classification (e.g., fetch network flows, call sandboxes, enrich context)
  - Automatically assemble investigation paths, extract relevant traits (e.g., geo-infeasibility, certutil abuse)
- **Security guardrails:**
  - Use of human-in-the-loop and audit trails for decisions
  - No model fine-tuning with customer data (to preserve privacy and avoid cross-tenant influence)
  - Dynamic instructions based on recent case feedback (via case note ingestion)
- **Evaluation:**
  - Benchmarks include Base64 decoding, tool selection accuracy, and hallucination rate
  - Preference for read-only prompt engineering and QA evaluation over model fine-tuning
  - Visualizations and metrics inform trust and tuning decisions

## Full Transcript

- [Jason] I'm Jason Garman, a principal security solutions architect here at AWS specializing in security. And just a quick raise of hands, does everybody hear us in the audience, making sure those headsets are working. Awesome. Alright, good to hear. Go ahead, Aaron. - [Aaron] So today's
session, we're gonna talk about some gen AI fundamentals, just to make sure we're
all on the same page. We're think gonna talk about
some of the security use cases for gen AI. We're then gonna talk about
a gen AI maturity matrix, and then we're gonna have
some real lessons learned from Trellix applying this in the field into an actual real product and service. - [Jason] So real quick,
some of the things that you'll get out of this session. We wanna explore how you can
adopt this new technology for your security and
cybersecurity use cases, right? This way we can explore
some of the concepts, the use cases of gen AI
that you can take back into your SOCs and really understand some of the lessons learned. And we're gonna hear some of
them from our guest speaker from Trellix, and things
that you can apply into your own deployments of gen AI in your security organizations. - [Aaron] So when we talk
about gen AI for security, we're really talking about really these three core dimensions,
security of generative AI, that's how we build secure
applications that utilize gen AI. We're talking about then
engine AI for security, leveraging gene AI to meet a
specific security objective, and security from gen AI,
protecting assets from gen AI. For today, we're talking
about this center funnel here. And when we talk about gen AI as a whole, it's really important to talk
about really the construct of the past few years where we've been. We started in really 2023 with directly interfacing
with models themselves. What does that mean? Chat applications, querying
the model directly. We then started in 2024, moving these pilots and chat systems into limited production states. And in 2025 is when we
really started to see the advent of imbuing these models with being able to access
external tools and systems. And that's where we hear agents and agents are really what we're
starting to see more in 2025. The next construct you
might be thinking though is what is an agent and how
has this been evolving? So at AWS, we define an agent as an autonomous software
system that leverages AI to reason, plan, and complete tasks on behalf of a human or a system. The evolution of what we call
agentic AI has been, again through gen AI assistance. That's where we typically
started in 2023, and others, you think about following a set
of rules or repetitive tasks to now gen AI agents where we're having
achieving a singular goal, automating a workflow, and now an agentic AI system is where we're moving to
more autonomous actions that execute multi-step plans and can actually do replanning, all of which have
different levels of agency that requires different
level of human oversight. No matter which of those
constructs an agent is defined as, they all center around
this core architecture of using an LLM as a
brain, a central interface to decide which specific actions to invoke in a specific environment, in an iterative loop and reflect on that based on every step at
different observations. Each step the agent brain has access to, you can think of as different appendages. The tools are specific
actions that could be invoked. Memory has short-term and long-term memory to persist past conversations
and interactions to be retrieved in context, and goals to maintain
the specific objective that that loop is operating in, when to enter and exit that loop. Now over to Jason to talk about some of the
applied AI security use cases. - [Jason] All right, thank you, Aaron. So, you know, generative AI
really has taken the world by storm over the past couple of years. But I would like to just
take a quick step back because you'll notice the
title of the slide says, Applying AI to security use cases, not specifically generative AI. Well, why is that? Well, really the industry has been using artificial intelligence
and machine learning in security for decades now, right? This is a paper from 20
years ago talking about using artificial intelligence
and machine learning to analyze TCP dump
PCAP files, for example. So this isn't new. And to be honest, there's a lot of applications
of artificial intelligence. There's a lot of technologies
behind machine learning that are not just generative AI. So when we think about that,
I'd like to kind of go back and, you know, investigate how are all of these different
technologies related? So if we look at what we kind
of refer to as traditional AI and ML technologies,
typically these are used to predict based upon some source data. So you can do things like
identify class memberships, apply labels, forecast future
performance and other tasks. So you can think about these as, you know, malware classification, anomaly
detection type of use cases, computer vision and
time series forecasting. So these are technologies
that have been in production for many, many years and are still using very, very relevant
artificial intelligence and machine learning
technologies and methods. Of course, now we have this new
technology of generative AI. And so what I like to point out here is that these two technologies, these kind of generic
categories of technologies, they're not mutually exclusive. You can use, depending on your use case, items from the left, from the
traditional AI and ML space. And then for use cases that apply, you can now use this new
tool of generative AI to address those use cases as well. So when we think about generative AI, well, this is a technology
that's typically used to create new content based on data. So some examples could be summarization, creating draft reports, creating
a chat bot is, you know, kind of the quintessential example of generative AI technology. You can generate code
and so forth and so on. So then the question is,
when is generative AI a good fit for your security use cases? Well, we like to think about it in terms of complementing human skills, complementing formal methods. We in fact, at AWS have
been working tremendously in order to find ways to
integrate both generative AI and traditional hard
mathematical reasoning skills, such as our automated reasoning tools. Another way that generative
AI can be a good fit for security is processing large
amounts of multimodal data. So a lot of organizations and
even security organizations may have large amounts of freeform text and unstructured data that
they previously had no way to use in their day-to-day operations. For security use cases,
you can think of things like threat intelligence
reports, for example. So now you have a mechanism
by which you can take a bunch of these reports
and other artifacts that you may have access to and start generating insights out of them. And finally, if you have a need
for flexibility and outputs that are required for the
outcomes of your use case, when you don't have a
clear well-defined problem, this is another way that
generative AI can help you understand or help be a good fit for your security use cases. On the flip side, there are places where we feel generative
AI may not be the best fit. So if you think about those
well-defined use cases that we saw on the last slide, things where you don't require the processing and
flexibility of large data sets and unstructured data, when you're not having
to generate novel content in some fashion. In those types of places,
if you need AI and ML, that sort of flexibility, you may be better suited
with a traditional ML or analytical technique. And lastly, one thing that
we definitely want to address is how you handle accountability, and also the fact that generative AI is non-deterministic in its reasoning. So when you think about activities that require accountability,
a human level accountability or certainty in their execution, these are places where thinking
about human-in-the-loop and other mechanisms that
can complement generative AI, that can be a very useful
tool in your tool chest. So let's take a look at some of the practical
security use cases that do fit that gen AI mold
for our cybersecurity users. So here's an example of a
couple of different use cases that we've come up with. Now, this by no means
is an exhaustive list of all the different ways
that you can leverage generative AI for your
cybersecurity operations. These are just some examples
that we've seen out in the wild and the things that we've
built ourselves at AWS. You'll note that a lot of
these, they will align very well to the NIST Cybersecurity Framework. So if you think about the
identify, protect, detect, and respond and recover
pillars of that framework, you can see where you
can plug in generative AI across all of those different pillars. So thinking about the
different source data sets on the bottom, feeding in
generative AI-based use cases in the middle, and then grouping them along your chain of how you're thinking about your cybersecurity program across the NIST Cybersecurity Framework. But the problem that you can see here is that there's a lot
of different use cases that we've listed, right? And this is one of the key issues that we see customers facing, is that they just don't
know where to start. There's a lot of possibilities, but how do we know where to get started? And in order to address that,
I'll pass this back to Aaron and he's gonna introduce
the maturity matrix. - [Aaron] Thanks, Jason. So as Jason just laid out the stage, the really the construct
and the problem is how do we actually classify and have a operations maturity matrix to these different use cases? So we really have thought about
four different levels here. The first being Level 1 and Search, being the ability to
retrieve and synthesize data from multiple sources. The second construct is Workflows. Once you are able to do search correctly, now we can talk about generating
content in multi-step steps using LLMs within specific
defined workflows and paths. The third is orchestration. This is where we now introduce agents to actually work in tandem
in a multi-agent framework to then complete a specific
task across a system. Next L4 is when we go to full autonomy. That's when you have systems,
AI systems and agents that have self-healing
abilities to plan, execute and dynamically replan until
a core objective is complete. Across these four levels,
we see on the top, the increasing autonomy
and business impact. This is then going through effectively, maybe starting at L4, full autonomy is not necessarily the best step if you don't have a classic search system. If you can't find information correctly, then well, you can't really
well orchestrate that, you can't automate a process. If you can't automate a
process, why add more complexity or add features like autonomy to that? When we start thinking about what are the different dimensions
within each of these, and by no means are these
exhaustive, we are thinking about at least these
four kind of key pillars around technology, data
and security in AI/ML. Effectively an L1 search, that's when you typically
have API model access to an inference provider. You have access to a database, you're typically executing
single step tasks, like in a retrieval
augmented search application. You're typically accessing
pre-trained models. When we talk to L2, that's when we're typically
executing multi-step tasks. We start bringing, introducing
concepts such as memory. That's when we start to
have a more important need for content moderation,
identity and authorization. And you're at the end of the day, executing a plan and a
workflow that is defined and using the model
really as a flow router to decide what is the right node and edge that the path should take for the model. L3 is really with orchestration. That's where we start to bring
in actual agentic frameworks to allow the model to imbue the model with multi-agent capabilities
and external tools. These tools are what allow the model to go from just executing based
on its own knowledge, it allows the interface of tools. And that's where we start hearing about model context protocol
and tool use within models. And that's where it becomes
more important to have secure runtime and
human-in-the-loop validation for specific tasks we're invoking. L4 and full autonomy
is when we start having self-improving agents
and models that can cross organizational boundaries. They have dynamic goals
where they can reoptimize at different steps during
long-running processes and they have access to
agent and tool registries to then access tools
dynamically on the fly. Jason, over to you. - [Jason] So now we wanna map
some of those capabilities and this maturity matrix back into our cybersecurity use cases. So if you look at the
kind of rough mapping, and again this is a, you know,
kind of a notional diagram and not fully exhaustive,
but it gives us an idea of how we can start
building out business value with generative AI in
our security operations in a staged process, right? We can start on the left-hand side, implement some quick wins with
a Level 1 search capabilities and move into workflows
orchestration on our way to reaching that Level 4 full autonomy,
which is kind of where, you know, I think everyone wants to go at the end of the day. And so if you look at some
of the use cases down there, you can start with things
like alert enrichment and intelligent log analysis, enterprise wide search for security logs and vulnerability prioritization
and mitigation techniques. And then you move along the maturity level and start building out
more complex workflows and orchestration pathways in the future. But let's describe how
each one of these work. I'll pass it back to Aaron. - [Aaron] Thanks, everyone. We're now gonna run through
each of the different levels and give a construct of
what this is defined as, and then a security example. So when we talk about L1 search, what we're really talking about is, again, search use cases like an
enterprise search example of using retrieval augmented generation to take an enterprise
corpus, retrieving from that and augmenting that based
on initial user question to do question answering. That typically takes the implementation of doing RAG and semantic search. You and then as an organization
typically have API access to an LLM with basic prompt
engineering on the backend for that solution and
read-only access and controls, and typically implement it
first in a pilot program that is then scaled out over time. As we're seeing here on the left side, this is Amazon Q for Business, this is one of the managed products to perform enterprise search. And we're just seeing
the application of that within that small demonstration. The application of that
insecurity though applied, over to Jason. - [Jason] Absolutely. So think about from a search standpoint, how powerful it would be in order to take your existing
security documentation and placing that into a
generative AI-based application. Being able to interface
via natural language with intuitive querying capabilities across multiple security
tools and services. You can simplify the access
to critical information and start building
contextual understanding. So one of the things that generative AI is exceptionally good at is
taking multiple data sources and starting to correlate
data across them. Generative AI is like search on steroids. You can find a ton of
information in what you thought was just a pile of just
nonsense very, very quickly. It's very good at finding
signal out of a lot of noise. So one of the things that this helps from a business perspective is helping to break down those silos by integrating disparate data sources from multiple locations. And that's gonna allow you to have seamless access into previously all this security information that's fragmented all over the place. - [Aaron] Now moving to
L2, as mentioned earlier, this is where we're doing workflows, where we're using AI in the model itself to orchestrate and reason through
connected nodes and edges, typically through directed acrylic graphs that help to find the paths for
these nodes, task and edges. Again, using the model
as a really a flow state rather just like what that
next step action should be. And this L2 workflow is
actually traditionally what 80% of today's use cases
actually are defined as, if we think about our roles
in a SOC as a tier one analyst doing investigation, we're typically following
a predefined path. And that's really because for the past, you know, 50 years or so for doing any type of
real business use case, we wanna go through a sequential process. But does that really
mean that's the future of business use case as an application? Here, we see an example of Bedrock Flows. This is one of the services
in Bedrock that allows you to create L2 workflows
for sequential paths where one state feeds into the next, and there could be branches depending on if certain
conditions are met. But again, you're using the
LLM and the model itself to go through specific tasks
and branch when needed. Now applied in the security context. - [Jason] So you can think about this from the perspective of threat
and vulnerability management. So this is a pretty standard workflow where you may have, you know, a static or dynamic code analysis tool that's going to feed you
various vulnerabilities that may be present
inside of your code base. Those can then be flowed into an automated remediation engine using and empowered by generative AI. So you can then take those remediations, they'll show in context code patches. The generative AI system
can tie all of those back with some natural language description of the changes that were made. It can suggest pull requests that can then go into your
source code control system. And of course, all of this is
going to be using, you know, detections or remediations in
line with AWS best practices. And you don't have to build this yourself. For example, we have in Amazon Inspector, the Lambda code scanning capability also comes with generative AI based and powered remediation
recommendations for you. So some of these things you
can certainly build yourselves and some of these are built-in features in some of the AWS Core Security services. - [Aaron] Thanks, Jason. Now in talking about L3
with multi-agent systems, this is where again, where we're executing these workflows within constrained systems and having an agent, a supervisor agent orchestrate and define
what that plan should be, plan being to execute subagents that have access to specific tools through a sequential system. And this is where we're having
an orchestration framework, whether you're using Bedrock
agents, Strands agents, LangGraph, et cetera, to hand off within specific workflows, use tools and APIs to
interact with other systems to imbue the model with
external knowledge and access. Typically as well too
that's where we want to have human-in-the-loop validation
for specific tasks and actions. In the image you're seeing on the right, this is a visual of an investment
assistant notional example that's showing as a
user submits a question, that investment assistant is reaching out to subagents from market
analysis, crypto analysis, pulling 10Ks. Each of these agents have specific tools that they can access to
do API calls effectively, pulling back financial information, whether that be from documents
from an external source, whether that be structured
time series data, and then synthesizing that together to formulate a final response to the user that ultimately is what gets presented. Over to Jason to talk
about the applied example. - [Jason] You bet. Thank you. And so when we think about sort
of that progression, right, we looked at the idea of
automated code remediation, making those suggestions. And now what we can do is augment that and put that into a larger framework and put that into our CI and CD pipelines. So if you think about kind of
taking that one point solution of taking vulnerabilities and suggesting remediation actions, now we can actually plug
that into our larger pipeline as part of an orchestration workflow. And so this is an example
of, for example, fine tuning and tailoring those AI responses, creating those pull requests automatically against CVE findings. And then those can be
reviewed either by humans, they could be, you know,
determined, you know, in an automated fashion as well inside of the continuous
integration pipeline. - [Aaron] Awesome. Now let's talk about L4, full autonomy. This is where we're trying to
have self-evolving systems, AI systems that can proactively
optimize and do innovation. Now, what does that
really mean in practice? Think about code assistance,
like Amazon Q Developer CLI. This is where a user
provides a high-level task. The agent itself that's running decides effectively what code to generate, or first decides the plan
to accomplish this task. The code then to generate and
reasoning through the response iteratively until that system is complete. That is then going in a loop with accessing tools like
file read operations, file writes, having shell
access to execute TAMs or use AWS to execute AWS CLI commands. It's not executing a defined path, it's executing actions based
on the tools it has access to. And again, self-healing as
it identifies new issues and constraints, replanning
over those with human input in terms of what the next
step action should be based on the output they find. So this is what we're thinking about when we think about full autonomy. Now obviously there's different levels of human input validation
we want to apply, and those will all change
during the business context and level of determinism we
need for the specific use case. Over to Jason to talk about
the applied example now. - [Jason] All right, thank you. So really where do we
see this going, right? Obviously, you know, we
wanna give a, you know, kind of a roadmap for
where we see, you know, where we are now today to
where we wanna be in the future with kind of this idea of full autonomy. So if we go to the next slide,
we can see here is an example of what we would see as
kind of a next generation multi-agent security operation center that's powered by generative AI agents. And really when we think about it, right, the generative AI is
doing all of the thinking, it's thinking about the next step to take, it's thinking about the orchestration that's going to happen. So it's going to take in the raw data from all of the standard
AWS security services, could be third-party security services. All that raw data is then ingested in. And you can see, for example,
taking in also things from threat intelligence. You can see also how it can go through and maybe do alert triage through pulling findings
from security hub. And so all of these things
are gonna be orchestrated by a set of agents, right? And so it still requires
the well-architected pillars of the security frameworks. It requires all of those
basic information sources that you have from your
current security operations. But now what we're seeing is this ability to build these agents, these sub-agents on the right-hand side, which are going to take in those as input and provide a set of insights. And those insights can then be fed into larger orchestration agents, which can then decide the
next step in a plan, right? If it receives, let's say a
set of threat intelligence, that includes indicators of compromise, and you need to go ahead
and start adding those rules into say, your firewall
manager, for example. You can have the SOC
director agent go through, think about what needs to happen next depending on the urgency of those threat intelligence
reports that you're getting, maybe correlating that with logs and other sources of information you have in your own environment, and even contextual clues
such as what's the industry that that threat intelligence
report is related to? Is it related to your own
industry or a different industry? So you can think about all of those things that are decisions that you
would make as a human analyst and now you can start
delegating some of that into the generative AI systems, right? And so at the end of the
day, you have these agents and you kind of get to decide where you want that risk
management threshold to be when it comes to where
humans come into the loop. I gave you the example
of adding a firewall rule based on incoming threat intelligence. That may be, you know, an
applicable, you know, use case for your particular organization, right? That may be the risk level
that you deem acceptable because you're going to prioritize protecting against known
threats as quickly as possible over the potential for
having an availability issue for some of your customers in case that threat
intelligence was faulty. You may have different
decisions that you make in terms of let's say
delegating the decision to automatically quarantine workloads in the case of a suspected compromise. And so in that case,
maybe a human-in-the-loop would be invoked to take any
actions that could impede your application's availability depending on its sensitivity. So these are all kind of the concepts that you're gonna think about. As you move down the maturity matrix, you start with search and so forth. And if we go to the next slide, we can see exactly how you
can start building that out in this example roadmap, right? This is just kind of an
example that you can use and tweak for your own use
cases where you can see, okay, I'm gonna start on the left-hand side, get my feet wet with this
generative AI technology, starting with those search-type features. I can take some of those, you
know, documents that I have for my SOC, I can take some of the existing
security findings that I have in my security organization and start using those search
features built into gen AI and LLMs to start building insights and getting comfortable with
the technology, the use cases, its great strengths and
potentially some of the weaknesses. And so as you become
more comfortable with it, you start adding in that L2 and that L3, going from the workflows
into the orchestrations. And really at the end of the day, something like 80% of the
work that is done by your SOC is going to be using
those fixed workflows. And so you can see immediately how even at those intermediate levels of adopting generative AI, you can start making a real impact on how your security organization, giving them a lot more productivity gains, and so you can get a lot more activity out of your very, very expensive analysts and really just highlighting
the things that need human insight instead
of having to make humans go through a bunch of tedious work. Things that are already
defined as workflows can be defined instead
now as code workflows for your regenerative AI agents. And so you can see on that timeline, we move all the way from left to right, and even as we increase our capabilities from level one to level four, we continually also increase the scale of our existing
investments, right? So this is a way that you
can kind of think about this holistically for your organization and start prioritizing
some of those use cases so that you feel like you
are making step functions along the timeline and not feeling like you're kind of going from zero to a hundred all at once. So with that in mind, I'd like
to introduce up to the stage my friend Martin from Trellix and he's gonna talk
about some of this stuff actually in practice. - [Matin] All right. Thanks, Jason. All right, I'm on a different mic. Can everybody hear me okay? Good? All right, awesome. Alright, thanks. So yeah, I'm Martin Holste, I'm the CTO for Cloud and AI
at Trellix, and you just saw a lot about the building
blocks and the process that goes into how you
actually do something with AI. I'm gonna show you what
we've been doing with it, and I think it's pretty fun. Alright, so before I get into it too far, I'm gonna do something a little bit fun. Raise your hand if you
have a really good idea of what agentic AI is and how it works. Okay, I'm gonna say that's
about 15% about, right? Okay, so my buddy Claude
and I put this together. I don't know how to do any
3D coding and that's okay. I had an idea because
when I talked with people, they didn't really know
what agentic AI was over the last few months. And you see that list of
things, GuardDuty, Security Hub, there's some Trellix stuff on there, and then there's some random
things like an HR System. So these are all tools in a toolbox and we're gonna talk about that. But I think one of the
best ways to see this is when we actually look at
what this means visually. So let's imagine that we've got a scenario where we have something
like GuardDuty alerts. We have something like Security Hub, which you saw some updates on yesterday. We have Security Lake that
stores a lot of data in it. And our goal is to update verified access to change a privilege level
based on somebody's risk score. We're gonna combine AWS with
some of our Trellix stuff. And then you're also gonna
see how we can combine that with just random data
that we have lying around. You heard earlier from
Jason how important that is to be able to use AI to
bring all this together. So we call our stuff Trellix Wise. That's why you're gonna see this owl guy. It's kind of fun. This was a fun coating project because the owl didn't look
like an owl when I first started and I said, "Claude, can you make this
a little bit more owly?" And it's like, sure, here you go. So I'm not sure exactly
how well it does as an owl, but the illustration here
is that it's working on data in that upper left, and don't
worry about what the data is, just understand that as
it goes to each tool, it's reading in JSON. So it's gonna read in all
the different things and say, alright, now that I have this information, which tool in my toolbox
should I go to next? And so at each moment,
it's gonna go and say, well, I'm looking at this
threat from GuardDuty, so I'm gonna go find some
Network Flows over here. So it goes over to our
Network product, right? So it's at each phase,
considering what it's got and then making a
decision what to do next. And this is what's so
important and so different about agentic is that this
is a non-deterministic flow. So it's given a goal
and it's given a toolbox and we're gonna cover
exactly what that looks like. But at all times, it's going
back to Bedrock to say, okay, now that I have this information,
what should I do next? I'm gonna make this decision. And it's building its
story with data as it goes. And finally, it goes to
verified access and says, "I need to update the
risk score for this user because I saw some interesting alerts. And what's important here is that it's not turning
something on or off. It's got the level of nuance where it can write up its
entire decision and say, "Here's what I found. Here's why I think this,"
in a very plain format, and say, "This is why I'm
adjusting the user's risk score and therefore with verified access, what they actually have access to." So we're not disabling user,
we're not quarantining a user, we're simply updating
what they have access to based on some suspicious
things that happened. And you have a full documented writeup on exactly what happened that can go into your
ticketing system, et cetera. So this is a fun way to look
at essentially the boring stuff that's happening behind the scenes that I'm gonna walk through. So I used to run a SOC
for a very long time, and this is the kind of
stuff that we'd walk into on a Monday morning and it would be, okay, how many critical alerts do I have? Zero critical alerts, okay,
we can work on other stuff. And what's really sad is,
I've been working in security for a long time and I
know just how hard it is to go out there and write
detection content to say, I'm gonna write a rule that does this. I'm gonna write an
analytic that does this. So working with those teams
that build all this content and customers that pay
for all this content to then see nobody look at that
content, it breaks my heart. So what I'm really happy
with is now with AI, we're able to actually
evaluate all of those alerts. And I'll tell you, the
really good bad guys, they're not setting off
any critical alerts. They're hiding in all
those low level alerts and humans don't have
enough time to look at them. So that's really what
we're addressing here. Now, if you look at any
one product out there, it's gonna have a pretty limited
view on what's happening. You need full context to see everything. So if you take a network alert and you say, "What can
I do with this in AI?" The best you can do with
just a network alert is really to summarize it, maybe put in a little different way, might be able to enrich it a little bit, but you're not gonna be able
to do a full investigation with any of this. To do that, you need full context. You have to bring in all the stuff that I showed you in that 3D thing. You have to go out, collect
this information, bring it back, and then figure out what happened. If you're just looking at one tool, it's gonna have a very limited view. So this is really the key thing, is that each one of these tools has access to just what it can look at. A network tool is looking
at network packets. It's doing the best job, making the best decision
on just network packets. So back to my idea of critical. For something to be so critical that it's entirely available
in just network packets, that's very rare. You often need to know, okay, well, what did the user do next, right? What happened on their
system after that happened? So it's really important
to put all of that together to understand what's going on. So we're gonna go into
exactly how we're using this, but here, I'm gonna give
you a quick crash course in what it means to actually
work with agentic AI. This is a really important piece of this. So we've all been trying to be
good prompt engineers lately, but this is a super important piece. So this is your overall prompt structure. And I mentioned earlier with agentic AI, the idea is you're giving it a goal. And the way that I like to think of this is you are onboarding an employee that is going to be there
for about 15 seconds, and you have to give
them what their job is, what the company policies
are, all that stuff. That's what you're doing, is you're giving a list of instructions 'cause that AI employee is
gonna be gone in 15 seconds and they have to just based
on what you told them, do their entire job. And that's actually pretty difficult, if you don't use a good framework for it. My other little tip here is use ordinals. So use 1, 2, 3, 4, be really specific on exactly what steps it should take and you'll get very consistent output. This is another thing that
we've learned over the years working with gen AI, that
it's not hard to do that, but once you know that's the concept, that you get much better output
to do that kind of stuff. But you start with the goal,
you give it the framework, you tell it how you
want that return format. And when you're working with tools, that's actually done for you, we'll get into that a little bit later. Then you give it some
warnings and guidance. Say, "Oh by the way, don't do this. This didn't work last time." Again, this is an employee
that you have for 15 seconds. What do you wanna tell them
that the last employee you had for 15 seconds learned, right? You need to communicate that back to them. Then, once you've outlined
everything that's gonna happen, you dump all the raw information and that's where all the network telemetry and all the other things come in. So that's the overall format. Now, the way that we do this is to start with classifying
the alert that's coming in to decide what to do next. So we essentially have a framework that will give a very
specific multiple choice test to the LLM. We say, "Okay, based on this alert, which category most
applies to this alert?" And we don't say, hey, pick a category, or we don't say come up
with your own category, we have a specific list. Here's another really
important general tip for coding in ai. Don't have it come up with things, have it pick from a list. You'll get very consistent results. This is a really important piece to this. So in our guidance framework, we don't ask for it to just
go out and invent something. That's when you run into hallucinations, you run into problems. What you wanna do is say, "Here's what we know,
which is closest to this?" You're gonna get a defined
outcome when you do that, and that's what's so important. So we have sort of a
tiered system for this where we go through and say,
"Alright, pick a category, then pick your common
foundational investigations. Is this a network flow? Is it host based? What are we looking at here?" And then get into the specific categories. Is there a specific product involved? Okay, well, bring in those
investigations as well. And so we use this to build a series of high-level questions. And we've actually been doing
this for a really long time, and generative AI has made this so much
more valuable for us. We've been building out
these high-level questions that we convert into data
lake queries for a long time. And we thought that this was gonna be something that changed the
entire security industry. We did this about 10 years ago. And then, we put it out to
market and we looked at it and customers used it a
little bit, but not very much and we couldn't figure out
why they weren't using it. And then it occurred to us. You have to actually read
the output from all of this. And so that was kind of
a bummer for a while. But then, gen AI came out
and we instantly realized we could use this to have
gen AI read the output and suddenly a solution was born. So now we go through every
single alert that comes through and we ask questions like this. And these are the high-level
questions that get translated into data lake queries that
go through and figure out, okay, based on the raw information, is the user currently traveling? Do they do password resets? Do they have an executive assistant they might be sharing a password with? What level of access does this user have? These are all the kinds
of questions that you ask when you get an analytic
alert like geo-infeasibility because we spend a lot of time and money on putting a whole bunch
of data in one place and doing some really
hardcore analytics on it. And then most of those
alerts just sit there because when you get an login anomaly, that's not that bad, right? There's a hundred of those a day, maybe a thousand of those a day. How do you know which ones matter? You have to ask all these questions. And we don't have time to do that, but thankfully, Bedrock does, so that's where it comes in. So now that you've seen how
important this context is and you see exactly what
those flows look like, let's dive in. So we have this concept of
the toolbox and the goal. Now, think about how different this is than a playbook, right? That's the key difference between
agentic AI and a playbook. A playbook is a script. It says, "I'm gonna start here, I'm gonna hope this works out and then I'm gonna end down here." And if anything goes wrong
during that playbook, chances are you're not gonna
get the outcome that you want. What's so different about agentic AI is that while you start in
the same place with this goal, it uses those tools as the data comes in to make its decision about
which path it's gonna go. So with that 3D animation,
it was a good example of how it can pick which
thing it's gonna go to to grab that information. It's not scripted, it's
making its own decision, which means it's super adaptable to any situation that it encounters. And yeah, if you don't
have all the right data, it might come up short. And that's actually something that we do, is measure the response that we get. And I'll show you some
examples here in a little bit. We look at those outputs to
see if they're good enough to give to the human. So here's what a specific
example looks like. If you guys worked in a SOC, you know this happens all the time, you get a domain intel hit. Now, why is this not a
big deal most of the time? If you have a DNS server that you run and somebody queries your
DNS server for a domain that has an intel hit on it,
then you get an alert for it. But that's not really an actionable thing. So the vast majority of domain intel hits that come from a DNS server are something that no one should look at. But how do you know if it's
the one you should look at? And so this is the process
that the agents go through. So the first thing is they say, "Alright, what tools in the toolbox do I have that can help with an intel hit itself?" And in our case it says, "Oh, okay, let me go find out what threat actor is attached to this intel." And then from here, something
really cool happens. We can use the gen AI to say, "This is what the threat
actor looks like." And it works at a human level, so it says, "Okay, well, what would it feel like if this threat actor were
actually in the environment?" And here, we get into scientific method because it essentially is
building a hypothesis that says, "Alright, this is attached loosely to a specific threat actor. Alright, let's pretend that
threat actor were here. What would it look like if the threat actor were
actually in the environment? What kinds of information would I need?" And again, the agents
are doing all of this, and it's get that goal at the top. Does this thing matter? Yes or no? So the first thing I'll say,
well, who else has seen this? I'll go check EDR to find out do we have any command
lines that match up? And then here's the other cool part. So we work with a ton of, pretty much everybody here
is one of our partners. And so you see all those
little logos down there. We have 500 plus
integrations with everybody 'cause we learned early on that to make our customers successful at figuring out what's happening, you're gonna need data from everywhere. So that might mean vulnerability
management information. So Tenable's a great partner of ours, so we share asset information with them. So this now can figure out,
oh, I have asset information. I can go and see what the risk level was for this particular user. Again, as long as you describe
what data is available, it's a tool in the toolbox
and the gen AI will figure out which things to use and
put it all together. 'Cause keep in mind, this
stuff has already been trained in the MITRE ATT&CK Framework, and we'll walk through
that exactly how that goes. So we do two phases with gen AI. And this is why Bedrock is
such a big deal for this. We use the right tool for the right job when it comes to models, and I'll go through how
we select the models in a little bit, but we have
two different model selections. We use Amazon Nova upfront to figure out which questions
best apply to this given alert so that if a customer
creates their own alert, we will apply the right
investigation to it. And actually something that's really cool, a customer can create their
own alert that goes in that might be on some random
thing, like I wanna know anytime this user logs in. In the description of that custom alert, they can put in the
instructions to have the AI take those actions when it comes in. So because it's completely
dynamically generated like that by Nova, we can handle all of that stuff. So that just generates the
questions for the data lakes. It goes out to the data lakes, retrieves all the information. That's step one. After that, now we use
Sonnet, which is super good and I'll show you just how good it is at analyzing that full content. So notice we had two different models doing two different jobs, and that's really important to this. So Sonnet will go through, read
through all the information and decide does this
matter to you? Yes or no? And what's so critical about this is this is not just writing a summary and dumping it on someone's desk, it's actually making a decision. We are trusting the AI to
actually make a decision. And you can audit the whole thing, which is a really important part of this. And you can transparently see exactly what data it was working
with, all of those things. But the fact is it's
going to do work for you, not just the analysis. It's also going to make the decision about is this in that top 10 alerts that matters for the day? As in you probably have time as an analyst to get through 10 alerts in one day for a real investigation? Is this one of those 10? Or is it in the other
pile of a thousand alerts that don't really matter today? So this is the kind of
output that we work with. And don't worry if you can't
see the individual text, that's not a big deal. The point is that it's
doing a complete writeup on everything that's happening. And you can see all the different agents that are being pulled in by
the story that it's telling you in the data that it's describing. So the first thing is kind of funny. This is from our demo
environment and the AI knows it's in a demo environment, so you get kind of a matrix
moment where it says, "I noticed this is a demo user, so we're probably in a demo environment, but just for kicks, we're
gonna keep going with this," and it keeps going through. And fun weekend read,
check out the model card for Anthropic's Claude, there's some really
interesting stuff in there for understanding just how
LLMs work, how they think because they understand the
environment that they're in and they make different decisions based on the environment that they're in. So there's a whole other topic we don't have time to get into today, but definitely worth a look. Secondly, it's gonna say,
alright, what's the IP address that we're dealing with here? That says it's a 10. Okay, this thing
understands RFC 1918 space. It knows what an internal address is and it knows that's role. So that might seem like a small thing, but think about this
when we get to the end in the orchestration, it knows
internal versus external. So when it says this should be quarantined and this should be blocked, it knows exactly which IP is
which and what to do there. Next, it says we're looking at certutil. Okay, well, that's a
legitimate Windows tool. We didn't tell it it's a
legitimate Windows tool. It's pre-trained on that,
it already knew that. It already knows the
MITRE ATT&CK framework. It understands threat
models, it knows all of this. We're telling it the
tactical information it needs to make a good decision. So it knows it's a Windows tool, but it's pointing out it
could be used by attackers. So it's not a free pass just
because it's a Windows file. So now it's putting all this data together and describing it in essay
form exactly what happened. These write-ups are so good
that we're finding customers are using these to train
up their level one analysts into level two analysts. We're finding that these
are just incredibly detailed and it's on every single alert. So this is the power of having something that doesn't get bored. It will go through all of this information with a fine tooth comb because while it might
be a low-level alert, this might be that one
day where a bad guy got in and you need to find them right away 'cause you're down to about 90 seconds before they ransom your
entire environment. That's what we're dealing with here. So as it goes through all this, it'll say, "Okay, well, I need to know
if this object is malicious." So now it's gonna say,
little selfish plug here, it goes to our sandbox and says, "Alright, IVX, is this thing good or bad? Oh it's bad, okay, how did it get here? Now we need to find out
where the flows are from." So it goes and finds those. It could go to Security
Lake and figure out what VPC flow logs apply to this. Then it needs to know more
about this particular intel, so it says, "Oh, I've
got a tool over here. I'm gonna go pull the intel. Now I know this is malicious. I know who talked to it, and I know what this attacker
looks like in environment. I better tell someone right away." So it's saying, "Okay,
we got full evidence that this thing was executed successfully and this thing's gotta be critical, somebody's gotta look at it right now," and then it'll even go on to all the recommended
actions that come next, which is super important
because you can on day one that you set this up, read
through the recommended actions, make sure you agree
with them, and then say, "Yep, from now on, I want you
to automatically do this." And because it's spelling
out exactly what it's doing, you instantly build that
confidence that yes, I agree with what you're
doing, we're good to go. Now, here's just how good this gets. This is actually about six months old and when I first saw this, I
almost fell out of my chair because I've never seen anything
that could ever do this. And I have moments like
that on a monthly basis at this point with AI because
it's moving so quickly. But here's what I want you to understand. You can write a script
that decodes Base64. We did not tell it explicitly
to decode the Base64. We told it to make sure you understand the commands that are being run. So if it's any other kind of encoding, it would also decode this. Now, here's the really magical part. Not only did it automatically decode what was in that command, it
has read the entire internet, so it's read our partner
Tenable's documentation on what their tool is supposed to do and it knows the exact
parameters in that API call, and it matched the decoded content up with what those parameters were to make sure that the
payload in this Base64 was exactly what it should be. And this is something that we as a society have never had before. Anything that could do
that level of reasoning with that level of knowledge
in one context window has never happened before. So for you guys, you need to be thinking, how can I put more information into this? 'Cause I want this thing
making a lot more decisions because when you start
seeing how good at it is, you start to realize that our job is now to just feed the beast, get
as much stuff into this thing as we can because this thing is gonna do all that hardcore analysis for us. We don't have to sit there and write 30 million different Python scripts for every different thing that can happen. That's what's so valuable on this. Okay, so what if it made a
decision you don't agree with? We have two different ways
that we've approached this, and this came directly from customers. So one thing I didn't mention, we've been doing this
for a year and a half, so we've learned a ton
through all of this process. We've been doing the agentic stuff basically since it was available, I would say honestly about six months ago. You could technically
do agentic before that, but we've learned a lot. And one of the things that
customers told us was, "Hey, sometimes it escalates
things that we don't want. And you know, it did its best, it just didn't know something." So here's the first thing that we do. Instead of giving an analysis
a thumbs up or thumbs down, we realized we could just go
through the old case notes from the customer picks
the timeline, by default, it's the last 24 hours,
read through all the cases that they closed in the last 24 hours, read through all the notes
that they put in them and then create guidance for the next day. So all of the stuff you're
seeing there is AI generated, reading through human
case notes to figure out what are the human preferences? What are the actual human analysts saying that I need to pay attention to? And critically, it's
saying this is guidance. So I use that word likely
very specifically here. It's not building rules that
are hard and fast and brittle. It's building guidance. So if the evidence that
it's looking at outweighs what happened yesterday because the situation's
a little bit different, it's not gonna make a bad decision. If an analyst makes a mistake
and they put in something that's not very good in the case notes, it's not gonna blow up your entire thing. It's using all of this as part
of the guidance and evidence and weighing it all equally. And that's super important because the second you start
to do things like pre-training, which I'll talk about in a minute, you start to run into problems because it puts too much
weight on something. Now, the second way that we can do this is a little bit more explicitly. You might know day one, hey, there's certain things
I want this thing to know. So here is a use case from
a customer that we had, and they were getting a lot
of escalations on analytics that didn't really matter
for them specifically. And back to the, you
know, breaking my heart when people turn stuff off, they said, "Well, should we just
turn off the analytic?" And they said, "Well,
you're using, you know Salesforce as your SSO, right?" I said, "Yeah, well, you
probably still wanna know why isn't it working?" They said, "Well, we have
people log in from everywhere and that's kind of weird for Salesforce." And we said, "Okay,
just tell the AI that." So we didn't mention
anything about Salesforce, we didn't mention
anything about analytics. We just gave the AI
information it couldn't get out of the telemetry, was that
they have people logging in from all over the world. That one sentence, look
at the cases dropped just that handful you'd expect each day. So you can do that
explicit tuning this way. And the key is you're not going to every little security
tool and tweaking a knob, you're just saying what you want. And this is kind of the big deal, is you get all the information in there, and then instead of going to all your different security tools and worrying about how they operate, you just make it really specific and say, "Alright, dump all the
information in there as a clearinghouse," and I'm gonna go say, "Here's what we expect,
here's what we want the most. Here's what to look out for." Again, back to that
prompt framework, right? This is where all of
this starts to come in, it's way more effective. Alright, we did a joint
blog post last year. You could see that the bottom there. So if you want a closer
look at this, no problem. We have a bunch of
content out on trellix.com that'll point at this as well,
if you want the specifics. But the point is that you
can't just grab a random model and then hope it works,
and you can't just look at random benchmarks that are out there. So you'll see a lot of coding benchmarks and like math benchmarks for models. That's probably not gonna work
for your specific use case. So one other tip I have
for you just in general about working with AI is you
need a proper QA framework, and there's a lot of ways to do that, but really a system for
benchmarking your specific use case because there's a new model every week and you wanna make sure that you're using the best model for the job 'cause there's a huge price difference, and I'm gonna show you in a second. But see Nova Micro up there? It's a hundred times cheaper than some of the other models on there. So if Nova Micro could do the job, you definitely wanna use Nova Micro. So it's absolutely worth a day or two putting together a program to figure out can I use something like
Nova Micro to do this? Or do I have to go and
use a different model? And you need to know how good it is at it. And the other thing that
you're gonna have to mention to the engineers, you
can't just run one test and then say, "Oh yeah, I
passed the test, we're good," because it's non-deterministic. Anything you do in Gen AI
as a testing framework, you have to do at least 10 times to make sure you get enough samples to see that this thing is truly working. So that's my other tip for you. It's not QA like you're used to, it's not benchmarking like you're used to. You gotta run a lot of samples through it to really understand what it's doing, and you're gonna see some
very big differences. So we have another benchmark that we use. It's similar to that one. We make it a little bit simpler though. And so you saw that Base64 decoding. So part of our evaluation framework is its ability to understand
what it's decoded. And in these cases, and this is a little bit older slide here, but you can see the green
there is when it's able to do that proper decoding on certain alerts. But this is a good layout. And the one to watch out
for there is the dark red 'cause those are hallucinations. And so you can tell
right away which models are not gonna do the job for you and are gonna be actually
counterproductive to run, and the other ones that you
can trust a whole lot more. So this is a big part of the process, understanding given our current prompts, and you can also do the same
process to keep the same model but switch out your prompts, what's gonna actually perform
the best and how do I know? You need to set that for
your own specific use case to figure that part out. So now I'm gonna walk
through really quickly the specific nuances between these models because I don't think this
gets called out often enough to understand, okay,
just how good is a model? When we say this model's
better than another one, what does that really mean
from a business use case? So we talked about the
Base64 decoding, right? So in this case, Sonnet 3.5
V2 was not only decoding it, it's understanding what's
in the decoded material, and understands that
this is a Windows update. Further, it understands that
there's other Windows event IDs that would be associated
with that particular thing. So you can see just how good it is at understanding what's happening. And look at that statement. This appears to be
legitimate MDM automation. It understands the concept
of managing devices. So it's understanding that and applying one command
line for that whole thing. It's operating at a
human level conceptually, it's putting concepts
together, not bits and bytes, and that's what's so
critical about all this. So it understands, in this case it was an
alert with AirWatch. It knows that AirWatch is an MDM. It knows what these Windows events are, and it understands that
the decoded content fits that use case perfectly. That's the level of analysis
that it can do, all right? Well let's check out Llama 3.1. Again, this is a little bit older. I use yellow here because it's not wrong, but it didn't go in a deep dive. It didn't go to that extent. And it calls out that, yeah, It looks like a PowerShell script with a Base64-encoded string. Could be a sign of malicious activity. I don't know, you'll have to
go ask someone else, right? So this is where the different models doing different jobs comes in. Some of them could do that,
some of them could not. Micro does a pretty good job
at a very good price point at a very fast speed, but again, it's not doing that full Base64 thing, but it notices that yeah,
there are Base64 in here. That could be a bad thing. So maybe you can use that as a first pass, and then if it detects something
that it wants to punt up to a larger model, you can do it that way. And I call this model tiering, we'll talk about that in a little bit, but this is a really
strong use case for that. But I just really wanna call this out. It's such a big deal to know that one is a hundred times
cheaper than the other. And it's not just from a cost perspective. It opens up so many more use cases to know that there are
cheaper models out there. And so to say, "Oh, well, we
can not normally do this," to say, "Well, now we can inspect every single event that comes through. We can look at all these different angles because before, it was cost prohibitive." That's a really big deal for this. So there's a couple of
ways that you can make a smaller model perform
like a bigger model. One of my favorites is
the best-of-n attempts. Basically you run the same
prompt three or four times or more and then you take the best result. So even if you run it 10 times and it's a hundred times cheaper, that's still 10 times cheaper, right? So that's a great way to get
some really good results. If it's a kind of a medium-sized model, maybe run it two or three times. And with caching and things like that, this can actually become pretty cheap. So you have to be
careful with the caching, play around with it because
if you're caching it, then obviously you're gonna
get the same response. You can cache different parts of it. That's a whole other topic, but know that there's a lot
of tricks that you can do. So the high-level thing here
is if a project looks like it's gonna be too
expensive to do with this, there may be some tricks that you can make this cost effective. Then, there's distillation. What if you want that smaller model to have some of the knowledge
that I talked about? So like what is an MDM? Maybe your tiny model
doesn't know what an MDM is. You can distill a model and
put that information in it. That's a great way to
get it to perform better for your specific use case. And then the one I showed
earlier is tiering. And I think this is
probably the most popular and easiest one to use,
which is do a first pass with the little model and then punt it up to the bigger model if it passes that first test. So you can kind of do
that overall tiering, and there's so many
different ways to do that, but that's a great pattern to go with. And then I wanna talk about
bias and responsibility. So for two reasons, we don't train models. One is privacy. It's super important to our customers. We wanna make sure there
is absolutely no way, whether explicitly or implicitly, that a decision one customer makes is gonna impact another customer. So the models are read-only, we wanna make sure that happens. So that's the biggest
reason we don't do it. But then we found out because of privacy, that actually it's much better
not to fine tune your models. Never put customer data in
there because you want the LLMs to sit on top of all the other decisions that were made at the machine level. So if you know something
is bad for everybody, put that in a security rule. Don't tell the LLM. The LLM is basically filtering out the most important rules at the end. And then lastly, I just wanted to call out that you can put this in
an end to end workflow with GuardDuty, as you saw with the owl, being able to go out, check a sandbox, then do that full analysis
with every tool that it's got, and then it can go out and do
remediation at the end of it. This fits into pretty much
any different scenario. Alright, with that, I'll
bring up Jason there. - [Jason] Awesome. Thank you, Martin. So just a couple of
concluding thoughts real quick as we come to the end of our hour. You know, as Martin described, right, AWS core security services are still the solutions that generate those insights that will be, you know, pushed into your generative
AI decision making engines, start kind of building
all of those decisions, understanding what the impact
of some of those findings are, all that kind of good stuff. And of course, to build what you know, Martin just described,
they're using abstractions, such as MCP, Model Context Protocol, so you can start abstracting
out the complexity of the tool configuration,
the integrations, and all of those pieces. And so that allows those agents, those generative AI-powered agents to perform tool selection
and API parameter generation. And finally, you wanna make
sure you document everything in a case engine so that you understand what decisions were made at what times. And with that, thank you
so much for attending. Don't forget to go ahead and
fill out the survey in your app and have a great day here in Philadelphia. Thank you.
