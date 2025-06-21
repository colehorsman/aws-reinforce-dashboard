# AWS re:Inforce 2025 -Visualizing workforce identity: Graph-based analysis for access rights (IAM341)

**Video Link:** [Watch on YouTube](https://www.youtube.com/watch?v=JsPug0rh7BM)

## Video Information
- **Author:** AWS Events
- **Duration:** 48.3 minutes
- **Word Count:** 8,948 words
- **Publish Date:** 20250620
- **Video ID:** JsPug0rh7BM

## Summary

This session demonstrates how to visualize workforce identity using graph-based analysis for AWS IAM Identity Center access rights. The presenters built a comprehensive solution that combines data from AWS IAM Identity Center, DynamoDB, and AWS Neptune to create visual representations of user access relationships. The solution addresses common identity management questions like "who can access what resources" and "how did a user gain access to specific data" by mapping relationships between users, groups, permission sets, accounts, and AWS resources. The architecture uses Lambda functions orchestrated by Step Functions to collect identity data, stores it in DynamoDB, and visualizes it through Neptune's graph database capabilities. The solution also integrates with IAM Access Analyzer to identify critical resource access and unused permissions, providing a complete picture of identity access patterns for compliance, auditing, and security optimization.

## Key Points

- **Problem addressed**: Traditional identity management approaches based solely on group membership don't provide complete visibility into actual resource access due to complex policy interactions (identity-based policies, resource-based policies, SCPs, RCPs, permission boundaries)
- **Data collection**: Automated extraction of users, groups, permission sets, accounts, and IAM roles from Identity Center using APIs, with parallel processing through Step Functions
- **Graph visualization**: Uses AWS Neptune Analytics to create node-and-edge relationships between identity entities, making complex access patterns visually understandable
- **Access Analyzer integration**: Incorporates IAM Access Analyzer findings to identify who has access to critical resources and highlight unused permissions for least privilege optimization
- **Cost-effective**: Running costs under $40 per month for the demo environment, with ability to start/stop Neptune instances to optimize costs
- **Automation**: Fully automated pipeline that can be scheduled to run periodically, updating the graph with current access patterns
- **Export capabilities**: Data stored in DynamoDB can be exported to CSV for reporting or integration with other tools

## Technical Details

- **Architecture**: Step Functions orchestrate Lambda functions that call Identity Center and IAM APIs to collect data and store in DynamoDB tables (users, groups, accounts, permission sets, role assignments)
- **Graph database**: Neptune Analytics used for in-memory graph processing with CSV import format requiring specific node (ID, label) and edge (ID, from, to, label) structures
- **Data processing**: Lambda functions handle cross-account role assumptions to enumerate IAM roles with "AWSReservedSSO_" pattern and extract attached policies
- **Visualization**: Jupyter Notebook on SageMaker connects to Neptune with Graph Explorer interface for interactive exploration using Gremlin and Spark queries
- **Event integration**: Access Analyzer findings consumed via EventBridge and automatically added to the graph database for real-time critical resource monitoring
- **Node types**: Users, groups, permission sets, accounts, IAM roles, Access Analyzer findings, and critical resources
- **Edge relationships**: Group memberships, permission set assignments, account provisioning, role associations, and resource access mappings
- **Deployment**: Three CloudFormation templates automate infrastructure setup, with workshop materials and GitHub samples planned for publication

## Full Transcript

- [Meg] Awesome. Let's get started then. Welcome everyone. Thank you for joining
us in today's session where we're gonna be talking about how you can visualize
your workforce identity using a graph-based
analysis that we've built using some of the new
access rights as well. I'm Meg Peddada, a senior
partner solutions architect based in AWS, and I'm joined
today by Alex Waddell. - [Alex] Hi, good morning, everybody. I'm Alex Waddell. I'm a senior security
specialist SA at AWS. - [Meg] Awesome. - [Alex] Okay. Now, who here has ever had
any of these questions? Things like, who in our company can access our cloud resources and
what can they do to them? Can you show me how Bob was able to update the customer data
in our production account? Or do users with access
to our cloud resources have access rights that
follow least privilege? Or even, can you give me
a report of everything that Alice has access to
in our production account? Anybody get that kind of question, yeah? - [Meg] Show of hands. - Few hands.
- Yeah. - [Meg] Yeah, awesome. Yeah, great. - [Alex] Okay. So the challenges with that that we see are that basing resource
access assumptions on group membership from
your identity provider doesn't tell you the whole story because resource access
can be granted by having a combination of identity-based policies, resource-based policies,
service control policies, resource control policies, which are a new kind of control policy that we've launched in
the last six months, permissions boundaries
and also session policies. And teams might also
deploy custom IAM roles and policies into accounts. So when you're mapping a group to a role, you don't necessarily get
easy visibility into that. And so, providing your AWS account and resource access visibility to teams beyond just the cloud operations teams can often be a bit of a challenge. So here's our goal for today. We're going to get some data. We're gonna get lots of data. - [Meg] Yeah. - [Alex] We're going to process that. We're going to enrich that data. We're going to then visualize it and we're going to be
able to report on that. We're going do all of this
in a fully-automated fashion so that you can run this at will, so that then as identity administrators, you can start to get access
to that data when you need it and then give that information
out to your stakeholders, like your internal
regulators, internal auditors, and your compliance teams, your external auditors and regulators, but also some of your senior stakeholders. And what you might also think about doing is maybe even giving them access to it, which means that you're almost
out of the loop, but why not? So. - [Meg] Awesome. To get started, I'll give
you a bit of a quick overview of what AWS IAM Identity Center is, because it's kind of the foundation that we need to get this data. So to quickly level set for everyone, if you've used Identity Center
before, a show of hands. Awesome, a lot of you. Okay, great.
- Good. - [Meg] But, basically, it's a mechanism of integrating your existing IdP with AWS's IAM Identity Center, which helps you provision
your users, groups and give them access to your AWS accounts using the notion of permission
sets and stuff, right? So you're able to connect
your identity source, be it whether it's your on-prem, whether you have a third
party vendor who's like Okta or CyberArk or whoever you have, connect them using the
IAM Identity Center, you're able to then manage
your access into AWS, and then you're able to
manage that user access to applications and accounts as well. But today, we're kind of focusing more on that management of the user access and how that flows into all those different accounts you have. I'm sure a lot of you
have multiple accounts or thousands of accounts
and thousands of users, and you're trying to map the access between those users and accounts, right? So quickly just to again level set how the provisioning works. So in your IdP, you have the notion of your users and groups. You have the SCIM provisioning protocol, which provisions the users
into Identity Center, and it also provisions the
groups using the SCIM protocol into Identity Center, right? So it's that seamless integration, so you don't have to manage it and your users have that seamless, single sign-on experience. So as you make updates to it, that'll get propagated into
Identity Center as well. And we can see that information. So this is all great. And so, you have these
two different systems where you're managing your identities. But you kind of wanna go beyond it, right? So the question that Alex
asked in the beginning, this is the million-dollar thing
that we wanna answer today, which is this awesome graphic. And I want you guys to pay close attention to how exactly we're
building this relationship between these entities
so that you can see it in that graph visualization. So we have the notion of users. We have the notion of groups, right? In Identity Center, we have this thing called permission sets. So you also have this thing of having users in your groups, right? You provision them into a security group or a networking group or something. And then those users and groups are assigned permission sets, yeah? So you've all configured
permission sets in Identity Center. Great. And then once you also
configure a permission set, you have to grant, for example, Alex access to an account, right? So you have to say that user group can access an account, all right? And they're assigned that permission set. So that permission set has
to exist in that account for them to get access to that. And then once that happens is that these permission
sets are then gone and created in those individual
accounts as roles, right? So if you've ever seen
in your IAM console, you've gone and seen AWSReservedSSO, those are the roles that are being created from Identity Center, right? So that's how we map them. And so, once we have that, they're also provisioned
into the accounts. So we have this nice linkage between how these things are forming, and this is kind of the relationship that we want to get into. And, obviously, in your accounts, you'd have a lot of
different critical resources or just regular resources
for the matter of fact. And then those roles and permission sets are what's gonna grant you access, right? So in AWS, everything is explicit. You have to say, I grant you access, and that's what the policy and the permission set would define. And so, that's how you get
access to your resources. So this is a pretty cool relationship. This is kind of what we wanna build. Few shakes or few nods, right? This is what we wanna build and this is exactly how
we're gonna replicate it in a visual representation. - [Alex] Yep. - [Meg] So Alex, I do
wanna ask the question, how are you addressing this problem? - [Alex] Okay. - Yeah.
- All right. So many late nights, Megan
and I have spent a lot of time doing this so that you don't have to spend all that time doing it yourselves. The code that you'll get to see, and there's gonna be a workshop link that we'll put up on screen in a moment, is gonna let you get access
to certain parts of this. We're working our way
through getting it published onto our AWS samples GitHub. And we should, hopefully, have that later this week or next week. So keep an eye on that link. But what we've got is this access rights for identity on AWS graph visualization. Now, we're not officially
allowed to give it a nice title. We want to call it this nice title. We're gonna be working
with our branding teams and our legal teams to
see if we can do that. But as it stands today, this is just our outline
title for the project. If you have, please scan that and you should get access to workshop- - Link
- Studio. - [Meg] Yep. - [Alex] And what you'll
be able to see on that is what I'll start to walk you through. Okay? Everybody got that? See there's still a few
people with cameras. Okay. - [Meg] Awesome. - [Alex] Right, so let's
address this problem statement. Let's try and figure out how
we're gonna get all of this. So we need data, and as I said earlier, we need lots of data. So we need to have things
like all the principles or users and groups. We need to have all the users
that are in all those groups. We need to have all the permission sets. We need to have all the
accounts that you have and all the users and groups
that are assigned to accounts, the permission sets
provisioned to the accounts, the principles assigned to
all the permission sets, and then the definition
of each permission set that's being created as an IAM
role in all of your accounts. And maybe at the end,
what about the resources that could be accessed by these principles and what the actual permissions they have. So that's kind of the second half of what we're gonna talk about today. So, fortunately, we've got
some APIs that you can use. We're a very API-centric
organization as you know. So things like the Identity
Store is going to allow us through some particular API calls to get all the users and groups. But if we want permission sets
and accounts and principles and things that are provisioned, we can go to the Identity Center API and we can list these
permission sets and accounts. So that's reasonably straightforward. That's pretty easy for us to do. You can make those calls today. You can get all that access
and get all that information. But what about the rest? What about things like
the users and groups that are assigned to the permission sets? Or what about the definition
of the permission set that gets created as an IAM role? So what an Identity Center does is it does all the hard work of creating the roles
in each of the accounts. And if you've ever seen one of the roles, it puts a random series
of characters at the end. And if you remove that
permission set from that account and re-provision it, it
creates a brand new role with a different set of
random characters at the end. It's not something that
you can depend upon. Fortunately, we've worked out a way in which we can get that information. And that's what we do in this solution. So, first of all, we're
gonna build relationships between the principles
and the permission sets. And we'll do that in a bit of code, but also in some of the graph,
which Meg will talk about. And then we're actually going to, and this is where it gets
a little bit painful, we have to connect to every single account and do a ListRoles. And we're looking for
this particular template, the AWSReservedSSO_, and then it will have
the permission set name and a random series of characters. And we get also the
ListAttachedRolesPolicies for each IAM role. Because what you can do in Identity Center is you can have a permission set with a customer-managed policy that in each account is
called the same thing, but has very different access. So you can't rely upon the fact that it says network
administrator is the role. Within that network administrator role, they might have a set of
actions from one account that's entirely different
to another account. So we capture that as well. So this is the architecture that we have. Now, walk through a list a little bit. We've got, at the center of this, you'll see there's a lot of
Lambda that's running here. We've got the AWS accounts. We're using step functions and state machines within
the step functions. That's all working through
the Lambda functions that are communicating to Identity Center and into the accounts. We're then taking all the information and putting it into DynamoDB. We've got some tables, which
I'll show you in a second. And then we have another a step function that gets run that can
then export that data. Okay. - We're live.
- Right. So you see we've got lots of lovely tables sitting in DynamoDB. So we've got ones for users, for groups, group memberships, accounts. We have permission sets. We have permission sets that have been provisioned into accounts. We have users assigned to accounts. We have, what else do we have? Groups assigned to accounts. We have, I think that's it. And there's another one
called IDC IAM roles. So if I look at say, the
user account assignments and just explore that table quickly, what we're doing here is we're taking, we've got the account
ID, we've got user IDs. Now, user IDs and Identity
Center are unique ID strings. But we can also bring back information like the account name. We've got the name of the
permission set, which is there. We've got the arm of the permission set. Now, the arm of the
permission set is the same 'cause it's only in one account. So we have the full arm of
that and we have the principal. So you can see we've got
like Alice, we've got Meg, we've got Judy, we've got Bob, and so on. So we started to build up
by making various calls using existing data tables that we've got, start to tie relationships
together and build all that. So reasonably straightforward using a set of pretty simple DynamoDB. What we've also done is we've got lots of Lambda functions that go do this. So if I look at, say, let's pick one, probably the most complex one. - [Meg] Yeah. - [Alex] This is the one
that does the Get IAM roles. And what it's doing is
it's assuming a role in a target account. That's something that we're calling. So we're going into each
of the accounts in order. So again, we've got the accounts table. So what we're also trying to
do here is minimize the number of API calls that gets
made into Identity Center. If we do like a one-off call
to get the account information, we can start to leverage
all the information out of the DynamoDB tables without
making extraneous calls into APIs that we don't really need to and it would use up your quotas. So we're starting to list the accounts. We get the IDCU, the Identity Center roles that are in those accounts. We then work our way diligently
through each of those and we get the attached policies. We make a call and we say, let's get the IAM attached
policies for that. And we build up an array and then we, ultimately,
dump that into a table. Not that one, that's emptying things. So down here, we're basically writing all the information into DynamoDB. So what we're trying
to do here is leverage the power of DynamoDB and
the fact that it's great at storing data of all
sorts of different types. We don't have to define the schema. We just decide which attributes
it is we actually want to extract when we make these API calls. If you want to add more
metadata into that, if there's other data fields
that you would want to add, then you could add that. You could augment with
other pieces of information. So you're not restricted by that. That's great. Now, let's go to what the
state machine looks like. - [Meg] Quick show of hands. Have you guys used state machines before? - Step functions?
- Step functions, yeah. - Few people.
- You're familiar with what it does.
- Few people shaking heads. Okay.
- Yeah. - [Alex] So step functions
are really, really powerful. It's a great way to be able to orchestrate a flow where I've got an
example at the top here, and this is something
you could schedule this to run on a weekly basis. We've just manually triggered this. But you can schedule this
to run on a regular basis. First thing it does is it goes off and it calls the function to
create the Dynamo DB tables. So if somebody decides, you know what? I'm gonna just delete all
these Dynamo DB tables. I don't need them anymore. They're taking up space. I want to optimize my costs. Let me just get rid of them. Well, when you run this,
it will recreate those. Or if you wanted to add additional tables and you've not created
it, it creates the tables. Then we do some parallel
processing where we list the users. We list the groups. We list the accounts and we
list the permission sets. These are all individual API calls. They're not related to each other, but what we're doing is
we're capturing that data to then populate some DynamoDB tables to then use in the next layer down. So the next layer down,
we need group memberships. For group memberships,
we need users and groups. So we just use the users and groups and we can get that information. We need provision permission sets. So we needed the permission
sets to start with. We needed the account information as well. So having that information, we
can make well-informed calls to the APIs within Identity
Center to make those calls and populate more tables. Same for user account assignments, and then also group account assignments. So using this, you can
work your way through this. You can parallelize a
lot of the functions, use the output of one to feed
into the input of the next. And then we have one at the very end. And this is where kind of all of the clever part of this happens, where we take all of that data and then we go through all of the accounts and we enumerate all of the IAM roles that Identity Center has created. We have all the information
that we need to go get that. When we get that, put it
all into the DynamoDB table, and then we're pretty much good to go when it comes to creating a graph. - Yeah.
- Yeah? - [Meg] Yeah. - So it's that one?
- Awesome, yep. Great. So I just wanna give you a quick overview of what Neptune is. So preface is that Alex and
I aren't data scientists or data experts, right? So we were learning
Neptune on the go as well. So trying to figure out
how graph databases work. And so, basically, we have a range of database services within AWS, right? So whether that's RDS- - [Alex] Hands up, sorry,
hands up who here is data? - Yeah, data.
- Anybody, data person? - One.
- One. - [Alex] Who here is an identity person? Right, okay, good. We're in good company then. - [Meg] Yeah, yeah. So we were like trying to figure out how do you build a graph
database, what do you need? Yeah, how exactly it works, right? So there are a range of
database services out there, RDS, Aurora, all this stuff. But Neptune is our native service, which helps you build
these graph databases. And that's what we use today to actually visualize
these different identities. So there are two different
forms of Neptunes. Again, I'll preface by
saying I'm not a data expert, but I've learned it on the go as well. So we have two different types. We have the database type and
we have the analytics type. The database is, if
you're trying to provision a lot more data in a
quicker bulk upload manner. It is instance based, so there will be an instance attached to the database. You can do bulk uploads using Lambdas, and it does have persistent storage. On the other aspect, we have the analytics aspect of Neptune, which is a more memory-based service. It is a graph, like an in-bulk
graph mechanism as well, which is what we've
used for our demo today. It does have a bulk upload feature again, and more ephemeral analytics, right? So again, not big data experts, but we've kind of navigated
our way using Neptune using the analytics space. And that's what we'll go into today. And then, so the Neptune is
just the serverless database that we have that can scale and has a lot of availability options. The thing that compliments Neptune on how we view all these things is, is anyone used Jupyter Notebooks before? Or SageMaker AI? Yeah, okay.
- Cool, nice. - [Meg] Cool, yeah. And so, you guys are familiar
with how we can automate a lot of the actions and tasks that we have using these
Jupyter notebooks, right? And so, that's exactly
what we do today as well, is that there is just a Jupyter Notebook that's connected to your
Neptune analytics instance, and we're able to use either Gremlin or Spark QI, which are all
these interface languages that help you build these
graph relationships. Yeah, so then our architecture, initially, we had that sort
of right section grayed out, but we bring that back into scope, right? And we'll walk you through
what exactly the step function on the Lambda looks like here and then how exactly we can
import that into Neptune. - [Alex] So I've got Neptune
Notebook and I got graphics- - [Meg] Do you wanna go to
the state machine first, or? - [Alex] State machine? - [Meg] Yeah. - [Alex] Right, let's go to, one second. I'd love to, except there's not one there. Hold on. - [Meg] Yeah. So we have two state machines, right? The one that Alex built, which is actually building
the data into Dynamo, but then we built a separate one, which is more of the export function that will get the data into Neptune. And so, this is a very easy, simple, three-step state machine, right? And this is just so that
we maintain consistency and we know how to do it. And during deployments, I think we can both attest
that it's very easy. If you make a lot of errors, you just go to state machine
and you can keep running it. So you don't have to
manually do all these cells. So again, Lambda's doing a
lot of the heavy lifting here where we have an export
function that will actually go and convert the data
that we have in Dynamo into the graph database format. And I'll walk you through
what that format is. And then we wanna sort of,
if you have data in Neptune, you want to kind of flush it out and then reimport that data, right? So there's just two very simple steps. And so, if we go to the
Lambda export function, sorry, I'm making you drive. - [Alex] Yep, that's fine. - [Meg] So we have an S3 export function. - That one?
- Yeah, that one, yeah. And then we'll expand. Okay, so here we have
these things called nodes. So again, not graph people. I'm assuming you don't know graph. So here's a quick crash course
on how graph databases work. You have the notion of
nodes and edges, right? A node is like an end entity, right? So think about it as a user
or a group or an account, that is considered a node. The way we build it is
that we have the data coming in from DynamoDB. And the way to import
it into graph databases is using a CSV format. And there's a specific
type of heading format that you have to follow. So each of them, each
node needs to have an ID, and each node also needs
to have a label, right? So if we're looking at line 69 where we're actually creating a user node, we have the user ID, the
username and a label, right? So the ID always has to be a unique field. And so, we have the username, it's a string field, and then the label. So the label is what defines
what the node is gonna be. So here, I have a label called username. So right, when you go in a graph, I'll show you what exactly the label does, but it's a way to identify
what exactly the node is. So we do that for users, groups,
permission sets, accounts. It's just rinse and repeat. So that's the node. But you might be asking, how do I build that relationship, right? So that's what an edge is. So a user exists in a group, that means I need to build a relationship between a user and a group. So again, we have to
have that table format that graph is expecting. You can see in the CSV headers, we have ID, the from and to. So I need to say where the relationship is going from and to. And you have to give it
a label again, right? So we have a unique ID. We have the group ID and the user ID because a user ID would
exist in a group ID, right? So if you think about that
image that we had up before, and then the label is
just has members, right? That's just a meaningful
way to show you what exactly that relationship is building. So has members means that
that group has members, those users exist in that group. So we do that for
permission sets and users. We do that for groups and permission sets, for users and accounts. So you have to keep
building this relationship in that node and edge format. So once we do that, this is where we get to the fun bit, right? So I'll just show you the Neptune console here in the analytics. You can see I talked about the
database and the analytics. So in the analytics, I have a graph called the Identity Center graph. And then I have a notebook
that is attached to it, right? So this is a Jupyter Notebook, right? It's running on SageMaker AI. On the backend, what's cool about this is, is that here we're able to just quickly go and say open Graph Explorer, right? So it's in bold. Again, because we're not data people, I don't wanna go and build my own graph format visualization, but the Graph Explorer does it for us, which is like an open source tour, right? Yeah. So we have the Graph Explorer here, and this is the interface
you're given with, right? So here on the right-hand side, you can see I have all of my nodes. I have roles. I have users. I have permission sets, and I wanna sort of import them, right? If I add them all, that's a lot. These are all my nodes. But I just wanna quickly
show you how awesome of a graph this builds. And then we'll scope it down and then look at different things, right? So if I go, you can see
that the number expands and it's building, it's
building, it'll keep building and it's gonna get very messy. And I can only assume
in a customer scenario is this is going to get
very messy very quickly because you guys would
have thousands of accounts, hundreds of users, and you
wanna build this, right? So this isn't meaningful yet, but if say, I have a question and I kind of just wanna walk from a user, right? So this user, which I can change here, so yeah, so here, I'm
just customizing the user. So this is just modifications on how to best represent your graph. I wanna make a display attribute. So here's Bob Sanders from
Unicorn Rentals, right? So he has an assigned permission set. He's part of a group. Weirdly, the group name is not changing. There we go. He's part of the AppDev group. He's assigned to three different accounts and he's part of two different groups. And he has two different permission sets, or he's part of three groups. He's a busy guy, right? Does this sort of help
you guys start thinking about the visualization, right? So if you remember when we
built that initial slide, a user was part of that group. So we have Bob is part
of the DataLake_Admin, the AppDev_Admin, and
the AppDev_Read, right? And so, he's also assigned
two different permission sets. So I think one is like
an admin permission set or a dev permission set. And then he's also assigned
to three different accounts because a permission set can exist in multiple accounts, right? So if you start thinking
about that relationship, we can start expanding on it and it would start bringing
up more and more of that. - Yeah.
- Yeah? Is this kind of a cool way to represent your Identity Center? Excellent. - [Alex] Yeah. - [Meg] Do we wanna come back? Yeah? - [Alex] Go back to that one? - [Meg] Yep. - [Alex] So. - [Meg] Oh, this was just,
yeah, so this was just the image that we kind of wanted to go back, right? We wanna have it in parallel, but this was like groups
that we wanted to show you that those users exist. So Bob existed in that group. He had those permission sets. He had the accounts. We had those roles. We didn't actually expand on the roles, but we'll show you again when
we have a better use case about how they expand into those roles. And then maybe what resources they might have access to, right? That would be the fun bit. - [Alex] Yeah. So that was when we asked ourselves what if we could get a list
of all our critical resources that could be accessed by principals and the actual permissions that they have? This is the Nirvana thing
of somebody says, look, I've got this bucket and it contains all of our customer data and it's
got this bucket policy on it. But I know I've got SCPs
and I know I've got RCPs and I know I've got an identity policy. Can you just tell me what this person who's got this role can do to this bucket when you add all that together? All right? Well, as you may have seen yesterday, we launched a brand new feature
within IAM Access Analyzer, which is the ability to get insights, which is Access Analyze, Access Analyzer. Access Analyzer, get my mouth right. - Yep.
- Does things like unused access and external access. So it is continually
monitoring your environment. It's continually looking
at your IAM principles and your policies and so on. It gives you the ability to aggregate all that into Security Hub. And then you can have
automated notifications. And what we launched yesterday
was an extension to that, which allows you to identify who within your database
organization has got access to your critical AWS resources. And this is something
that you will define, you decide what is a
critical resource for you. So it lets you understand
who within your organization can access critical resources. And we use provable security
assurance to do that. So we have an automated reasoning group that works really hard to figure out how to do this mathematically and with a 100% surety applying all of the different policies together can then give you the end result that says this role can do this set of actions to this particular resource. You can then centrally
view all that access within the unified dashboard that's there. And then you can also pick
specific resources to monitor. And that's what we've done
as part of this solution. So let's now add that
into our architecture. So now our architecture
has all of the great stuff we've just done to get all that data, all the great stuff we've just done to be able to visualize that data. But again, we want to automate
this as much as possible. And what Access Analyzer does is when it creates a finding, when you set up the Access Analyzer to
monitor a critical resource, any principle, any role that it identifies that has access to that, it will create an EventBridge finding. It creates a finding, which
it puts onto EventBridge, which means you can consume that. And if you can consume that automatically, which is what we do, then we
can put that into DynamoDB. You see where we're gonna go with this? We can put that into the database. We can extract the data
we need out of that. We can add into the graph and start to build more relationships because we've already got
80 to 90% of the other data and it's the last kind
of few hundred meters of that access that we're getting here. So.
- Yeah. Whoa. - You're gonna?
- Yeah. - Yeah.
- So actually, we wanna make a few updates, right? Because now that we have Access Analyzer, how do we get this data
into the graph database? Again, you have to add a node and an edge. So a node becomes the
Access Analyzer finding. So if I just go, oh, oh,
you don't wanna do that. So if I just quickly go and uncomment it. So we have a bunch of fields that are coming back from Access Analyzer, that becomes a finding node itself. And then we also have the unused analyzer. And we also want to import
that into the graph as well. So Access Analyzer has three
different types, right? So internal, external
and the unused as well. And then we also want to identify our critical resources, right? Because that's where the pot of gold is. And we wanna work backwards
from who has access to these critical resources. So when you saw the graph before, it was cool to see the representation between the different entities, but was it kind of really answering what exactly you were looking for, was the question that we all
had in our heads, I hope. And so, we have those nodes, but we, again, we also have
to build a relationship between those nodes and edges. So here, we're trying to
map the analyzer finding to a resource, to that critical resource as an example, right? So we're building that edge again. So here, we're again calling it the to and from, the resource
on, the resource account. We're pulling it from a
different DynamoDB tables and making a CSV file out of it, right? So pretty cool here. So when we go there, we're
able to go into our statement. - [Alex] Do you wanna deploy that? - [Meg] Huh? - Deploy it?
- Yeah. We'll deploy it. Yeah, awesome, so it'll go there. We'll go to, so S3 would have our export. I'll just show you very
quickly what it looks like. So our export bucket has
all of those CSV files. Those CSV files are
what's getting imported into the Neptune graph as well, right? But I think, Alex, you might
have some questions, right, for me that you want me to answer? - Yeah, so we had that question of Bob had access to some
critical information. So do we have a critical resource? - We have, yeah, I see something here called a super-sensitive data store. - All right.
- Is that something? - [Alex] So let's work backwards from that and see what Bob has
actually got access to. Can we add that one?
- Okay, yeah. We've added that as a node. - Okay.
- We see that it has two edges, right? Three, or three, sorry,
three relationships. If I expand that out, what do we see? We see that it has a
internal access finding. - Mm-hm.
- We see that it belongs to this account and that
role grants it access. That still isn't telling you much, is it? - [Alex] No, we need to
keep exploring the graph. - [Meg] Keep going. - Right.
- Oh, what do we do? So we saw that the finding is
actually a link to that role. - [Alex] Okay. - Okay.
- Good. - [Meg] Interesting. Maybe you wanna know who
this role belongs to? Who has access to this role? - Yeah, please.
- Yeah? Okay. Oh, look at that. - Okay.
- This role has another internal access finding. Oh, sorry, it has three more
internal access findings. - [Alex] Okay. - [Meg] It also grants access
to another critical resource, not just one, but two critical resources. It's assigned to that permission set. So we know that-
- We're getting closer. - From Identity Center.
- Getting closer. - [Meg] Yeah. So let's actually look at who has access to that permission set. Oh wow, okay. Well, let's just slowly
unpack this a little. I'm gonna expand this out. Provision into. Okay, so here, let's look at
this edge for a section, right? So that permission set
has been provisioned into that account, right? That's how we're mapping the relation back that
that role got access to. And then we have two users here. So I think this is a group. Yeah? The multi-user account.
- Might be, might be. - [Meg] And then we
have, Alex, is that you? Who has access to this role? Who has access to the bucket? - Maybe?
- Oh no. - Maybe.
- Oh no. - Okay.
- Am I in the admin group, though? - [Meg] Yeah, let's check. - [Alex] Oof, I am. - You are.
- Okay. - [Meg] And so, the thing about this is that you can even remove
certain nodes, right? So if you're trying to
work backwards from like, hey, how did Alex get access? We can see that Alex is
a member of that group. - Yeah.
- And because he has an admin access, he was also provisioned into
multiple accounts, right? So we're building this relationship. - [Alex] Yeah. So can you take out the
three accounts at the bottom? Take them off the graph?
- Yeah, yeah. - [Alex] Let's take those off. Let's see what this looks like. Okay. Now, what else have we got here? We've got Access Analyzer findings. - Yeah.
- So- - [Meg] So yeah, actually maybe let's look at the Access Analyzer finding, right? So we have a finding here, and if you click on the details,
it is actually exporting the Access Analyzer
finding details as well. - [Alex] Mm-hm, so it
looks like I've got quite a lot of access to that one. - [Meg] That's not following
best practice, is it? - Not really.
- Or at least privilege for that matter of fact. - Yep, not really.
- So we have the principle. We can see that here, there
are two fields as well. Whether there was a
resource control policy that was evaluated during this or a service control policy
that was also impacted during this evaluation, right? - [Alex] Yep. Okay.
- Yeah. - [Alex] So what about, is there any other Access Analyzer findings
that are related to that? Anything?
- This is a DynamoDB table. - [Alex] All right, let's
take the DynamoDB one out. Let's keep it simple, let's take that out. Take the DyanomoDB. - This guy out as well.
- Yeah, let's take it outta the way 'cause it was that, it was a particular S3 bucket, wasn't it? - Yes, it's this guy.
- Just that SD bucket, yeah. - [Meg] Yeah, super sensitive data store. - [Alex] Okay, so that
bucket belongs to an account. - Yeah.
- I'm assigned to that account. - Yeah.
- I'm assigned to the permission set and I'm
a member of the admin group and there's a finding
against it at the top left. - This is the finding that we-
- So that's the finding. So that's all the access that I've got. All right, okay, cool. So you can see how by bringing together a lot of that information, we've now got a much
more informed position. So I can see and I can draw
relationships between all these. So I can see that particular user. Remember going back to the very beginning when we had the users and groups, those users and groups came
from your identity provider. So you'll have the group names
from your identity provider and your usernames from
your identity provider. So that's, you can sort of
leave your identity provider alone at that point. And you're now all in the graph. So you've got the user in the group, the group and the user
have access to the account and the permission set
and they get this role. That role gives them
access to this resource because we've done this internal
critical resource analysis that we've been running and we've identified
that the user's got that. That's great. But is there anything
around unused access? - Oh.
- If we reset the graph. - Let's clear the graph.
- And picked an unused access. - [Meg] So we have an unused access node. All right.
- Okay. So we've got one finding. So unused access and, in this one, I think it's this unused permissions. - Ah, yes.
- So this is a great tool within the toolbox of Access
Analyzer to drive you towards or help you move towards least privilege. What this is going to do
is analyze the activity that a user actually
or users actually make when they're assuming
that particular role. Because there's a set of actions within that role they're
permitted to execute. But what if they don't make, what if they don't use all those actions? You might be over-permissioning. So what this does is it identifies, have you got unused
actions within your role? - [Meg] So we have the
details expanded out again. - Yep.
- And so, we can see that the number of unused actions, a 188. The number of unused services, a 184. So if you go into Access Analyzer and actually look up that finding- - Yep.
- It should give you a scope down policy, yeah. - Yep, because I get the finding ID there. - Yep.
- Then you'd be able to take that and go off and look at it and you can actually see in the console, 'cause all the actions that
are actually being used and a whole lot of actions and services that are not being used. So again, if somebody says, "So have we over-provisioned
access to a critical resource?" You can say, "Well, yeah,
this critical resource, "which is this DynamoDB table, "which is grants, it's granted
access by this IAM role, "we've got all of these
permissions that are in that role "that just don't seem to be used." So why don't we think about
turning down the permissions and reducing the
permissions that we actually have in that role to drive
us towards least privilege? So that's something that we just decided this week to add into this and it took us, didn't take us that long? - [Meg] Two days? Yeah, less than a day? - Yeah, a lot less than a day. - Yeah.
- We were quite busy this week and it probably took us a couple of hours. - Yeah.
- To add the unused Access Analyzer into that. So, and there, we've got the external Access Analyzer as well and that's something
we'll probably look to add into this as well. Okay?
- Yeah. So I think we'll just switch back to see if we've addressed the questions. - [Alex] Yeah, so sounds like
when we get all this data we might be able to start answering some of these questions and
we've started to visualize it and I think I can probably now answer a lot of these questions. And if I was to reword
the questions that we had, so we've got these questions here, I might say, you know, who has access to this critical resource? So that's who in our company can access our cloud resources and
what can they do to them? Or can you show me how Bob was
able to access this resource? Yep, I'm pretty sure in the graph, I can now show how Bob
was able to access that. Bob was assigned to an
account and a permission set. They gave him a role that gave him access because that role grants access
to a particular resource. And I could see the actual
actions that he was permitted to perform against that resource. And then, are there any findings
for the critical resources? Well, yes, because we've ingested internal Access Analyzer
findings that are now created. Everything is sent through EventBridge and we can consume those automatically. And the service, if you leave this running will continue to do that. If you run the state machine, it will start to populate
the various tables and the various files. And what are the details
of the finding as well? So again, you can make
this information available without somebody having to necessarily go into the IAM console. They can look at it in the graph. So you could give somebody outside of your team access to that. So I think we've pretty
much covered most of those. - [Meg] Yeah. - So.
- But the age-old question, cost optimization. You might be thinking Neptune,
Access Analyzer, DynamoDB, what is it gonna cost us, Alex? Did you build something
cool to show us here? - Well, like all good AWS practitioners, we've used tags 'cause who here uses tags? Fantastic.
- Awesome. Yeah. - [Alex] Good, cause you all should. Now, everything that we've
deployed gets tagged, which means that, and if you
haven't seen this before, you can create applications within AWS and you go to here and you can actually go and create various applications. And we created one for this implementation and we do it by taking
advantage of the fact that there are certain ways in which you can add resources to that. And we had done it based upon tags, which it's not showing
in there for some reason. But what you'll see is
that we've been running this pretty much consistently since the beginning of
June and we are at halfway And it's under $40. Now, for everybody else, it
could be a different cost. We're just trying to demonstrate
that when you look at this, create this as an application,
you can get oversight and visibility into what
the actual costs are. But what you can see
there is that Lambda costs are next to nothing. CloudWatch and DynamoDB and
S3, obviously, for each of you, if you were to implement this
in your own environments, you're going to have
potentially many more accounts. Many more permission sets and draws. But again, it's very, very lightweight. We only capture the data
that we actually need to perform then build the graph. So one thing you can do. - Switch?
- Yeah. - Yeah.
- You gonna cover it? - [Meg] Yeah, it's just that
with the Neptune, right, because it's a graph database, obviously, there's a lot
of computer attached to it. You wanna size your instances
appropriately, right? So the instance that we
were using for Neptune was like a T2 medium. Obviously, if you have a larger data set, you'd want a bigger instance. The other thing is that you would see there was a reset task and a start task. You could also do a stop
and start of Neptune, so that you're not
constantly running Neptune all the time in your account. You can take snapshots of it. Again, like as an identity expert, you'd only wanna do this
like couple times in a month. I don't think this is a daily
activity where you want to go and start building
graphs in your accounts. But if you're visualizing,
if you're doing, maybe we weren't expecting
instant response scenarios where you're trying to work
backwards from findings and things to help your IR teams, right? And how to find and investigate those. So you can spin up that
graph, do the visualization, turn it back down and then you
can still have all the data. So, and then like Alex showed, he was able to tag all his instances. You're able to set billing alarms. I think that's always a good way to monitor your resources in your account. And then Neptune, again, because I said, I'll keep
harping on this point, is that we're not data experts, right? So I was doing a lot of data testing. What is the right format of getting this into the right tools? So there is like a Neptune tools on GitHub that we've published where
if you wanna just go test, see why things aren't working or why it's not breaking or working, the Neptune tools has a
good like link checker, format checker off the
tables and nodes and edges to see that you have
it in the right format. - [Alex] Yeah. - [Meg] Yeah. - [Alex] Cool, so I guess five takeaways? - [Meg] Yeah. - [Alex] Please, try and experiment with some of these services if you have the opportunity to do that. You know, we built this from our services that we have available to us today. We spent a lot of time
experimenting with this and learning and really
kind of appreciating the power of what we can do with graphs. And once you create a
set of nodes and an edge, it gets a lot easier to do. Once you understand that
once and create one of these, I added a couple of things, Meg said she had a
customer meeting to go to, could I quickly do it? Sure. I went in and I was able
to add an extra node. I understood it really quite simply. So once you get your head around it, it's really quite easy to do. Watch out for a blog
and a workshop on this. In that workshop link that we sent you, there should be part of that
that says that we are going to be publishing this
to our GitHub samples. Take a note of that
particular workshop link. We will update that with the
link to the GitHub samples once we get approval to
put the whole lot up. There's cloud formation that you run, basically, three cloud
formations that auto deploys a script that you run and then it creates everything for you. And then you run the state
machines to generate the data. There's really not a huge amount that you actually have to do. We've automated as much of this as we can. Use the data that's been
collected in various scenarios. You might be asking, why
didn't we just get that data and stick it into CSV in the first place? Well, the data in DynamoDB
can be exported out to CSV. You could tabularize that. You could put that into HTML. You could, somebody says, can
you just do me a quick report of all the permission sets
that we've got deployed into all of my accounts? Sure. Don't go into Identity Center to do that. Run the state machine, export
that table out of DynamoDB. So it's a great way of just
getting the tabular data if you want it at that
particular moment in time out into a CSV format. And you could stick it into
other tools if you wanted to. And because that data already existed, we were able to build relationships and you might discover that
there are other relationships that you want to build between
certain bits of data as well. There's potentially no
reason why you could not be, as part of these Lambda functions, going to maybe some other data sources that you have internally to
start to bring in other data to augment this and to
be able to enrich that. So take this and build out from that. That's really all we've got for today. I wanna thank you all for your time. - [Meg] All right, we have a couple more talks that-
- We've got some more talks. - [Meg] If you guys guys
wanna get a bit more interested in IAM, check out
the other sessions today. It's the last day of session, so make the most out of
it while you're here. But yeah, like Alex said, if
you thought of any use cases while we were showing you the graph, other relationships that you could build between your own entities and
things in your organization, come chat to us after the talk. We'll be really interested to know how you are going about it. But yeah.
- That's it. So thank you all very much. (audience applauding)
