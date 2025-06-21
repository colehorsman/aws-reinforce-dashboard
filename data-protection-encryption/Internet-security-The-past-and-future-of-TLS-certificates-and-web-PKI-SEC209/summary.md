# AWS re:Inforce 2025 -Internet security: The past and future of TLS certificates and web PKI (SEC209)

**Video Link:** [Watch on YouTube](https://www.youtube.com/watch?v=lZLNPtL8-2c)

## Video Information
- **Author:** AWS Events
- **Duration:** 51.5 minutes
- **Word Count:** 8,725 words
- **Publish Date:** 20250620
- **Video ID:** lZLNPtL8-2c

Looking at this AWS re:Inforce 2025 session transcript about TLS certificates and web PKI, I'll extract the key information to replace those placeholders:
markdown# AWS re:Inforce 2025 -Internet security: The past and future of TLS certificates and web PKI (SEC209)

**Video Link:** [Watch on YouTube](https://www.youtube.com/watch?v=lZLNPtL8-2c)

## Video Information
- **Author:** AWS Events
- **Duration:** 51.5 minutes
- **Word Count:** 8,725 words
- **Publish Date:** 20250620
- **Video ID:** lZLNPtL8-2c

## Summary
This session explores the evolution and future of TLS certificates and web Public Key Infrastructure (PKI), featuring a collaboration between AWS and Let's Encrypt. The presentation covers how Let's Encrypt transformed certificate issuance from a manual, expensive process to automated, free certificates that enabled widespread HTTPS adoption. The session details Let's Encrypt's technical architecture, upcoming innovations like 6-day certificates and IP address support, and addresses the critical challenge of post-quantum cryptography. AWS's role as both a supporter of Let's Encrypt and operator of Amazon Trust Services is discussed, along with the industry's preparation for quantum-resistant cryptography.

## Key Points
- **HTTPS Transformation**: Let's Encrypt increased HTTPS adoption from 39% of page loads in 2015 to widespread encryption across 600 million websites today
- **Automation Revolution**: Moved certificate management from manual, expensive processes to fully automated issuance and renewal
- **Technical Scale**: Issues 6-7 million certificates daily with $4.5 million annual operating budget, demonstrating efficient nonprofit operations
- **Short-lived Certificates**: Transitioning from 90-day to 6-day certificates for improved security through faster key rotation rather than relying on revocation
- **Privacy Improvements**: Replacing OCSP (Online Certificate Status Protocol) with CRLs (Certificate Revocation Lists) to eliminate privacy risks from browsing history exposure
- **Infrastructure Innovation**: New "tiled" certificate transparency logs reduce operational costs by order of magnitude while improving reliability
- **Post-Quantum Readiness**: Industry preparing for quantum computer threat to current asymmetric cryptography, with focus on TLS handshake protection first
- **AWS Integration**: Amazon Trust Services runs 100% in AWS cloud, demonstrating cloud-native certificate authority operations

## Technical Details
- **Let's Encrypt Architecture**:
  - 25 staff managing $6.7 million annual budget across three projects
  - 12 engineers (3-4 on certificate authority software, 8-9 SREs)
  - Custom "Boulder" certificate authority software written in Go
  - Hardware Security Modules (HSMs) for private key protection and signing
  - Three racks of hardware across two locations for compliance requirements
  - Domain Control Validation using ACME protocol challenges

- **Certificate Innovation**:
  - 6-day certificates available through ACME profiles specification
  - IP address certificate support (limited to short-lived certificates only)
  - ACME Renewal Info polling system for proactive certificate renewal during revocation events
  - 90-day certificate lifecycle designed to encourage automation over manual management

- **Transparency and Revocation**:
  - Certificate Transparency logs handling massive scale (AWS credits essential for operation)
  - Migration from RFC 6962 to "Static-ct-api" tiled logs using S3 storage
  - OCSP service termination (August 4, 2025) handling 84 billion responses per week
  - Maximum Merge Delay elimination in new log architecture

- **Memory Safety Initiative (Prossimo Project)**:
  - Ntpd-rs (already deployed), Hickory DNS, Rustls, and sudo-rs
  - Rewriting critical internet infrastructure in Rust for memory safety
  - Reducing security vulnerabilities from C/C++ implementations

- **Post-Quantum Cryptography Preparation**:
  - ML-KEM (from Kyber) standardization through NIST process
  - AWS implementing PQC across API endpoints (KMS, Secrets Manager, ACM)
  - Formal verification and automated reasoning for cryptographic correctness
  - HSM hardware support requirements for high-throughput signing (10,000+ signatures/second)
  - Timeline pressure: quantum computers potentially viable in 3-10 years
  - "Store now, crack later" threat model for encrypted network traffic

## Full Transcript

- I'm Josh Aas. I'm the Executive Director at Internet Security Research Group, and we run Let's Encrypt. - So welcome to our session. We're going to cover some of
these items on the agenda. Just very quickly, we'll talk a little bit about, I'll start off by
talking about relationship with ISRG and the Let's Encrypt team, which has been a really
good and fruitful one. Just a little kind of intro section. I'll hand off to Josh
for probably the bulk of the conversation, which
will be around these items, you know, kind of two,
three, four, five, six. So TLS overview, some history of web PKI, the background for Let's Encrypt, something about the organization, and a little bit about the future for PKI from the perspective
of the Let's Encrypt team. And then I'll close with
a short section on PKI from the perspective of
post-quantum cryptography, which is obviously an interesting
topic that we all have to become more and more aware of and start to, start to address. So let's get going here. Here's the clicker. Oh, I start, sorry, - Things are gone. - Lack of rehearsal here. So we've had a great relationship with the Lets and Encrypt team. We've been both able to help the team with direct contributions, so
cloud credits for running some of their infrastructure, some of their critical infrastructure. We also have been able to contribute through an organization we call
Alpha-Omega, where a number of the large cloud providers get together and collaborate around helping
the open source community increase and kind of do
uplift around security. Great example of that. Another part of ISRG is
the Prossimo Project. So there's a project where
we're funding the creation of a lot of critical secure tools that are widely used in the
infrastructure of the internet in rewriting those in REST language. So REST provides the performance of a C, C++ implementation,
but with the language and the compiler enforce
a number of memory safety and threat safety capabilities, which in the end we believe will result in fewer bugs and fewer security bugs. So that's been a great project. We both use Let's Encrypt for our Amazon Trust services. So we issue, as you know,
public certificates, we'll talk a bit more about that. And the Certificate Transparency Logging, we're a heavy user of the capabilities that the Let's Encrypt team has. It's also the case that we get
the statistic from you guys, which is that a lot of
Amazon customers are users of Let's Encrypt certificates. Even though we have ACM and we have capabilities in this space, it's still super useful to be
able to have access to these, you know, state-of-the-art capabilities from the Let Encrypt team. And a lot of Amazon
customers are using that and they can, you know, sort of tell by address space like
what's coming from AWS and what's being, what's being
used by their infrastructure. And we'll talk a little bit more about how Let Encrypt uses AWS. One quick little note, people,
just to be super clear, we've now just this week launched for the first time the ability to use ACM certificates outside of AWS. So to this point, that
was always a feature that was confined to our endpoint. So you could have a free
certificate automatically rotated for ALB, CloudFront and LB, other types of infrastructure that we provided. And we even provided this
kind of interesting capability to use our enclaves feature so that you could deploy a
certificate to an EC2 instance and the private key would
get automatically deployed into an enclave and we
could do TLS termination in that fashion. But till this week,
we've never allowed you to fully export not only the certificate, a public certificate, but also the associated private
key to make it fully usable outside of AWS. Customers over the years
have said, we, you know, we love the free certificates
from Let's Encrypt, but we'd really kind of rather manage things
in a more central way. So now we've enabled this feature and it's a paid feature, so not free. Still, you know, hopefully
reasonably priced and will be useful for customers. And I'll talk a little bit about the end about how in the, in post-quantum
world, this is interesting because now customers are
accessing a very sensitive piece of data, which is the secret key and you can now use post-quantum
resistant cryptography to actually download those keys. We'll talk about a little
bit more of that at the end. And main point is the last bullet, which is our collaboration with
Let's Encrypt remains strong and will continue into the future. So let's get more into
how you guys operate. - Thanks. I'll start by going over a
little bit about the basics of TLS Security. TLS really provides two different things, authentication and encryption. You need both of these things
to have a secure connection. The certificate stuff
we're talking about today is about authentication. But like I said, you need both. Authentication is making sure
you are talking to the entity that you think that you're talking to. Encryption is making sure
that conversation is secure. So you can imagine all sorts of problems if you have
one without the other. You could have an encrypted
connection that's, you know, well encrypted, but you're talking to the wrong person on the other end, or you can be talking to the right person, but a bunch of people's gonna
be listening in the middle. So you need both these things. Certificates or what the
authentication, like I said. And the really specific thing that certificates do is they tell you which cryptographic keys you should use for a particular entity. So if you boil a certificate
down to its essence, it is connecting a domain
name and a public key. It used to be that if you
want, so you need a share, you need a shared secret with whatever server you want to talk to. And it used to be that if you wanted to have a shared secret, you know, if Mark and I wanted to share a secret, we'd have to go find some private room to meet and come up with a shared secret together and then we would have that. But if Mark and I wanted
to create a shared secret when we're thousands of miles
away from each other, it used to be there wasn't a great way to do that. Now we have something called
public key cryptography, it's been around since
I think the late '70s, where we can create shared
secrets without ever having met. And in this scheme you have a
public key and a private key. The public key, as you
might guess something you make public private,
you keep to yourself. So in a certificate that
lists the public key that you should use to talk to a website. We need to make sure that when
we issue these certificates, they, you know, are matched
up with the right public key. So we do this through a process called domain control validation. And control is a really key word here. A lot of times you'll see
people either incorrectly or casually refer to the
question of who owns a domain. And that is not really
at issue in this system. You know, when I use a
domain, for example, on AWS, I may own the domain, but AWS is getting a certificate from me because they are the ones who have delegated control of the domain. So we need to just do
control here, not ownership. The way that that works
is through challenges. So we issue a challenge
as a certificate authority and you as a domain
controller, you have to prove that you have control of a domain. So in this exam, in this you
know, diagram, you can see that the web server is
saying, I would like a certificate for example.com. And then Let's Encrypt
is issuing a challenge. And we're saying, essentially
put a big random number at a path that you
would only be able to do if you actually controlled this thing. Then once we've issued the
challenge, the web server has to complete that challenge. So part of that completion
is signing an account key, signing a NOS with an account key and that's what you see at the top here. But you also need to
place this random number at a certain path and then
Let's Encrypt will go out and check to make sure
that you actually did that. So let's talk about a
little bit the history here. We started in 2015. Prior to 2015, the reason that we started Lot
Encrypt is that getting and managing certificates
was quite painful, and as a result of that, people weren't doing it often enough and the web was largely not encrypted. It was pretty complex. You know, there's, if you got
a certificate prior to 2015, there was probably a lot of
clicking around website UIs and using arcane OpenSSL commands to generate a certificate signing request, a bunch of back and forth. It was expensive, tedious. And the result of this is
that in 2015, about 39% of page loads used HTTPS, and that's paged loads, not websites. Those 39% of page loads are
quite concentrated on some of the biggest websites on the internet. The percentage of encrypted
websites is far lower than that. We wanted to do something about that. I was working on web browsers back then, and it's frustrating to work
on security in a web browser when all the data coming
in isn't encrypted. We wanted to get to 90% HTTPS or higher and we wanted to do it
in about five years. Five years seemed like the fastest we could possibly
realistically pull this off, and we did not want this to
turn into an adoption timeline, the kind of thing you see
for IPV6 or DNSSEC, right? That is way too long. We wanted to get this done in five years. The roadblock to this was getting
and managing certificates. It wasn't obvious to us in the beginning, but it became obvious the
more we looked into this, that that's what we needed to deal with. The solution that we came up with here was to start a new certificate authority. We thought about all other
things we might be able to do to solve this problem. They weren't gonna get us
to that 90% in five years. We needed a new certificate authority that just did things differently from how, from how they had always been done before. In 2013, we started planning this out. In 2014, we incorporated a nonprofit. We had some great sponsors and volunteers and other people involved to
help get this off the ground. And in 2015 we issued
our first certificate. In 2013, I personally knew very little about building and running a CA, so I had a real crash
course going through this. Moving forward to today, over time, you know, we
started off at no websites, no certificates issued, and today we're up at
about 600 million websites, over about 500 million certificates. That works out because certificates can have
multiple domains on them. So we can cover 600
million websites in fewer than 600 million certificates. So let's talk a little bit about what Let's Encrypt
actual, consists of, you know. So Internet Security Research Group, ISRG as we call it for
short, is the nonprofit that runs Let's Encrypt. So Let's Encrypt is the name of a service, not the name of a nonprofit. ISRG is a nonprofit, Let's
Encrypt is a service. ISRG actually runs three
different projects. Let's Encrypt is by far
the most well-known, but we have a second
service called Divvi Up that does privacy respecting metrics. And a third project that is not a service, but that's where we work on building and adopting more memory safe software for core components of the internet. We have about 25 staff, and our annual budget
is about $6.7 million. Only part of that is Let's Encrypt. I mean, most of it is Let's Encrypt, but not all of that 6.7
million is Let's Encrypt. For Let's Encrypt in particular,
there are 12 engineers, there's about three or four
at any given time working on the software for the
certificate of authority, which is open source. And we've got about eight or nine SREs that operate our infrastructure. Those staff are supported
by Fundraising, Finance, Legal, Comms, HR and Management. For physical infrastructure, certificate authorities
actually can't use the cloud. It's not allowed per the rules. We do use the cloud for some systems that are not involved in the actual literal
issuance of certificates. So we use AWS for some
non-issuance systems related to monitoring and logging
and things like that. But the actual issuance
happens on our own hardware. It's about three racks
of hardware distributed across two different locations. It's got, you know, the only thing that's different than the usual mix of hardware you would see for something like this compute database
networking is that we use HSMs to protect our private keys and actually sign the certificates. HSM stands for hardware
certificate module. It's basically looks like
a rack server with a bunch of special stuff to protect private keys and handle high capacity signing. Our physical security is a bit more robust than a typical data center set up. I get into the details here, but it's relatively difficult
to access our hardware. Like I said before, we use AWS for some non-issuance systems. We use CDNs for OCSP and
CRL revocation objects, and we have some accommodations
for key ceremonies. So that's where we
perform a special ceremony to generate the private
keys that are the root of trust for Let's Encrypt. - So before you move on,
I have to comment here. So what you said is completely accurate. However, Amazon Trust
Services does actually run 100% of AWS. The industry's in a transition period where yeah, physical infrastructure
is considered, you know, necessary for certain security properties, and we're this kind of hybrid state that we actually own all the hardware and the infrastructure
that we need to run our CA. So while we haven't yet
ever seen an example of other CAs running 100% in the cloud, AWS is able to do that, and we'd like to get to a point where we can convince the
auditors in that community that we provide all the necessary
security at the physical and other layers to do that. We use, in our case we use
KMS as our fundamental kind of, you know, crypto, a fleet of HSMs as which are behind
our KMS service and so forth. So I didn't, I couldn't resist jumping up and saying that there is at
least one vendor in this world that runs their CA full 100% in the cloud, but it isn't common and it's
probably gonna be a journey before that becomes a commonplace thing.
- Yeah. There's certainly times when I wish we had more access to cloud resources and-- - We should work on that together. - Yeah. - You should be number two. (Mark laughs) - A software stack, you know, Linux Prox Max or virtualization. We make pretty heavy use of
OpenZFS for a bunch of things. Probably not a shocking software stack. Might be roughly what you expect. We write our own certificate
authority software. It's called Boulder. It's on GitHub. GitHub, it's written in Golan. A lot of other CAs don't
write their own software, which is why this is somewhat notable. But we do 'cause the way that we issue certificates
at least was very different from how it had been done before. Though I think more CAs are
going to the model that we do. So it's not such a, such
a niche model anymore. Another thing that we
think about when we think about our infrastructure is memory safety. There are all sorts of ways that you can have security issues in your infrastructure. One of the most dangerous ones is memory safety,
vulnerability, vulnerabilities. It makes me nervous to see large piles of CNC++ on the other
side of a network port or on a privileged boundary. I think there's a lot of
evidence to back that up and why that should make anybody nervous. So in part for the
security of Let's Encrypt, but also because we want
to help everybody else, we have our Prossimo
project where we build certain critical pieces of software and functionality in safer languages. A lot of the time for Rust,
that's Rust, you know, but like I said, we also
use Golang quite heavily. Most of Let's Encrypt
is written in Golang. So we built these four
pieces of software here. Ntpd-rs is already
deployed at Let's Encrypt. It works great, we have
no problems with it. Hickory DNS will be next later
this year or early in 2026. Rustls will be shortly after that. And somewhere along the
way here we're gonna add sudo-rs as well. So we're very happy to be able
improve our infrastructure by bringing additional memory safety. So that, the output of this whole system that we've been talking
about, the engineers, the infrastructure, the
software, stuff like that. We currently issue about 6
million certificates per day. I think there was a day recently where it was seven or 8 million. It's still growing pretty rapidly. It's 600 million websites covered, and it's also growing pretty rapidly. It's not gonna be too long until that's 1 billion, it looks like. For revocation, we run
a service called OCSP where you can get revocation information. We do about 15,000 requests
per second at the origin and 139,000 requests
per second at the edge. We're actually turning
off OCSP later this year. I'll get into that in a later slide. This number here is just to give a sense of some of the scale. And we also operate
certificate transparency logs. And those are used by Let's
Encrypt but also by other CAs. So any certificate authority
can submit their certificates to our logs and then
reading is public as well. And that's a place where AWS
really helps out quite a lot 'cause those logs do operate
in AWS infrastructure, and it would be tough to
do without AWS's support because they're not that cheap to run, which is another thing
that we'll get into later. All this costs about $4.5 million a year. In some sense, that's a big number. In another sense it's not
that big of a number, right? I think there are probably
quite a few companies around the world that have internal PKIs that cost less than 4.5 million a year. So we're quite proud of what we're able to do on this budget. And AWS has generally contributed, generously contributed a
lot of credits that help us with our cloud-run services. So we can talk a little bit
about what's coming next. Probably the biggest feature that we've put out there in a long time, and that it will be
generally available this year is short-lived certificates. When we started Let's Encrypt
in 2015, it was not uncommon to see certificates that were
valid for three years or more. That has come down over time. But when we started, we said that all of our certificates are
gonna be 90-day certificates. There was a range of reaction
to that that for some people that seemed just like panic
level short like 90 days. Is that even a realistic
option for people? The reason we want shorter lifetimes is because if you have a
key compromise, revocation of certificates doesn't
always work that well. It's not something you
really wanna rely on. If you have a key compromise, it's either because you made a mistake or something like Harp Bleed happens. What you really want is
those certificates to age out of the system relatively quickly, 'cause the only revocation that actually works reliably
is the expiration day. So Harp Bleed, I forget
exactly what year it was, but it was-- - 2015. - Somewhere around 2015. 2015, yeah. People with three that had just got a three-year certificate
issued during Harp Bleed, they're in a tough spot. You can get that certificate revoked, but a lot of people
don't check revocation. It's a fail open system. We don't want people
to be in that position. And if you're gonna
automate all your stuff, then it doesn't really
matter if your computer is getting the cert for you. It doesn't matter whether
it renews every 90 days or every six days or whatever. So what we would say to people who were concerned at the
time about 90-day certificates is that this is not a
certificate authority for people who want to manage certs manually. If you wanna do manual
certificates, like maybe you can do that on a 90-day cycle, but you are not the
target audience for this. We really want people
to move to automation that has so many advantages. So 90 days gets people better security and it really pushed
people towards automation. Pretty soon we are going to make six-day certificates
generally available. We have issued some production
six-day certificates, but we've only issued them to ourselves for testing purposes. Pretty soon there will be an allow list and then general availability. There's a feature called
profiles introduced in the ACME specification
where you can say which type of certificate you want. Up until now, there's
only been one option. You get one kind of certificate from Let's Encrypt and that's it. That's gonna change with profiles. There'll be a default if
you don't select anything, but you will be able to opt
into six-days certificates and that is a big change for us. It's the first time we've
ever issued a certificate that wasn't 90 days. It changes a lot on our
end in terms of volume, and I mentioned before that
certificate transparency logs are not that cheap to run, right? They have to ingest every certificate. Well, once a lot of people start using
six-day certificates, you're issuing a lot more certificates to serve the same population. So for us, you know, we, we need to get ready to issue
billions of certificates of this is what the future looks like. So internally we spend a lot of time thinking about
what that looks like. What does that mean for our database? What does that mean for our certificate transparency logs? Things like that. The next thing that's coming
out around the same time as the six day certs
is IP address support. Today you can get a
cert for a domain name. Later this year we'll be
able to choose domain names and, or IP addresses. So you will not have to
have a domain name in order to use HTTTPS with Let's Encrypt. To be totally honest, I'm not really sure how popular this is gonna be, but there are definitely some people for whom this is gonna be valuable. It may turn out, you
know, a few years from now that IP address certificates
constitute, you know, 1% of our issuance. That seems believable to me. It also seems believable to me that it's a much bigger number. I think it's gonna be
the most popular for sort of infrastructure use cases, IoT and other things where humans
are less involved in the loop 'cause domain names are
ultimately a convenience issue. Computers don't care,
they just want the number. So we'll see how this goes
in terms of popularity, but we've heard enough
important use cases for this that we wanna make sure
that we support it. Did you wanna jump in about the computer?
- Yeah. It's an interesting
phenomenon that, you know, for many these decades, IP addresses were essentially
represented a host, and therefore if you had
dynamic infrastructure, you might reuse an IP, but
it was kind of, you know, there was some kind of risk in that. But as cloud technology has evolved, at least that's what I
know well, IPs have become kind of more of a virtual thing. Like I can reassign IPs
dynamically between hosts. For example, with an elastic
IP, I can bring my own BYO, bring your own IP, your own cider range, and that you can assign
willy-nilly to infrastructure. And then we have virtualization
of IP as kind of a feature for some of our services. Like our global accelerator
service gives you what are called Anycast IPs when, which is a router
conspiracy that tells the world that hey, you wanna reach
this IP address, come here. And that is around the
edge of our network. So we attract traffic. And those IP addresses are
yours for as long as you keep that accelerator alive
and they don't change. So there's there, and similarly
with network load balance or some of it in our NAT gateway. These are services in which
an IP address represents kind of an object in the system and we take care of keeping that stable even though the
underlying infrastructure changes, even though there
might be 25 hosts that we, you know, do ECMP across all those hosts with that single IP address. So that's not maybe directly
related to, you know, how often the certificates will be useful for IPs, but I just thought it
might be worth mentioning that you know, the kind of
the role of IP addresses, especially as you say like in these IoT or machine to machine
scenarios is kind of changing. And if you want to use,
potentially use IP addresses for kind of long periods of time and still have control over those and use those to kind of expose or consume infrastructure, it's a pretty reasonable
thing to do these days. - Yeah. So the reason IP address
support is coming now and not a lot early earlier is because we did not wanna
offer IP address certs for 90-day certificates. IP addresses tend to be, in general more transient than domains. You know, people buy a
domain, they own it for years, maybe longer, but IP
addresses people often have for much shorter periods of time. So we don't want to issue a
certificate to an IP address and then have that IP address
belong to someone else during the lifetime of the certificate. So we are only gonna be
offering IP address certificates for the six-day certificates. If you get a 90-day certificate,
this will not be an option. What Mark's talking about
here is that essentially that with AWS, IP addresses
don't have to be so transient, which is a nice feature of the system, but for us we are only offering them in short-lived certificates. - Yeah. That actually reminds
me of something else, which we didn't talk about
when we were rehearsing, but I'll mention it anyway. This is actually an abuse
pattern we've seen historically is people will do, you know, they'll cycle through IP addresses on our
platform, looking to try to get one that someone
else was using recently and then see the traffic that may be accidentally coming to that. So we've actually introduced
a bunch of technology to sort of have cooling off periods for IP reuse. So it's very much less likely today that you can ever get an IP that was recently used by someone else. And it's essentially to deal
with that transient problem. But I totally makes sense
to me that, you know, we're talking about automation scenarios and short-lived certificates
make sense even given what I mentioned earlier
about how IPS can be useful and can be relatively
stable over time if you use the features in the right way. - Yeah. So this I alluded to before. OCSP is a protocol for checking whether a certificate is expired. And the way it works is there's
a URL in the certificate. You can make a request to that URL and will return a signed
object that's specific to that certificate that
will say this is revoked or this is not revoked. This has been around for quite a while. It's been the most common
normal way to do it for a while, but it has some problems. The number one problem is that
it is a huge privacy risk. So if someone is out
there browsing internet, if you're browsing the internet,
if you send an OCSP request and say, Hey, tell me
about the revocation status for example.com, you're basically telling the certificate authority that you're about to visit example.com. And then when you go to the next website, you do another revocation request and you're telling the
certificate authority again, I'm gonna visit this other website now. We don't want that information and you should not want to give it to us. The way it works now
is we just drop those, we don't keep any record of OCSP requests. We drop that data. But we don't even want the
opportunity for abuse here. We don't want people's
essentially browsing history broadcast to us. So we wanna get rid of
this system in favor of something called CRLs, or certificate revocation
list, which is just an object that says, here's the
list of all the things that we've revoked and you
can see if what you want is in that list or not, and that does not have
the same privacy risk. So the main reason we're
gonna turn this off is privacy risk. The second thing here is that
it's expensive to operate. I mean, we're a nonprofit,
we try to be efficient. I mentioned before that there's, you know, so many, so much traffic happening here, 84 billion OCSP responses
per week right now. That just goes up over time. It's expensive to operate,
we don't really want to do it when we have CRLs, which are a better solution anyway. It also interestingly takes
up most of our HSM capacity. So every time we need to do a signature as a certificate authority,
that happens on an HSM where the private keys
for the CA are stored. Signing certificates takes
up something like, you know, actually issuing the certificates
themselves is like 15 or 20% of our HSM capacity, because those certs get
signed every 90 days. OCSP gets resigned, I think,
every three and a half days. So the vast majority of our
signing capacity is devoted to these objects, and
we'd rather not do that. Well, let me see, it's gonna
get turned off in August, 2025. I'm pretty sure August 4th is the date. We've already removed the
URLs from the certificates, so the traffic is already dropping off. But once the last certificate
that had a URL expires, then we'll turn the service off. We don't really expect much disruption, but we'll see what happens. Another, so ACME Renewal info is a feature that we already have, but I bring it up because it is not very popular yet. Not enough people are using it yet. And it's really important
and it's really important because this is a huge part of how we're gonna make
the web PKI more resilient. There are reasons that
certificates have to be revoked by the Certificate authority, not because you as a
subscriber wanna revoke them, but because we have to. So it could be security incidents, could be compliance incidents,
who knows what else? When we have to do
that, it is very painful because we have timelines on which we have to revoke this stuff and it's hard to reach
all the people involved and get them to take action
before that timeline hits. So if we have 24 hours or five days to revoke a certificate, that might be 1 million certificates and 1 million different
people, it is very hard for us to contact everyone and
get them to take action. ACME Renewal Info is a,
it's a polling system where your system will reach out to us. Could be as much as every few hours or
as little as once a day and say, should I renew
my certificate early now? And if we know that we're going
to revoke your certificate for some reason, let's say we're going to revoke it 24 hours
from now, we will sort of flip a bit so that when
you check, we'll say yes, please renew right now, then you can renew before we have to revoke
your old certificate. And we, and this scales
really well, you know. Worst case scenario, we're revoking 500 million certificates if we make a big enough mistake. That is hugely disruptive to the internet, it's gonna be hugely disruptive today and it will be tomorrow. And really the only hope we have for making this not hugely disruptive is to make ACME Renewal
info much more popular than it is now. So I would highly recommend that if you are running
your own certificate client, that you find a way to
use ACME Renewal Info so that if we have to revoke
your certificate someday, you can sleep soundly, your
computer will just take care of it, you don't need to worry about it. No disruption. So this is a really
important but, you know, it's something people are
not well enough aware of. We're also evolving our transparency logs. There are two different
kinds of logs out there now. What I, the older style
is called RFC 6962 logs. The new style logs called the tiled log and the formal name is Static-ct-api. And the reason that we're doing this is that we wanna make these
logs easier and cheaper to run and we wanna make them more reliable. The reason that we want make them easier and cheaper to run is not just because we
wanna spend less money or use up fewer AWS credits. It's because we want there to be more of these logs in the world. Right now, not enough
people are running CT logs, which is an issue for the ecosystem. And the reason people
don't wanna run CT logs is because it's very expensive. No one wants to spend
hundreds of thousands of dollars a year running a log. So we need to make them cheaper
so that we have more of them and that is better for the ecosystem. We also need to make them more reliable. So we run tiled logs already, and we are planning to shut down our old style logs later this year. For most certificate consumers, this is not gonna be something
you need to worry about, but it is an important
event in the ecosystem. So let's talk about the
problems are with RFC 6962 logs. First of all, they require large and expensive cloud-managed SQL databases. That's the way that we do it anyway. It's the way that I'm quite sure most of the other major
providers do it as well. These database, these databases can be relatively easily overwhelmed by dynamic queries. In other words, the people who
are querying them are giving all sorts of different query parameters, which makes the results very hard to cache or not really cacheable at all. So they get quite easily overwhelmed. The third point is what I would
say the most serious issue here, which is something called a maximum merge delay violation, which is when a certificate gets submitted to an RFC 6962 log, the log
doesn't necessarily integrate that certificate into the log immediately. It instead issues a receipt and says, I promise I will
integrate this certificate within the next X hours, where X, I think, is
usually about 24 hours. And then if the log violates
its promise to do that, the log is considered non-compliant and is taken out of the ecosystem,
which is both disruptive and means we have one fewer of these precious CT logs out there. So the maximum merge delay
introduces the potential for maximum merge delay violations,
which is a huge problem. So we'd rather have logs that
don't have this going on. The new transparency logs
don't have dynamic queries. You don't like give it
a bunch of parameters and we do a big SQL search
and put together a result. We publish very easily
cacheable tiles of data. They just exist on S3. We create the tiles, we write them to S3, and we don't have to run
these big expensive databases to back the whole thing. It drops the cost massively. They also integrate
certificates in batches and there's no more max merge delay. So the cost you get here
is there's a little bit of latency increase between
when you submit a log or when you submit a cert to a log and when you get a receipt 'cause it does need to
actually integrate it first, but it means it's not making a promise, therefore there is no promise to violate, and we don't have these
uptime issues because of that. The new logs, you know, we don't have enough
operational experience at scale and the ecosystem doesn't
depend on them yet. So it's hard to say for sure
what the final cost would be, but it's about in order
of magnitude less costly to operate than the other ones. So if you were spending, you know, $1 million a year running a log or $100,000 a year, it's like 10% or less to run the new
style logs, which is great, and hopefully that will encourage a lot more people to run them. - Could I ask a a question about that? Is it fair to say this is a
classic distributed systems move of pushing some of the
complexity out to clients? When you have millions of clients, they can do a little bit more computation and especially for the easy
queries, it's easy for them to do the computation? And if they want to do
complex queries right now, they're able to push
the complexity onto you as the server provider, service provider, whereas now they would have to do a little bit more
computation locally to check the validity of the
Merkel trees, blah blah blah. But there's a millions of them and there's only a
handful of the back end. So I think it to me-- - Yeah, that's exactly--
- It's very reminiscent of what often happened to
distributed systems is like, hey, make the clients do more work because we can scale more
effectively that way. - Yeah, I think the RFC
6962 authors had their heart in the right place where they're saying, let's make this really easy
for the consumers of CT logs. But they just ended up
being so much burden on the CT log operators that nobody wants to operate them and they're pretty cagey. So post-quantum
cryptography comes up a lot in the PKI world. There is no support for it in the publicly
trusted web PKI today. In other words, there are no
publicly trusted certificates that are using post quantum algorithms. There are a bunch of reasons for that. The biggest one is that the
rules don't allow it yet. Right now, the priorities on
TLS handshakes, which is not a, it's not a web PKI thing, but the idea is that when you
do the key exchange in TLS, you can use post-quantum. The reason that matter, well, we'll get into more about
why that matters later. Yeah, talk about that. So when is this going to
be a thing in the web PKI? So the community needs to
have an agreement on a plan. So what algorithms are gonna we use? Is anything else gonna be different? Then once we have an
agreement on a plan, it needs to result in a change to the rules that allows post-quantum signatures. But also because all of our
signatures happen inside of HSMs, we need HSMs that
support post-quantum algorithms. And not just that they support them, but to support them at
a large enough number of signatures per second. So often in HSMs for example,
they'll support a bunch of different signature types, but some of them are hardware, you know, they have hardware support and some of them are
just software support. So the ones that are just in software have like 100 signatures per second and the ones that are in
hardware can be like up to 10,000 signatures per second. We need hardware. So for some people at the scale of like AWS, maybe they have, you know, I'm certain they have
access to a lot more HSMs than we had Let's Encrypt do. So they can maybe afford to pile them up and do that kind of thing. At Let's Encrypt, we do not have access to those kind of resources. We need our HSMs to pull a lot of weight. So we need HSMs with hardware
support for post-quantum that can do somewhere in the ballpark of 10,000 signatures per second so that we can realistically
roll this out to everybody. HSMs are not a piece of hardware whose ecosystem evolves quickly. So the lead time, you know, who knows when HSMs will
support post-quantum at fast signature for a second. And what fast enough is. What is fast enough is different depending on who you are, right? Yeah, it's quite different
for a mark than it is for me. - And there's a whole ecosystem
around like FIPs validation that has to be updated. So all the laboratories that
validate the correctness of the behavior of the HSM. So there's a lot of work
to be done here, so. - Yep. So to wrap this up, some recommendations. Protect your private keys. That is like the golden rule
in the web PKI ecosystem. Don't commit them to GitHub. Protect your keys. - Don't save them on your laptop. - Yeah. (Mark laughs) Automate your issuance
and your reissuance. So if you're ever manually
getting a sort, think hard about how to get off that train and get onto the automation train. And the last one here is try
to use ACME Renewal Info. On a day-to-day basis, it may not seem like it
makes a big difference, but it eventually will. Every CA makes mistakes. We wanna be resilient when that happens and ACME Renewal Info
is the way to do that. - Great.
- I wanna turn it over to Mark. He's gonna talk a little
more about post-quantum now. - Yeah, thank you. So let's talk a little bit
more about this fun topic and we'll back up and say like, what are we
even talking about here? Well, many years ago,
academic mathematicians and cryptographers postulated and seemingly have proven that if someone can invent a sufficiently powerful-quantum
computer, then a lot of our current infrastructure that we use for encryption is in danger. So in particular, the elliptical curve, the RSA technology,
these asymmetric PKI type of signatures could be brute-forced with a powerful quantum computer. And that creates a problem for us, right? Because brute force attacks currently are just require way too much
computation to be successful. As mentioned at the very beginning, today we use symmetric encryption
off typically for like, you know, local encryption disc database and so forth, you know, using the same key to encrypt and decrypt the data. But almost all of our
network scenarios involve this asymmetric cryptography because they have this beautiful property that we can encrypt
something without sharing a secret with each other. And that's critical for
kind of bootstrapping. What's happens inside of a TLS session, as you probably know, is
one of the first things that happens is we
exchange a symmetric key so that we can encrypt very efficiently, but the outer envelope has to be done with asymmetric technology because that way we can encrypt
without sharing secrets. (Mark clears throat) Therefore, because there's a probability that at some point in the
future, experts disagree, could be five years, 10 years,
maybe three years, probably, you know, somewhere in that range, worst case, three years, worst best case, depending on your perspective, 10 years, there will exist such computers, quantum computers, which will put at risk our current asymmetric cryptography. Now you may say, well if
they don't exist until five or 10 years from now,
what are we worried about? And that leads to this,
you know, classic kind of a threat model that has been developed and the, as people have
thought about this problem, which is sort of the
long-term confidentiality of these network sessions
that are happening today. So today we have the TLS
connection between a client and a server traveling
across often public networks that are, you know, reasonably secure, but you can't ever say for
sure that there's not any way for some sufficiently resourced and motivated actor to get
access to the encrypted packets as they flow across our public networks. The threat would be that
if this today someone were to harvest and you know, grab a copy of all those packets and storm
them somewhere permanently or semi permanently in a disc driver or database somewhere,
or a giant object store, then in the future, once
a quantum computer exists, you could take that recorded session, crack that outer envelope of the PKI using your quantum technology, grab those symmetric keys that are kinda the very first
thing you'll find inside there and that can, you know, get rotated through Diffie-Hellman, et cetera. But still you, once you kind of get that outer envelope
broken, then you can begin to read all the data
inside those sessions. And therefore, when it comes
to the TLS world, we're trying to get ahead of this problem. And that's why the focus of
the cryptographic community and of governments and others and concerned about some
of these issues has been to, let's first, you
know, deal with that sort of TLS handshake and build quantum resistant
technology into that. And then as time goes by, we
can go to these other topics because that is more
of a real time attack. Like I can't emulate
your website five years in the past with a
quantum computer, right? I can't pretend to be Google and have a fake
certificate five years ago. So once the quantum computer exists, then those threats become real. Namely I could, you know,
create a fake version of some, you know, authentication material and fool you into connecting to me thinking I'm someone else. So that risk will exist once
quantum computers exist. And that's why the web PKI community has to solve the problem before
the quantum computers exist. But it's not as pressing
in those scenarios again because they don't have
this property of, you know, store now and crack later, which is, which does exist
for network sessions. So what are we doing about this? (Mark clears throat) As I said, good news here is
asymmetric crypto is at risk. And you know, sometimes when you talk to your colleagues about
this, you're like, oh no, quantum computers are
gonna break everything. No, it's, it's not everything, but it is something important,
which is asymmetric, symmetric crypto is as far as
experts are able to tell today with their analysis, it's not, you can speed up
brute forcing of like AES 256, but it's only by a factor of 1,000, which isn't nearly enough because it's super, super
resistant to brute forcing. So that's not an issue. Now, the good news here
is that the industry and the community has gotten together, been working on this problem
for a number of years. There was a kind of a
defacto international, I'll call it a beauty
contest for like, hey, let's get all the world's
best cryptographers together and have a series
of submissions and analysis and come up with what we believe to be good solutions to this problem. It was actually run by
NIST in the United States, the National Institute for
Standards of Technology, but it had very strong
international flavor and I'm not aware of anybody,
even our, some of our, you know (clears throat)
governments who are not so friendly to the US who are complaining about that. It's been a very, a very
international process. And this now has standardized on a couple of the early versions of
this including a technology called ML-KEM, which came
out of the Kyber submission. And this is now kind of the standard for doing post-quantum
cryptography on the web. Now, what (clears throat)
the, so another good news here is that we're actually,
I've already implemented in our production systems
the option to negotiate a post-quantum algorithm if
you want to connect to us over a TLS protocol. I don't have the statistics
for how often that happens. I think it's probably super rare 'cause your client obviously
has to support this as well. But it is an option. And the another really good news here is that we're open-sourcing all
the work we do in this area. So we are developing
with a broader community the post-quantum algorithms,
we're integrating them with our open source TLS
stack, our s2n stack. We're using formal, and also
another open source library we have called libcrypto. We are using formal methods
or formal verification or what we call automated
reasoning to build a formal model of the correctness of these systems and logically prove the correctness of the code that we're writing. And every time a developer
does a code check-in and then tries to make a,
you know, improve that code, we run these proofs against the check-in. So we've made the formal
methods very much part of the whole engineering process. So all these things are good
in allowing us, I think, to get ahead of it. You might say, well, why those particular
services right now? Why not EC2? Why doesn't EC2 have PQC? Well, first of all, it
will have pretty soon we're actively going to be
pushing out the post-quantum TLS across all of our API endpoints and over the next, you
know, six to 12 months. The ones we focus on now are
the ones that where you, often, where you can interact with us
with very sensitive material. And ACM is a great example. Today, this week we launched the ability to export X.509 certificates. Part of the API is to,
hey, give me my secret key. And that's a pretty
sensitive piece of data. So you can use the post-quantum algorithm for that API call, maybe just
that API call if you want to, that we, so we implement
that on these three services, KMS Secrets Manager where
again, you send us secrets or get secrets from us, and ACM, but it will become very
generally available across our API endpoints. (Mark clears throat) Again, I mentioned earlier
that the, it's not as urgent for the X.509 certificate case because the kind of store and record and crack later scenarios aren't as, are not possible. So we have a little bit
of time to get that done, but we'll work together with you folks and others around the world who care about security on the web and we'll solve that problem
and hopefully in time before the quantum computers arrive to make our lives a little more difficult. So I think that's it for our session. We thank you very much for your time. Appreciate you spending that with us and also for coming to reinforce, and we'll hang around a little bit and take your questions afterwards. Thanks. Thanks so much, appreciate it. (audience clapping)
