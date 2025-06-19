# AWS re:Inforce 2025 - Customer Keynote with Comcast

**Video Link:** [Watch on YouTube](https://www.youtube.com/watch?v=2fthKhQdw6Y)

## Video Information
- **Author:** AWS Events
- **Duration:** 8.5 minutes
- **Word Count:** 1,243 words
- **Publish Date:** 20250618

## Summary

In this customer keynote, a Comcast cybersecurity leader presents how the company secures its massive scale operations serving millions of customers across diverse business units. The presentation outlines Comcast's cybersecurity mission: "We protect the incredible technology and platforms that connect millions of people to the moments that matter," supported by over 2,000 cybersecurity professionals who contributed to more than 10% of all Comcast patents in the previous year.

The talk centers around Comcast's three long-standing "North Stars" that have guided their security strategy for seven years: building security and privacy into all products and services (shift-left approach), using data to improve security effectiveness, and operating on zero trust principles. The speaker demonstrates how these principles have evolved to incorporate generative AI capabilities, showing remarkable adoption where 20% of all threat modeling and penetration testing findings now relate to AI solutions developed in less than two years.

Comcast's mature security infrastructure, including a 10-petabyte security data lake with 100+ normalized data sources, positioned them well for AI integration. They've implemented AI across governance, risk, and compliance (GRC) functions, automated data pipeline management, enhanced threat modeling processes, and built sophisticated identity risk ranking systems. The presentation emphasizes their six-year strategic partnership with AWS and showcases how continuous controls monitoring, security hygiene, and operational excellence support their comprehensive security approach.

## Key Points

- **Mission-Driven Security Organization**: Comcast employs 2,000+ cybersecurity professionals with a clear mission to protect technology platforms connecting millions of people, with the team contributing over 10% of all company patents
- **Three Strategic North Stars**: Seven-year commitment to (1) building security and privacy into all products/services, (2) using data to improve security effectiveness, and (3) operating on zero trust principles
- **Rapid AI Adoption**: In less than two years, 20% of all threat modeling and penetration testing findings result from developers building AI solutions, demonstrating massive organizational transformation
- **Enhanced Threat Modeling**: AI-integrated threat models now evaluate data provenance, model provenance, guardrails, hallucination detection, input validation, and data exfiltration risks
- **Automated Development Tools**: Built AI workbench and matured AI software development lifecycle, including tools that generate security user stories from natural language prompts
- **Mature Security Data Infrastructure**: 10-petabyte security data lake with 100+ normalized and correlated data sources providing two years of historical security data
- **AI-Powered Data Operations**: Developed six-stage generative AI pipeline that automates everything from data content analysis to schema generation and population, significantly reducing resource requirements
- **Comprehensive GRC Automation**: Deployed multiple AI bots for continuous controls compliance, SOC2 attestations, vendor questionnaire completion, and other governance functions
- **Zero Trust Implementation**: Built "One Risk Engine" that risk-ranks every user authentication using contextual company, people, and infrastructure information
- **Strategic AWS Partnership**: Six-year partnership leveraging multiple AWS security capabilities including Security Groups for micro-segmentation

## Technical Details

**Security Frameworks and Standards:**
- OWASP LLM Top Ten guidelines for AI security
- MITRE ATLAS framework for adversarial ML threats
- SOC2 compliance attestation processes
- Continuous controls monitoring systems

**AI and Machine Learning Security:**
- Generative AI integration across threat modeling workflows
- AI workbench platform for development teams
- Six-stage AI pipeline for automated data processing
- Natural language to user story generation tools
- Automated threat model generation from developer documentation
- AI-enhanced penetration testing preparation and reporting

**Data and Analytics Infrastructure:**
- 10-petabyte security data lake architecture
- 100+ normalized and correlated data sources
- Two years of historical security data retention
- Automated data pipeline management and schema generation
- Network reliability engineering data integration
- Asset management and ownership tracking systems

**Zero Trust Architecture:**
- One Risk Engine for authentication risk ranking
- Contextual risk assessment using company, people, and infrastructure data
- Micro-segmentation platform with AI-powered tenant communication analysis
- Identity and access management integration

**AWS Services and Integration:**
- AWS Security Groups for micro-segmentation
- Six-year strategic partnership with comprehensive AWS security capabilities
- Multi-service AWS security toolset deployment

**Governance, Risk, and Compliance (GRC):**
- AI chatbots for continuous controls compliance
- Automated vendor questionnaire completion
- SOC2 attestation processing bots
- Asset ownership claim automation
- Risk assessment and reporting automation

## Full Transcript

>> THANK YOU AMY. GOOD MORNING
EVERYONE. WELCOME TO PHILLY. PHILLY HAPPENS TO BE THE
HEADQUARTERS OF COMCAST. AND AS YOU CAN SEE COMCAST IS BIG. AND
THE QUESTION YOU MAY ASK IS HOW DO YOU SECURE A BUSINESS OF THIS
SCALE, THIS COMPLEXITY AND THIS DIVERSITY OF BUSINESSES. AND WE
THINK THAT IT IS REALLY IMPORTANT TO HAVE A WELL-DEFINED
MISSION. THE MISSION FOR COMCAST CYBER SECURITY IS WE PROTECT THE
INCREDIBLE TECHNOLOGY AND PLATFORMS THAT CONNECT MILLIONS
OF PEOPLE TO THE MOMENTS THAT MATTER. THIS IS A REALLY
PURPOSEFUL MISSION FOR OUR 2000 PLUS CYBERSECURITY
PROFESSIONALS. THIS GROUP OF PEOPLE IS NOT JUST MISSION
DRIVEN, THEY ARE EXTREMELY INNOVATIVE. LAST YEAR, MORE THAN
10% OF ALL PATENTS GRANTED AT COMCAST WERE GRANTED TO COMCAST
CYBERSECURITY TEAM. I AM SO PROUD OF THAT. THANK YOU. THAT'S
APPLAUSE FOR MY TEAM. YAY! SO WE ALSO TAKE A VERY LONG TERM VIEW
OF SECURITY. AND FOR THAT WE HAVE DEFINED THREE NORTH STARS.
OUR FIRST NORTH STAR IS BUILD SECURITY AND PRIVACY INTO ALL OF
OUR PRODUCTS AND SERVICES. THIS IS WHAT AMY JUST TALKED ABOUT
WHEN SHE REFERRED TO SECURE BY DESIGN. IT'S ALSO KNOWN AS
SHIFTLEFT. OUR SECOND NORTH STAR IS THAT WE USE DATA TO MAKE SURE
THAT WE ARE IMPROVING THE SECURITY EFFECTIVENESS OF OUR
SOLUTIONS. AND OUR THIRD NORTH STAR IS THAT WE OPERATE ON ZERO
TRUST PRINCIPLES. NOW, THESE HAVE BEEN OUR NORTH STARS FOR
SEVEN YEARS. WE REALLY DO TAKE A LONG TERM VIEW OF SECURITY, AND
SOMETIMES WE MAKE REVOLUTIONARY PROGRESS, BUT USUALLY IT'S
EVOLUTIONARY SLOW, STEADY PROGRESS ALONG THOSE THREE NORTH
STARS. NOW, I KNOW YOU'VE BEEN WAITING FOR THIS SLIDE. YOU
CAN'T DO A PRESENTATION THESE DAYS WITHOUT THE WORD AI. SO, AS
YOU ALL KNOW, IN 2023 GENERATIVE AI BECAME PART OF OUR COLLECTIVE
CONSCIOUSNESS. AND PEOPLE AT COMCAST, INCLUDING THE CYBER
TEAM, WERE SO EXCITED. I'M LIKE, YOU KNOW, NEW WAYS OF DOING
THINGS, NEW TOOLS AND METHODS TO TAKE ADVANTAGE OF. SO WE STARTED
THINKING, OKAY, HOW DOES CYBER ADAPT TO THIS? AND I WILL TALK
OUR FRAMEWORK OF OUR THREE NORTH STARS. SO WE WERE ALREADY DOING
THINGS LIKE THREAT MODELING PENTESTING. WE WERE FINDING AND
FIXING CODE VULNERABILITIES. WE STARTED TO NOW ADAPT THESE
PROCESSES. YOU KNOW, WE LOOKED AT THE OWASP LLM TOP TEN. WE
LOOKED AT THE MITRE ATLAS GUIDELINES. WE DID OUR OWN
RESEARCH. WE LEARNED FROM OUR PEERS. AND SO TODAY, THREAT
MODELS NOW INCORPORATE THINGS LIKE DO WE KNOW THE PROVENANCE
OF NOT JUST THE TRAINING DATA, BUT THE MODEL FOR PROMPTS? DO WE
KNOW DO WE HAVE THINGS LIKE GUARDRAILS? ARE WE LOOKING FOR
HALLUCINATIONS? ARE WE DOING INPUT VALIDATION? ARE WE LOOKING
FOR DATA EXFILTRATION? AND WE'VE LEARNED A TREMENDOUS AMOUNT.
WHAT IS SURPRISING TO ME IS THAT IN LESS THAN TWO YEARS, ONE OUT
OF EVERY FIVE. SO THAT'S 20% OF THREAT MODEL AND PENTESTING
FINDINGS AT COMCAST TODAY RESULT FROM OUR DEVELOPERS BUILDING AI
SOLUTIONS. THAT'S AN AMAZING TRANSFORMATION. IN LESS THAN TWO
YEARS. NOW AS WE'RE DOING THIS, OUR CTO'S OFFICE IS BUILDING
TOOLS AND PLATFORMS FOR OUR DEVELOPMENT TEAMS. SO WE ARE
CREATING AN AI. BENCHMARK. SORRY, I LOST THE WORD FOR A
MINUTE. AI WORKBENCH SORRY ABOUT THAT. AND ALSO MATURING OUR AI
SOFTWARE DEVELOPMENT LIFE CYCLE. SO AN EXAMPLE OF THAT IS THAT WE
BUILT A TOOL WHERE YOU CAN DO A PROMPT OR A NATURAL LANGUAGE
INPUT, AND THE OUTCOME IS USER STORIES FOR OUR DEVELOPMENT
TEAMS. WELL, PART OF THAT PROCESS NOW INCLUDES GENERATION
OF SECURITY USER STORIES. SO THAT IS HOW WE'RE INTEGRATING
NOW. WE'RE ALSO USING AI TO IMPROVE SOME OF THESE PROCESSES.
FOR EXAMPLE FOR THREAT MODELS, WE USED TO REQUIRE AN
ARCHITECTURAL DIAGRAM OF SOME TYPE. TODAY WE'VE BUILT TOOLING
THAT GOES DIRECTLY ONTO DEVELOPER WIKIS OR DEVELOPER
DOCUMENTATION. AND IT EXTRACTS ALL OF THE RELEVANT INFORMATION,
SUMMARIZES IT. AND NOW YOU CAN DO THREAT MODELS MUCH FASTER
THAN BEFORE. SAME FOR PENTESTS. YOU KNOW, PENTESTS TAKE A LOT OF
PREPARATION AND THEN A QA AND THEN THE REPORTING. ALL OF THAT
IS RIGHT FOR GEN AI LEAVING PEN TESTERS TO DO WHAT THEY LIKE TO
DO BEST, WHICH IS TO PEN TEST ON THE SECOND NORTH STAR. WE REALLY
GOT LUCKY BECAUSE WHEN GEN AI BURST ONTO THE SCENE, WE ALREADY
HAD A VERY MATURE SECURITY DATA LAKE. WE HAD TEN PETABYTES OF
DATA, TWO YEARS OF HISTORY. ABOUT 100 DATA SOURCES ALREADY
NORMALIZED, ALREADY CORRELATED. AND AS WE STARTED TO LOOK AT
WHAT GEN AI WAS BRINGING TO THE TABLE, IT WAS LIKE PARTY TIME.
EVERYBODY WAS SO EXCITED ABOUT THE NEW CAPABILITIES THAT OUR
DATA WAS ABOUT TO UNLEASH. SO TODAY, OUR NETWORK RELIABILITY
ENGINEERING TEAM USES OUR DATA SECURITY DATA. OUR ASSET
MANAGEMENT TEAM USES OUR DATA TO IDENTIFY LIKELY OWNERS OF ASSETS
WITHOUT OWNERS. WE ALSO HAVE A CHATBOT THAT REACHES OUT TO THE
OWNER AND MAKES SURE THEY CLAIM OWNERSHIP. REMEMBER THAT 100
DATA SOURCES I JUST TALKED ABOUT? WELL, MAINTAINING THOSE
DATA PIPELINES WAS BECOMING TREMENDOUSLY RESOURCE INTENSIVE.
SO WE HAVE DEVELOPED A SIX STAGE GEN AI PIPELINE THAT DOES
EVERYTHING FROM LOOK AT THE CONTENT AND SHAPE OF THE DATA
COMING IN TO GENERATING THE CODE THAT GENERATES THE SCHEMAS, AND
THEN POPULATES THE SCHEMAS SO THAT ENTIRE PROCESS IS NOW
AUTOMATED, FREEING UP A TON OF RESOURCES. AND I CAN'T LEAVE
THIS SLIDE WITHOUT TALKING ABOUT GRC GOVERNANCE, RISK AND
COMPLIANCE. WE ARE FINDING THAT THIS IS THE MOST RIPEST GROUND
FOR USE OF GEN AI. SO WE HAVE SO MANY BOTS THERE TODAY ALREADY.
WE HAVE AN AI BOT THAT TALKS TO OUR CONTINUOUS CONTROLS
COMPLIANCE SYSTEM. WE HAVE BOTS THAT LOOK AT SOC2 ATTESTATIONS.
WE HAVE BOTS THAT GENERATE FILL OUT VENDOR QUESTIONNAIRES. IT'S
JUST REALLY ALMOST EVERY FEW WEEKS THERE'S A NEW USE CASE
THAT EMERGES. AND THEN FINALLY, IF YOU LOOK AT OUR THIRD NORTH
STAR, YOU KNOW, IDENTITY AND SEGMENTATION ARE CORNER STORES
FOR CORNERSTONES FOR ZERO TRUST. SO WE HAVE BUILT SOMETHING WE
CALLED ONE RISK ENGINE THAT LOOKS AT EVERY USER
AUTHENTICATION AT COMCAST. AND IT RISK RANKS IT. AND WE DO THIS
WITH ALL OF THE CONTEXTUAL INFORMATION THAT WE HAVE ABOUT
OUR COMPANY, OUR PEOPLE AND OUR INFRASTRUCTURE. AND AGAIN FROM
MICRO-SEGMENTATION, WE REALLY, REALLY RELY ON THINGS LIKE AWS
SECURITY GROUPS. WE HAVE BUILT OUR OWN MICRO-SEGMENTATION
PLATFORM AND AI IS REALLY HELPING THERE AS WELL, BECAUSE
ONE OF THE BIG ISSUES WITH MICRO-SEGMENTATION IS TO FIGURE
OUT WHO YOUR TENANTS ARE TALKING TO AND WHO YOUR WHO IS TALKING
TO YOUR TENANTS. THAT'S WHERE I REALLY HELPS US. NOW, ALL OF
THIS IS REALLY GREAT. YOU KNOW, HAVING NORTH STARS IN A MISSION
AND AN AWESOME TEAM. BUT WE ALSO NEED GOVERNANCE AND CONTROLS.
AND FOR THAT WE HAVE CONTINUOUS CONTROLS MONITORING. WE REALLY
FOCUS ON SECURITY, HYGIENE. YOU KNOW, THAT GRUNT WORK THAT
NOBODY WANTS TO DO BUT IS REALLY IMPORTANT FOR SECURITY. WE FOCUS
ON OPERATIONAL EXCELLENCE. AND THEN FINALLY OUR STRATEGIC
PARTNERSHIPS ARE SO IMPORTANT TO US. AND THIS IS WHERE OUR SIX
YEAR OLD PARTNERSHIP WITH AWS IS SO, SO VALUABLE. THESE ARE JUST
SOME OF THE AWS CAPABILITIES THAT MY CYBER TEAM USES AT
COMCAST. SO THANK YOU AWS. AND WITH THAT I'M GOING TO CLOSE
THANKING YOU. WISHING YOU A WONDERFUL REST OF THE DAY AND AN
AWESOME REST OF THE CONFERENCE. THANK YOU.
