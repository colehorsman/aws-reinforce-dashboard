# AWS re:Inforce 2025 - Know your data: Building a strategy to address OWASP Top 10 for LLMs (DAP122)

**Video Link:** [Watch on YouTube](https://www.youtube.com/watch?v=z-yB73eHCLg)

## Video Information
- **Author:** AWS Events
- **Duration:** 19.8 minutes
- **Word Count:** 2,415 words
- **Publish Date:** 20250620
- **Video ID:** z-yB73eHCLg

## Summary
This presentation by Yuri Duchovny from Cyera explores the critical challenges of data security in generative AI, emphasizing the complex landscape of protecting sensitive information across AI systems. The talk highlights the evolving nature of data security, moving beyond traditional protection methods to address the unique risks posed by large language models and AI applications.

## Key Points
- Generative AI introduces complex data security challenges that differ from traditional web application security
- Four major risk buckets in generative AI:
  - Model and data ingestion risks
  - Operational data access risks
  - Model behavior and potential information leakage
  - Regulatory and compliance challenges

- Key security considerations for AI systems:
  - Prevent sensitive data from entering training pipelines
  - Implement fine-grained access controls
  - Monitor data flow in and out of AI models
  - Understand data context and ownership

## Technical Details
- Security approach based on OWASP Top 10 for LLMs
- Critical vulnerabilities include:
  - Prompt injection
  - Sensitive information disclosure
  - Data poisoning
  - Embedding weaknesses

- Data security strategy recommendations:
  - Comprehensive data discovery and classification
  - Implement least-privilege access controls
  - Continuous monitoring of data pipelines
  - Use AI-powered data classification techniques
  - Authorize each data access request with end-user identity

## Full Transcript

- [Yuri] Hello, everyone. And thank you for coming
over for this session. The last one for today, but the first day of the
conference, I'm Yuri Duchovny. I'm Director of Solution
Architecture at Cyera. And we will talk, let's guess,
we'll talk security, right? But we will talk not only security, we will dive into the cutting edge. We'll talk about generative AI security. How many of you are dealing with securing generative AI
workloads on daily basis? Awesome. I see hands. And with securing data in relation to generative AI workloads? I pretty much see the same
hands here, which is expected, because data today in
our digital world is the crown jewel of every organization, and everything revolves around the data. So another question. Is any of you find
yourself in that situation when your businesses are
running thousand miles per hour and they're building these
amazing generative AI chatbots that are increasing productivity, making our life easier, opening
new business opportunities, all that amazing stuff. But you are the person who needs to figure out how to secure it. Yes. And imagine the most powerful
of this agents are dealing with the data. And the most sensitive data
that you need to secure. To understand how we should
approach data security in generative AI, let's step
back in time a little bit. Do you remember when our biggest worry was to secure an all good
three-tier web application? And the biggest attack vector we were thinking about
was SQL injection, right? But why threat actors were so
obsessed with SQL injection? Because they were hunting for our data. But back then, the data. Sorry. Back then, the data was
in a single database. We knew where it is. It was rarely changing. And we know what we are protecting. And we had the set of tools, right? We could apply web application firewall. We were embedding the input sanitization, and all those good techniques, right? Good times, like we know what to do. We had the tools, it was
a clear cut what to do. If we are coming back to today's world. And we look at the
generative AI agent built, for example, on Amazon Bedrock. It has maybe some data in the
agent instructions, possibly. It has data in the vector database and it might be built on the
custom model that was trained or fine tuned on your very data. And your agent is also accessing or even updating data in the real time. So this picture is way
more complex already and we need to understand
what to do with it. So if we apply the same mindset that we were using for years to protect against SQL injection here, and we will try to protect
against prompt injection that we are talking about all the time, and we will throw in a AI gateway that will do this nice
prompting completion filtering and we will implement some guardrails. That will not be enough. Don't get me wrong, like we
need to do all this, right? We need those guardrails. But the two key differences
between the previous world and this world and one of
them is pretty obvious. It's way harder to filter and to analyze the
natural language comparing to the structured input like
SQL or structured forms. But the second one is even more important. In that previous world, we had a single entity
which wasn't trusted, which was the user, and it was
outside of our application. So if we filter everything
here, everything is good. Our life is good. Now we have another entrusted entity that sits in the heart
of our LLM application and that's the model itself. And this very model is interacting with our most sensitive data across this architecture diagram. So this is why we need to definitive controls around
what data used for training, what's data included
in the knowledge basis, and what is the data that
AI agents are accessing via these tools in the real time. And today, it's not a simple answer. What is the data and where the data? Data is scattered across environments, data lives in different
data stores, in formats, data is moving, and data is changing. And we are generating more and more data. So to formulate the risks of generative AI on little higher level, we probably can put them
in this four major buckets. First one, model and data ingestion. I'll be using sensitive
proprietary information in our training pipelines. Do we know what is flowing
into our rag data stores and through these pipelines? Next, operational risks. Is data access properly governed when agents are accessing
external data sources downstream via the SQL connectors or APIs? For example, do we have
agent deployed in a, let's call it Shadow IT outside
of organizational controls. Model behavior. Can model risk proprietary
or sensitive information because of overfeeding, overmemorization? Can we verify how the decision
has been made by the model? And finally, the regulatory
and compliance questions. If we can prove compliance
to these frameworks and can we audit who is accessing the data through these systems? When and for what use case? So all these questions are not isolated, they're deeply interconnected. And they all, again, revolve
around the single thing. The data. So to address all this from the little more
structured perspective, it's helpful to look at
them from the OWASP plans. And OWASP's top 10 for LLM
is a security framework, designed to highlight
the most critical risks with LLM applications. It's also useful to take
a look at Miter Atlas, which focus on more documented and low level attack techniques
against AI/ML systems. But we don't have time to
address it in this session. We just mention it here and come back to the OWASP framework. So here is the map of
these vulnerabilities to the different components
of modern LLM application. Starting down the bottom from the training and data sanitization pipelines, going to the ingestion
to direct vector stores. Agent themselves in tools that are accessing the data downstream. Each of these components
can introduce its own risks. And if you zoom into the subset of LLM
vulnerabilities we may have, what is the common trend between this? They all deal with the data. Prompt injection, sensitive
information disclosure, data poisoning, embedding weaknesses. Each of these introduce
the attack surface, are risking your data to be
exposed to an authorized user or leaked by your LLM application. So we need to recognize
it's all about the data. LLM security, it's
around the data security. So how do we secure it? Here's some, again, some not all, high level security
controls that you must have. First, you need to
ensure that no sensitive or unauthorized data ends up
in your training data sets. From the identity perspective, you need to limit not just who accesses that LLM application, but also authorize each and
every request downstream when agent is calling your data sets. And use the end user identity for that, not the LLM identity. Your RAG vector data sets should enforce the fine grade access control or employ the tenant restrictions
for different use cases, not mixing them together. And you need to monitor and filter what goes into
the model, what comes out, especially to prevent sensitive data leak. All this is good, right? But all understood? But here is the thing. To enforce this controls,
you need to know the data. And this is why the deep
knowledge of the data through classification and data context such as data ownership residency must be the foundation of AI security strategy. You cannot protect what you don't know and you cannot defend and
control what you cannot see. To prevent sensitive
information from being leaked or exposed unintentionally
by your LLM applications, data knowledge here is the cornerstone. And it's not only about
the content of the data, it's again, the context
where the data stored. Who is the owner, what
is the data residency? Is it identifiable data or not? So all this context is the foundation. Those factors are critical
to protection AI systems, not only from the technical threats, but obviously from regulatory
and compliance risks as well. So now let's talk a
little bit about Cyera. So Cyera data security platform gives you data admins, data owners, full visibility, and
control over the data. We start from connecting
to the environment via API and we automatically inventory and discover the data stores,
either it's RDS, or Snapshot, S3 Bucket, or it is DynamoDB,
or even SQL Server running on the EC2 instance. We find them and we
classify how we do that. We have hundreds of
classifiers, traditional and the most importantly,
AI based classifiers that discover sensitive data in minutes. And enrich it with the ownership identity and business context. We also look into the compliance
frameworks violations, and we lend this data to the identities who or what can access this specific data. Most importantly for this talk, we also looking into the
specific AI use cases when AI applications or frameworks have access
to the specific data, and you can define your
policies based on that. I mentioned that we use
AI to classify the data and our AI native
classification can be broken into three major pieces. First, we have these data
elements in unstructured files like Words and PDF files
scattered across all environments. So we find them, we look into the specific data
elements like SSM address, name, also in industry specific jargon. So maybe something that is
very specific for your company. We will learn it and we will present it as
a finding or as a context. The second is file level classification, where we take in more holistic approach, not on the specific data
elements, but the file at whole. And the last one is structured learned when we use ML to group this data and to find the data classes that you have in your
structured data stores and structured files. (crowd chattering) So when you build your
data security strategy, and this is what a numerous
customers of us are doing today, you start by discovering
and classifying your data. Making this precise picture what you have. When, Cyera AI-Native
no touch classification, helps you to gain this
visibility into your data where the data lives and
what context around it. You know how to protect this data. So the next step, you use this intelligence
to enforce least privilege, business driven access model. Not just for human identities, but importantly for non-human ones or NHIs that your AI pipelines or
AI workloads are using. (crowd chattering) So when you, for example, when you define the specific roles that used by your SageMaker or Bedrock model customization jobs or Bedrock knowledge base ingestion job, you apply these techniques and assign these roles
specifically to access to the data based on the sensitivity
and based on the context. So in other words, if you have this foundational
know knowledge of the data, you can define and enforce these policies. Now let's dive deep into
some architectural examples. Let's imagine you are
customizing your model on Amazon Bedrock. For Cyera customers, that
is training the models on the data sets. It's very easy to enforce that only specific data is getting into the pipeline workflow. First, Cyera will classify the data and then you instrument the
model customization workflow with Cyera data, either using the tags, data sensitivity tags on the resources, or directly using the API and getting this rich metadata there. And your model customization
workflow makes decisions based on this data sensitivity. And if the data changes, Cyera
will recon the environment. Next workflow run. If unsanctioned data landed
in one of these data stores, it will be stored from being ingested into the training data set automatically. Simple, automated, enforceable, auditable. Next example is knowledge
based ingestion workflow. Same thing. Cyera classifies the data. Your workflow uses either
tags on the data stores or interacts directly with Cyera, and getting this information
into authorization on what data is getting
into your RAG data store. Again, enforcing the governance policies automatically across your pipelines. And once you train your model and you build your knowledge
base, don't stop there. While building your agent, enforce the same data
centric controls in runtime. When your agent tools
are accessing the data, make your tools aware of
this end user identity and authorize each and
every single request to the data downstreams. But do it based on deep, extensive knowledge of
your data from Cyera. Instrument this authorization
again against the data classes that we found against
the data sensitivity. We don't have time for the full demo, but I took couple of
screenshots from the platform. It's very easy on the
platform to get the identities that Bedrock is using
and to access the data. And you can track them
down to the specific data that these identities can
access and assess this use case. Is it the right use case
for this specific data? And you can drill down
into specific data classes, context, data ownership. And you can either use
console or better again, you will embed it in your MLOps pipelines
using APIs for example. And couple of takeaways. Start your data classification. Start your AI strategy
from data classification. Inventory, discover, classify,
and label your data first. Get the knowledge of your data. Then define the data usage access and retention policies based
on this sensitivity knowledge. Sanitize the data. Make sure that only the data appropriate for this use case lands in the pipeline, but embed it in your MLOps pipeline. Do it continuously. Rescan the data because your data is most
likely changing today. Your tomorrow pipeline
run may be different. You need to enforce that you're not getting wrong
data on the next time. Use classification to enforce
least privilege access when you build your models, when you build your knowledge base, but also when a gen AI is
accessing your data stores. And log everything. Monitor everything. And monitor for abnormal
access patterns to the data. But again, based on the data sensitivity, look for what is important. In other words, know your data and start your data security for AI from this foundational knowledge. Thank you. (crowd chattering)
