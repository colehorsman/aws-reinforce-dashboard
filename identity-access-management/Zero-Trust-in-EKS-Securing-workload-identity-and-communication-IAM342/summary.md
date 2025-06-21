# AWS re:Inforce 2025 - Zero Trust in EKS: Securing workload identity and communication (IAM342)

**Video Link:** [Watch on YouTube](https://www.youtube.com/watch?v=OaATzJJrB2E)

## Video Information
- **Author:** AWS Events
- **Duration:** 46.0 minutes
- **Word Count:** 7,167 words
- **Publish Date:** 20250620
- **Video ID:** OaATzJJrB2E

## Summary

This session demonstrates how to implement zero trust architecture in Amazon EKS by securing workload identity and communication. The presenters explain that traditional network-based security doesn't scale with ephemeral Kubernetes workloads that constantly change IP addresses and locations. The solution involves shifting from network perimeter security to identity-based controls using two key technologies: EKS Pod Identity for accessing AWS services, and SPIFFE/SPIRE for universal workload identity. The session covers how SPIFFE provides cryptographically verifiable identities (SVIDs) to workloads through an attestation process that validates both nodes and workloads before issuing certificates. These identities enable mutual TLS (mTLS) communication and fine-grained authorization policies in service meshes like Istio, allowing explicit authorization for every request rather than implicit namespace-level trust. The demo shows how workloads without proper identity are rejected, while those with attested SPIFFE identities can communicate securely with path-based and method-based authorization controls.

## Key Points

- **Zero Trust Shift**: Move from network perimeter security to identity-based controls due to ephemeral nature of Kubernetes workloads with changing IP addresses
- **Dual Identity Foundation**: EKS Pod Identity for AWS service access and SPIFFE/SPIRE for universal workload-to-workload identity
- **Workload Attestation**: SPIFFE solves the "bottom turtle problem" by providing attestable identities that verify workloads are running where they claim to be
- **Node-to-Workload Chain**: Attestation process starts with nodes, then extends to workloads - only attested nodes can attest workloads running on them
- **SPIFFE Federation**: Multiple trust domains can federate to enable secure communication across organizational boundaries while maintaining granular control
- **Service Mesh Integration**: SPIFFE identities work directly with service mesh sidecars (like Istio) for mTLS and authorization without application code changes
- **Certificate-Based Trust**: SVIDs (SPIFFE Verifiable Identity Documents) are X.509 certificates with SPIFFE IDs in Subject Alternative Names
- **Explicit Authorization**: Move from implicit namespace-level trust to explicit per-request authorization using identity-based policies
- **Layer 7 Controls**: Authorization policies can control access based on HTTP methods, paths, and hosts, not just identity
- **EKS Integration**: SPIRE server can use EKS Pod Identity to securely access AWS Private CA for certificate signing, creating end-to-end trust chain

## Technical Details

- **EKS Pod Identity**: Improved iteration over IRSA with support for IAM role session tags, simplified trust policies using "pods.eks.amazonaws.com" service principal
- **SPIFFE ID Format**: Standard format is spiffe://trust-domain/namespace/service-account with customizable templates for automatic substitution
- **ClusterSPIFFEID Resource**: Kubernetes CRD that defines workload selection criteria including labels, namespaces, image registries, and attestation requirements
- **Workload Selectors**: Can enforce signed images, specific nodes, registry sources, and other security requirements before issuing identities
- **SPIRE Components**: SPIRE server (central identity issuer) and SPIRE agents (deployed as DaemonSet on each node for local attestation)
- **Trust Bundle Distribution**: SPIRE server continuously distributes trust bundles containing CA certificates to enable cross-domain verification
- **mTLS Implementation**: Service mesh sidecars use SPIFFE certificates for mutual TLS where both client and server present certificates for bidirectional verification
- **Istio Authorization**: AuthorizationPolicy resources can specify principals (SPIFFE IDs), HTTP methods, paths, and namespaces for fine-grained access control
- **Certificate Chain**: Full PKI chain from AWS Private CA → SPIRE server intermediate → workload SVID with traceable attestation path
- **Federation Endpoints**: SPIRE servers exchange trust bundles through configured federation endpoints for cross-organization trust relationships
- **Envoy Integration**: Istio uses Envoy proxy sidecars to enforce mTLS and authorization policies, with x-forwarded-client-cert headers showing identity validation
- **Default Deny**: Istio requires explicit default deny policies before implementing allow rules based on SPIFFE identities

## Full Transcript

- [Chris] Good afternoon, everyone. Thank you for taking the time to be here on the last day of the conference. I know it's been a long three days, so thank you for being here. My name is Chris Sciarrino. I'm a solution architect with AWS, and with me is my colleague Matt. - [Matt] So I'm Matt Bruneau.
I'm a container specialist SA. Nice to meet you all. - [Chris] And today's
talk is gonna discuss how do we think about building
a zero-trust architecture in Amazon EKS, or Kubernetes in general, specifically focused on how do we secure workload
identity and communication? Now, before we dive into the
content, a quick show of hands. Who here is using Kubernetes today? Okay, good. You're in the right talk. Who here is using a service
mesh in production? Less hands. Okay, and who here has heard of SPIFFE? Okay, that's about what I expected. Gradually dropping off, and this aligns with a
lot of the challenges that we're facing in securing
Kubernetes environments today. Workloads running in Kubernetes,
microservices in general, they're ephemeral by nature. There's a lot of them. We might be facing hundreds or even thousands of pods in our clusters. They're spinning up.
They're spinning down. They're being recreated
on different nodes, different IP addresses, and the way we typically
secure these workloads, in traditional systems, with IP addresses and network controls, does not scale with this
type of ephemeral nature. Makes it a lot harder to do, and this is why shifting to a zero-trust mindset and
architecture is so important is we take the trust
outta the network layer and the network controls, and we shift that to something else, and today we're gonna talk about how do we shift that trust
from the network to identity, which is gonna be foundational to us having a successful
zero-trust architecture? Now, here at AWS, how we
think about zero trust is not from a product perspective. We don't believe there
is a single solution that you go and you buy off the shelf and you put it in and
now you have zero trust, but it is a security model and mechanisms that moves us from a network focus or network perimeter security controls towards having, or not just
solely network perimeter, but towards having other controls, and today we're gonna
focus on identity, right? So moving from the network
to also including identity. Matt, can you take us
through a little bit more about some of the common challenges with securing workload identity? - [Matt] Sure, so the first
question we always get is how can my workload, you know, especially running in a
Kubernetes environment, can establish their own identity? A lot of people actually
go to SSL certificate or TLS certificate, you know. As we know, there are probably
more X.509 certificate, but when you, you know, you can manage maybe tens of them, (indistinct), no problem,
not too much problem, but when you get to hundreds
if not thousand of them, there's a lot of (indistinct) operation. The actual goal is also to make them as
short-lived as possible, so that actually adds a
lot of management to it if you were to replace them
(indistinct) every hours, nobody will do that. Interestingly, inside of
the EKS, specifically, the Amazon Elastic Kubernetes Service, we do have mechanism to inject IAM roles, so we'll see that in a couple slides to your pods directly so
they can use those IAM role as their identity when they're
reached to AWS services, and the question we always get is how can I enable trust across different organization
that are kinda separate or even insides different business unit inside of the same organization? So today we will focus on two service identity big aspect, right? So you're all familiar
with the AWS IAM roles. We'll see how we can use this to access AWS services from EKS pods, and we'll also talk about SPIFFE, the universal standard
for workload identity, so I'll start first to present the Amazon EKS pod identity, so this is a service that you can use to connect your pods running inside of EKS to IAM roles, so a lot of people in this room may be familiar with what we called IRSA, the IAM role for service accounts, so EKS pod identity has the same goals, just if you want some kind of a iteration over what IRSA was providing. It does come with a couple
of interesting benefits. One of them is it does
support IAM role session tags, so you can actually use those tags to provide fine-grain control
through resource policy, and we'll see an example of that. Of course, although the call of assume role of this through the EKS pod identity
is log into CloudTrail, so you can have a nice way of following what type of action is actually being done with those, so how does pod identity actually work? So inside Kubernetes most
people start their deployment by pushing an object that we
call a Kubernetes deployment, so when you push this inside your cluster, it will create some type, you know, basic object inside Kubernetes. You also all have the AWS IAM section, where you can define role
policy and line policy, basically permission that you want to give inside of AWS. What you also define
on a specific IAM role, there's something called the trust policy. Actually, the biggest change
in between the way IRSA and the EKS pod identity actually works, and we'll see that a little
bit later in the demo, so when you have those created, so your deployment inside Kubernetes will use something we
call the service accounts, so service accounts is a
way to give your workloads permission primarily to the
Kubernetes API of your cluster, but inside of AWS, so if you wanna use the EKS pod identity, you can actually use that unique pair of cluster namespace and service accounts to link this back to a specific IAM role through something that we call the EKS pod identity association, so overall, this is really
what's provide the basic of EKS pod identity for workload
accessing AWS (indistinct). We do have an example here on the screen of what a resource policy
for a secret manager could look like when you're using the actual session tags, so if you wanna give finer
control, you can use conditions, and you can specifically
use details of the cluster and the resource tag that
it's actually coming from. Any question on EKS pod identity? Looks like we have a
couple Kubernetes expert in the room, Chris. - [Chris] All right, thanks, Matt. - [Matt] No problem. - [Chris] All right, so we
talked about EKS pod identity for that first use case of how do we have our workloads
access AWS services? But what about everything else? We have all our other workloads. We might have other
services outside of AWS. How do we establish an
identity foundation in EKS that allows us to do that? And this is what SPIFFE
was designed to solve. As Matt mentioned, it's
a universal standard. It stands for Secure Production Identity
Framework For Everyone. Do not ask me to repeat
that. It's a tongue twister. I'm gonna say it that once.
It is an open standard. It's a project under the CNCF, the Cloud Native Compute Foundation, and graduated in 2022. Its main goal is to provide workload identity
for distributed systems, not necessarily for EKS. It could be essentially
any distributed system, but we do most see it in Kubernetes in cloud-native environments. What it does is it provides a cryptographically
verifiable identity for every workload, and I can show you how... We're gonna show you how this
works a little bit later on, but those identities come in either as JSON web tokens, so JWTs, or more commonly, X.509 certificates. We refer to these, in a SPIFFE environment,
we refer to these as SVIDs, so the SPIFFE Verifiable
Identity Documents. The main thing that SPIFFE solves for is what we call the bottom turtle problem. How do we secure the foundation
of our infrastructure that we build the rest of our
security on top of, right? So when we're talking about
a zero-trust environment, how do we baseline our identity that we're building on top of? The one good thing that... An additional good thing that SPIFFE does is it provides attestable workload, so I'm gonna talk to you a little bit more about what that is, but that helps us solve for
that bottom turtle problem. Now, before I show you how this works, there's a few other concepts I need you to get familiar with. First one is a trust domain, so in a SPIFFE environment,
the trust domain is the... Think of it as the root of trust for our identity provider. Commonly, in most organizations, this is going to be a business unit, or it might be the whole
organization itself, depending on the size of the enterprise. Another term that you will see commonly is what's called SPIRE. They're often used interchangeably, but SPIRE is a
production-ready implementation of the SPIFFE APIs, right? So they're commonly used interchangeably, so here in our diagram, you'll see we have the
SPIRE server in red, and that SPIRE server is like
the brain of the operation. It is what handles the
issuance of the identities, and without that SPIRE server,
things will not work, right? So we have our SPIRE server
issuing the identities, pushing them down to our workloads, and with that, they're
also issuing trust bundles. If any of you familiar with general PKI, trust bundles would usually be the CA certificate that has signed, the certificate that's
being issued, right? So we're pushing the identity, which is commonly the certificate, as well as, essentially,
the CA certificate down so that way any other certificate signed by that SPIRE server we can verify, and the last thing I want you
to see is at the bottom there, there is, what you'll see
is a spiffe:// trust domain. That is commonly the format
in a Kubernetes workload, what that identity would look like. With SPIRE, it is customizable, but that is commonly what it is, so a trust domain, which
looks like a domain name, doesn't have to be, followed by the namespace of the workload, followed by the service account. That is the template, and
we'll see that as we go on. Any quick questions here
before I build this out for you and show you how this works? - [Audience Member] Does it
get (indistinct) meaningful to sort of mutate namespaces,
something like this? Or, you know, my great namespace
A, my great namespace B, but it's still the same service. - [Chris] You can have templates that do the substitution
for the namespace, and I'll show you that later on. All right, so as we talked about is the SPIRE server's the
brains of the operation. It is the main thing when you're building out a
SPIFFE or SPIRE environment, but in most enterprises, the
root of trust in your PKI is not necessarily gonna
be the SPIRE server. You're probably gonna have
something that already exists, so you can integrate it with your existing certificate authorities in your enterprise. I've depicted AWS Private CA. We're at re:Inforce, but
it could be anything. There are a lot of built-in
plug-ins that you can use. If you are gonna use AWS PCA, the EKS pod identities, that
Matt talked about earlier, allow for that secure access between the SPIRE server and
the AWS service, the AWS PCA, so you can use it. You're using them both together. Once that SPIRE server is up, every node in our cluster is going to have a SPIRE agent on it, and that SPIRE agent is what's going to do the
attestation of the node, so I mentioned earlier that one of the great things about SPIFFE is it allows for the
attestation of our workloads, but in order to attest our workloads, we need to make sure that
what we're running on is attested first, so as those nodes come up,
the SPIRE agents get deployed. The SPIRE agents attest that node. In an EKS environments, it's looking for a service account token. The agent provides that
to the server over TLS. The SPIRE server independently verifies that those tokens are valid, that this node actually
does belong to the cluster, and once it's done, it provides an SVID, so it's providing, essentially,
a certificate to the node, and then we form mTLS between them. We'll talk a little bit
more about that later on, but we have secure communication now between our nodes and our SPIRE servers. Once the agents are up on our nodes, now, as we bring up workloads, our workloads can now start
requesting their own identities. This happens automatically, so the agent on the node
will look at the workload, see if it matches the
criteria that we have set, and I'll show you how that
works a little bit later, but if that workload matches
what it's set, it's attested. We now provide that we
request from the SPIRE server an SVID for the workload, which
comes from the SPIRE server, and we pass that on to the application, which it can use for various things, commonly mTLS service-to-service
communication. That is very common. We're gonna show you that later on, but you can use that for anything else that you can use an X.509
certificate or a JSON web token. Okay, so I talked about
how SPIFFE and SPIRE provide a standard for issuing identities, but those identities, you know, might need to interact with services beyond just our trust domain. Might need to interact
outside of our organization. There might be other SPIFFE
and SPIRE environments that we need to interact with, and this is where the concept
of federation comes in, right? So if we imagine the
environment we just looked at was Trust Domain A on the left-hand side, so it's pushed down the
Trust Domain Bundles and the SVIDs for our environment, but if we set up federation between ourselves and
another trust domain, essentially, we set up an endpoint, which, and through configuration, our SPIRE servers communicate through those federation endpoints. They exchange the trust domains, sorry, the trust bundles
on a continuous basis after the bootstrapping process, and we have authenticated each other, so what happens is when,
let's say Service B, which is the green box on the bottom left, needs to talk to Service Z,
we've set up that federation, the trust bundle that gets pushed down to those individual services will have both the trust bundles for Trust Domain A and Trust Domain B. We'll have both, so we can now validate the certificates signed by both trust domains. That was a lot. Is there any questions? Yes, I'll take a few over here. Go ahead. - [Audience Member]
(indistinct) EKS Auto Mode? - [Chris] It does absolutely
work in EKS Auto Mode. Yes. (indistinct) question. - [Audience Member] (indistinct) mean that it is (indistinct) service
and domain (indistinct), domain (indistinct)? Like, you said it with (indistinct). - [Chris] The question was does
every service now automate? If we set up federation, does every service in both trust domains automatically trust each other? The answer is no. You have to specify, like, I want this. I want this particular set of workloads to be able to federate
with these workloads, and only those workloads, when they get their trust
bundles pushed down, will have the particular trust
bundles for the other domain, so few things I wanna explain here first, so I have a very simple
Kubernetes environment stand up. It is actually EKS Auto Mode. That was the question earlier:
Does it work in Auto Mode? Yes, absolutely, it does. I have a front end, I have a back end, and like in regular Kubernetes, there is automatic
communication between them. There's nothing blocking
at any space level. Can you all see that okay? Or should I make that a little bit bigger? - [Audience Member] Make it bigger. - Okay.
- It's not very bright, so maybe that'll compensate. - [Chris] There we go. - Yes.
- There we go. Okay, so like I said, simple. We have a front end. We have a back end. We have communication, but that doesn't give us any identities. We just, those workloads could
be anywhere, any namespace. We have no way of proving
what those workloads are, so the first thing we need to look at, like I was talking before,
is that node attestation. Before we can give those
workloads identities, we need to have identities
for the nodes themselves in our cluster, right? So automatically, and
I've set this up already, but automatically, you can see here, we have an attested agent, so like I said, the agent on the node. Every node has an agent. The agent on the node has the identity, so there is an ID here. I'm gonna scroll over. You can see it 'cause this
is gonna be important later, so just remember c99, okay? c99 is the SPIFFE ID for our node. We can see how it has been attested, so this k8s_psat, this is the out-of-box
verification for Kubernetes nodes. It is looking at the service
account token on those nodes, and we can see that it
is expiring shortly. It will automatically renew itself, and we can see the serial number, and it has, we can reattest, so that's step one. Our node has been attested in
our SPIFFE SPIRE environment. Now, there was a question
before about how do we do this? Does it get tedious to do this repeatedly for every namespace? I'm gonna zoom out just one so this... It's a little bit, so we fit everything. There is a few thing... In order to set up identities
for the workloads now, we need to use a resource called the ClusterSPIFFEID resource. This is what is going to be able to grant our workload's identity, so when I was talking before about does our workload match
any of our requirements? This is what defines that, so you're gonna have a manifest file, and in this manifest file, I mean, you can see here, number one, the kind is a ClusterSPIFFEID, number one. You will also see... That should be... Oh, sorry. ClusterSPIFFEID, number two,
we will see here the template, so when we were talking before about do we have to define this
for every single namespace? There is a template we can use, and this is what defines
that SPIFFE ID format that I was showing you earlier, right? Trust domain, namespace, service account, and this gets automatically substituted, and I'll show you that. These bottom two sections
are really important. This is what's going to
essentially select the workloads that we want to use for this cluster resource ID, right? So the first one is telling us does it have the label of spiremanaged-identity equals true? And the second one is just
defining our application, right? These are labels that
can be anything you want, but this is just tying our
workloads to this resource, and the last piece here is what's called the workload selector, and this is what helps us choose what do we want to select on how we're going to
attest the workloads? So this can be as simple
or as complex as you want. Very simply here, I'm saying that this
workload needs to exist in the curl name space, and that this workload
needs to be using an image from this particular image registry. If those conditions do not
match, it's not gonna get an ID because we have not attested that this, it meets that criteria. This is a very simple example. You can take this a step further. I wanna make sure that
it's running an image that has been signed, that
I'm the signer of, right? No one has replaced this image. It's running on particular nodes, right? So we can take this a step further, and that, like I was saying,
that is the main thing. It's not just giving
identities to workloads, but we're solving that
bottom turtle problem. We're attesting that these workloads are actually running and
who they say they are, so once I put this in the, this is once I deploy this manifest file, as I bring up workloads, automatically, if they meet those labels, like the spiremanaged-identity
and that app label, SPIRE will start looking. It's like, "Okay, does it meet
any of those other criteria "in terms of the curl
name space and the image?" If it does, automatically... I'm sorry. This is just showing what
I was talking about before Automatically, it's going to get an ID. I'm gonna show you what
this looks like now, but before I do that, there's two things I just want you to kinda
wrap your heads around. The IDs themselves are, number
one, they're attestable, so think of the attestation chain, so there's the node to the workload. We've trusted the node.
We attested the node. We now attest the workload. Then there's, from a PKI perspective, we can trace this ID from the workload, the SPIRE server back to our root of trust from a PKI perspective. Those are just two things I
want you to keep in your head as we go forward, so when my workload gets an ID, this is what I can see
in my SPIRE environment. I can see... I'm gonna try and zoom in a
little bit more on that for you. Number one, I can see my
SPIFFE ID, so it's taken my... So my trust domain was chris.example.com. - [Matt] Push it back. - Oh.
- To the top. - [Chris] Oh, good call. - [Matt] Yes. - [Chris] Chris.example.com,
very original, but what I also want you to
look at is the parent ID, and this parent ID,
you'll see it's very long, but if I go to the end, it ends in c99, which was the ID for our node that I just showed you a moment ago, so we can very easily trace that this ID was running on our attested
node from a minute ago, so I can show you that attested chain. This workload was running on this node. This node attested that this workload was running on that right node. The other pieces here, less interesting. We can just see the selectors that we had put in our ClusterSPIFFEID. A little bit less interesting. The main thing here to
show you was the SPIFFE ID and that parent on how that links, so that's the attestation chain. The other chain I wanted
you to think about was from a PKI perspective: How do we trace that workload
back up to our root of trust from a certificate authority perspective? So I am just going to show you, quickly, lemme just run. - [Audience Member] Chris, I have a kindergartner question for you. - [Chris] Sure. - [Audience Member] You're
doing that node attestation because you must or because it's a darn good
idea and a good practice. - [Chris] A must. We must, yeah. We need to have... It's fully... Everything's-
- Bouncing to the node, and that's-
- Exactly, so if you think back to that
diagram as I built it out, SPIRE server came up. Then the node... Sorry, the agent on the node comes up, and that is what actually
does the attestation for the workload, right? So once everything has verified, only then can we start issuing identities.
(questioner speaks faintly) No problem. Okay, so what I'm gonna show you here is I'm building out our chain of trust from an identity perspective now, so I've got my private CA. We could see it's issue, or it's a self-signed
certificate authority. This is the root of my private CA. The next thing gonna
scroll down to the bottom. I'm gonna skip all this. Now, in my work... Now, this is what actually
gets pushed to the workload, so in that workload, you'll
see here, this is the trust. You'll see here, this is part
of the trust domain here, so my common name is my SPIRE server, so this is the certificate
for my SPIRE server. It has been signed, if we look
at the issuer, as my root CA, so this is the private
certificate authority I just showed you a minute ago. This my intermediate certificate, and if I scroll up to the top, this is my workload certificate. This is my SVID, and my SVID, we can see here,
the issuer is my SPIRE server, so my intermediate sorority
is now signed my SVID, and if I scroll down to my
subject alternative name, right at the bottom, you'll
see here's my SPIFFE ID, and that is where you find the SPIFFE ID in the actual SVIDs. It is in the subject alternative name, and it is taken the same
template that I just showed you in that cluster resource ID
a few minutes ago, all right? So if we... I'll let you get your picture there, so if we wanna just think
about that logically again, I'm gonna scroll down. I make this a little bit easier. From a certificate authority perspective, we start at our, you know,
in this case, AWS PCA. AWS PCA is the root of trust. It signed the SPIRE
server's intermediate CA when that SPIRE server was created. That's part of that bootstrapping process using EKS pod identity. Once that SPIRE server came up, there was that whole
node attestation process, that other chain I wanted
you to think about. I tested the nodes. Then
the workloads came up. Once the workloads were attested, my SPIRE server issued the certificate signed by the SPIRE server, right? And you can see that full chain there. Okay, so while Matt gets set up there, so what we just talked about is how do we establish an identity foundation in Kubernetes, right? So we had our identity. We
talked about EKS pod identity. We talked about SPIFFE and SPIRE for our workload-to-workload
identity that we can use, but now we need to use those identities. It's not enough just to have identities. We need to use them for something, right? And this is where we start getting into thinking about authorization, right? So we're applying the
policy to those identities and moving from having implicit trust to where we want to explicitly authorize every single request, and Matt, if you're ready, I'm gonna turn it over to you to continue. - [Matt] That looks good. - [Chris] Nope. - [Matt] Oh, sorry. Forgot the part of the presentation, so common challenges that we get into authorization, right? Even though we have a strong identity now, we do have to ensure that
that identity is validated on all service-to-service requests. The goal, you know, we want to minimize the, you know, the call to external services to validate those identity/permission because we had, you
know, latency challenges, scaling issues, all those kinda things, so the goal will be to
have a consistent way to manage those identities and authorization across
the entire environment, so what if we could.... And, you know, the goal of what
we talk here with zero trust is you want as well to
validate the identity of the server you're calling, but the server should be
able to validate the identity of the client doing this, and a lot of question we
do get is how do I do this so that my 15, 30, 100
different application doesn't have to
reimplement the same thing, and, you know, this is not scalable. Doing this in all your
application takes a lot of work, a lot of potential mistake, and, you know, whenever you
need to change something, and it's also a lot of work, so inside Kubernetes, a lot of people go to the concept of service meshes for this. Service meshes do bring a
lot of interesting controls, advanced control, advanced routing policy, so it is really, you know, a solution that we see implemented
in a lot of customers. They do also bring a couple
of extra security features, one of them being encryption. We did talk about
identification, you know, since the beginning and also authorization policy. They usually bring some kind
of a service discovery as well, and then, you know, kind
of a layer of monitoring absolutely a lot of people love as well, but this is not the main talk of today, so for service meshes, the goal is how can I control my
service-to-service access? So by using the identity that we were talking
here provided by SPIFFE, is actually a very good way of doing this. To do this, a lot of people
are actually moving to, are actually using what we
called mutual TLS, mTLS, and inside of service meshes there's a pattern that
we called the sidecar, which basically allows
to have a proxy running next to your application that can handle most of the
encryption authorization, you know, work for you
so your application team don't have to reimplement
all of this together, so the nice thing about SPIFFE
and the SVID certificate is those are actually certificate that you can use directly
into your sidecar mesh for doing mTLS, so if you're not too familiar with mTLS, I'm sure everybody here
is familiar with TLS, so in TLS there's an handshake. The mTLS, basically, you know, in the handshake, when
you connect to the server, the server present a certificate so you can validate it is identity. In mTLS there's basically a server is asking you for a client certificate, which you do provide, and then it will validate (indistinct) trusts
your client certificate to continue operating with those servers, so the trust is built both ways, so if that sound familiar
to all the SVID thing we have been talking since the beginning, you're exactly right, so inside service meshes, if we are, you know, in Kubernetes, one of the very common
service mesh that we see is called Istio. Inside of Istio you can
build a authorization policy all the way to fine-grain identity provided through your SVID certificate, so we do have an example here, where we're using the principals so the trust domain here is example.com, the namespace is called frontend, and we're using a service
account called checkout, but you also can combine this with fine-grain control
over layer seven, you know, (indistinct) specific pack, whole space. You can kinda combine all of
this into multiple scenarios. How about we look at a small
demo of this with Istio? - [Chris] While he's getting set up there, any quick questions from the audience? Sure, go ahead. - [Audience Member] How
does this complement work with network policies
that control (indistinct)? - [Chris] That's a really great question, and so if I go back to my
definition of zero trust before, it's not an and/or; it's how do we move
beyond just using network to including identity as well, so we can use network policies
from a network perspective to control namespace level access, but that doesn't still prove to us is that workload actually
where it says it is? - [Audience Member] Still use both. - [Chris] You absolutely
can still use both, and you should still use both. It's not one or the other; it's an and. Sorry, Matt, go ahead.
- Cool, so I do have a cluster running. Somebody did ask about Auto Mode. My cluster is not running Auto Mode, but it works in both cases, so we can actually see the list of pods that I have here, so, like Chris, I do have
a SPIRE server set up with my SPIRE agent
running on my two nodes. I do have, also, actually, so my SPIRE server do use the
EKS pod identity association that we talk about to have access to my private CA authority, so let me show you this
inside of the EKS console, so if this is my cluster that am I using, so if I'm going to the Access tab here, and I scroll down a little bit, I can actually see my
pod identity association, so we can see that this cluster for the namespace SPIRE server and my service account SPIRE server, I actually have a role attached, so I know that this is blur, but let me open this up for you, and we can see that role actually have the
permission attached to it. So far, this is exactly the same at IRSA. No problem there. The difference come into
the trust relationship for pod identity, so if you already set up IRSA, you kinda see, know that we
have a specific OIDC provider that's actually registered into
your IAM identity provider, and this is an URL that is
actually unique per cluster. With pod identity, that's
one of the big change. We're using a service principal, so the EKS API is actually managing who can assume that role through that service principal for you through what we just saw
into the EKS console, and basically, when you define the role, you just link it to this "Service": "pods.eks.amazonaws.com," and basically, that's how your pods in any, you know, in any cluster will have the same trust policy, so it's, you know, a little
bit it's less management, especially if you migrate thing
around different clusters, those kind of thing, a little bit easier to use, so if I come back to my cluster, the other thing that my
cluster is running is Istio, so I have few namespace
that we'll use here, so actually we can see the Istio running into his own Istio system, and the two namespace
that I'll be using here is the default namespace and the echoserver specific namespace. We can see that the pods
running in those two namespace have actually two containers each. The second container
is actually the sidecar injected by Istio, just like we saw in a
couple slides before. Any question on the
setup? Or everyone saw it? Cool, so the first thing I wanna show is in my cluster, so I did define SPIFFE
IDs, just like Chris. I use roughly the same template as him. One difference is my, you know, I did not put specific workload selectors. All any pods running in my cluster that do have the specific labels of the SPIRE managed identity through will get an ID, basically,
SVID certificate, so let's look at what happen when you don't have an identity, so my first pod here,
let me show the describe, doesn't actually have the
SPIRE manage identity, right? So it doesn't have any ID, so if it calls a server, basically, we will get an error from the Istio proxy, right? We can see it's actually
coming from envoy, the proxy used by Istio, and basically, we do have an error is we're not able to connect. The reason for this is my Istio mesh is configured to enforce strict mTLS, and right now, I'm not able
to present a certificate that will be trust by the other sidecars, so I'm basically getting rejected, so let's try the same thing, but this time with a pod
that do receive an identity, so if you do a describe, we
do see that we have the line with the SPIRE manage identity equal true, so this pod, just like Chris show up, is getting the SPIRE, the SPIFFE ID that we show up, and now, if I call the same service, I'm actually getting a
RBAC denied (chuckles) because I probably forgot
to clean up my stuff. Lemme just remove my policy here. All right, back to... Let's redo that request. Oops. All right, so we're still in the pod with the specific label, and now we do get specific 200 OK, which is actually what we expect, so I'm using the echoserver. I'm sure some of you already play with it. The echoserver just send back all the data and the others that you
see from the request, so that's kinda interesting to look at, so let me just come back up. Sorry, I think I lost... Oops. SPIRE. Oh, okay, here, so if we run this, and I grab the most
interesting editor that we get from the Istio sidecar, so we do see we get a
x-forwarded-client-cert here, and if we look at that very long string, we do see that it was, so it's giving us a By, which is basically who validated
that specific identity, so in my case, I'm using math.example.com
as my trust domain, and basically, we're getting
the echoserver namespace and service account default, which is the receiving Istio sidecar that did validate that identity. There's also a hash here that will pass, and then, towards the end, we have, basically, the
identity that was validated from the actual other, you know, basically, the color identity, and in this case, you
know, it's math.example.com from the default namespace, and my service account
was called curl-spire, so that's great, but so far, we only did
connect through the mTLS. We haven't actually used those identity into fine-grain control, so let's do that first. Istio needs a default deny policy, so you do have to apply it first, so let me apply this. Take a sip of water, and maybe we have a question. No question. All right, so I did apply my default deny, and then I redid my same
curl command, right? So we do expect this to apply correctly. Probably the policy takes a couple second for the Istio sidecar
to apply the, you know, get the policy push from
the Istio (indistinct), so sometimes they need couple seconds, so let's retry this. The nice thing about Kubernetes is it's a declarative system, right? So even though I did reapply
my specific policy here, did not change anything because the object was already applied. However, we now see that
the policy was applied, and as expected, I'm now
getting a 403 Forbidden, and basically, no answer. Actually, there is an answer
called RBAC: access denied, which is kind of obvious what's happening, so now we can build those
authorization policy by using the principal that we have, so let me apply this
one, and let me show you, so inside of my policy right now, I'm using a simple allow just of the principal that I'm using inside of the echoserver, so that specific
curl-spire service account could now call anything, any of the workloads
running into my echoserver specific namespace, so let's do exactly that, so let's call the echoserver
on a specific URL, so took a couple seconds. We're still getting RBAC denied, so my cluster has been
doing slowly this afternoon for a strange reason, so I'm now getting the 200 OK, and as before, we do see all the outputs
from the echoserver back, just like we had in our previous call, so is this really the best we can do? Of course, no. As we said, you know, the Istio sidecar right now
is configured for HTTPS, so it can do specific
authorization layer seven, so you can use path base, host
base, method base, all this, so let me here enable the POST to /api/payment, for example, in my specific authorization policy, and let me go back here, so if we were to apply this, let's wait a couple second
for the sidecar to reload. - [Chris] Yep. There's a question. - [Audience Member] Policy
(indistinct) sidecar, or (indistinct)? - [Chris] The question was is the policy enforced by the
sidecar or the EKS controller? Did I hear that right?
- The ingress controller. - The ingress controller. Sorry.
- Yes, so I'm not using any ingress
controller right now, so I'm doing sidecar to sidecar, so it is enforced by
the receiving sidecar. That's also important. Sure, so my policy is applied, so now I'm doing a post
on /api/payment, right? And so we do see that
we're getting a 200 OK with the same output as before, but let's say I was calling a different API this time, right? /list. I want a list of all the action
available on that service, and we'll actually, we'll get forbidden, with the RBAC: access denied because the policy doesn't apply this. When you think about this, right? Instead of using a list of IP address that your pods inside your
cluster could potentially use is seems a much better approach to me by using the identity
control that is SPIFFE and the SPIRE framework kinda propose. - [Chris] So wrapping up today's talk, just to kinda recap what
we went through, right? So we talked about why
a zero-trust strategy requires a strong identity
foundation, right? Going back to those ephemeral
natures of those workloads, not always having the same IP addresses, potentially coming up
on different subnets, so moving away from using
solely network controls and introducing more on identity controls. For those identities,
those workload identities, they should be attested. We should not just be giving
credentials to workloads. We should be attesting in some manner that those workloads are actually running where they say they are
or where they should be before we give them those credentials, and then, ultimately,
using those credentials to secure our service-to-service
communication explicitly, moving away from implicit
trust at a namespace level to explicit authorization
for every request, as Matt showed us. If you wanna learn a little bit
more about SPIFFE and SPIRE, that is a very deep concept, so there are some great
YouTube videos on the left. Those first two are YouTube videos. They'll take you in a way deeper dive, and then, as well as there is the
SPIFFE documentation as well. I would give that a read. It takes you way deeper in as well, but it is a really great concept for securing your workloads in Kubernetes. With that, thank you once again for taking the time to
come to this talk today. Would really appreciate. It would help us if you
filled out the survey. That does make a difference for us. Would appreciate if
you did enjoy the talk, or didn't enjoy the talk, still fill out the survey, and we now open it up to
any questions you have. Thank you.
