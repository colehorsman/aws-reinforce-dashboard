# AWS re:Inforce 2025 - What good looks like: Building and improving cloud security (SEC203)

**Video Link:** [Watch on YouTube](https://www.youtube.com/watch?v=zs2IhKv5kFk)

## Video Information
- **Author:** AWS Events
- **Duration:** 56.9 minutes
- **Word Count:** 8,334 words
- **Publish Date:** 20250620
- **Video ID:** zs2IhKv5kFk

## Summary

This comprehensive session outlines seven foundational areas for building and improving cloud security, emphasizing that security is about systematic and continuous improvement rather than perfection. The presenters, drawing from over a decade of experience with AWS customers and internal service teams, focus on establishing a culture of security as the foundation, followed by technical competencies including account management, identity and access management, data protection, secure deployments, monitoring and alerting, and vulnerability management. The session emphasizes that security must be everyone's responsibility, not just the security team's, and that successful security programs accelerate business rather than slow it down. Key themes include eliminating long-term credentials, implementing least privilege access, encrypting data everywhere, using multi-account strategies, and building automated security controls that make it easier to do the right thing and harder to do the wrong thing.

## Key Points

- **Culture of Security**: Security must be everyone's responsibility with executive support, distributed ownership, psychological safety, and continuous education - not just the security team's job
- **Multi-Account Strategy**: Organizations that build account separation early move faster with better security controls than those who try to retrofit boundaries later
- **Eliminate IAM Users**: Move to federation and temporary credentials using IAM Identity Center, IAM Roles Anywhere, and built-in compute primitives for workloads
- **Least Privilege**: Use IAM Access Analyzer to continuously refine permissions and eliminate unused access - overpermissioning is like including unnecessary packages in containers
- **Data Classification at Scale**: Amazon Macie solves the problem of knowing what sensitive data you have and where it resides as data volumes grow exponentially
- **Encryption Everywhere**: Encrypt data at rest and in transit as a fundamental design principle, not just a security control - "Dance like no one's watching, encrypt like everyone is"
- **Secure SDLC**: Integrate security into CI/CD pipelines with threat modeling, automated testing, container signing, and reliable rollback capabilities
- **Centralized Monitoring**: Use Security Hub as single pane of glass, CloudTrail for all API activity, GuardDuty for threat detection, and Config for compliance monitoring
- **Vulnerability Management**: Maintain strong asset inventory, make reasoned decisions based on deployment context, and use continuous deployment for faster patching
- **Incident Response**: Prepare and rehearse responses before incidents occur - automate tasks but not decisions requiring human judgment

## Technical Details

- **AWS Organizations**: Implement organizational units (OUs) with service control policies (SCPs) and resource control policies (RCPs) for governance at scale
- **IAM Identity Center**: Central federation service that replaces IAM users with permission sets assigned to accounts, integrating with corporate identity providers
- **Temporary Credentials**: EC2 instance profiles, Lambda execution roles, ECS task roles, and EKS service accounts automatically provide time-bound credentials to workloads
- **IMDSv2**: Upgrade from Instance Metadata Service version 1 to version 2 for improved security on EC2 instances
- **KMS Integration**: Use AWS managed keys, customer managed keys, or client-side encryption with AWS Encryption SDK and Database Encryption SDK
- **TLS Enforcement**: Implement resource control policies to deny non-TLS requests, use ALB for TLS termination with ACM for automatic certificate renewal
- **Container Security**: Sign containers and packages for end-to-end assurance of software bill of materials throughout deployment lifecycle
- **CloudTrail**: Enable management events on all accounts, optionally enable data events for S3 and other services for investigation capabilities
- **Security Hub Standards**: Automated compliance checks against AWS Foundational Security Best Practices, CIS benchmarks, and other industry standards
- **Amazon Inspector**: Vulnerability scanning for EC2, Lambda, and containers with continuous monitoring and software bill of materials generation
- **Config Rules**: Continuous compliance monitoring with automated remediation capabilities for common misconfigurations
- **GuardDuty**: Machine learning-based threat detection using CloudTrail, VPC Flow Logs, and DNS logs with integrated threat intelligence

## Full Transcript

- Hi there. When we talk to customers about
security, they often ask us, what does good look like? And the reality is security
is not about perfection. It's about systematic and
continuous improvement. We've learned a lot from working with customers in our
internal AWS service teams over the years. And Peter and I wanna show you today what we would go back in
time and tell ourselves. - That's right, and this
talk is gonna be a primer. So if you're already
operating a cloud security organization or program, this will hopefully be a good refresher. And if you're looking to
get started on the cloud, this is an overview of
some of what we consider to be the fundamental core competencies that you must not just have but
work continuously to improve and refine over time. My name is Peter O'Donnell. I'm a principal SA focused on security and I've been with AWS for
more than a decade working with some of our largest and
most challenging customers. What we're gonna talk about today is some of the lessons that we've learned. - And my name is Lia Vader. I'm a security engineer in AWS security, but I started my career
at AWS over 10 years ago as a solutions architect
helping customers like you. And recently I've been in our
AppSec organization helping our internal service teams
build and launch securely. So these are the seven areas
we wanna prioritize for you. We only have an hour and there's
so much we wanna tell you, but think of this as the basics of what you should put your efforts into. We start with what I think
is the most important part of our cloud security journey, which is building a culture of security. And then we get into all of
the technical competencies. - In this idea of continuous improvement is really fundamental and it needs to be part of your culture. But the more important
aspect of this culture is the culture of security itself. It provides a foundation
for everything that you and your colleagues and your leadership all the way across the entire organization have to be part of. And it demands rigor,
rigorous, obsessive ownership that everyone in the org from
all parts of the business are committed to making
security the top priority. You've heard us speak about this, about this idea this same way that at AWS security is
job zero, our top priority, and what we know from
working with our customers and some of our highest
performing customers is that they take the same responsibility in the exact same way, that security is
everyone's responsibility. It is everyone's job and it has to be something
that you obsess over and continuously refine. The role of the security organization becomes setting standards and expectations and making it easier to do the right thing and harder to do the wrong thing. But security ownership
has to be with the people that are actually creating the software and the products that you
are operating on the cloud. That security is not an afterthought. It is not a meeting you have at the end of a development cycle. It is a series of meetings
you have at the very beginning of the ideation of the project. And as we talk about
these competencies today, they need dedicated
teams, they need funding, they need obsession and
rigor at all levels. So let's talk about what this means to have a culture of security. We know that it's a common
denominator for success. Again, not only here
at Amazon Web Services, but for so many of our customers who build and operate their critical
workloads on the cloud. Because culture is a series
of beliefs and values, it's easy to understand it as
a set of normative behavior. It's a body of things about
which you've already agreed to and that you will not
continue to negotiate, that the purpose of
culture I submit to you is to eliminate continuous renegotiation about whether or not it is important. And if you approach
the stairs in the west, you go up the right, and when you visit the Tokyo
subway, you go up the left. And it would be insane in that moment to have a conversation about it. Culture of security demands the same, that when you're building a product, you're thinking about a launch date when you're thinking
about design decisions, that you are no longer questioning whether or not security
is a top priority for it. And as you develop this in your heart, we want you to recruit your own colleagues up and down the organizational line, including your executives, that all of this is a necessary evolution for your organization to
get high quality, reliable, and repeatable security outcomes. That the rigor you place into
the things you are building must also be the rigor that
you place into security. And so we see four key components
of the culture of security in high performing organizations. Executive support at AWS, our CEO spends a week or
spends an hour every week, an hour every week focused
on the top security questions or topics that the team brings to him. This is fundamental to
have executive support, but to be clear, it is
not only exec support, it is in the bones of
the entire organization. From every junior
engineer to every manager, every director, every vice president. That security is
everyone's responsibility. And that means distributed ownership, that application teams,
compliance teams, audit teams, and most importantly
product development teams have this ownership. And in order for that ownership to work, especially for a junior engineer to be able to raise their hand and say, "Hey, I'm not so sure about this," you have to have a culture
of psychological safety. It has to be reasonable and expected and safe to ask hard questions, to object to things that
you know are not secure, to object to timelines that
compromise on security. And of course, continuous
education and refinement. People have to know what good looks like. Talks like this can help but within your own organization, set standards and allow for your customers and your internal partners,
your internal customers, to know what it is they need to do in order to reach high security outcomes. So how do we scale this ownership? Well, at AWS we have this
program called Security Guardians and we've got a lot of
great talks both this week and in the past focused on
what guardians really means. And this is another mechanism
to scale out ownership by deputizing and giving
a special education and training to certain people
across the organization, you could shift left not only
better security outcomes, but you could shift left the idea of inculcating security
culture in the minds and hearts of your entire organization. I mentioned earlier to set
standards and expectations, and this is fundamental. It must be very clear
what's secure is acceptable and what is not acceptable for security. Correction of error. Correction of error is a
unique thing at Amazon. And we want you to adopt
the exact same mindset that root cause analysis is not enough. You must endeavor to make sure that the same problem does not recur. And finally, you have to be
able to measure these things, get together, agree on
KPIs, agree on metrics, and then review them regularly. If you're not measuring it,
you're probably not managing it. And if you think you're getting better, you should be able to
prove it to yourself. And if you think you're getting better and the metrics say otherwise, then you've got a lot to think about. So we know that good security programs accelerate the business, that you're not in the
business of saying no. You're in the business of saying yes. The purpose of the brakes on the car is so that it can go
fast, not to slow it down. The purpose of the guardrails are so that the car can accelerate through the journey that you're on. Security and engineering,
and audit and compliance, all in fact want the same things, that the same outcomes that a great high
performing SRE would want are the same outcomes that a compliance or audit officer wants. And that you must see
each other as partners and not as adversaries. - All right, so after security culture, what's the next thing? I would focus on account management. So when I first became
a solutions architect 10 or so years ago, a common struggle I saw
was customers trying to work around a single account strategy. And I wanna talk about some
of the lessons we've learned. First, multiple accounts. Organizations that build
this foundation early, move faster with better security controls and better guardrails than those who try to retrofit boundaries later. And if you scale too quickly,
it could take a long time to unwind these decisions
and create separation. Next, you need tooling. As your account structure
grows and it will grow, you must have the right tooling
to manage your accounts. And lastly, security controls. You want a standard, you want standardized controls
across all of your accounts. You need to automate
this so it's predictable and reduces the operational
burden on your teams. So I'd start with account structure because it's the foundation
everything is built upon. And let me share what's
worked for our customers. So even if you're starting
your AWS journey today, I still suggest you begin
with a separation like this. First you have your management
account at that top layer. It's where your organizational
structure is established. And then you're gonna have
dedicated security accounts. And this is gonna have
your centralized logging, monitoring and security tooling. And you're gonna have backup accounts for administration and operations. And each team or workload is gonna get their own set of accounts and you're gonna separate production from development and testing 'cause it not only helps
with a blast radius, it's also about implementing appropriate controls for each environment. Now let's talk about AWS organizations. This makes that account
structure I just showed you, practical to manage at scale. AWS organizations gives
you account management through defined
organizational units or OUs. This allows you to group your accounts by function or by environment, creating these natural boundaries. And this is important because you can apply policies
to your organizational units. We have authorization policies and we have management policies. So authorization policies
establish guardrails through things like what we
call service control policies and resource control policies. And we'll dive a bit
deeper into those later. But at high level, they allow you to limit
permissions on IM principles and resources respectively. So an example of an SCP would be to only allow actions in regions that your organization operates in. And an RCP example,
resource control policy, would be to enforce HTTPS
on all of your S3 buckets. Now so management policies, they allow you to centrally
manage services and features. And what that means is
it's covering things like tagging and backups or specific declarative policies like enforcing VPC, block public access. And we know this can be a lot to learn and manage on your own. This is why we created AWS Control Tower. Control Tower takes these best practices that we just discussed,
the multi-account strategy, organizational structure
and policy implementation and packages them into a managed service that does a lot of the
heavy lifting for you. And the most successful
customers I've worked with treat accounts as a strong boundary, not just an organizational one. They provision accounts
through automation, they enforce consistent
controls across all the accounts and regularly assess
their account structure as the business evolves. Okay, so as I mentioned, organizations can be used to
deliver authorization policies and that's part of identity
and access management. So I'm gonna turn it over
to Peter to talk about IAM. - So one of the core primitives on AWS is identity and access management. Every API call that your
software calls into the cloud is discreetly authorized and
authenticated using AWS IAM. In fact, at the scale that
we're operating today, we're authorizing over a
billion API calls per second. That puts us in trillions per day. And it's fundamental to understand how these things come together. AWS IAM is a question of who is doing what
actions to what resources? Pretty simple stuff. Who is doing what actions
to what resources? And when you think about
establishing that concept, you have to have strong authentication. And I urge you to avoid
indefinite credentials. Before we had federation, before we had the STS service where you could get temporary
credentials to call the cloud, we had something called IAM users. If you're starting off
today, do not use IAM users. Federate your identities. If you already have IAM users, make sure that at a minimum you are rotating those
credentials regularly. Like secrets that you might need to call a database from
an application server or any of another variety
of types of secrets, API keys to call other services. You must have high velocity
rotation of those secrets. And again, avoid IAM users. If you're calling AWS
from off cloud or on-prem, we have a new service
as of a few years ago called IAM Roles Anywhere that allow you to use an X509 entity
certificate, a digital identity, and exchange that for temporary
time bound AWS credentials that can be used to call AWS APIs. For your humans instead of
having a username and password to log into the AWS
console using an IAM user, you can federate your identity. Federation means having
an identity provider in your own house. Your own company already has something like Active
Directory or Intra Online. Being able to federate that identity to the cloud means
exchanging that identity. We give you back temporary
time-bound credentials that are scoped exactly to the authorization policies associated with what is called a role. And again, I must emphasize, get rid of your long-term credentials, move towards a place where
everything is time bound and that you are using federation and services like IAM Roles Anywhere to always use temporary credentials. And so we have a service that can help you do this with federation. There are other choices in the world and you may already be using them, but if you're getting started, using AWS IAM Identity Center
is a great way to do this. IAM Identity Center allows you to converge your own
identities into this idea called Identity Center on the cloud. Using Identity Center, you can develop what is
known as permission sets and assign those to accounts, allowing you to connect a
bright line between this person or group to this set of
authorizations to that AWS account. IAM Identity Center can make managing all this much, much simpler. And by connecting it to your
corporate identity provider, you can use existing tooling that you have for movers, joiners, and leavers. So as people change job roles
when Dave from accounting goes over to the treasury department, that you lose certain
permissions and gain others. And again, IAM Identity Center can help bring those together. And I must repeat again
and I'm repeating it because this is the number
one source of bad days for our customers on the cloud. Get rid of your IAM users, move towards temporary credentials, but you're also gonna have
non-human need for credentials to call AWS APIs. Not a user who's logged
in, but a workload. A workload may be running on EC2, our virtual compute service
and AWS Lambda, our serverless, and any one of our container services, ECS or Kubernetes with EKS. Each one of these compute
primitives has a way to automatically introduce
temporary time-bound credentials to the workload itself. This allows you to associate an identity with where the software is running so that the software
can automatically obtain temporary time-bound
credentials to then call APIs, maybe write something to Dynamo, maybe invoke infrastructure
on your behalf. And by using these built-in primitives, you can avoid doing dangerous and dare I say reckless things
like putting credentials into your software directly. Do not store your
credentials in config files. Do not store your
credentials in repositories. Use the built-in primitives of AWS to introduce dynamic on
demand time-bound credentials throughout our compute fabric and associated with
each of these IAM roles that the credentials correspond with is a series of authorizations, authorizations written
in a policy language. Enforce lease privilege. If you don't know what
your piece of software needs to use S3, find out. If a developer brought you a container and the container was 10 gigabytes and the developer said to you, "Well, I didn't really know
what packages I needed, "so I put 'em all in there,"
you'd say that's crazy. In the exact same way, don't permission your
software with S3 asterisk. Permission your software
with exactly what it needs. Now sometimes least privilege
can mean maximum effort, but we have tooling to
help you figure that out. IAM Access Analyzer is
a very powerful tool that got some very cool capabilities that were announced
today during the keynote to help you refine and understand what permissions are being used. We make managed policies that
are a good starting point, but continuously refine them
down and we give you governance and the ability to have guardrails. Lia talked about these two
interesting policy types, service control policies and
resource control policies. Service control policies, SCPs, are used to govern what
an IAM principle can do. They bound what actions
could possibly be allowed. In the exact same way, a resource control policy
applies to the resources, either everything in your organization or selectively to only certain
accounts based on the OU that contains that account. This idea of Access Analyzer is just one of the
several tools that we have to make this simpler and easier and programmatically addressable. You must continuously baseline and refine the
authorizations that you have. Access Analyzer can help
you discover permissions that are assigned but
are no longer in use. It can also help you discover resources that might have inappropriate access or even access from the public. By using Access Analyzer together with conscious,
business-driven authorization, you can get higher
quality security outcomes and reduce the blast
radius of the compromise of any of these credentials. By winnowing these down, you
can make deliberate choices so that you know exactly who is using what actions against what resources. So again, use this tool Access Analyzer. It's enormously powerful and it gets more powerful all the time. Again, Amy had a pretty good, great announcement this
morning in her keynote. I encourage you to check it out. Service control policies and
RCPs are really effective ways of establishing governance for teams that may wanna manage their own IAM, but the central team needs
to put guardrails around it. Multi-factor authentication is
not optional for your humans. Get away from usernames and passwords. This takes investment, it can take time, it means maybe some
training for your users, but the dividends are enormous. You can unsubscribe from
entire classifications of risk and threats simply by using MFA and no longer relying on
just usernames and passwords. And finally, where
there's a special version of the way we provide credentials
to EC2 mentioned earlier that the compute fabric itself has a way of associating the identity. Where we introduced dynamic
credentials automatically. Version two came out six years ago. It's very possible, that you
were still using version one. Go home and change that. - All right, I wanna talk
about data protection now and the minimum that you
should be considering for your organization. So when I was in SA, I saw a trend. Most organizations don't truly know what sensitive data they
have and where it resides. And I've seen this pattern repeatedly. You create a solid data
classification policy on paper and then your data
volumes grow exponentially outpacing any manual efforts. Developers and business
units create new data stores faster than security can keep up. And at the end you have this widening gap between your classification
policy on paper and the reality of your data landscape. So we created Amazon Macie to help. Macie is a fully managed data security and data privacy service. It uses machine learning
and pattern matching to discover, monitor and protect
your sensitive data in S3. So Macie provides visibility
into your S3 environment and evaluates your bucket
inventory and policies and can identify configuration gaps, looking for things like
public access settings or unencrypted data. So when you turn it on, you'll see something
like this in the console. You can see one pane of glass, what is public, what's encrypted, how it's encrypted, and what is shared. More importantly, Macie
discovers sensitive data through automated inspection jobs. And you can find a flexible scope to scan your entire environment or focus on specific buckets
based on your priorities. And we talked earlier about how hard it is to manage at scale and sensitive data
normally spans accounts. So Macie solves this by
integrating with AWS organizations. So you can view your data security posture across your entire S3 environment from a single Macie administrator account. And you can use managed data identifiers to detect common sensitive data types or custom identifiers to
let you define patterns that are specific to your business. Macie also delivers detailed findings showing what sensitive
data was found and where. These findings can trigger
automated workflows through EventBridge for
remediation actions. This automation bridges the gap between classification policies on paper and continuous enforcement at scale. So you can maintain visibility of your data however it grows. Okay, let's move on in our
data protection journey. So outside of understanding
the data you have, where it is, we need to encrypt it. And Werner's quote gets
right to the point, "Dance like no one's watching,
encrypt like everyone is." Encryption is not just a security control. It's a fundamental design
principle both internally at AWS and with our most successful customers. And when we talk about encryption, we need to address encryption at rest and encryption in transit. So let's start with encryption at rest, and specifically we're gonna talk about server side encryption. So you have your data
classification policy, now you can align your
encryption strategy. The AWS Key Management Service
makes it straightforward by transparently integrating
with the service you use. It supports AWS managed keys and AWS own keys which handle the overhead of managing these keys. However, you have the option as a customer to create your own customer managed keys that give you complete
control over the key policy and the lifecycle of that key. So I wanna show you an example. Here's an S3 bucket. We're gonna create one. So S3 is encrypted by default, you don't have to do anything. But if you want, if you
want to manage your own key and have control over the policy
and the lifecycle, you can. And that's called SSE-KMS or
server side encryption KMS. And for the third option, while
this may not apply to you, you may have compliance requirements for dual layer server side encryption and that's available in some regions. Now the next thing I wanna
show you is S3 bucket keys. And this isn't a security control per se, this is more of a cost savings control, but I think it's worth mentioning. So S3 bucket keys reduces the cost of S3 server site encryption with KMS 'cause when it's configured, S3 is able to reduce the
number of calls to KMS, therefore reducing your
cost significantly. Okay, now let's move on
to client site encryption. So based on your data
classification policy, you may wanna encrypt your
data prior to sending it to AWS and the AWS Encryption SDK and the Database Encryption
SDK make this approach easier without requiring cryptographic expertise. The encryption SDK handles just general purpose encryption needs and the database encryption SDK extends this to database
workloads for DynamoDB providing field level encryption
that protects attributes. So let's move on to
encryption and transit. What should we look at? Well, first we wanna enforce TLS and we want to enforce TLS
and configure our applications to require HTTPS and reject
unencrypted connections. We should also implement minimum
TLS version requirements. We recommend standardizing
on TLS 1.2 or above. We should monitor for
certificate expiration. Expired certificates
create both security risks and availability issues. And finally, avoid
self-signed certificates. Self-signed certificates don't provide the identity validation that
comes with certificates issued by a trusted certificate authority. So I wanna show you a couple examples on how you might enforce this. So while S3 supports TLS 1.2 or above, it still does support
HTTP for legacy workloads. And you can enforce that
all requests occur over TLS via resource control policy like this. So you can see here, we're denying all S3
actions unless TLS is used. But you also need to think
about your own applications. And ALB can help you with this. There's a few things it can do for you. One, ALB can terminate
TLS connections for you and you can create certificates in the AWS certificate manager and associate it with your ALB. This is really, really valuable. ACM automatically renews
certificates before expiration and deploys it to your ALB for you, so there's no downtime and
no manual intervention. And additionally you can configure an HTTP to HTTPS redraft on ALB. So you don't need to do
this on your backend. So let's check in really quick. First, you should turn on Amazon Macie and get visibility into your S3 data. You should enable encryption
on all your AWS resources and look at the documentation and determine which KMS
key is right for you. And then depending on
your data classification, use the client site encryption, SDK, to perform client site encryption. And then lastly, enforce TLS
on all of your resources. - Let's talk about secure deployments. We've covered some pretty basic
primitives for what you need to get right in the cloud, but the reason you're in the cloud is to deploy software to it. So let's examine what it means to have a secure software
development lifecycle. That your process, that your mechanism of
how you release software to run on the cloud is
itself a very critical place where you will apply security controls and get security outcomes. That it begins with threat modeling. Before you ever open an IDE, before you even kind of
understand the exact architecture that you're gonna end up with, you have to be able to reason about the flow of information
in and out of the application that you intend to design. This idea is called threat modeling. Understanding where the entry
points are for an adversary to do any of the several bad things that they could do to you, tamper your data, corrupt your data, spoof their identity and more. And by threat modeling
is the responsibility of not only security engineers, but you want your application engineers to kind of be able to think this way too. And as they build tests and unit tests and functional tests that the purpose of those tests is not just to ensure that the software works, it's also to ensure that
the software is correct, that the software understands
what it is supposed to do and it will resist attempts to get it to do something different. There are lots of very
important security outcomes that you're going to be able to achieve by developing really good competent tests. Integration with CICD, even
if you're a waterfall shop, the manner in which you
integrate new functions and deploy into your
production environments is another clear point where security has to be a top priority. By building this way,
you can develop agility. And agility is one of the best things about building on the cloud that if you need an extra
computer to try something, you can get it and then turn it back off when you don't need it. If you have a major release and you wanna launch a brand new computer with a new piece of software on it and then slowly move traffic over to it, the right way to do that is with comprehensive
continuous integration and continuous deployment. But as this software goes out, you want assurance that it is
the software you think it is and that the systems that
you're deploying it onto have a sense for what the
software they should be receiving. And that's the idea of signatures. You can sign your packages,
you can sign your containers, and get good end-to-end
assurance about the lifecycle and the entire bill of materials of the components that
you eventually deploy into your production environments. And while ensuring security and production is extremely important, you should have the same rigor
in your lower environments because after all, the
purpose of a lower environment is to prove out and exercise
all of the capabilities, not just of the functional software, but of the release process itself. And then once things are in production, you may need to release patches, patches to your own software, patches to the components
and tooling that you rely on. And all of this fits into a lifecycle. And by delivering security and integrating security
into that lifecycle itself, you can really achieve a
lot of critical outcomes. Now sometimes customers
have come to me and said, well, I'm from the governance team and we've got too many
ways of deploying software, so I'm gonna pick one and I wanna make sure
they can't use the others. And on so many occasions
I've had to patiently explain that while that can be great, disabling these other
pipelines is the last step 'cause you have to be very
careful on this journey that you don't break prod. If you've got rogue teams
deploying software today and you want to get them to do it in the new better, safer way, that has to be attractive, that has to be something desirable. If you go in with a mindset that you're going to
turn it off or break it, number one, you become their adversary, which is not great organizationally. It's not great for their quality of life, but also it means that
you're really talking about breaking something that
the business depends on. And so while there is great value in having a good known safe
pipeline that everybody uses, if you're going to restrict
access to other ways to do it, you do that last. And when we talk about this SDLC and we think about the continuous
integration and the safety and the security outcomes
that you could fold into it, one of the most important and often overlooked elements
is reliable rollback. Yes, it's very cool to be able
to automate your releases, but if you're not
automating your roll back, that is to say undoing change. You're only doing half of the job. We know firsthand that
one of the worst ways to break a system is by modifying it. And yet the business demands that we do, and this is the same for
effectively every organization, new features, new upgrades,
patches, security patches, major releases of software
that is going end of life. Yes, automate all of that, but also always develop the capabilities to automate the rollback. And just like I mentioned earlier, that the purpose of the brakes of the car is not to slow it down
but to let you go fast. The purpose of the rollback, yes, it's safety to be able to undo something, but in your confidence of automating it, you can do it more often
and you can do it faster. This is true for everybody at every layer of the organization. The devs will feel more
confident about trying new things if they can feel more confident
that even if it goes wrong, you can pull it right back by building this entirety of a secure software
development lifecycle, with automated deployment
and automated rollback, you can accelerate your velocity. And again, what we hear from customers is that one of the best
reasons to come to the cloud is to accelerate that velocity. And so the operations of this kind of idea of having a secure software
development lifecycle is the operations itself
that I mentioned earlier, that the responsibility of these things is not just with the security department, it's with the people that
own this tooling as well. That by automating and refining
these systems over time, that you can all work together in partnership, in collaboration, not adversarially, to get high quality
outcomes for the business in the form of higher
velocity feature release and enhanced safety and security
at every step of the way. - All right, let's talk about
monitoring and alerting now. And what do we need to consider? First you need secure logging and it should span from
infrastructure to your applications and you need to have automated checks that continuously evaluate
your security posture and then alert on anomalies
and audit findings and create automated playbooks
to respond to those issues. You also need to have
centralized visibility across your entire environment. Security events don't normally
respect account boundaries. So implement centralized monitoring that aggregates all those findings from all your environments. And let's talk about how we do this. So first and foremost is CloudTrail. CloudTrail should be the
first logging you enable and it should be enabled on every single one of your accounts. It captures all management
event API activity, whether actions are
taken via CLI, API, SDKs, or AWS services making
calls on your behalf. And for deeper insights, you can opt into data events
for specific services like S3. After working with hundreds of customers, I can tell you that having
this historical record is invaluable during investigations. So let's talk more about the monitoring
infrastructure changes. This is so important for
maintaining your security posture. Evaluating resource compliance, excuse me, is an ongoing challenge
in cloud environments that are constantly changing. You need to create tooling for continuous assessment
of your resources against your security
controls and best practices. And managing this at scale becomes increasingly complex
as your footprint grows. Lastly, reducing manual
errors and interventions is where automation
delivers significant value. When systems detect noncompliant
resources automatically you allow your developers freedom to innovate within the defined guardrails. So let me introduce AWS Config. This is our service designed specifically to address those infrastructure
monitoring challenges. It records configuration
changes as they occur and evaluates them against your rules, giving you real time visibility into your compliance posture. And to manage compliance at scale, config rules can be deployed
across all your environments because they have integration
with AWS organizations. So when non-compliant
resources are detected, config can trigger automated workflows to correct common issues. Now let's talk more
about the logs you need to consider in your cloud environment. We talked about CloudTrail, but we also need to be monitoring and correlating activity against DNS logs, network logs and audit logs. And there's real challenges
with monitoring logs. You need to analyze security signals across multiple data sources because logs in isolation
create blind spots and you need to correlate threats across different log types. An incident often leaves
traces across various systems, network traffic and VPC flow logs or API calls and CloudTrail. And connecting these events is hard and finding a needle in the haystack of security events is
increasingly difficult as your data volumes grow. And GuardDuty helps address
these monitoring challenges. It combines machine
learning, anomaly detection, and integrated threat intelligence to identify and prioritize
potential threats. And it automatically ingests
logs from multiple AWS sources including CloudTrail, VPC
flow logs and DNS queries. So you don't have to. GuardDuty continuously
analyzes these events, correlating information across sources to detect suspicious patterns and when threats are detected, GuardDuty provides actionable findings that include severity ratings and recommended remediation steps. So we've covered everything here so far except for centralized visibility. So let's talk more about the challenges with cloud environments and
how you can overcome them. So we've already covered
some of these challenges, but when you have a cloud environment with multiple accounts, you
have a lack of visibility. It can be really hard
looking across environments and there's so many different tools and data sources, vendors, and your teams get alert fatigue
from all of these alerts. And finally, logs and alerts and varying formats are
scattered across the organization and tough to find silos. So to address this and to address the centralized
visibility challenge, we created Security Hub. So Security Hub serves as
your single pane of glass for all of your AWS security postures. It aggregates findings
from our security services, some I mentioned already like GuardDuty, but also Inspector for
Vulnerability Management and Macie, that was for
sensitive data discovery. And it does all this in one unified view and it doesn't just collect all this data. It integrates with AWS Config and automates compliance checks against industry standards
and best practices. And this highlights misconfigurations that could lead to security events and all this, it creates a
centralized visibility you need. So here's a practical example of this. Here's the dashboard. This is for AWS Foundational
Security Best Practices, and you can see like I
have all of my controls and you can see which controls are failed and then you can click
into each one of those and get more detail. And this is all in a single pane of glass. So let's check in. What should we be doing? We should enable CloudTrail
for all accounts. We should use Security Hub
for that single pane of glass and ensure compliance with
the security hub standards and that integrates with Config and then we should be using Config and we can create our own config rules for our own customized detections and then enable GuardDuty for detection. So I'm gonna turn it over to Peter to talk to you about vulnerability management, threat detection and incident response. - So even the best organizations that are really high performing and getting a lot of this right still have to maintain their environments. They have to maintain their environments by managing emergent vulnerabilities. And even if they get that right, the idea of incident
response is fundamental. You will have bad days inevitably. And vulnerability
management requires agility in the exact same way that we talked about speed to deliver new
features and capabilities using a great high
performing pipeline and SDLC, those same mechanisms can
help you develop agility to patch and update your systems, keep your versions current
beyond just patching. At some point, even if you're
good at vuln management, you will need to deal with major releases, whether that's a database
engine, an application framework, even operating systems, that is necessary for a high
quality security outcome because there will come a day that there will be no more patches for the version that you're on and you will get squeezed by vendors. Some vendors will charge you even more. We keep certain versions
alive here at AWS, but it becomes more costly. We want you to stay on
current versions of software and your developers want you to stay on current versions of software. By and large, new versions
are gonna be better, more feature rich, more stable,
higher quality outcomes. And so vuln management
needs to be a holistic thing that you're not just responding to a new CVE common vulnerability, you're also responding to evolution in the software that you rely on, but you need to know what
software you're using and where it is. We were all taught a very hard lesson when Log4j happened a few years ago, but we were able to respond because we knew where we had used it. If there's a new vulnerability tomorrow in a particular module, you don't know necessarily
where you need to go do the work if you don't have good
situational awareness of the software that's
operating in your environment. And that means building and maintaining a strong asset inventory of what software your developers are using and where and how it's used. And I say where and how because you need to be able
to make reasoned decisions about the speed with which you respond to new vulnerabilities, that the CVE score is
just a starting point, that it may be a high score and it may be internal audit is coming and telling you you
need to patch everything eight and a half and above. But the right way to run a
security program is to be able to reason about whether or not the eights and the nines are
actually dangerous to you. It may be that the nature
of the architecture or where it is deployed internally within a closed off network or publicly anywhere on the internet changes the exploitability
and therefore the severity of any given vulnerability, even two, that might otherwise have the same score. So make reasoned decisions
that include the context of how the software is deployed
and where it is deployed. And if you get good at
continuous integration and continuous deployment and you get good at distributed systems, it actually means you can
respond to vulnerabilities faster because again, anytime you're
making change to a system, you are introducing the potential
for something to go wrong. By having anti-fragile systems
designs in the first place, you can reduce the risk
of the necessary activity of changing a bunch of things at once in response to a vulnerability. Now if you don't have
this kind of visibility or you're looking to improve it, we've got some software that can help. Amazon Inspector can give you visibility into not only what's
running on your EC2 fleet, but also in your Lambda
functions and in your containers and identify pieces of software that may have serious vulnerabilities. And we are continuously
improving this software. And so Inspector began
life as just listing CVEs that were installed on a box, but today can introspect your own software in your own Lambda functions and give you a heads
up as to whether or not there might be some problems there. It can also help you maintain
operational visibility across your entire environment, that this idea of producing and publishing software bills of material become more and more important to perhaps your downstream customers who are going to expect you as part of your compliance program or as part of a regulatory program to be able to produce
software bills of materials. And Amazon Inspector can help you do that. I mentioned earlier that
a continuous integration and continuous deployment is a place to apply a lot of security and Amazon Inspector
fits in there as well. We can help you scan lambda functions, we can help you scan container images and everything in between. It's a very powerful tool and there's lots of tools that do this. This one is AWS-ified. We hear from our customers that they really like that about it, but of course preventing bad
days also means expecting them and that the time to prepare for the rain is while the sun is shining. If you attempt to figure
out how to respond when you are being demanded to respond, you will have a bad time. Making decisions under duress
or in the middle of the night leads to unhappy engineers
who might just leave the second or third time they're paged to a call in the middle of the night and no one knows what to do about it. It also leads to low quality
outcomes for your stakeholders, whether that's the board
or the shareholders, the PE guys, whatever, that you need to rehearse and plan how to respond
to events great and small before they happen. And this takes work and this takes rigor. You can automate tasks around this, but I urge you to be very cautious and mindful about automating decisions. And so automating response
to events is great. Automating decisions that
require human judgment and management authority should probably not be
left up to the computer. If you're just getting started with this or you're kind of tired of
being in the business of it or you'd like some help, we
have a terrific managed service. A managed service that's
not just software, although there is some
very clever software that's associated with it, that we've gotten really good
at customer incident response. A lot of customers have done
a lot of different things and had a lot of different
types of bad days and we've learned a lot from that and we have a managed offering
that can help you do this. There are lots of ways to get help. This is a really good one. - All right, in security,
we are never done. We are continuing to look at our controls, our processes, and our systems and building and improving
mechanisms to continue to raise our security bar. But continuous improvement
isn't just security and at AWS we know that understanding what good looks like across
your entire environment is hard. And that's why we created the
well-architected framework. And we have a pillar dedicated to security to help you after today to
understand what good looks like for security and other pillars. We covered a lot of ground today, but if you remember nothing else, focus on these 10 foundational
security practices. So I'll step through them really quick. First, culture of security. It's non-technical but
it's so foundational and everyone needs to think about it. We actually had a talk on this yesterday, so if you missed it, there will be a recording that
you can go back and watch. Next, enable MFA. It's the simplest, most effective control to protect yourself. And third, eliminate long-term credentials and hard-coded secrets. As Peter emphasized, this
is critical leverage. IAM roles and IAM roles
anywhere to provide temporary, automatically rotated credentials and use secrets managers to manage and store any
other remaining secrets and implement the, excuse me, principle of least privilege. Yes, this is challenging
and labor intensive, but is absolutely essential. IAM Access Analyzer is your ally here. It helps identify overly
permissive policies and unused permissions so you can systematically
tighten access controls. Number five, encrypt data
at rest and in transit. This is non-negotiable
in today's environment. So take the time to
understand encryption features specific to each service you're using and how they align with your requirements. And then implement a
multi-account strategy with AWS organizations. This gives you clear separation of environments and workloads. Also it allows you to implement
tailored security policies based off the specific risk
profile of each environment. And then enable CloudTrail
in all accounts. You should be monitoring all of your logs, but this is a non-negotiable baseline. And then you should be regularly patching and updating your systems. Number nine, implement security scanning, detection and remediation capabilities. And you can absolutely build
a lot of this on your own. But services like Inspector
and GuardDuty and Macie and Config are here to help, and finally centralize
your security findings and compliance checks 'cause it's hard doing this in this multi-account environment. You can also spend time
building out your own, but Security Hub is a really,
really valuable resource here. - So again, back to the top. I showed this slide earlier that good security programs
continuously improve and we've given you an
overview of those areas that demand your attention, your care, your rigorous obsession that in getting these things right, call them core competencies, are exactly what good looks like and none more important than a
set of norms and expectations for how you think and behave
that you could call culture. That the culture of security deserves to be part of your organization. And your organization deserves
a culture of security. And so do your stakeholders. So do your customers,
so does your auditors, and so does your board, that this culture of security
can pervade everything you do, that its security is not an adversary to product engineering. That it's not a team that
shows up late and says no, that it is a partner that
is there at every step of ideation and development
and product market fit. That security was part of it all along. And depending on the organization
that you're a part of, depending on the business
that you're into, maybe audit and compliance is too. That the truth is you
all want the same things that you want repeatable,
high quality outcomes with a clear explanation
of how things work and why you made the
decisions that you do. Every engineer wants that. Every auditor wants that. This idea of the security
organization making it easier to do the right thing and harder to do the wrong thing. Set expectations, make clear what is
acceptable and what is not, and perhaps most importantly, give those teams the funding and the direction that they need in order to enable truly
what good looks like. Thank you so much for being here today. - Thank you. (audience applauding)
