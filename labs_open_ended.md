AI407L  
Deployment Packaging   ·   Automated Quality Gates  
Submission Deadline: 3 May 2026  
 
Industrial Packaging & Deployment Strategy  
 
Objective  
At this point your agent runs on your laptop. This Task  asks you to answer one question: how do you make it run 
the same way on any server, cloud instance, or colleague's machine with a single command and zero manual setup?  
 
The Core Problem  
  The "It Works on My Machine" Problem  
Production systems cannot depend on your local Python version, your virtual environment,  
your local .env file, or your OS -level library paths. Any of these will differ on another machine.  
Containerisation solves this by bundling your application with everything it needs to run.  
Your packaged system must start cleanly from your source files alone no manual steps.  
 
Mandatory Outcomes  
Your submission must satisfy all four outcomes below. How you achieve each one is your design decision.  
 
Reproducible Container Image  
1. Your agent and all its dependencies must be packaged into a container image.  
2. The image must be reproducible: building from your source should yield the same result on any machine.  
3. Your written report must justify: choice of base image, layer ordering strategy, and any multi -stage build 
decisions.  
 
Secret -Free Image  
1. No API keys, passwords, or .env files may be embedded in the image at build time.  
2. Secrets must be injected at runtime. Demonstrate exactly how this is done.  
3. All unnecessary files (caches, local DBs, virtual environments) must be excluded from the image.  
 
Multi -Service Orchestration  
1. Your system has at least two services: the agent API and a backing data store (vector DB or checkpoint 
DB).  
2. Define how these services are started, how they discover each other, and how they are stopped together.  
3. Persistent data (your vector index, checkpoint state) must survive a container restart. Prove it.  
 
End-to-End Test  
• Provide verifiable evidence that your packaged system works after being started from your configuration 
files alone.  
• Acceptable evidence: build logs, curl output, a test script, screenshots.  
• The evidence must show the agent receiving a query and returning a correct answer.  
 
Submission Checklist  
File / Artefact  Contents Required  
Dockerfile  Container build instructions. Layer order must be optimised ; base image 
choice must be justified in the report.  
Compose file (or equiv.)  Multi -service orchestration configuration. Must include the agent API, a 
data store, volumes for persistence, and runtime secret injection.  
 
 
 
Automated Quality Gates & CI/CD  
Objective  
Every code change a rewording of the system prompt, a tweak to a tool, a new document in the knowledge base  
can silently degrade your agent's quality. Manual testing after every change is not scalable.  
This task asks you to build an Automated Quality Gate: a pipeline that runs your evaluation suite on every push 
and blocks deployment if quality scores fall below thresholds you define and justify. The pipeline is the last line of 
defence before production . 
 
The Evaluation Gate  
  From Measuring Quality to Enforcing It  
In Lab 7 you measured quality. In this task  you enforce it.  
Every push to your main branch triggers an automated check. If Faithfulness drops below  
your threshold, the build fails and the degraded agent cannot reach any downstream environment.  
Think of your metric thresholds exactly like unit test pass/fail criteria.  
 
Mandatory Outcomes  
 
CI-Ready Evaluation Script  
• Adapt your evaluation script from Lab 7 to run headlessly in an automated environment (no interactive 
input, no hardcoded credentials).  
• The script must exit with code 0 when all metrics pass and code 1 when any metric fails — the CI platform 
reads this exit code to mark the build.  
• All credentials must be read from environment variables. Demonstrate this in your report.  
• The script must write  a machine -readable results file (JSON or equivalent) listing each metric name, score, 
threshold, and pass/fail status.  
 
Pipeline Configuration  
• Define an automated pipeline that triggers on every push to your main branch.  
• The pipeline must: check out code, install dependencies, run the evaluation script, and surface a clear pass 
or fail result.  
• All sensitive credentials must be stored in the CI platform's secret store , no secret may appear in any 
committed file.  
 
Versioned Threshold Configuration  
• Define your quality thresholds in a configuration file that is committed to version control alongside your 
code.  
• The file must specify at least two distinct metrics (e.g., minimum faithfulness and minimum answer 
relevancy).  
• Your report must justify each threshold value: why that number? What would happen if it were set 10% 
higher or lower?  
 
Breaking Change Demonstration  
• Intentionally degrade your agent (examples: remove RAG context, corrupt the system prompt, introduce a 
hallucination -inducing instruction).  
• Show the pipeline correctly detecting the degradation and marking the build as failed.  
• Restore the agent and show the pipeline returning to a passing state. Both states must be evidenced in your 
submission.  
 
Submission Checklist  
File / Artefact  Contents Required  
Pipeline config file  e.g. .github/workflows/main.yml or equivalent. Must trigger on push, inject 
secrets from the platform store, and surface pass/fail clearly.  
run_eval.py  CI-ready evaluation script. Reads credentials from env vars, exits with 
correct codes, writes a machine -readable results file.  
eval_thresholds.json  Versioned threshold configuration file. Must include at least two metrics. 
Threshold values must be justified in the report.  
 
 
Also submit A Report of what you have done and how you have done (include screenshots).  
 
Assessment Rubric  
Criteria  Marks  
Requirements  30 
Working Demo  30 
Viva  40 
 
