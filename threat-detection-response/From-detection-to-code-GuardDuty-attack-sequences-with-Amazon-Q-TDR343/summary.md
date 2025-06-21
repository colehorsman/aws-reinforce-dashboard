# AWS re:Inforce 2025 - From detection to code: GuardDuty attack sequences with Amazon Q (TDR343)

**Video Link:** [Watch on YouTube](https://www.youtube.com/watch?v=9CyvdkBLTDg)

## Video Information
- **Author:** AWS Events
- **Duration:** 56.0 minutes
- **Word Count:** 9,320 words
- **Publish Date:** 20250620
- **Video ID:** 9CyvdkBLTDg

## Summary
This session explores how **Amazon GuardDuty's new Extended Threat Detection** and **Amazon Q Developer** can be used together to accelerate threat simulation, detection, and incident response. The speakers demonstrate how Q Developer enables non-developers to generate test environments, simulate realistic attacks, and automatically create remediation playbooks using generative AI. GuardDuty’s new attack sequence findings correlate multiple events into a single narrative, making threat detection and response more contextual and efficient. The talk includes several live demos of GuardDuty Tester, Q CLI, and VS Code integrations, culminating in an end-to-end workflow that automatically builds and documents an incident response framework for EKS attack sequences using AI.

## Key Points
- **GuardDuty Overview**:
  - Ingests foundational sources: CloudTrail, VPC flow logs, DNS logs
  - Adds optional sources: S3 data events, EKS audit logs, Lambda network activity, EC2/ECS/EKS runtime monitoring, and malware scans on EBS/S3

- **Extended Threat Detection (ETD)**:
  - New GuardDuty feature that correlates multiple findings into a single "attack sequence"
  - Supports IAM credential compromise, S3 data exfiltration, and (new) EKS cluster compromises
  - No additional cost or config for customers

- **GuardDuty Tester**:
  - Open-source CDK project to simulate realistic GuardDuty findings
  - Supports EC2, EKS, and attack sequence simulations
  - Helpful for tabletop exercises and testing automation workflows

- **Amazon Q Developer**:
  - Uses generative AI to automate remediation tasks, build incident response templates, write tests, and generate documentation
  - Can create Lambda functions, CloudFormation templates, Markdown docs, architecture diagrams, and Kubernetes policies
  - Supports natural-language prompts, VS Code integration, CLI usage, and identity-aware workflows via AWS IAM Identity Center

- **Security Automation with Q**:
  - Automatically generates Security Hub custom actions and EventBridge rules for new GuardDuty finding types
  - Builds EKS response playbooks with Kubernetes manifests, IAM roles, Lambda remediation code, and isolation policies
  - Offers dynamic interaction, correction, and improvement based on real-time errors

- **Developer Workflow Use Case**:
  - Demonstrates detecting and fixing Log4j vulnerabilities in Java code using Q inside VS Code
  - Q can scan code, highlight insecure dependencies, offer inline fixes, and provide markdown explanations
  - Integrates with Git, helps manage secure code reviews, and generates remediation diffs

- **Agentic Approach to IR**:
  - Q CLI session state persists across prompts for context-aware workflows
  - Q builds layered responses: detection → orchestration → remediation → documentation
  - Enables SOC teams to generate tailored playbooks across AWS and Kubernetes environments

## Technical Details
- **GuardDuty**:
  - Extended Threat Detection creates high-context "attack sequences" instead of isolated findings
  - Findings integrate with Security Hub, EventBridge, and Amazon Detective

- **GuardDuty Tester**:
  - CDK-based deployment creates EC2, EKS, Lambda resources to simulate attacks
  - Can trigger specific types of findings (e.g., S3 exfil, EC2 crypto mining, EKS compromise)

- **Amazon Q Developer / CLI**:
  - Can generate:
    - Architecture diagrams (via Mermaid in markdown)
    - CloudFormation YAML for remediation infrastructure
    - Lambda functions with built-in IAM roles and SSM config
    - Kubernetes manifests for network/pod security policies
    - Markdown documentation and IR guides
  - Identity-aware via AWS IAM Identity Center
  - Supports model selection (Claude 3.7 / 4 Sonnet), contextual memory, file access confirmation
  - CLI session persists context unless exited

- **Security Hub Integration**:
  - Q can create Security Hub custom actions and EventBridge rules to automate remediation
  - CloudFormation templates are generated with proper IAM roles, least privilege by default
  - SNS notifications, Lambda triggers, and forensics hooks included in templates

- **Developer Fix Flow Example**:
  - Q identifies vulnerable dependencies (e.g., Log4j 2.14.1), suggests upgrade (e.g., 2.17.1)
  - Inline code suggestions (⌘+I in VS Code) update dependencies
  - Multi-file scans and markdown explanations help devs resolve issues efficiently

- **Security Best Practices**:
  - Q prefers least privilege and secure patterns even when instructed otherwise
  - Non-deterministic: responses may vary across sessions, especially with broad prompts
  - Contextual prompts yield better results than prescriptive commands

- **Useful Resources**:
  - GuardDuty Tester GitHub Repo
  - Q Developer documentation
  - EventBridge + Security Hub automation guides
  - Amazon Q CLI help docs

## Full Transcript

- [Marshall] A little caveat about this. Pratima and I, we're not
developers. We're security people. But ultimately one of
kinda my day jobs at AWS as a specialist SA is to
create a demo environment and have a ready-to-go demo environment for the generalist SAs out there, the security SAs around the world. So that involves creating
tons of resources and breaking things and
creating GuardDuty findings. And frankly, that took a lot
of time a couple years ago. We've been able to speed a lot
of that up with Q Developer. So we're gonna go through
some of that today. Also, talk about why you would do it. Talk about, you know, how
can you do remediation and how, as a security professional, even if you're not a
developer, like ourselves, you can use some of this technology to create better outcomes in your role. So if you are a developer, please don't cringe or yell
at me when I do weird things that are probably not best practices. So first we're gonna start
with a service overview. What are the different services that we're gonna be talking about? Hopefully everyone's somewhat aware, but let's talk about it a little bit more. How can you configure Q
Developer, pretty straightforward. And then we're gonna walk
through demos most of the time. It's gonna be GuardDuty finding creations, remediation walkthrough. I forgot to update the agenda,
but we're gonna go through some vulnerability
recommendations and remediations. And then we'll talk about key takeaways. After that we're gonna go to Herschel's and get pastrami Rachel's,
which are amazing. Okay, so let's get started with GuardDuty is the first thing we're gonna talk about. If you're not too familiar with GuardDuty, it's AWS threat detection service. It does a couple different things. So at a foundational layer, we collect data from AWS environments. So what we call our foundational
data sources is CloudTrail, VPC flow logs, and DNS logs. We collect this service
to service communication. So it's not anything a
customer has to turn on in their environment. Whether you have five, 50, 5,000 accounts, it doesn't really matter. We collect all this data and abstract that heavy
lifting from the customer. Over the years, we've expanded
into more data sources. More data sources, the more we can detect, the more insight we
have into an environment to understand where
threats might be happening. So where we've expanded
to is S3 data events. So we can see the reads
and rights of S3 data and see when there might
be malicious activity. EKS audit logs, that's the
control plane level activity for Amazon Elastic Kubernetes Service. Amazon Aurora login events,
Lambda network activity. And then we have runtime
activity as well for EC2, EKS and ECS, the Elastic
Container Service from AWS. And then we also have the
ability to scan for malware and EBS volumes as well
as S3 where, you know, a lot of customers might have an S3 bucket where they have untrusted uploads and they need to verify that those files don't have malware in
them before they move them into their application workflow. We create findings based on
either threat intelligence and machine learning and then integrate these
finding capabilities or these findings into a
number of different services, whether that's Security Hub, where we contextualize some of that with Inspector and Security Hub data if you saw the announcement yesterday. Or Amazon EventBridge where a lot of customers
create remediation workflows or integrations with ticketing systems. And then also integrating
with Amazon Detective for root cause analysis
and resource relationships. So speaking about announcements, I wanna make sure that
people are aware of this: Amazon GuardDuty Extended
Threat Detection. We announced another
extension to this yesterday. This is really just a finding type that happens in GuardDuty. It's not anything a
customer has to turn on. If you're using EKS
protection from GuardDuty, you get this automatically. It's not something that costs money. It's not something you have to turn on. But essentially the way that this works is previously you might've
had like a GuardDuty finding for an enumeration activity,
an exfiltration activity, an impact type of tactic. They would be different
GuardDuty findings, I would say. Like, you know, somebody's
scanning your environment, someone's got crypto mining on this, someone's destroying something. Now with this Extended Threat Detection, we create attack sequence findings that bring all these
kind of signals together and say here is the extent of
your security issue, right? They started here, went
here, ended up here. And ultimately, you know, this
is the whole security issue. So bringing a lot more context
and correlation together for our customers. So with that said, I'll
pass it over to Pratima. - [Pratima] How many of us
have heard about Q Developer or Q at all? Do you use it? Have you tried any bits and pieces of it? Okay, so you have heard about it, right. And the rest of you have heard about the general term generative AI. Yes. Okay. - [Marshall] This is a code talk, so. It's meant to be interactive.
- Yeah, it has to be, yeah. You guys don't speak out, I'm gonna take all the (indistinct) away. (Marshall laughs) So, yeah okay, so Q Developer
is a specialized tool that uses generative AI
models under the hood. It's a massive agent. Amazon Q, as such, is a massive
agent system under the hood. So when you use Q Business or Q Developer or Q with QuickSight, it's
using multiple sets of agents to get the right model
doing the right thing to get you the most
appropriate answer, right. So you don't have to build
that system yourself. You can use Q Developer if you're like me. If I had to code, you know,
probably I'd be out of a job 'cause I don't know how to. So Q Developer has been very useful. The other thing that is useful for is when you're writing massive code or maybe you are in a
business where you've acquired another company and
you've got a bunch of code that you need to now
integrate with your systems. You need to write tests, right. So you can just throw Q
Developer on top and say, "Write me tests for
this entire code base." And it'll make an attempt to do it. It'll read through it, it'll do it. Now, the one thing we need to keep in mind is with generative AI,
like, as much as we love the amount of capability it gives us, that human intervention
or human supervision is really required. It'll get you kick
started, like, super quick. But then make sure that
whatever it's doing, at any point of time,
it's not getting confused. And for that, your prompts need to be slightly more descriptive
so that the model really has the context
of what it's going to do. The one other thing that I'm very bad at is I love doing security things. I love telling my customers, "Look, this is what you can do." But they want documents. They want, "Can you document this so that we can make it a business case and present it to our team? Or we can showcase that this is what the architecture diagram looks like." So as much as I wanna go into PowerPoint, pick the right, icons and
stitch it up all together, I could use Q Developer, and
I'll show you in a bit as well, to build a markdown, and
it prints out pretty boxes and does all the arrows and things. And I'm like, "That's so much
work that I don't have to do, that I don't like to do, but I have to do as a part of my job." So it really is that assistant or that augmenting function for my role. So I'm not necessarily wasting time in all of these things
that I don't want to do, but I'm thinking more about
what my customers benefit from. And when I tell Q, it kind
of tries to think like me and builds out the artifacts for me. Now if you were to integrate
Q in your environment, you would be doing that
through IAM Identity Center and surfacing Q as an application. Can someone tell me why should I be using IAM
Identity Center with it? Like, what capability is
Identity Center giving me? - [Marshall] Is that a hand? - [Attendee] Access to
the right data sources that correspond to your user rights. - [Pratima] Right. Yeah,
so permissions control. What else? From the context of generative AI, what else do you think Identity Center adds to the experience?
- There's nother hand here. - [Attendee] I was just gonna say, I mean, can also sync
it up with your current either (indistinct) directory. (attendee speaking faintly) - Yeah, single sign on. Anyone else? Now think about Amazon Q as an application that surfaced through Identity Center. What it gives you is as
soon as the user enters through Identity Center and
accesses the application, it preserves the context of that user. So now my business could
have 20 people talking to Q, but I go in as Pratima, and it knows that Pratima talked to me about these different things. This is probably what she wants
to talk to me about as well. So it gives you a personalized experience, which is quite powerful 'cause every human is bespoke, right. Each of us have a
different interpretation, slightly different for different things. Even if we do the same job,
we think slightly differently. So it builds that context space within that Q business application or Q Developer application so that it works according to, it starts thinking like I am thinking. So it becomes more of my,
sort of, you know, assistant or more of my, for the
lack of a better word, like a pilot that next to me. That's the primary use case when you say I want to use Identity Center with Q Business and Q Developer. From there we will now move
to a little bit of demo. We are gonna be flip-flopping
between two laptops. So there'll be moments of
silence when we do that. But you can crack a
joke while we are at it if you wanna kill the silence. And over to Marshall. - [Marshall] Cool. So we have come out with
our GuardDuty Tester, open source repo. So essentially, it looks like this. It deploys a bunch of resources. It's a CDK project, and you know, folks can put this into
a sandbox environment where you can go create a bunch of realistic looking findings. So in GuardDuty there is an
option for sample findings, but it's just dummy data. Like, the instances is
I-11111111, however. I think there's nine characters. So that doesn't look that realistic. This'll create the actual resources and then trip the findings so that you have realistic
looking resources. It is a big CDK project with a
bunch of different resources. So maybe you want something more specific, and that's where we're gonna start with our kind of first Q Dev demo. So the first thing that we built in here is a EKS GuardDuty demo. And for the record, when I started getting
ready for this talk, I went through the QCLI and said, "Hey, I'm giving a talk at re:Inforce. I need to show off Q Dev, I need to show off
GuardDuty creating findings. Build me this repo, A, and then
tell me what to do with it. So it even gave me, like, a demo summary and it built different automations. So the first thing it gave me
was a demo setup shell script that we'll get started with. Essentially what it's doing is making sure there's an EKS cluster that it can run these findings against, making sure that we have the context set at GuardDuty is turned on, a number of the things that we would need to make sure these findings get created. And then let me, I'm blanking on the name of the file. So then we'll run the
GuardDuty-EKS demo Python script. It says, "Are you ready
to start your demo?" Yes. Keep in mind I did not code any of this. And if we go and look at the file, it's essentially a Python file. It did a bunch of the
different, like, comments so we know what it was doing. If we look at what it's doing, it's essentially creating
a Kubernetes manifest file so it can do suspicious pod activity. I wanted to do these EKS findings since we just launched our
EKS Extended Threat Detection, and we can look at those findings. So if we look at what it's doing, it's saying it's executing
suspicious kubectl commands. If you're not too familiar with kubectl, it's the Kubernetes command line utility that you can run commands in
the Kubernetes environment via that utility. So it's getting secrets on all namespaces, getting pods, getting
nodes associated with that. That might be like some sort
of enumeration activity. And then it's execing into different pods. Execing is like a way to
run the commands directly on the compute resource in the pod instead of against the
Kubernetes control plane. So it set all this up for us
so we could go create findings. And if we go further
through the Python script that's creating these findings, we can see that it's
creating malicious services. Services is just another
concept through Kubernetes if you're not too familiar. Setting some of this stuff up for us. And then it's also kind of commenting where we're doing these
different things and show. You can see the different
print statements, and here's those suspicious
commands that we saw earlier. Once again, I did not do any of this. So like, I'm gonna show
an example in a minute of creating some of this. But if you just needed
to create something quick and scrappy in your environment, you could just essentially
give it a prompt and it would do that. And then it even asked me if I want to clean up these resources. I'm gonna say no for now. And then if we went over to the console, which I'm gonna pull up here, we can see the types of
findings that it creates. So I'm gonna go to
GuardDuty, go to Findings. So EKS Cluster Inspector Demo, they named it Inspector Demo 'cause I was doing something else, but this is the one we can
see that six minutes ago it was last seen. But there is a Bitcoin-related
domain being queried from this instance. This is from a runtime monitoring agent that saw this activity. So this is the actual
agent that is on the host for these EKS clusters. It uses an EBPF agent. It's getting telemetry,
sending it back to GuardDuty. One of the things I said before was GuardDuty being easy to turn on. We collect that data with agents that introduces a little bit of complexity but we use different use
cases for enabling that, whether it's an EKS add-on, injecting a sidecar with
Fargate or using SSM to install the agent on an EC2 instance. We can still give that ease of
deployment without, you know, while we're introducing
a runtime agent as well. Some of these findings
do take a few minutes. So we're looking at findings that have already happened, FYI. So who has ever seen a attack sequence extended threat detection finding or is familiar with how those look? I know I talked about 'em
a little bit earlier, but. Anybody, yeah. (attendee speaks faintly) Not talking about miner. We can talk about that if you want. No, these are the extended
threat detection findings. So that finding we were just looking at was, like, a single thing. We've seen bitcoin mining
reaching out to, you know, we've seen a known bad
instance that is looking at a known bad bitcoin
mining domain, right. It's on the EKS cluster with a, what we introduced, this was originally introduced
at re:Invent last year. And then we've just been expanding to it. We launched it with an
attack sequence finding for IAM credential compromise
and then S3 data compromise. And then what we launched yesterday was an EKS cluster compromise. And this is an example of that, and it's just bringing
multiple things together. So for example, these signals
are the various findings that we had associated
with this EKS cluster. So for example, there
was a phishing domain that was queried. So this is initial access, a drop point domain was queried as well. So it's more of an an
exfiltration type of activity. DGA or domain, I'm blanking, domain generated algorithm
domain was queried. Command and control, and then you know, kind of so on and so forth. So this is bringing essentially
the different findings that were all part of the
same security issue together and then bring it, you know, essentially bringing it all together so we can see that in one finding versus you as a customer saying, "Oh, these all have a
common instance together. These all have a common IAM role or actor associated with them. They're all probably
part of the same issue." So, you know, bringing those
different things together. All right, so that's essentially
what the findings look like after the finding creation happens. If you do want to run
the GuardDuty Tester, the CDK deployment takes like 30 minutes. So I've actually already
deployed it in this environment. But essentially the way that this looks is we'll go over. It deploys a number of EC2 instances associated with, like, Kali
Linux and Windows and EKS to create the different finding types. But there is one instance that is labeled "Driver-GuardDuty Tester." I'm just gonna get into
this using session manager. Let me get the command from here. It actually gives you the SSM command to just get to use SSM
through the command line. So that's getting into the
instance, the session manager. You can either do it through the console or through the command line. I'm just gonna do it
through the console for now. Change the directory, and then it's python3
guardduty_tester --help. And this will tell us
the different examples of what we can do. So obviously help will
tell us there's more stuff. We can declare that we want to test attack sequence findings. We can declare that we
want to test EC2 findings or ECS EC2 or ECS Fargate. You know, maybe if you're
doing that tabletop exercise and you want to do, like, a specific type of finding to respond to, this will help you get a little
bit more tailored to this. But for this scenario, we will just do the
attack sequence finding. I definitely can't type
when people are looking. Attack sequence. Oh. And you gotta use the
right version of Python. And then one cool thing
about this tester too is it will say, like, "Do you want the tester to
make changes on your behalf?" So say for example, you're
doing a Lambda finding but you don't have Lambda
protection enabled, it'll actually turn it
on and then turn it off. One thing I would be sure to specify is each GuardDuty protection
plan has a free trial. So if you're gonna be
doing this in a sandbox, it's probably fine, but I wouldn't. You possibly burn your free trial on a different account or
something if you're not ready to. Cool. So the only one that actually
exists in this one now, we're gonna be extending
this in the coming weeks, but is the S3 compromised
data attack sequence finding. It went ahead and ran that for you. If you actually go look
at the code in the repo, you can see the different. Ooh, I forgot where it is exactly. You can see the different, how they're creating these findings. Hmm. All right, there we go. Stacks, common, test resources scenarios. Cool. So if you look at Attack,
S3 compromised data, you can go see what this is doing and how it's creating that finding. If, like, say for example, once again, you didn't want to create
all of these resources in your environment. This is, you know, public
GitHub repo that you could go, you know, pull these commands off of and then replicate it in
your environment as well too. Cool. So that's enough on creating
GuardDuty findings for now. I will hand it over to Pratima, and we'll talk about responding
to these findings, so. - [Pratima] It wasn't all
for nothing that, you know, Marshall went on about
GuardDuty finding creation 'cause that's gonna be critical. What I've done is, and
as soon as it shows up. You know, we really have
to pray to the demo gods for this thing to work. 'Cause I'm going to make an attempt to use the most recent kind of finding, which is attack sequences
for EKS compromised clusters, which was announced yesterday. I've prepared the demo. If everything didn't work, I will definitely show you
what I've done in the past. Let's see this working. What I want to do is,
say I've now, you know, services keep releasing new features. This particular finding
is new for GuardDuty. So what happens in your
security operations function when there's a new finding type? You're gonna go back and see can I build an incident
response playbook for this. So if you don't have context of what this finding is going to do, you can't build that framework, right. You can't build that
incident response playbook. Which is why the tester really helps 'cause you could just say, "This is GuardDuty finding. This is new. Build something for me." So what I'm gonna do now is
I've prepared a few prompts and I'm gonna walk you through
those prompts as we use Q. What Marshall showed you
is Q Developers integration within Visual Studio Code. I'm gonna use baseline
QCLI on my terminal. 'Cause like I said, I'm not a developer. I'm much better off. I used to do infrastructure as code, and I used to do, I can
do a lot of scripting. So terminal is, you know, my
safest place to operate in. So that's where I'm gonna be. If I just say "Q-Chat," It's gonna open up my console. And this Amazon Q integration is coming through my Identity Center
integration with my AWS accounts. And you can see it says I'm
chatting with claude-4-sonnet. But I could change if I do a slash model. I have a different option. Like, I have a few different options. By default it uses 3.7. I've just opted to 4
because I was curious. And that's about it. It's using 4. Now let me go back. So you can see I have had a few attempts to doing this, right. So why do you think we
need to make attempts at using gen AI models? Like, why doesn't it get
it right in the first time? Or will it ever get it
right every single time? What's that one thing about gen AI that we should always have
at the back of our minds when we are using it? It's non-deterministic. What I talk to Q about today
and what response it gives me will be completely different from me asking the same question tomorrow and the response that will generate. And the fact that this is
now using Identity Center and it has my context,
it's sort of learning that this user had asked
me about this thing, I gave it that response. Maybe I know better now so I
can give it a better response. So what I've asked it to do is I have Amazon GuardDuty
configured in my environment. GuardDuty findings are
sent to AWS Security Hub for aggregation. And then I want you to build me a Security Hub custom action solution that will resolve a GuardDuty finding of the type attack sequence
for compromised cluster. Now, nowhere am I giving
it context of which cluster is compromised. I'm not giving it a specific finding. I'm just saying there's
a new finding type. I want you to build me a
baseline IR template for it. So I'm gonna copy it and cross my fingers and paste it here. So let's see what it does. And like I said,
documentation is not my thing. Like, I would love to
operate on infrastructure and tell customers, you know, "This thing stitches better. That is better for your solution. But if I had to write it in a doc that'll take me longer
than writing an email about, you know, this is
the best infrastructure. So now it's thinking. It's starting to think,
"What am I supposed to do? Let me create an architecture diagram. Let me see how I can build
all of the components out." And while it's doing that, it's going back to the online
resources that you have. What it does is because
it's Amazon's models, or not models, like, Amazon's service, it has more context of
AWS services, right. So it's able to pull it's learned, it's basically done its learning and training on AWS services as well. So it'll give you more
contextual information. So you can see this is just
the verbiage it has spat out. It said for EKS compromised cluster, this is the remediation architecture. You're gonna send the GuardDuty
finding to Security Hub, and then security custom action is gonna be based off
of an EventBridge rule. These are remediation
actions you gotta take. And then SNS notifications. So it's built out all of
these components, you know, in a pretty sort of document. And then it's given me the
flow description as well. Now as with any gen AI model
or any agentic workflow that you might be building, there are controls that
you should be operating on. So usually they're
safeguarded against writing onto your file system 'cause that's a potentially
problematic thing if it happens in an environment where you don't want it to happen. So it's gonna ask me
whether I trust it or not. If I say I trust it, if I put the T on, henceforth, it's never gonna ask me. But if I say yes, then
every time it's gonna write into a file, QCLI will ask me what to do. So now it's written
out that markdown file. So it's written the architecture diagram. I also want it to write
me infrastructure as code. So slowly I'm building out that
incident response template. So it'll keep thinking 'cause there's so many
different pieces involved, it'll start looking at,
you know, all of the things that are available, all the
resources that are available for it through cloud formation, and it'll start stitching it up together and it'll produce me a YAML. Can I just go ahead and deploy
that YAML in my account? I mean, I would love to, but
I would want to make sure that it's right, right. It's doing the right thing. So what you can do in that
case is you can ask Q again, "Can you assert that all of the resources in this cloud formation template are going to be deployed properly." So you're sort of reverse
engineering and telling it, "Now you assert yourself whether you've done the right thing." 'Cause what happened when
I was building this demo was I tried to deploy the Lambda
function that it had built and it started failing on
certain dependencies of Python, and I could be none the wiser. And it kept failing, so I
had to continue to tell it, "You're failing with this
error, can you improve?" So it's a very interactive, it's like having a conversation
with your peer and saying, You know what? This
thing is not deploying." So you sit and do some troubleshooting, but here Q is doing it for you. Let me see if it ended up doing anything. But while it's thinking, if I go back to the
document that it is created, it created me a markdown file, and I hope it's visible, And everything that you saw,
it created pretty boxes. Although the alignment is a bit wonky. With just that much, you have built an incident response playbook. It may not have the commands
there but it's got the flow. So you could then extend on it and say, I keep going back to that agentic system 'cause a lot of the
conversations these days are about agents and how you put it in the security operations function. If you had a security operations function or a platform that's
driven with generative AI, you could use Q to build
these architecture diagrams for each type of finding
that GuardDuty has. So maybe weekly just pull
all the GuardDuty findings, build me out or keep these updated. And as soon as it sees a type of finding with tangible data, like business context, can you extend upon the
finding that we already have and build me the
remediation template for it. So it's taking a lot of time to think 'cause it has a lot of things to do. - [Marshall] One thing to
note too while we wait on that is the trusting and allowing. If you look at the documentation, it'll tell you what's trusted. By default, really the
only thing is a file read. And then what are the
different, like, components that you can either trust, deny, allow. And the the actual, like,
information that you might want to know of, like, what all
is it really gonna ask you? That's all in the Q Dev documentation. It's pretty straightforward. So something to potentially
check out if you need to. - [Pratima] So now if you see, it's built me out a
cloud formation template. It's a massive template 'cause it's doing all of those remediation steps. It's taking a few inputs and
these inputs can be provided through that EventBridge
integration, right. It's created an SNS topic 'cause it said it's gonna create one to do those notifications. It's talking about an IAM
role for Lambda function, and it's kind of, you
know, it's named it as such so that you're aware of what's happening or why is this role being created. It's adding least privilege. Otherwise it could have done
Security Hub star but it's not. So there's those security controls that it's providing out of the box. The one thing that I've observed with Q is even if you ask it to be, you know, ditch all of the security controls, it tries to go back to building
better security practices. So that's kind of a
reinforcement function of, "Hey, let's not do anything
stupid in our environment." So this is a massive
template it has built. And for network isolation of EC2 for credential rotation of
IAM for CloudWatch logging. And it's starting to build
the Lambda function as well. So it's using the right libraries, it's doing all of the imports. So it's basically doing
all of that coding for you and it's trying to make a
separate Lambda function for better code organization. So now it's trying to
improve itself to say, "Well this is the baseline I've built. Use it if you like it. But I think that there's
scope for improvement." So it now it's thinking for you and doing that needful for you. And it's taking a bit of time 'cause the EKS compromised
cluster finding is massive. Let me show you the kind of
finding that was generated. It's the same finding that
Marshall had showed you. But if you see... did anyone attend the
GuardDuty and Mitre session on Monday, Monday morning? So we talked specifically
to attack sequences and how it ties up with Mitre. And why that's useful is
because you now within GuardDuty correlating that information
to surface as a single thing. So when you think of remediation, Q is going into each of these bits, each of these individual findings that line up with certain
type of Mitre attack tactic, and it's building
remediation for each of them or quarantine for each of them, which is why it's taking longer. Now you see it's built out the
Lambda function and it says, "You know, there's something I can do to improve your experience, and I'm gonna build up the
Lambda function as well." Now I could go in and say, you
know, go in a loop and say, "Well, you know what, now I
want you to write those tests." And it could go ahead
and write those tests. So you can say, "Now I want
you to go back and think what I'd asked you. Can you write tests to make sure that this thing is delivering on that. So there's a lot you can do with Q Dev that'll get QCLI, that'll get
you started straight away. - [Marshall] Another
thing too is if, like, say you wanted to stage this
infrastructure in the account. That way you don't have to deploy it, like, when you want to do the remediation. Like, you can also ask Q Dev to, if you have credentials
local to this machine, like, you're using IAM roll
with temporary credentials that you're putting in the profile, you could essentially ask it to deploy this infrastructure as
well but not run it. So it's something that it can, you know, do as well after you verify. - Yeah.
- like Pratima said. - Right. It's gonna think more, but
I am very conscious of time. So I am gonna stop it at the point where it's built me the Lambda
function for remediation. It's built me the cloud formation template and the documentation. But this is all off of the
back of a single finding type. What happens if I give
it an actual finding of that same type? Now I've tried it in two
different ways, right. So I went ahead and I was, you know, all starry-eyed with gen
AI and I told it, you know, "I'm gonna tell you exactly what to do. Build it out for me." And as deterministic and
prescriptive as I become, the worst output I get from it 'cause I'm not letting it think. I'm not letting it be creative and reach out to different sources and figure out what's
the best way to do it. So I always got into this loop of, "I'm telling you exactly what to do. Why can't you build this." And it never works. So you need to keep a
little bit of space open. So that first one, do you see
the attempt one that says, "GuardDuty is configured a certain way. I'm telling you do this. Do create a Security Hub automation rule. Do not create an automation rule. Create a custom action. It needs to be through EventBridge." So I'm giving it very much. I'm basically teaching a child how to read without understanding the
fact that the child can read and I'm just wasting my time here. So instead of doing that,
what I tried to do was, the second attempt I made, I asked it, "You've already done this, right. You built that IR playbook. I want you to extend on that playbook based on a specific finding." So I've asked it to extend it. Now, because I'm using QCLI, and I've put a finding JSON, the finding that I just showed you, into a JSON template. This is how it'll appear
as an EventBridge, as an event through EventBridge. And I'm gonna tell it, "Hey, go back to that finding JSON, and I want you to build
cloud formation templates. Extend on the solution
that you have just built." Now, 'cause I'm in the same session. It has context of what it has just built. Now, if you were to look at
this from the perspective of how can I operationalize
it in my environment, you'd be looking at maybe Lambda functions triggering off that Q workflow or maybe containers triggering
off that Q workflow. You could have step
machines or step functions doing this thing for you
and then committing it to source control. So you can keep extending it to say, and then you have version
control access as well if you keep committing
it to source control. (Pratima coughs) - Sorry, and now I'm gonna say, "Extend the solution
based on GuardDuty finding in that directory which is
in context of where it's at." And you should build the related AWS cloud formation
templates to create resources needed to remediate this finding. (Pratima coughs)
Sorry. Write the files in the
current working directory. So just, you know, don't
assume any resource IDs. I'm providing everything
through that JSON. So it's important for me to say it because what happens is I don't want my, I don't want to confuse the model 'cause it is under the
hood and agentic function. So if one of the agents is confused, it'll talk to the other agent, get more confusing information and that confusion chain will continue to just not give me any output. And that's how you can just
continue to fill up the context and you'll have nothing
productive coming out of it. So now it's gonna say, "Okay,
I'm gonna do my thing." It's again going to take a lot of time. So it's gonna examine that finding. Whoop, sorry. Oh well. There should be the file. Okay. Let me see if it likes doing this. Whoop. Sorry, I've exited out
of Q, and it's lost my... So what happens if you lose context. Now I've got all the files, right. I'm gonna do some dirty
operation here, and- - [Marshall] Something
that to point out here too. Pratima got out of the chat and then went back into the chat. It still has context of
what you were talking about. It'll store the context for
a certain amount of time. I'm not too sure how long. And then it will also, if the
conversation gets too long, it'll ask you if you wanna,
like, compress the conversation to make it more responsive and stuff. So it is keeping track
of that information. So if you exit out and
need to, like, you know, re-paste your temporary
credentials or something and come back into it, you'll
still have that context. Yeah. (attendee speaking faintly) Yeah, so say you want it
to do something in AWS. It'll look for a profile
related to the current user. And if you've given that
permissions via a role, right, not a user, then yeah, it will assume
those to do that action. - [Pratima] Right. So this particular prompt that I gave it, I told it to go into the prompt one folder where I had that sample IR playbook. And I asked it, "Now look into prompt two for that finding.JSON
and extend the solution based on the information now I provide." 'Cause now I have context
of a specific finding. So it's going to continue building that cloud formation template, but now it'll have specific resource ID. So if I go back to the thing
that it had created earlier, it didn't have the specific IDs. It was expecting them as inputs. Now, here it'll create
a bespoke YAML template that you can just, cloud
formation template, that you can just deploy. So which means as a security
operations function, you can have a battery
of these IR playbooks, and you can stitch it in and say, "Well if you see a GuardDuty
finding of this type and maybe you can play
with the titling and stuff, then call the relevant
or build the context or extend the solution that
you've seen in that finding." It is going to take a bit of time. So I might just hand over to Marshall to go through the next one, and I'll connect back
once it's done its thing, and I'll show you what it's built out. - [Marshall] So we're gonna
switch gears a little bit and talk about a different scenario. So before we talked about
you're a security person. You are, you know, trying
to create findings, trying to create runbooks, trying to respond to GuardDuty findings. Another scenario that
somebody came up to me that I wanted to include
into this talk was, let's think back to, I'm
blanking on the time, but Log4j when it was like January- - [Pratima] December, 2022. - December, 2022. There we go. So it was a big thing that
happened at the time, obviously. And I'm sure everybody in
here was probably affected in one way or another. One thing would be cool that
is from the developer persona is hey, could I use this
thing to help me remediate my Log4j vulnerabilities? Maybe you're using Inspector and Inspector said, "Hey this repository and this, you know,
these sets of resources have the Log4j vulnerability." Now you've handed it off to
your developer, and you say, "Get after it. We need
this done by tonight." So for this demonstration, I
went into QCLI, and I said, "Hey, create me a vulnerable
Log4j application, which it will do for you pretty well. I'm gonna go through a
couple different ways that you can use Q in the the IDE to interface with with these repositories. So let me start a new chat. And I'm gonna say, "Hey, tell me where in my current repo I have Log4j vulnerabilities." And then it's gonna think for a second, help me scan, you know, where this is. This is the chat that's part of the IDE. So you can chat with it,
tell it to look at, like, a specific repo. You can tell it to look at, you know, specific files in the repo. It's just another way to interface with the Q-Chat functionality
but directly from the repo. If we look at what it's doing,
it says, "Hey there's one." These are named pretty obviously, right. It essentially would
start looking for, like, Java files and everything. One thing to point out is I can't write a single line of Java. So I asked it to comment and we'll look at what
some of these look like. So it said, "Hey there's
some directories here." There's a number of files
and we'll start looking for different Log4j vulnerabilities. And then we're looking for a pom.xml file in the root directory. And then it's also gonna start looking at a number of other things. So let me pull up some of this as well. Cool. So now it's starting to do its analysis. And I'll scroll up in a second, but it's starting to find some
of the Log4j vulnerabilities. I can see the locations
in this demo original in this demo dupe file. Here's the CVE for this log
for shell, critical severity. You're using Log4j version 2.14.1. It should be 2.17.1 or later. And here's the different
affected files that we have. And then exploitation vectors
and then recommended fixes. So if we were to go back
to this file structure, we can see the pom.xml
file that it talked about. I also, when it created this, I don't know how to read Java or write it. So I was like, "Hey, can you comment and let me know where these problems exist so I can go find out about it." But essentially you could also ask it to update the file with comments so that you understand
where these things are at before you go fix them. And then you can see that
here's this reference to 2.14.1, and it's saying, "Hey
look, you should do this, you should change this to 2.17.1. So another thing that you can do, we use the Q-Chat in the IDE. You can also highlight a line of code, and on the Mac, it's Command-I. So this is like inline suggestions, and you can say "Fix this Log4j vulnerability for me." So Q is generating an inline fix. As you can see, the one piece is, the piece up top is red, the old code. And then green for the
new code that it would do. And it's saying, "Do you want
to accept or reject this?" So I'm gonna accept it. And now it has changed this for me. Like Pratima was doing, you
can also use the Q-Chat. So let me. And then I'll use Q-Chat
to just change the rest 'cause maybe you change one line, but you're like, "Hey look, I
need to address all of these." So in the Log4j vuln demo original, fix all of the Log4j issues." Cool. So what it's gonna do is
it's gonna start looking for those issues again and then it's gonna make those changes. Also, I think it'll already do it, but 'cause a lot of times
it essentially defaults to giving you, like, a
summary of what it did or a markdown file associated with that. You could also say, like, you know, "Before you make any changes, let me know. Or write down in a markdown
file all the things that you're gonna change,
the suggested changes, the original issues," and it
will write it all out for you. That way you can look
at that before you... Tool validation. Oh, I'm in the wrong file structure so maybe it's not gonna find that. So let's look at this real quick. All right, so if you
wanna quit outta the chat. All right, and we're running outta time. So Q-Chat. And then let me do this again. Cool. So now it's in the right structure. If you saw before, I was still
in the like GuardDuty folder and it couldn't see, it would
essentially had to go back in the file system to
understand where that was. So now perfect, I can see
the vulnerability clearly. The project is using Log4j 2.14. I didn't save the POM file. So it still sees it as broken. And now it's starting to
read the rest of the files and understand what needs to be changed. And it'll essentially
just keep going on and on. There's another validation error. One of the cool things
that I found about QCLI is especially when you're,
like, deploying things to, say you're doing some test
infrastructure and deploying, one of the things that, you know, when generative AI first came out and we had different, just, chats, you'd be, like, pasting
over what it gave you and then, like, it hit a different error and you'd go back over and, like, maybe your prompt's not that good so it doesn't get it 100%
right, and then you go back. With the QCLI, it essentially will work through those issues for you. So, like, when I was doing
some of the GuardDuty demos, it would say, "Hey, I
accidentally missed something in my cloud formation template. Let me change that and redeploy. And I was just sitting there, you know, watching it go through the whole cycle and getting through those errors. So that was a much better experience than the whole Marshall
copying pasting over and over and continuing to run into the wall. So if you've not used the Q-Chat, it is absolutely a game changer. - [Attendee] So obviously,
if your IAM user's not provisioned to, let's
say, like, list findings, it'll run into an error- - Yep.
- based on your permissions. And then secondly, is there a self-hosted
version of Amazon Q at all? 'Cause it's scanning
all of your files here, presumably looking for them,
uploading that somewhere to think through it and
then, like, DLP concern. - [Marshall] Yeah, I mean, you can specify what it can look through. If you do, like, slash help, like, Q-Chat and then do slash help, it will tell you, like,
how you can scope down what it has access to look at. And I think in our documentation, if I remember reading correctly, it goes through, like,
that scenario, right. Like, you should not
run this where you might potentially have sensitive information because it will, you know,
if you tell it to look at a directory and the file's in it, it's gonna look at the directory and the file's in it, right. So, like, there are certainly
some security considerations to take into account there. So yeah, definitely
look into that as well. Okay, so I know we're running outta time, so I'm gonna hand this back over. But essentially what's gonna happen here is it's gonna gimme like
a markdown with, like, here's the things that I changed, here's the information
that you need to know about these vulnerabilities and stuff. So it gives you, like a really
good writeup on what it did. - [Pratima] Now if you think
about EKS as an ecosystem, there's AWS resources,
but Kubernetes itself is its own ecosystem, right. I've built an EKS platform
in my previous job, and outside of understanding AWS, there was so many nitty
gritties of Kubernetes, namespaces, services, pod
identities, control policies, that we had to understand. So our, like, learning
curve had to be steep but had to be fast because
we had to build all of that. And then incident response was
just a whole different story 'cause we were still understanding. So now I gave it one
prompt that I showed you to extend on the solution. So it read all the files. It told me, "Hey, I've read all the files. I'm gonna take everything slowly." First off, it built me a
high-level architecture diagram. Now, it's using Mermaid for some reason, but in markdown it said hey
this is the ingestion flow. We're gonna see EKS runtime
finding, DNS monitoring, network traffic analysis in GuardDuty. They're all gonna give
us a finding aggregation in Security Hub and I'm
gonna create a custom action. Now this is the extension
of that IR playbook that we'd created. And then it spits out a diagram on remediation orchestration. This is what I'm gonna do. I'm gonna build an event parser. It'll analyze the attack sequence, and then it'll build a forensics connector and everything else. And it realizes it's talking
about Kubernetes, right. So it also talks about what is
the Kubernetes security layer that now I have to target. So it talks about network
policies, RBAC policies, pod security policies,
PSPs that you might deploy and any other DNS
filtering through core DNS or any networking controls through Calico that you want to apply. And then it finally produces
a data flow architecture. Like, this is the detection
that has happened. And this is what we are gonna be doing, the controls that it's going to implement. So these are all diagrams. It's just showing you slowly but surely, like, these are the things
that I'm gonna target. 'Cause when you really
look at the remediation, now you say it's title enhanced 'cause I asked it to
enhance the previous one. The enhanced module is
looking for different aspects, but it's also looking for,
like, a quarantine CIDR and a forensics S3 bucket. It realizes that I need to respond, and quarantining and forensics
are a part of response. I didn't tell it I needed
all of those things. So it's now started thinking
as a security response person 'cause it realizes I'm talking to it about security incident response. This is a massive template. So without scrolling it, the other aspect, the other thing that it also did was it created the Lambda function that'll help me with the remediation. And it takes in all of the
inputs that are being given through the cloud formation template. But what it also does, it
creates the Kubernetes constructs for the network policies,
the PSPs, the IRSA policies, and they are ready to deploy. 'Cause there's multiple
layers in this ecosystem. And if it was only addressing the resource-based layers with AWS, the Kubernetes layers
would be your problem or the developer team's
problem or the product team, whoever's building it. But now it's consolidated everything. So now you've got constructs
to deploy straightaway into the Kubernetes
cluster that's gonna help with remediation, with
quarantining, with forensics. And finally it's deployed
security policies as well that are there any security
policies that are missing that need to be applied. And I didn't ask for, I didn't have to be very specific
that give me all of this. It just figured that there's
so many moving pieces. Let me bring it all together. Imagine the number of human hours that would've gone into this. And we've been able to do
five, four different use cases in about under an hour. And then it spits out a read
me file, which I've taken you. Sorry, it spits out a
solution deployment file. Because now I've got
so many moving pieces, how do I know which one to
deploy when or what is ideal? So Q's been able to figure out, like, someone's gonna need to
do this orchestration and it's done it for you. It's given me, "Hey, I'm
gonna check whether the CLI, I'm able to do what I need to do with AWS. I'm gonna check if you're
providing me the right parameters. I'm gonna deploy the stack." So it's first deploying
the remediation stack. And then it says, "I'm gonna
update that Lambda code 'cause I feel like we
could do a better job. And we were maybe constrained
by the number of characters in that cloud formation template." And then it says, "Once
I've deployed that, I'm gonna extract the finding parameters and I'm gonna push it through
the Kubernetes stack," the Kubernetes resources
that it had pulled, And then it'll deploy
the Kubernetes manifests, which included network based controls, pod security policy-based controls. And then finally it's
gonna display a summary of, "This is what I've done so far. These are the different
things I've applied, and these are the different stacks." So I've basically had to build nothing. Now, I could be deploying
this in my AWS account and maybe some bits of it fail, but I can go back to Q and say, "I'm getting this error
in this particular module. Fix it for me." So I'm not having to do
that introspection myself. It feels a bit tedious,
but what would be better than someone, like, something
like Q solving it for you or you Googling 100 different pages and then trying to figure out
which one stitches better? So this is your kickstart
into using generative AI for incident response. And obviously you can then, you know, do better with agentic
AIs and agentic SOCKS and all the different capabilities that you can do with other
types of capabilities, like strands agents and MCPs and stuff. That's more or less
everything from my side unless there are any questions. And we are pretty much
on time at this point. Thank you so much for being here. (audience clapping)
- Thanks everybody. - [Pratima] Thank you
for being interactive. And if you like this session or if you would like something
more from this session, please give us feedback on the app. And we would love to hear from you.
