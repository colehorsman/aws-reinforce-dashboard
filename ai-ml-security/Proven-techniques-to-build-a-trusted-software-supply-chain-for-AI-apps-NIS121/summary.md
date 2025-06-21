# AWS re:Inforce 2025 -Proven techniques to build a trusted software supply chain for AI apps (NIS121)

**Video Link:** [Watch on YouTube](https://www.youtube.com/watch?v=xc2CaLPLAyo)

## Video Information
- **Author:** AWS Events
- **Duration:** 16.8 minutes
- **Word Count:** 3,175 words
- **Publish Date:** 20250620
- **Video ID:** xc2CaLPLAyo

## Summary
This presentation by Michael Foster and Sudhir from Red Hat explores techniques for building a trusted software supply chain for AI models and applications, focusing on security, safety, and integrity throughout the AI development lifecycle.

## Key Points
- AI Development Challenges:
  - Low POC to production conversion (12-30%)
  - Infrastructure scalability issues
  - Lack of AI security and safety assurance
  - Explainability concerns
  - Undefined success criteria

- AI Security and Safety Approach:
  - Merge software and model development lifecycles
  - Ensure software integrity
  - Manage risk profiles
  - Provide transparency and explainability

- Key Security Strategies:
  1. Trusted Artifact Signer
   - Ensure software integrity
   - Verify provenance
   - Track model fine-tuning lineage

  2. Risk Profile Management
   - Identify and mitigate potential risks
   - Continuous monitoring of vulnerabilities
   - Alert developers to changing risk landscapes

## Technical Details
- Open Source Tools for AI Safety:
  - Trustee AI: Focuses on explainability
  - LLM Evaluation Framework
   - Assess safety metrics
   - Measure bias, fairness, toxicity

- Guardrails Implementation:
  - Filter input and output content
  - Protect against privacy risks
  - Mitigate potential harmful interactions

- Model Evaluation Techniques:
  - Use LLM evaluation tools
  - Assess model performance across metrics
   - Bias
   - Toxicity
   - Truthfulness

- Continuous Monitoring:
  - Runtime monitoring of model behavior
  - Track potential model drift
  - Detect and respond to emerging risks

- Transparency Practices:
  - Create AI Software Bill of Materials (SBOM)
  - Document model training and fine-tuning
  - Provide visibility into model composition

## Recommended Approach
- Integrate security from developer stage
- Automate security guardrails
- Continuously evaluate and iterate
- Use comprehensive monitoring tools
- Prioritize explainability and risk management

## Full Transcript

- [Michael] Sudhir and I are gonna talk to you about proven techniques to build a trusted software
supply chain for your AI models and AI enabled applications. Ben Sudhir, director
of product management, specifically trusted software supply chain and data services. My name's Mike Foster. I do technical marketing
for OpenShift Security. And what's on the agenda? We're gonna talk about
some of the challenges and expectations for AI app development and deployment, how Red Hat
specifically enhances security throughout the AI model and app lifecycle. And then we're gonna talk
about how Red Hat's Trusted Software Supply Chain helps
to manage risk, integrity, build safety across the
software development lifecycle and model development lifecycle. AI's a hot topic. I don't know,
you can't get away from it. It's everywhere, right? This week. But there's also some concerns
that we want to talk about that we're seeing with our customers and some of the analysts
are seeing as well. This number's pulled from
a few analyst briefs. We've seen 12 to 30% of POCs
to production. It ranges. There's a bunch of challenges
that our customers are facing. Data model ambiguity challenge, you know, there's widespread adoption, but you know, they're facing issues with test data versus
scaling and production, getting the same accuracy in production. We're also seeing infrastructure
issues, scalability, MLOps, integration. How do you pull something from
a POC that's in a single VM and deploy it into Kubernetes or onto AWS and link it into all of your workloads? We're seeing challenges
with infrastructure, sorry, challenges with the lack of assurance, AI, security and safety. So governance, risk, and
compliance, AI safety, lack of explainability. And then we're seeing
some of the people issues. So down underneath four and five, undefined success criteria. So do the business challenges and the outcomes match up with what you're actually
deploying in AI, with AI? And then people and processes, you know, challenges, skills,
fear of job replacement. So we wanna talk specifically
about infrastructure and platform and governance,
risk and compliance today. Now, Red Hat security approach. We've been building
platforms for 30 years. Started with Red Hat Enterprise Linux, and we always start with
that strong foundation, built in at the operating system layer. Then we tack on infrastructure and automation with Ansible hybrid app platform with OpenShift. All to allow you to
deploy your AI ML apps, your visualization
workloads, all on top again, with that security and
safety built in underneath. Good example of this,
I've mentioned already, RHEL's inherent security. You know, we've been doing
this for 30 years, SE Linux, cryptography libraries,
application sandboxing, confidential computing, all extending seamlessly into
the app platform above it. And again, that's your
core layer when you're deploying AI models. Now, if you're using AWS,
you might just be deploying and having itself managed. If you're on-prem, these
are all considerations that you have to think about. And then when you're deploying
on-prem, you also have to think about how you're
gonna move those workloads into the cloud, and that's what
Red Hat enables you to do. Lastly, this is the layer kick slide. You know, again, we have that
underlying layer of Linux. We have Kubernetes, the foundational application
platform capabilities on top to allow you to deploy AI
and all your middleware and allow you to not have to
worry about those underlying details, especially when
you're deploying on-prem or in things like ROSA,
Red Hat, OpenShift on AWS. Now I'm gonna pass it over to Sudhir who's gonna talk AI safety and security. - [Sudhir] Thanks Michael. So
let's get down to more kind of AI application and AI models. You know, large language
models are here, especially with gen AI, it's running
all over the place. It's writing the code,
it's doing diagnosis for even the diseases right now and even interacting
with customers, right? The question comes that can
be is it secure and safe? Traditionally, we are worried
about the security, right? Supply chain security, you know, external actors coming in
trying to hack the things or trying to inject some of
the malicious code, right? With the gen AI, one of the
other aspect of security safety, because you have an embedded gen AI model that itself can cause some harm, right? Or it may have inherent
bias, it can create some of the contents, which your company may not
want to do that, right? The other biggest challenge
is how do you explain that this is what the
gen AI is doing, right? The customer wants to know
that, you know, you came up with this reason, what exactly
really you did that you, this is the outcome, right? So we wanna address both
the security and the safety, but it's not that we have to
invent these things new, right? You know, and traditionally
we have handled this thing for software development lifecycle. We do see the software
development lifecycle and model development
lifecycle merging, right? So you do actually take a gen AI model, create an application, you
fine tune that the model because it's not behaving
the way you want it, right? And then you again feed that
to the application, right? So we do see the merging from
both of these things together and we have to handle both
the software integrity as well as the risk profile for
both of them, right? For Red Hat, we have
trusted artifact signer. The main goal is to make sure at each step we can ensure the
software integrity, right? Sign and verify, you know, the provenance and you are test it, right? The key thing is that if
you do fine tune your model, you wanna know exactly how you trained it on
which data you trained it so you got that outcome. So the next time when you
fine tune it, you know that this is the modification
you have done, right? Generally we don't get this
thing with the foundation model, but you know, if you are taking it and adding weights, right? You do wanna get a lineage
of the both the data as well as the the fine tuning process you did so that you can actually go and
refine it the next time, right? This is for doing the software integrity. The next is risk profile, right? You do wanna know the risk
profile, you can't really go and get rid of all the
risk profile, right? Even simple thing like
CVs, you can't get rid of them from all the software, right? Same thing with the safety concerns. It'll be always be there, but the key is that you
should be aware of the what the risk profile at each steps and actually have
something to mitigate it. For example, developers should know that if they're using these libraries, this is the risk profile they see with that particular library and probably they can
go to the next version or what they can do to mitigate it, right? That's the main focus of
trusted profile analyzer. Same thing, we want to do it that even if you have
developed the application, if the risk profile changes, you do want to get alerted, it's not a
one time thing that you do and develop an application using a model and then you go there, right? Because new attacks can
occur or new CVs can be found and then you have to go and react it. Let's look at some of
the practical use cases. What we have done in terms
of how we have implemented that in, if you're
developing an application or if you're developing even the traditional chat bot, right? We have open source
project called trustee AI and the key focus for
them is explainability that you know exactly how did
you come up with the decision. Then you have LLM evaluation framework and the guardrails, right? The explainability is very
simple, that you do wanna explain to a larger extent. It's not yet figured it out in
the whole thing that you know how exactly the LLMs
come to decision, right? But your application should
be able to say that I came up with this decision because they
follow these logics, right? That gives the confidence
to the auditors as well as your legal team that it's okay to go to production, right? Same thing with LLM evaluation. It's not about evaluation
for your performance, right? It's also evaluation
of the safety metrics. So it's a fairness bias,
you know, toxicity and all. You need to be aware that
this is the safety parameter of your LLM and what you
do mitigate it, right? Last but not the least, the guardrails. There are many types of guardrails, right? The main purpose is that depending on what risk profile you see,
suppose it's a bias, right? You can add those guardrails
which can filter both the input and output content so that you can actually have
the protect your application not really crossing some
of the content, right? What it basically takes it from customers and not react in a way you
don't want it to react, right? One of the main concern
has been that you know, the LLMs, the gen AI specifically, right? It's very ambiguous, right? Depending on how many
prompts and what says and right, it can answer
in different ways. So you do wanna protect them and guardrails actually
does a very good job of at least in filtering both the input and output content to protect
from privacy and other stuff. So how do we do that, right? The first thing is that,
you know, any model you use regardless of you know,
whether you created them or you know you are
using a foundation model, do some kind of LLM eval, right? There's many tools, you know, in this one example we
use the LLM eval right? It gives you a kind of a
view of from zero to one that you know what's the
bias metrics, you know, what's the toxicity? You know, green is better,
red is not that good, right? But you will get this
with every model, right? There's no model where you
will get all the greens, right? So you want the developers to be aware if you're
choosing these model, this is what you are going to see. This is how it performs and it varies with different,
different verses, right? It even varies if you
go and change the weight or that you add different
prompts to the model, right? So the goal is that you run this thing and get a a blueprint that this
is what your model is going to behave or your application will behave and safeguard it against
the guardrail, right? That's the whole idea that you get the visibility
on that one, right? We have found this very useful. You saw the AWS also, a lot of people are using the guardrails to protect their application against any of these biases, right? You don't wanna do this at the very end. You do wanna do this starting
from the the developer when you are using the model, right? For example, in Red Hat, right, we have the dependency analytics. If you're using a model, you have get the blue cursor line, right? And you see all these
metrics that hey, you know, we see the truthfulness
like this one, right? Or you know, in toxicity .415, depending on the tolerance level of your particular application,
whether it's external or internal, you may decide that how do you protect your
application against these kind of metrics, right? Once the developer adds the
visibility, right, you do want to alert them that they're
looking at this particular aspect of your bias, right? You may want to add some
of the guardrails, right? You don't want to add all
the guardrails, right? Because it does slow down the application because it does filter both
input and output, right? The idea is that based on the metrics and profile you see either
you go and reiterate and reevaluate the model
or that fine tune the model or distill the model or you come back and add some of these guardrails, right? So if the developer is aware, they may choose a different model and they may actually, you know, go in and add some of these guard rails, right? That's the whole idea that you know, help them at least add the safety and security from the day one. It's very difficult. There are many types of guardrails, right? So our idea is that at
least in this particular when things are emerging, help them actually code
the developers, right? So for example, if we see that
they're using Llama Stack, we will go ahead and add them. "Hey, this is the code you
should be adding for the input and output and this is the
filter you should be adding given your profile of the model
you are using", right? So this is one example of Llama Stack. There are many types of
guard rail, it doesn't and at this point they're all evolving. The key's that what filter
you are using, right? If you are trying to protect against bias, then it's one filter trying
to protect against toxicity. That's a different filter. So you equip the developer
and then you actually go ahead and you know, once the
application is running right, you have to monitor it
continuously, right? Not only for the CVs but also even the bias
metrics if it changes, right? The whole idea is that the
model itself can drift, right? Not only in predictability of what kind of questions it answered, but
also as it's running, right? Different kinds of prompts and the interaction can cause it to really give a different response. So you need to have a
runtime monitoring for that. This is where Red Hat Advanced
Cluster Security helps. It'll continuously monitor it. Any risk profile change, right? Or if you are seeing a lot of
guardrail attributes showing that someone is trying to break
it, you do want to go ahead and take care of that
in fine tuning the next version of the model, right? We call it agility so that you know, you don't hold back just because you get the perfect application. You ship it with the
guardrails and monitor it. If you do see a risk profile
change, you come back and actually go and change it, right? Transparency, right? That's
the other aspect, right? Once you have a foundation model, generally they're not publishing the SBOM, but if you are taking a application and using some sort of LLM, you should create an SBOM including the AI models you are using, all
the weights you're using and everything so that you
know, even your team knows that exactly what all training or fine tuning you have
done so that they can, next time they go and actually
fine tune it, they know how to go and do that, right? This has been the missing piece. We are working with the industry
to even see that, you know, all the foundation model can
actually publish their AI SBOMB, but at least what we suggest and what we have implemented is that for applications using AI, right, at least they should have an AI SBOM so that we can actually know what exactly contains on the
particular application, right? Then protection from attacks, right? There will be attacks on your application, just like we used to have the
security threats from in the earlier days because you
have LLM, there is a prompt injections, you know, there are attacks where they will try to steal the data, which you're untrained on, even the model awaits
and everything, right? The guardrails, what we have
found is that when very useful, so they actually, you
know, either you embed that in the code or you actually
have that data surrounding so that you can actually
know that these kind of attacks are ongoing and you
can protect it against that. It gets very complicated, but the key is that, you
know, just like we used to have end-to-end and a secure
supply chain before, right? You have to start from the
developer if left as much as policy, implement the
security, not in a manual way, but in terms of automation,
so this is where I showed you that, you know, trusted
application pipeline, right? You know, it sets all the security guardrails end to end, right? It automates using the
backstage in developer hub so that the developers actually knows that this is the security profile and they can have the
policies that this is allowed or not allowed if they're
using the guardrails or not using the guardrails,
you give them the risk profile, you use the model, scan it,
and then you deploy them and have the continuous monitoring using any tools you like, right? In Red Hat we have the
Advanced Cluster Security tool so that you are aware
there is profile changes. Then you can come back and actually go and reiterate the application. - [Michael] Yeah, you
nailed it here, Sudhir. - [Sudhir] That's the, you
know, in short I had them. - [Michael] I was gonna
say, I think the summary is, it's similar to the
container lifecycle, right? You want to use trust AI
early in that process. Verify what model you're using, make sure that you're onboarding it,
seeing what the package dependencies and things like that are. Make sure it's cryptographically signed. Make sure you have a runtime
enforcement mechanism, right? You're doing all those pieces and that's really gonna
help with that percentage and help you get past those security and compliance checks,
legal checks later on so you can take your POCs and get it to production
as fast as possible. Again, similar story,
similar story as containers and virtual machines as it is with AI. Make sure you're doing your research first and building in those security guardrails. You're able to iterate way faster once you have those guardrails and you're able to go to your
security and operations team and show them that
you're taking all the key steps to secure AI. Hopefully that nailed the summary. That's what I got from
the time. Thanks Sudhir. We got a few links for you guys if you wanna learn more about Red Hat Trusted Software Supply
Chain and Red Hat AI. We're also at the booth right there. We're giving out black Red Hats, but if you just find me,
I'll be able to answer any of your questions or direct
you to somebody who can. Thanks again everyone for joining and I hope you really enjoy
Philadelphia this week and get home safe on Wednesday. Thank you. Thank you.
