# AWS re:Inforce 2025 - Understand who in your organization can access your AWS resources (IAM307-NEW)

**Video Link:** [Watch on YouTube](https://www.youtube.com/watch?v=ikLthKGE6lE)

## Video Information
- **Author:** AWS Events
- **Duration:** 44.8 minutes
- **Word Count:** 6,601 words
- **Publish Date:** 20250620
- **Video ID:** ikLthKGE6lE

## Summary
This session explores AWS IAM Access Analyzer, a powerful tool for understanding and managing access to critical AWS resources. The presentation demonstrates how organizations can gain comprehensive visibility into who can access their most sensitive data, with a focus on moving towards least privilege security model through innovative access analysis techniques.

## Key Points
- **Access Analysis Approach**
  - Set, Verify, Refine cycle for permission management
  - Continuous monitoring of access across organization
  - Tools for identifying and reducing excessive permissions

- **Key Features of IAM Access Analyzer**
  - External Access Findings: Identifies public and cross-account access
  - Unused Access Findings: Detects unused credentials and permissions
  - New Internal Access Findings: Reveals access within the organization

- **Technical Complexity of Access Analysis**
  - Utilizes automated reasoning and mathematical proofs
  - Analyzes incredibly complex permission combinations
  - Computationally intensive process (comparable to searching atoms in multiple universes)

- **Practical Use Cases**
  - Inventory of access to critical resources
  - Identifying unexpected or excessive permissions
  - Tracking access to sensitive data sources
  - Trimming down unused credentials

- **Integration and Notification**
  - EventBridge integration for access change notifications
  - Partnerships with identity management platforms
  - Ability to create custom workflows for access monitoring

## Technical Details
- **Supported Resource Types**
  - S3 buckets
  - DynamoDB tables
  - RDS snapshots
  - Other critical AWS resources

- **Access Analysis Capabilities**
  - Provable security assurance
  - Daily analysis of access permissions
  - Detailed policy evaluation
  - Support for complex permission models

- **Monitoring Mechanisms**
  - Organization-wide and account-level analyzers
  - Unused access tracking
  - External and internal access findings

**Key Takeaway**: Effective cloud security requires continuous, detailed monitoring of access permissions. AWS IAM Access Analyzer provides powerful tools to understand, manage, and reduce access risk across your AWS environment.

## Full Transcript

- Hello, everyone. Thank you so much for
attending our session. I know it's near the
end of the conference, but, I promise you are in for a treat. In case you missed it, yesterday, at the very
beginning of the keynote, the first new product launch announcement, new service feature launch announcement was Internal Access Analyzer for as part of IAM Access Analyzer. So, today we are gonna talk about that. But, to introduce ourselves,
my name is Jeremiah Dunham, this is Sophia Yang. I'm a software development
manager in Identity, and Sophia's a product manager. And really, the whole focus of our talk is using IAM Access Analyzer to understand who in your organization can
access your AWS resources. So, our mission is to
understand who can access what. In order to do this, we are gonna first
scope out the landscape, which means understanding
access controls at AWS, we're gonna use the investigative tools that have been available to us first, which is the existing features
of IAM Access Analyzer. We will then upgrade our tools to include the new
internal access findings. And then finally, Sophia is
gonna give us some awesome demos that are gonna show how to get
hands on with the new feature and all the use cases
you'll be able to address. So, let's first scope out the landscape. So, to get familiar with
what we're dealing with here, we're talking about access
controls, IAM policies, and there's really two major
categories of policies, and we think about different user personas that are associated with each. On the one hand, you have
developers or builders, people making things. They want to apply fine grain permissions, which come in the form of
identity-based policies, resource-based policies,
and permission boundaries to give their applications
the access that they need, and hopefully nothing more than that. And then, of course,
you have security folks who want to establish these
perimeter type controls. These are coarse grain controls that really set like kind
of the maximum boundary for the permissions that can
be assigned in the environment. And ultimately, the goal is for, is to move to lease privilege over time. And we say that over time because sometimes you may scope things a little more broadly at first
and then lock things down, or could just be that the
needs of your organization change over time, and that requires you to continue to scope
your permissions down. As mentioned, our user
personas who are involved here are security team, or say, cloud security or cloud architecture team, that is a centralized group, and their goal is to manage what's happening in security at scale, set up security best practices, and really what they want
is a centralized view of what's happening inside
their organ to understand where things are compliant or not. And on the other hand, decentralized, you have probably a lot
more of these folks, developers or builders, and their goal really is to move fast. And to be honest with you, they don't really wanna think
about permissions too much, any more than just getting
their application to work. And so, as we're going through this least privileged journey, it's going to be a collaboration
between these two folks, these two groups of folks. Okay, using our investigative tools. So, IAM Access Analyzer is
what we're talking about here, and our goal being to get
you to least privilege, we have this mental model,
which is set, verify, refine. And this is a cycle that you start out by creating the right
fine grain permissions after the fact, then verifying, okay, let's inspect, understand
who has access to what, and then let's refine any
excessive permissions, which takes you back to the set phase. And we do this over and
over and over again, and we understand that getting to least privilege is a
journey, it's not a destination. I mean, it could be, but once you got there,
then the world changes and then you probably aren't
there again and you keep going. So, with IAM Access Analyzer, we actually have tools that
apply at all of these phases. In the set phase, when you're defining
fine grain permissions, there are two sets of
features that you can use. The first one is IAM policy generation, and the way this works is you create a broadly permissive policy, hopefully in a test environment. Please don't do this in production, and let your application run, and what happens is a bunch of things show up in your CloudTrail logs. Policy generation then looks
at what shows up in CloudTrail and then creates a recommended
least privileged policy that would allow your, that you could then go
set for your application. So, again, start out permissive, run it, get the recommended policy, then go replace the
broadly permissive policy with that more specific one. If you already have a good handle on what the permissions for
your application should be, you can just define the policy, and then you can use this other
set of tools that we have, which are policy validation
and custom policy checks. So, policy validation,
these are both sets of stat, this is a set of static APIs that you can just pass the policy into and we'll return some findings, right? Some results to you. And policy validation
is looking for things like syntactic correctness, you know, whether or not the policy is well formed, and whether or not it conforms to some set of best
practices that we defined. Custom policy checks, on the other hand, allow you to specify, "Here are the things
that I want to look for in my policies to make
sure they don't show up." So, like let's say you
don't want STS AssumeRole, or let's say you don't
want S3 delete-bucket, something like that. Things that general
applications shouldn't be doing, you'd put those in there. On the verify and refine side, this is where our analyzers or
our findings come into play. Unused access findings and
external access findings are the existing tools that we have. And like I mentioned, we
did add a third thing. I'll talk about those more here in the next couple of slides. So, with Access Analysis, we are interested in who can access what, and the who's being IAM principles, the what's being resources,
and the can access, the definition is contained in policies. On the who side, this is where unused access
analyzer comes into play. So we analyze credentials
and principle permissions on this side to let you
know what things are unused, and then on the what side is where external access
analyzer comes into play. So, again, just trying to set the scene so you get the mental model of
how Access Analyzer is set up and where all the various features apply. Unused access findings, specifically diving deeper
into some of these things, unused access findings
continuously monitors your unused access
across your organization, and the way that it does this is when you, oh, I guess before I get
started on that part, how many folks are using
unused access findings today? Okay, a few folks. Great, thank you. If you're not, this is really great. In fact, we like to think of this as like the Marie Kondo analyzer. It tells you all the things
that you need to clean up because they do not bring joy. So, you can turn this on, it will tell you, "Hey, this
permission, this access key, this role has not been used
in some period of time." And you go, "Great, I think
I'm gonna go delete that, or I'm gonna clean it up." And when we say, "Some period of time," this is something you specify
when you turn the analyzer on. So you say, "I want to start
out with maybe a period of 360 days," right? So, a year-ish. Anything hasn't been used in a year, that'll show up as a
finding, and then you go, "Yep, I can feel fairly confident that is not being used anymore, I'll just make that go away." Okay, and then you can ratchet that down over time if you want. Along with this feature,
you get a centralized view, so a single dashboard
that has all the findings. And like I mentioned, it's
good for finding unused roles, users credentials like access keys, as well as unused permissions within that are assigned to a given role. There's also a cool
feature that we launched a little while back that
for that last use case where you look at the unused permissions within a given role, we actually have a remediation recommendation
that we'll make. So we'll say, "Hey, you're not using, let's say, S3 delete-bucket," we would give you a new
version of the policy that we would recommend that
removes that permission. And then you can copy paste that, update, and then that finding will go away. All right, external access findings is, this really is the original feature that IAM Access Analyzer launched with. So what this does is it continuously monitors your resources, and this is across over a
dozen different resource types, looking for public and
cross-account access. And this feature is special and kind of related to the new thing because it uses provable security to analyze all the access paths, and basically provides
a comprehensive analysis of who has external access. So, that is cool. And that, when we say provable security, what we're talking about here is the secret sauce that we
have in Access Analyzer, which is something called
automated reasoning. So, as I'm sure you're all
aware as AWS customers, you definitely use IAM, you have probably authored
policies or seen policies, and you understand that the
IAM policy language is very, very expressive, has conditions, has operators,
has all kinds of things. And then we have a lot of
different flavors of policies, identity-based, resource-based, SCPs, RCPs, all these things, and they all come into play when we make the authorization decision. Well, as a result, understanding what those policies mean and what they're trying
to do, it can be complex. So, automated reasoning is the way that we model the IAM language so that we can answer questions
like, is this S3 bucket, does this S3 bucket permit public access? Or, does Sophia have access to my bucket? Things like this. And we do that by translating
the policies into math, and then we basically do a
mathematical proof to say, "Yes, this condition does hold," or, "No, this condition does not hold." And you can read more about that, as you can see, we
published a paper on it. That's what this picture is, and you can also read more
about it by going to this link or scanning the QR code. So, if we go back to the original mission, trying to understand who has
access to your AWS resources, external access findings are great, but they can only answer
part of the question. So, the other part of the question is, well, what about access
within my organization? In order to get that information,
we need additional tools. And as I mentioned at
the beginning yesterday, we were very excited to announce that now we have internal access findings, which is a brand new feature that is specifically targeted
at your critical resources. So, for a lot of things,
you can generally assume that the access that has
been assigned is okay, but for critical things like, say, data sources that would
contain PHI, financial data, credit card information, right? All the super secure things, things that you want to pay
very close attention to, you wanna make sure that
access is locked down as much as possible. And that is where internal
access findings come into play. So, internal access findings allows you to understand who within your, well, you can create either
an organization analyzer or an account analyzer,
and when you do that, that defines the zone of trust. So, if you create an
organization analyzer, it will tell you, "Here
are all the principles inside of my organization that have access to the target resource." Or if it's an account analyzer, it would be all the principles within the account that have access. This feature also uses
provable security assurance, so when you get findings,
you can be assured that that is all of the access
and that is the only access. We run this analysis on a daily basis, and we have the ability to tell you when new access has been granted. The other cool thing with
this feature is now there is a new central dashboard that
gives you a resource-based view that includes both external
and internal findings at the same time. This is a paid feature. And again, like I said, it's targeted at only
your most critical things. So, you'll want to bear that in mind and only choose those specific resources when you set this up. All right, so back to the mission, answering who can access your AWS resources and external access, well, now we have, with
internal access findings, we can get a complete picture. This might be a question that you have, because like I said, external
findings was something that we launched several years
ago as the original feature. And you might think, "Huh, well, great, wouldn't you have wanted
to complete the story of who can access the things
in my environment right away?" Absolutely. However, internal access is harder, and not just a little bit,
it's actually much harder. So, I wanted to take a little
time and discuss that with you because it may not be obvious right away why that is the case. So, I thought, "Okay, let me tell you, here is the actual problem
that we're trying to solve." Because with internal analysis, in order to definitively tell you Sophia has access to my RDS database, in order to make that determination, I have to not only look
at the principal policy that applies to her, I might have to look at a resource policy, I might have to look at
permission boundaries, SCPs, RCPs, all these other things
that come into the context. So, given a collection of IAM
policies, all the policies, now we have to identify all principles that have access to a given resource. So, more policies equals much harder analysis. So with external access analysis, we only had to look at
the resource policies. Now we have to look at all
the policies, all at once. So we have harder analysis, and because now we have to
identify all the principles, we have a lot more analysis, 'cause we have to also look at, okay, now once we have identified, well, we think maybe Sophia has access, now we have to go run for just Sophia. Like, okay, does she really have access? Yes. Okay, well what about Bob, or Mary? Right? So, lots of enumeration. And so you might think, "Okay, I get it. Hard. More analysis," but I thought, you know,
it might be really helpful to come up with an analogy. So, I talked to one of our scientists, one of our researchers who developed the underlying technology for this, and he's my friend and personal hero, a fellow named Lee Barnett. And I asked him to give me some insight into the scale and
complexity of the analysis, and what he told me kind of blew my mind. So, I thought I would share that with you. So, here's what I came up with. I thought, "All right,
what's a really big number that we can visualize, that
we can actually understand?" 'Cause, you know, you
see a lot of big numbers thrown around in AWS talks, but I thought, "Let's really bring it home with something that we
all can understand." Oh, and there's an
asterisk on that because, well, I do some rounding and stuff, you know, to make it
a little easier for us to talk through these things. So, I started with, "Well, how many people
are there on earth?" So, already you can see rounding, right? Today, that number's around 8 billion. So I thought, well, just
for the sake of easy math, like let's round that up to 10 billion, and that's like 10 to the 10th, okay? That is a big number for sure, but that is not even close
to what we're talking about. So then I thought, "Okay, how about the
number of grains of sand on the planet?" That's pretty big. According to scientists,
this is estimated to be seven and a half sextillion, which I didn't even
know that was a number. But, rounding, that's like
around 10 to the 19th. So, same, big, still not even close. So then I thought, "Okay. Oh, right, how about the number
of atoms in the universe?" Also an estimate from our
friend, probably astrophysicist, I don't know who thinks
about these things, but somebody does, and it
turns out this is around 10 to the 80th. Which is cool, but also still not close. And so, okay, so we're talking
about really big numbers, but you might think like, "What are all the big
numbers, what's going on?" Well, in order for us to generate an internal access finding,
the way we do this is we have to consider huge numbers
of combinations, okay? Because when you write an IAM policy, when any of us writes an IAM policy, we have a lot of options of things we can put in that policy, huge numbers of combinations. So, basically the way you can think about what the analysis is doing is just sifting through all
the atoms in the universe looking for one that indicates that we have a positive finding, okay? Oh, right, except this number isn't big enough. So, as it turns out, the actual number is somewhere around 10 to the 160th. So to visualize this, this is actually like we had our universe and a copy of our universe, and then we had to pick
one atom from universe A and one atom from universe B, and the combination of those two things, that unique combination,
that indicates a finding. So, hopefully that gives you
some sense of the difficulty that's involved here. So, you might think to yourself, "Jeremiah, that does not
make any sense at all. I mean, there's not enough compute to even enumerate all of
the atoms in the universe, 'cause wait, how would that even work?" (audience members chuckling) No, it's not magic. It's math. Well, and to be frank,
it's math and some very, very clever algorithms so
that we can try and avoid looking at most of the combinations. And by most, I mean almost all, because there's no way we
can look at everything. And with that, hopefully you found that illuminating, I'm gonna hand the reins over to Sophia, who's gonna walk us
through some awesome demos. - Awesome, thank you, Jeremiah. So now that you guys saw the theory of how we were able to build this service and do all of this enormous computation, I'm actually gonna put it into practice with some live demos and complete our mission. So, our mission today was to
understand who can access what, and to do so, we're gonna
pretend that Jeremiah and I, we work at a boutique cake shop. I am the security admin, Jeremiah is a developer, and you're gonna see where
Jeremiah comes in later. But, we're a boutique cake shop, don't have a lot of people, but, for sure we've got some crown
jewels in our AWS environment. And, for the first, actually, lemme show this, for the first demo, my CISO has asked me to understand and inventory who has access to our
organization's crown jewels, our super critical resources. And there's three in
particular, there's an S3 bucket that's got a super secret recipe, DynamoDB table that contains some sensitive financial information, and then an RDS snapshot that
contains customer PII data. So I'm guessing many of
you guys, similar things. Probably not a secret cake recipe, but you've got some resources
that you really need to know and have locked down on who has access. So, let's switch over to my demo computer, and where I'm gonna start is in the Access Analyzer dashboard. So today, you're gonna see there is an existing external Access Analyzer, which I hope many of you
guys already have turned on. It's free. It's telling me whether
any of my resources allow public access, or
allow access out of my, allow access outside of my organization. But remember, my mission here is to understand an inventory
who has access within my org. So to do so, I'm going
to create a new analyzer, and you'll see we have the
three different analyzers that Jeremiah talked about. The new one is internal access, so I'm gonna select the middle one. You can change the name if you want to, check that the region is the right one, and then the zone of trust, I'm gonna keep this at the organization because defining the zone of trust determines the scope of the analysis. So when I say org, that
means I want Access Analyzer to go grab all of the data for all of the principles in my org. If I had chosen account, that would mean I only
look at the principles within my account, so I'm
gonna leave it in the org. And then for resources to analyze, there's three different ways I can select. I can select resources
by choosing which account and the resource types,
or I can be very tactical and paste in specific resource ARNs. To do this at scale, I can also upload a CSV
with all of those ARNs and account numbers, but I happen to know where
all my resources are, so I'm going to select by account, and I'm going to select all
supported resource types. And within my organization, I know that all of our crown
jewels lives in a account that's called Crown Jewels Account. So, I'm gonna go ahead and
add all of those resources, and what this table is now showing you is that for the six resource
types that we support today, Access Analyzer is gonna
grab all of that information about any existing S3 buckets,
DynamoDB tables, et cetera, that are in this Crown Jewels Account. And also, if any new ones get created, we're also going to be
analyzing those as well. I will go ahead and create the analyzer, and what's gonna happen in the background is Access Analyzer's gonna go and fetch all
of that information, not only about the resources, but also about every single principle within my organization. So if there's a role with
20 policies attached to it and a permission boundary
and SCPs and RCPs, we're grabbing all of that up and then doing the automated reasoning. So, I'm in a boutique cake shop, we're gonna pretend this is a bake show. I actually already have
an analyzer pre-created. So, I'm gonna select analyzer, and this is the internal access analyzer that I already created. So, with this updated dashboard, now what you're seeing
is a comprehensive view of external and internal access. So, top line metrics, I've
got, you know, this new number. The resource types tells me all of the different
resource types being analyzed across external and internal, so that's why you'll see some of, some additional resources that are not supported by
internal access right now. And then this key resources
widget is really cool, because now it tells me
at the resource level all of the resources
that are being analyzed. Previously, if you had
looked at Access Analyzer, we were giving you information
about at the findings level, but now we're bundling it together and letting you know about your resources, because that's really what you care about. So that, you know, seeing
the full list of resources is also available under
the resource analysis tab. And at this table, my top three resources are the ones that my CISO
asked me to do an inventory on. So, I'm gonna go ahead and click on my secret cake recipe, S3 bucket. It lives in the eights account, which is the crown jewels account. And then here, I can see the full list
of all of the findings. The first one I noticed,
there's an external access. I'm gonna wanna double check
that later and make sure that our organization actually intends for somebody outside to
know our secret recipe, but let me take a closer look at all of the internal access findings. So, I see a bunch of roles
from the threes account, this is our kitchen account, and I'll see delivery drivers got access, the sous chefs got access,
the pastry chefs got access. The delivery driver's
delivering our cakes, I don't think that he should have access, so let me take a look at this finding. Ah, indeed, he does have some read access. I'm going to wanna go
and remediate that later, because he really doesn't
need to know the secret recipe when he's delivering cakes. Let go back, and pastry chef makes sense for her to have access, but let me double click on my sous chef and see what level of access she has. So, she has read, which makes sense, but she also has write access, and I don't want her being able to modify or delete our recipe, so this is also some permissions that I'm gonna go and
remediate later as well. One other thing to point out is that the access you'll see on the condition, we, Access Analyzer is able to pull in the condition, any condition keys that are relevant in granting access. So this is a very simple condition key, it's AWS principle account, but you can imagine if access was gated based off of Source IP, or if it was gated off
of principle org ID, or some other condition keys, we're able to pull that in and give you that level
of information as well. One other thing to note is
that sometimes people forget that same account principles
get access to a resource. The way permission models work, it's either the principle
permissions grant access or the resource permissions grant access, and with internal access, you get to see that really show up. So, besides principles
and the threes account that get access, you also see some other
roles in the same account, in the same crown jewels
account that have access, and you can audit and make
sure, is this actually intended? So, this was information on my super secret S3 bucket cake recipe. Next I'm gonna take a look
at our financial data, our DynamoDB table that's
got some revenue information, some customer credit card information. So, let's look at all
of the active findings. And first, I noticed these
are all internal access, so that's good. Nobody outside should be having access to our revenue information, but let me take a look at who has access. So, this fours account
is our finance account, and I noticed that my CFO has
access, which makes sense, and she has read access. So, she's got describe and get item. Just the other day, she
was actually telling me that she was trying to write
to my, our DynamoDB table and she didn't have access. So, this finding shows that
it demonstrates and proves indeed, out of all of
the effective access, she really only has read access. So, what we can do is
actually take a closer look at the policies that she
has on her principle. So, she's in the fours account. I am logged in on my other
browser to the fours account, and this is, again, this
is the finance account. I'll look at the CFO, the CFO role, and you can see the permissions that she has is DynamoDB full access. However, she also has a
permissions boundary attached, and the permission boundary is what is denying that right action right there. So, even though the DynamoDB table may be granting that access, we evaluate the full effective access, and that's the finding that we show. So, that's the financial
data, our DynamoDB table. And you can see, we also have, an accountant also has access, but let me take a look
at my last resource, which is the customer PII snapshot. So this is used as part of our CRM tool, it's got customer PII information, so we also wanna make sure, yes, this is all internal access only. And I have an app developer in our apps account that has access, so let me just check what
kind of permissions he has. And I'll see that he's got
some RDS read permissions, but he's also got some
write permissions as well. And in particular, disable
and enable HTTP endpoint. I had established a SCP on
principles in that account, and I thought that I had
blocked those actions for everybody except for the admin. So, you'll see here, in this finding, we see that
the RCP and SCPs are applied, those restriction fields are applied, which means Access Analyzer
is evaluating SCPs and RCPs, but that probably means my SCP is not doing everything
that I thought it was doing. So, let me go into organizations. This is my management account, so I can go to the orgs console, and that, the app's account
lives under my workload OU, so let me see what
policies are being attached to that app's account. So there are some RCPs
and then there's an SCP, and you'll see, yes, there is a limit RDS actions
attached to this account, but if I look at the policy, I did not block enable
and disable HTTP endpoint. So, the finding is showing me I didn't restrict everything
that I needed to in my SAP, this is something I'm gonna
go and remediate later. So, that was demo number one. I have all of these findings,
I can now take this report to my CISO, but my CISO comes back
with another ask and says, "Great, now you've done the baseline. We know who's got access
to our crown jewels. Is there any way for you
to refine that permission? Are any of the roles and
users that have access not actually using any permissions, and can you go and remove those?" Again, moving towards
least privilege, right? So, here's what I'm gonna do next. I am back in my Access Analyzer dashboard. The top part, this is all
about resources, right? So, we have the external,
internal access findings. I can also then create an
unused access analyzer. So unused access, all
about the principles. Same thing here, I can
change the name if I want, I can also modify the tracking period. So, this is my definition
of what is unused, right? Anything that hasn't been used in 90 days means they're not using,
it should be remedied, so I can change this. And then, as Jeremiah said, a few months ago, we
allowed you the ability to even scope down and say, "I only care about these accounts, or, "These accounts don't
need to be analyzed, or these roles and users." So I can go ahead and
create this analyzer, but, just like a bake show, I already have the analyzer created. So that unused access finding shows up on the bottom half of the dashboard, and my tracking period is five days because that was the amount
of time I had to, you know, get everything set up. But for many customers.
we hear three months, six months is usually the tracking period that works for them. And on the unused access
dashboard, you get to see, you know, all of the different
types of unused access, and also you get to see
them grouped by accounts. So, the example I'm going to go with here is the kitchen account. So the kitchen account, remember, they were the ones who had access to the secret cake recipe, the S3 bucket, so I wanna take a look and see if there's any unused access here. And there's a way where you can filter the different findings. We see some unused
permissions, unused roles, but I wanna go after the heavy hitters, and that is unused credentials. So, long live credentials. Hopefully you're not using IAM users, but if you are, if they exist in your environment and you wanna trim those down, you can use unused access to find them. So, I see that my sous chef actually has access keys that
they have not been using. So, yes, so this is something that I'm going to go and remediate. I'm gonna talk to our developer, get them to, you know, confirm and get rid of
this long lived access key. So, this is just one
example I can go through. There were all of the additional findings that we can go and trim down permissions, trim down other, you know,
unused passwords as well. So, that was demo number two. And then next, demo number three. Now that we've baselined everything, I want to empower our development teams to be able to know when any
new access is being granted, and I'm the security admin. You know, I work in the management
delegated admin account, but these resources
live in other accounts. These resources live in accounts that are managed by Jeremiah, and so I want Jeremiah to be empowered to know when new access is being granted so that he can go and remediate
permissions on the bucket, permissions on his IAM roles as needed. So, for this last demo, what I'm going to do is actually utilize our EventBridge integration. So, EventBridge, I'll go to EventBridge, and what we're gonna do
is create a new rule. So, I'll call this my crown jewels rule, and I want Jeremiah to
be notified whenever Access Analyzer internal
access findings are generated. So, we'll use the pattern form. The event source is
gonna be an AWS service. In this case, this is Access Analyzer, and the event type is
internal access findings. So you'll see there are
a couple different ones, but this one in particular,
what I wanna do is on internal access findings. So next, I want to send these findings to SNS because I want Jeremiah to get an email. So whenever new findings are generated, I want him to get an email. But, you may have different workflows, so you may want to hook up
EventBridge to other services or to your own custom
change management workflows. So, for this one, I'm
just gonna use SNS topic. And for the topic, I also
pre-created an SNS topic, but then I can show you guys that one. So, the internal access
findings, SNS topic, you'll see here the subscription is I have it sending an email
to Jeremiah, Jeremiah Dunham. So, let's go ahead and select that. And then next, we don't need
to add any tags for now. And then, this is the event pattern. This is a really simple one, it just says, "Any new
internal access findings, generate an EventBridge event," which then sends a
notification through SNS and sends Jeremiah an email. But this is super configurable, there's a lot more configurations that you
can do with, you know, filtering and things of
exactly what gets sent where. But this is a very simple one, and then I can go and create the rule. And so now that means my crown jewels, Jeremiah's going to get new emails whenever new findings are generated. - [Jeremiah] Yay. - All right, so, we went
through three demos, and this is just the beginning right? Access Analyzer with this
new internal access finding, we're empowering you to know who within your organization
has access to your resources, to your own organization's crown jewels. One, as we were building this, you know, one of the things we
knew customers wanted was this powerful information. It's great that it's an
Access Analyzer dashboard, but I want this information
where I'm working. And a lot of customers, they
use third-party integrations, so we're really excited to announce that, at launch, we have five partners that are integrated or integrating, finishing their integrations
with Access Analyzer. So, these are the five partners that are going to be ingesting
internal access findings, so what this means is that you create these internal access findings
in your AWS environments, and then these partners will be able to slurp up those findings, enrich them within their platforms, adding additional risk analytics, and then being able to surface insights and recommendations for you. There's one partner that
I wanted to highlight, because they did finish their integration, and it highlights one of
the top asks that, you know, we know a lot of customers are asking. The next question after this of, "Great, I know that there are
specific IAM roles and users that are granted access, but what about my user identities?" And so, Saviynt is one partner that has an integration
with Identity Center. So, that means they know
your user identities from your IDP, and what they're able to do is make that connection
of the user identity, what accounts do they have access to, what IAM roles and users
they have access to, and then thread that along to then what are the critical
resources in your organization that they have access to? What they're able to do,
there's a new feature, if you click on that, that resource is to be
able to show permissions on that resource, on
that critical resource, and what they do is ingest
those internal access findings. So, you'll see basically this category, these boxes include all of those items that are available from the
internal access findings. So, takeaways for today,
IAM Access Analyzer, we've got a number of features all to help you on your
journey to least privilege. Today, we talked about the
new internal access findings. Many customers have these critical data in these three services, the
DynamoDB, S3, RDS resources. So if you have those,
turn on internal access to get that picture of who within your
organization has access. We also did a quick demo of unused access, also use unused access to
trim down the permissions that your principles are not using. So, if there's long lived credentials that are not being used,
definitely get rid of them. And then with external access, we launched five and a half years ago. If you're not using external access, definitely go turn it on. It's a free feature, and
external with internal together gives you that 360 degree of
who within your organization and who outside of your organization has access to your most
critical resources. So, with that, thank you for joining us today to learn more about Access
Analyzer and our new future, and we will hang around
afterwards for any questions. - Sounds good. (audience applauding) - [Sophia] Thank you.
