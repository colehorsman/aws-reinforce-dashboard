# AWS re:Inforce 2025 - Maintain business continuity using AWS Backup and Multi-party approval(GRC304)

**Video Link:** [Watch on YouTube](https://www.youtube.com/watch?v=Na2614X0ogo)

## Video Information
- **Author:** Unknown
- **Duration:** 35.8 minutes
- **Word Count:** 6,334 words
- **Publish Date:** None
- **Video ID:** Na2614X0ogo

## Summary
This presentation by Alex Merida and Vivek Mishra from AWS explores advanced data protection strategies using AWS Backup and Multi-party approval. The session addresses the growing challenges of data protection, ransomware risks, and business continuity, introducing innovative solutions to secure and recover critical organizational data.

## Key Points
- Data Protection Challenges:
  - Exponential data growth (expected to triple from 2023 to 2028)
  - Increasing ransomware threats
  - Average downtime from ransomware attacks exceeding 20 days
  - Potential millions of dollars in losses and reputation damage

- AWS Backup Key Features:
  - Centralized data management
  - Automated backup and restore capabilities
  - Logical air-gapping solution
  - Ransomware-specific protection
  - Cross-account protection
  - Restore testing capabilities

- Multi-party Approval Innovations:
  - Requires multiple authorized individuals to approve critical actions
  - Eliminates single points of failure in decision-making
  - Provides additional security layer
  - Creates clear audit trails
  - Integrates with AWS Identity Center

## Technical Details
- Recommended Recovery Architecture:
  - Use two separate recovery organizations
  - Create Multi-party approval teams in a recovery org
  - Share approval teams across accounts using Resource Access Manager
  - Implement minimum approval thresholds (recommended: 2 out of 3 approvers)

- Data Protection Strategy:
  - Set up logically air-gapped vaults
  - Implement strict access controls
  - Use service control policies to manage team usage
  - Establish retention guardrails for backups
  - Enable continuous monitoring and recovery testing

## Full Transcript

- So good afternoon, everybody. My name is Alex Merida. I'm a senior product manager
here on the AWS Accounts team. Sorry, we're jumping ahead a second there. - Vivek, do you wanna introduce yourself?
- Hi, my name is Vivek Mishra. I'm a senior product
manager in AWS Backup. - And today we'll explore how AWS, or how AWS Backup and Multi-party approval help you build resilient, secure, and recoverable data strategy, even when anything else fails. So we'll talk through a little bit of the business continuity
and data protection, AWS Backup logically air-gapped vault, its integration with Multi-party approval, show data recovery in
a cyber event scenario, and then do a demo, and then
follow up with a quick Q&A. So I'll hand over to
Vivek, and he'll start. - Yes, sir. Thank you, guys. So to set the context, we are really here to talk
about data protection. Both Alex and I are on different teams, but our real motive is, how do we ensure there is data protection so that you have business
continuity in your enterprises, in your businesses, and all that. But to understand what it really means, well, data protection
is simply the process of safeguarding your data
from corruption, from loss, or any other kind of compromise, and then have the ability
to restore that data to a functional state so that you can have
your recoveries happen, you can have your business continue. That's how we sort of define that. It's not just about
protecting it, encrypting it. It's also about being able to restore it so that you can make use of that data. Now, why data protection is important? Because data is going tremendously. It's actually exponentially
going from 2023 to 2028. It's almost going, like,
more than three times. It's just like, as I see it, it's just like dirty laundry that nobody really wants to deal with it. But unlike dirty laundry,
data is extremely valuable. In fact, I would even say
that in last few years, the GenAI and machine
learning use cases opening up, it has even become more valuable because now enterprises
are actually diving deep. All that data that was vast, unused, sitting there doing nothing, actually enterprises are
making use of that data. An example would be, like,
RAG-based models, right? What they're really doing
is exposing that data, giving you more context-rich answers so that you can unblock more use cases, do some innovation with that data, and make use of it. So if you look at it from a
Uber perspective, it has value, then really it needs protection for your regulatory,
compliance, business continuity, DR, you think what? But designing this data protection
solution has challenges, there are opportunities, and today we're gonna
talk about this launch, which will actually tell
you ways of getting there. So one of the challenges in, one of the challenges for data protection is, of course, ransomware. And I think everybody out here knows, I'm not gonna explain
it, what it really means. It's been there for the last 15 years, challenging the industry to
go build the right solution so that you can protect your enterprises, you can protect your data. It has become so mainstream, like, it has even become commoditized that really the bad actors
don't really have to do much. They can just pick up a
tool and start getting in and trying to hack you and
then demand ransomware. So from our perspective, what we think, it's certainly a big
challenge for the industry, big challenge for enterprises who are trying to actually move forward, have business continuity, but they need solutions. They can't build this on their own. And if you think about it, how ransomware is progressing, the average downtime is now
even longer than somebody, people keeping their New Year resolutions. And in actual data terms,
probably more than 20 days. And 20 days could be sort of
an eternity for a business because it can mean
millions of dollars of loss just because the business
is not an up and running. So in totality, it's the loss
of not only just ransomware that the enterprises
might be having to pay. It's about loss of reputation,
the loss of recovery, and all of that combined makes
it a pretty hard challenge for enterprises. But it's not all gloomy. Yes, we understand it's a big challenge, but it is also something that the industry is very keenly focused on in providing the right solutions so that customers can move on. And actually, customers have
very high awareness of it. Like, it's testament to that
is that you guys are here, you are interested in this topic, is the fact that the customers are aware and the industry itself is trying to find the right solutions. So we'll talk about what we're gonna do with the launch today
to address this problem. But to set the context again, we'll start about with
a AWS native service that tries to address the risks, well, which is sort of there
with ransomware attacks. So, because it's important
for you to understand what that service is because the solution that
we're gonna talk about is very specific to that. So, like, I'm talking in somewhat
of a broad general areas, but we're gonna actually focus
down to the exact solution that we are gonna present today. So AWS Backup, that was
released back in 2019, was launched to meet the customer need around data management so that they could automate, centralize, all of that, in one place. You can think of scheduling your backups, how do you restore them, how do you do compliance
auditing, reporting, all of that, as a native
capability within AWS and as something that you
can do it at one place in a simple solution and don't have to do too much
of heavy lifting to get there. It has capabilities around, like I said, backup and restore are
its core capabilities. It has even ransomware-specific
protection capabilities. You can think of how it does
locking of your backup data. It has cross-account
protection capabilities, KMS-based encryption access policies, and then we launched this
air-gapping solution last year. Plus, it has this restore
testing capability so that you can actually go verify if your backups are clean, what's your RTO in terms of how you can
get those backups up, and automate that in a single plan. So, we can dive one more level deep because this is the core functionality that we're gonna talk about. So the AWS Backups as a service also has this logical
air-gapping solution. What it really does is it
provides the level of isolation that you may not usually get, and it provides accessibility. So it tries to solve two problems. Are my backups isolated enough? Yes, you can isolate them
today with many capabilities, but it adds a few more layers. And then if I'm there facing an event, how do I get my backups
out in a fast enough time so that my business is not disrupted? So it does that today, provides that as isolation
through service-owned encryption. The backups themselves
are in service accounts, so that if your account gets compromised, your backups are still there, lying there, so that you can recover
them as you need them. And then from an
accessibility perspective, there are a couple of features. One of them is the one
we are announcing today and then another is the RAM-based sharing. So that if you need to recover fast, you can share your air-gapped vaults with other accounts
within your organization so that you can directly
start the restore process. You do not have to wait
for copying all the data to that another pristine account and then start your restore. So basically, those are the two things that it tries to address, and yeah. - Thank you, Vivek. So as Vivek mentioned, a lot of the times with AWS Backup, we run into some typical
traditional customer issues around traditional recovery. One is backups typically share and recover the same authentication boundaries, which helps risk a
single point of failure. And when you look at from the account and organization perspective, you are losing the opportunity and the ability to recover those backups, which leads to slower times of RTO, leads to impacting business continuity. So with that, we're happy to
introduce Multi-party approval. So what is Multi-party approval? Multi-party approval, excuse me for that. We heard from customers that
they wanted a better way to protect critical AWS operations from being executed unilaterally. So we delivered Multi-party approval. What it does is it helps guard against these specific protected APIs, and what you do as a customer is you define approval teams
made up of AWS human identities through AWS identity center. They will vote and approve, vote to approve or
reject any of the actions that are put forth. This goes beyond
traditional access controls by requiring multiple
authorized individuals to approve an action before it's executed, even if that same IAM principle has necessary permissions to do so. So what are some of the benefits
that we talked about here? So first, you have an
additional layer of security for your AWS organizations. We eliminate single points of
failure for indecision making, reducing the risk of unauthorized
or accidental changes. We also, with this, align with the principle
of lease privilege. Secondly, we centralize and standardize our approval workflows. So we're helping customers
replace these disparate or non-AWS native approval workflows by bringing them internally, helping to enforce maybe internal policies and integrations with
other AWS native services like Identity Center,
like AWS organizations. And thirdly, we want to help and maintain clear audit trails. So we automatically log all of the approval and rejection actions that those individuals have taken. And secondly, we help facilitate compliance
through some of the, through publishing to CloudTrail, so that way you can get
access to all of those events. - So with that, so now that you understand
what Multi-party approval is, we have integrated
logically air-gapped vaults with this capability that
was launched yesterday. And what this capability really does as an integration with air-gapped vault is that we are leasing that trust of getting access to those backups to highly privileged individuals
in your organization. So if you are able to form the right set of multi-approval teams, what you will get is an
ability to get access to those backups at the time of an event so that at the time of a crisis, you're not running around
trying to figure out what permissions I need,
who should I trust. The trust is actually set
with that multi-approval team who can then decide as per the
request that is started off that I need to go access this data, which is lying in a different account or even if in a different
organization of my account, and then start my recovery process. Or even if you do not any
longer trust that organization or for that account, you can actually transition your backups from that air-gapped vault to another vault within
this new organization or a new account that you have set up. And that's a new feature that
we have launched yesterday. - So really quickly, I want to go into what does
the Multi-party approval integration architecture kind of look like before we dive into specifically what logically air-gapped
integration would look like. So we're gonna walk through
four different personas today. The first two personas, I do want to call out ahead of time that these are one and done actions. Like, you set them up ahead of time and then after that, the approval team will not
need to be re-associated to that same resource. So first, we have our
Multi-party approval facilitator or our Multi-party approval admin. So what they'll do is they'll
create that approval team within Multi-party approval. They'll invite the IDC identities
that they've identified and put those in the approval
team which will get sent out. After those approvers have accepted their invitation to that approval team, the AWS Backup admin would come in and associate that approval
team at the resource level, saying, "We want this approval team to protect this specific
logically air-gapped vault." The next two personas,
this happens all the time. You don't need to set this up. This has already happened since Multi-party approval
has already been created and associated to the resource. So you have your recovery user. Your recovery user will initiate one of those protected operations. So if they try to restore one of the logically air-gapped vaults or mount them to a new location, they'll invoke that protective action which triggers the
Multi-party approval workflow. Lastly, you have your fourth persona which is Multi-party approvers. What they'll do is those approver, they'll log in to an IDC access portals, a managed first-party
application that we're providing. Using your IDC credentials, you'll log in and either approve or reject
the action that's been called. If the vote passes, the action that was invoked will execute. If the vote fails,
we'll have the opposite, the action will fail. I'm gonna pass back over to Vivek.
- Sure. So how will you go about incorporating a Multi-party approval team
into air-gapped solution, and then how do you set it up? So there's a very simple
reference architecture that I have here. So really what we would recommend any customer who's onboarding to this is to have two separate recovery orgs. And the reason for that is even if one of those
recovery orgs is compromised, you still have access to the data. Quite simply, if your
primary org is still intact, there is no problem. You can continue running your business. But if your primary org is compromised, then you have your recovery org which can initiate those workflows so that you can get
access to your backups. So what we would recommend
as a reference architecture is that you set up your
Multi-party approval team in a separate recovery org. You can always do it in the primary one. You would get all the benefits
of an account compromised. But in a situation where your organization
itself is compromised, then you would have problems
using that workflow. We are also trying to solve that problem, but that may come in some
near future, not today. So you start by setting up
your Multi-party approval teams in a recovery org. You have your data in your primary org, all your workloads are there, your air-gapped solution
has all the backups. And then you assign that approval team to your logically air-gapped vault, so now they talk to each other And once you do that assignment, there is no management account, there's no control anybody
has after that point in time to break this association. Only the Multi-party approval
team has the authority to break this association. So if your account or
your org is compromised, the vault will still
honor that association. And then what will happen is, let's say at the time of incident, you can choose a recovery org, in this diagram, I've
just shown a recovery org, which is the same, but you can actually
choose a recovery org, create an association
of that approval team with a recovery account, which is simply using a
Resource Access Manager, which is RAM, and share that MPA team with that account so that it's an authorized request. By authorized request just meaning no XYZ person can just come in and say, "I need access to your air-gapped vault." No, that's not gonna happen. Unless the management account is sharing that MPA team
with the recovery account, there is nowhere the
request can be initiated. So once that step is done, then the recovery account
can go set a request, "I need access to this air-gapped vault," and then the request
will go to the MPA team, and MPA team, minimum number of approvers
will need to approve it. And once that's done, the
linkage will be created, and that linkage or that logical
vault that we have defined is called a restore access backup vault in your recovery account, which you can simply, like we'll show you in the demo, but you can simply from that point onward start restoring your backups, or you can actually copy those backups to yet another different account
within your organization. And the same model can
work from the primary org. This situation is basically
where your org is still intact, but your backup account and your workload accounts
are actually compromised, and you really need to start doing it without trying to create
yet another recovery org, which is basically an
extension of the same workflow. So that was sort of the, let's say, recommended
reference architecture. But if you have to all put this together, how does air-gapped
vault today try to solve, I think there were two problems
that we're trying to solve. One is the problem we just talked about, which is how do you set up your recovery using Multi-party approval teams. And then the second one is essentially the existing use case that we
actually launched last year, is how do you actually
go test for the data that is out there using
restore testing capability that the platform already has. And that you can actually just use the lightweight RAM-based sharing model. So you can actually share
your air-gapped vault with other accounts,
your forensics account, using RAM-based sharing, and you can directly restore your backups using a restore testing plan and just do all your forensics, do all your cleanups, do all the reporting and audit compliance reporting, so that you understand
whether your data is clean, you understand what is your true RTO, and just go from there. You don't have to do, so left side is slightly
more heavy lifting because it's meant for
a very specific use case where you're trying to
recover from an event, whereas the right side is more about how to do day-to-day operation, knowing the health of your backups, trying to understand the
true RTO of your backups, and so forth. Okay, I think with that,
we can move to the demo. Just to give you a sense so
that you don't get overwhelmed, there are actually this
nine different steps, but there are really
three different groups. In the first group, we'll try to show you how a Multi-party approval
team is created and shared so that it can be made use of. And then we'll show you how
it actually is integrated with the AWS Backup. And then lastly, how do
you actually go perform an actual recovery using this integration. - [Alex] Yeah. - [Vivek] I think next slide and... Just, this we won't need. - Awesome, so I'll walk
through that first step, which is gonna be creating a
new Multi-party approval team. So the first thing we're gonna
do is we're gonna navigate to our normal AWS Management Console and click on AWS Organizations. From here, you'll find the
Multi-party approval console. From this screen, you can see that this is how
you navigate here, set up, and we recognize here that we need an active Identity Center instance. So from this, we're gonna go ahead and just click on our second tab and show that we already
have set up an IDC instance for the purposes of this demo. But just want to quickly show
that from this perspective, like, we have three users that we'll add to the approval team that
we'll use in this demo. And people might be wondering like, why are we using AWS Identity Center as a way to get approvals done, right? And the biggest rationale behind that is we wanted to be able to tie
the approvals or rejections to an actual human identity. Right now, with IAM rules, like, it's a little bit
trickier to track that down. So this is our first, like, product. This is our first iteration
that we're starting with, but we have been hearing already
from customers that like, "Hey, we wanna really explore what else we can do outside of this." But like I said, to start,
we're gonna do Identity Center. So moving forward. So from here, we're gonna go ahead and create our first approval team. So you see from below, the identity source that we
showed in that second tab has already been automatically attached since Multi-party approval did recognize you already have an IDC instance there. So we're gonna give this a team name, we're gonna give it a description. And then from this perspective, we'll go ahead and add approvers, and we will add those
three different IDC users we showed from that tab. Again, tying back to that
human identity portion and you might be wondering, well, why are we showing three? Right after this, we show how we're gonna
set the minimum threshold that we require for an
approval to actually pass. Our rationale behind this is we wanted a minimum of two approvals to occur on any related action. Because what we didn't want to happen is the person that's executing the action to also be part of the approval team and then can just approve
themselves doing the action. It would defeat the purpose
of what we're calling Multi-party approval. So here you could see we set
a minimum of two threshold, out of three, so two of these will have to approve, and then we've created the approval team, which has now moved into a pending state. In the pending state, that
means emails have gone out to each one of those
Identity Center users. They'll receive an email, a notification, where they'll take that email and log into their Identity
Center credentials. So next, we're gonna move
into accepting an invitation in what we're calling the Approval portal. Like I mentioned, we're
not gonna show here from the email perspective, but we're gonna do it a secondary way. So what you can do is you can
go to Multi-party approval and look for the Approval portal URL that's located within IDC. Sorry, and here we're showing how the team is still in a pending state. So like I said, we're gonna go here and we're gonna move to
our access portal URL. And in our first set of credentials. And we're gonna go ahead and federated right into the Approval
portal then from there. Now to orient you to what you'll
see on the screen just now. So in the access portal, what we have is we have two separate tabs. We have the Operations tab
and the Approvals teams tab. You can see here under the
Approval teams invitations. We can accept or decline this
operation from within inline. But if you click into
the Approval team itself, you can see some of the details that we entered when we
created the approval team. Like the name, the description. You can accept and decline the invitation from this view of point as well. Or like I said, we go back and just press Accept from here. And once we accept our invitation, that approver that has
accepted the invitation, their status will change
to successfully accepted. But again, the team will
still be in a pending state because not all three have. For the purposes of this demo, we won't show you all three
approvers doing the acceptance, so we moved the team into an
active status at this point. All approvers have accepted. In the event that an
approver does not accept, you will actually have
to add a new person, and the team will stay in a pending state. And everyone that has already
accepted will have to go in and re-accept their invitation here. So we could see back in the access portal, when your team has
entered an active status, if you were to log in, you can see here that here is your
Multi-party approval team that you're a part of. And the next thing we'll show real quick is how do you actually share
a team with another account using Resource Access Manager. So again, I think when
we've been talking through all these, like, things around
logically air-gapped vaults and AWS Backup, it's like why did we want to
make sure we could share teams to a different account or
a different member account. And it's all about the
availability perspective when it comes to backup, right? We want to be able to make
teams highly available and the backups highly available as well, so that way there's always
that chance of recovery even when everything goes wrong. So from a Resource Access
Manager perspective, you see, you know, we're
giving a name of the share, what kind of managed permissions
come with the sharing. You get all our typical permission sets that are already created
with Multi-party approval. You can share it from an
account-based perspective and IAM identity-based perspective. We have not restricted any way of how you wanna specifically
share those teams. But from this perspective, obviously we're gonna
share it with the account where the logically
air-gapped vault lives. And we'll move forward. Obviously, with all Resource
Access Manager sharing, you're gonna make sure that
everything looks correct and then go ahead and
create that resource share. And we get our successful. All right, and then I think from here, I'm gonna hand it over to Vivek to walk through.
- Yeah, so I think the last part to this is now the account to whom you share the
Multi-party approval team also has to accept the invitation. It's a standard process of how RAM works. So the last step is that
you accept that invitation and then you're good to go. So these steps basically cover the part where the Multi-party
approval team is created, ready to go, shared with
all the relevant accounts. And you can actually do
this at any point in time, even later, when recovery
accounts need to get access to it so that they can start the initiation. Now, one of the first things you will do when you come to the backup side, so this is yet another
protection layer that we have, is you simply just can't use MPA team just because somebody
has already set it up. To be able to use Multi-party approval, the management account has to
first enable it as a feature so that you first set things up correctly. You can set up SCP policies before anybody starts making use of. So let's say you've created five teams. You don't want every other
account to start using it just because you shared it
across your organization. You first have to enable it as a feature. And before you even enable
it, you'll set some policies so that the right use of
that team can be done. And I'll give you an example
of how this can be done. Like, one shows small
example of how it can be done with a service control policy. In the policy, you can basically restrict which team can be used
by certain resources, in this case, it will be air-gapped vault, and what is the action that it restricts. And the action it restrict is associating a Multi-party approval
team with air-gapped vault. So what you can do is that you can create a service control policy. And I just have a blurb here is because this functionality
wasn't working a month back. So what I'm doing here is essentially, I have that Multi-party approval, which is the one which we just created, and then I'm saying that
its effect is denied to all resources which exist. And now this is where you
can essentially constrain who's able to use, which
teams, and so forth, so that you can manage it centrally in a more organized way rather than everybody
trying to use everything, and it just becomes more difficult. So once you have done
that, you have enabled it, you have set some policy, you can now associate your
air-gapped vaults with this team. So the first step is
actually going creating a logically air-gapped vault, which is actually extremely simple. This just has a few fields. What you'll go is you
will go into the console, you will go create a new air-gapped vault, you'll set its name, and then you'll add the guardrails, which is the maximum
and minimum retention. Just for context, minimum and maximum
retention periods are nothing but they just act like guardrails so that you don't get accidentally backups into an air-gapped vault
when it should not be there. So if you have backups which are supposed to
be living for 10 years, you don't want to get
into an air-gapped vault because they'll be locked for 10 years. So you can set some guardrails that I don't want to accept any backup which is more than a year old, or has a retention which
is more than a year old. So it basically makes your
life a little bit easier that accidentally you're not trying to sort of shoot yourself in the foot. Okay, so once that's done, the air-gapped vault is created, one thing you need to do is
you need to actually note the ARN of the vault. This is important at the time of recovery, if your account or your
organization is down and you want to initiate a recovery. And these ARNs are not complex. They're basically vault name added to a bunch of other things and it's fairly easy. So what you do is once you have the air-gapped vault created, you simply assign the approval team to it. And the approval team was actually already shared in the past, so now this dropdown
will show me that team, which has been shared with me. If it is not shared, I
cannot make use of it. If an SCP policy denies
me making use of it, then this operation will again fail. So once the team has been assigned, now that association cannot be broken unless the team itself chooses
to break that association. Yeah. So I think once that's done, I think the number six step is just so that you guys have some sense of how backup works. This is how you'll make
use of an air-gapped vault by creating a backup plan,
making backups in your vault. And this is what, like
I'm showing you the steps so that it all links with the
steps which are coming later. Creation of a backup plan is fairly easy. You give it a name, you give it a frequency at which you're trying to do backups. You provide a primary backup role, where your first primary
backups are going to go. And then air-gapped vault
would be your destination or your copy destination, where the copies of those
backups will be isolated in service accounts. So this step basically shows
you that I can set that up, I can give it a copy destination, and that destination is going
to be an air-gapped vault where I have already assigned an MPA team. And once I do this, I can then set some resources
that I want to go backups. So you can do this based on tags. You can pick any resource. I think in this case, I picked, I think I picked up some S3
buckets, and then I had a, or I think EBS resources, and then I added a tag which
then allows at that frequency those backups to be made, firstly in the primary vault and then as a copy in
the air-gapped vault. And I don't know how many of
you have tried this feature, but this is actually quite powerful because I can easily scale
across my organization. I'm not mentioning any instances. I'm just providing a tag. And if your resources are
tagged with that value, those backups will be
made at that frequency which is set here. So yes. So that's my backup plan. Everything is set up. Of course, all the new
backups will be made in due time when they run. And you can see that there are
backups with recovery points which are already showing up that they have landed
in my air-gapped vault. So now that all that
is there, I'm going to, now this is the part where
the recovery workflow starts. I have those backups
in an air-gapped vault. I cannot access that account, so I'm going to go to a
totally different account, and I'm going to perform,
or I'll make a request to my Multi-party approval team that I need access to that
vault and the backups inside it so that I can start a recovery. So in a recovery account, what I'll really do is
I'll go into the vaults. Instead of creating any new kind of vault, there's a tab out there which says vaults accessible through
Multi-party approval. And this is where you create a request, and request basically needs just one ARN, which I told you that we
need to remember that. So there's an ARN that
I need to provide here. And then optionally, there's
a vault name so that, because there's this logical
construct that we have created, which is a restore access backup vault. in itself acts like a vault. So you can run all your APIs about, describe vault list, recovery
points inside that vault. So it actually is quite powerful is because it just doesn't do one thing. It actually behaves like a vault. So I've sent that request, and now what will happen is, in next step, all the approvers will
get the same request in their email accounts where they will get the
context of who's asking and why are they asking because I added a comment there. And then they can go
into the Approval portal, and then they can start
approving this request. So right now, the access
is pending request is because at least two out
of those three approvers need to approve the request. So now, this is the email
that I was talking about. So each of the approvers
are gonna get this email. They can go from here, and this will take them
to the access portal where they will make this update of. They can either deny it also. So if two approvers say, "No,
I don't wanna accept it," then this request will fail. That's the case where if
somebody has somehow done more, like, even though it's very
hard because RAM-based sharing controls that not any random
account can make this request. But let's say there was yet another attack and somebody was trying to do it, the Multi-party approval
team is the final authority to approve that request. Okay, so now you've seen
the Approval portal, as an approver, I can see
what this request is all about and then I can simply go approve this. And this approval will still stay there. So people really have to
compromise more than one approver to even break the system. So now you can understand
there is layer after layer after layer that we're adding to this, that it now becomes, like
it's almost next to impossible that somebody can sort of compromise not only the systems which are out there, but actually physically people out there, which in a Multi-party approval system is actually a very hard way to do it. So now my second account,
my second approver is gonna come in and
they're going to approve it. And as soon as two of them have done, this request will be completed, and they can then start
the recovery process. - And just to point out, like,
in case people are wondering, "Does it always have to be two? Can it be three? Can it be four?" yes, the answer is yes. You can make a team up to 20 people and have the approvers needed
from 2 all the way to 20. I don't necessarily recommend
that you do 20 approvals for 20 approvers. But if that is what your
organization believes you need, go ahead. Yes. - Okay. So now it's actually into that
restore access backup vault. The vault status is active, and I can actually see
those recovery points which are actually existing
in a different account, in a different logically air-gapped vault. And now what I'll do is
essentially the last step, which is either I can restore, just directly go to the console, or I can actually copy it
to a different account, because I have access to all of those. I, of course, cannot go and delete. It's a read access. I cannot delete, actually,
backups which exists that, even though I think the
UI is not gonna, yeah. So it shows you restore and copy. The edit part is not there. It's just test environment
so you could see it. And yeah, I'm just providing a role so that I can do the
restore process from there. I think that pretty much covers the three big areas that
we wanted to show here, which basically tells you that these are the
things that is required, this is how you go perform a
recovery when an event happens. Yeah, I think that's... - Yeah, I'm gonna say thank you.
- We're open to questions if folks have it here. - [Alex] Okay. Well, I appreciate everyone's time. If you have any other questions, please see me or Vivek afterwards. We're happy to answer anything for you. Thank you again.
