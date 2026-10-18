# Faculty Presentation & Live Demo Guide (Viva Runbook)

**Project:** Auto-Incident to Agile Ticket Pipeline (DevOps Incident Watchdog)  
**Student:** S Hemal (Registration: 24MIS0050)  
**Institution:** Vellore Institute of Technology (VIT), Vellore Campus  
**Course:** Agile Development Process and DevOps  

---

## 🎯 1. The 30-Second Elevator Pitch (What to say first)

> *"Good morning Professor. In modern cloud operations, there is often a disconnect between Site Reliability Engineering (monitoring) and Agile product teams (sprint management). When production servers crash, error logs are scattered across cloud consoles or lost in Slack alerts, and engineers must manually copy-paste details into Jira or GitHub boards.*
> 
> *My project, **DevOps Incident Watchdog**, automates this entire feedback loop. When our application on AWS encounters an unhandled runtime error, **Amazon CloudWatch** detects the anomaly. An autonomous **AWS Lambda Watchdog** parses the crash logs, securely archives an incident dump in **Amazon S3**, and immediately creates an **Agile Bug User Story** complete with acceptance criteria on our **GitHub Projects Kanban Board**.*
> 
> *When a developer commits a fix with smart syntax like `Fixes #1`, our **GitHub Actions CI/CD pipeline** runs automated unit tests, deploys the patch to AWS, and automatically transitions the Agile ticket to **Done**—achieving complete zero-touch traceability."*

---

## 🎬 2. Step-by-Step Live Demonstration Walkthrough

Follow these exact steps when presenting your screen to the faculty:

### Step 1: Show the Application & Baseline Health (30 seconds)
1. Open your browser and navigate to the application endpoint:
   - Live URL: `https://<your-lambda-url>.on.aws/` (or run local server `python app/app.py`).
2. Show the `/health` endpoint:
   - Displays `HTTP 200 OK`, `status: healthy`, uptime, and version.
   - **Say to Faculty**: *"Our application features proactive health monitoring that cloud infrastructure services ping continuously."*

### Step 2: Show the Agile Kanban Board (30 seconds)
1. Open your GitHub Repository > **Projects** tab (or **Issues** tab).
2. Show that the backlog / board is currently clean or in its baseline state.
3. **Say to Faculty**: *"Here is our active Agile Sprint board. Notice there are currently no unhandled production bug tickets."*

### Step 3: Trigger the Incident (1 minute)
1. In your browser or terminal, trigger an incident:
   - Either visit: `https://<your-app-url>.on.aws/simulate-crash?type=zero_division`
   - Or run the presentation script:
     ```bash
     python scripts/simulate_incident.py
     ```
2. The browser returns `HTTP 500 Internal Server Error`.
3. In the terminal, show the structured incident log generated for CloudWatch:
   `[INCIDENT_DETECTED] Type=ZeroDivisionError | Message=division by zero`
4. **Say to Faculty**: *"Our production server just crashed due to an unhandled calculation exception. Instead of relying on a human to spot this, Amazon CloudWatch and our Incident Watchdog Lambda detect this in real time."*

### Step 4: Show the Autonomous Agile Ticket Creation (1 minute)
1. Switch back to your GitHub repository and refresh the **Issues** tab.
2. Boom! A new issue has appeared automatically:
   - **Title**: `[INCIDENT] ZeroDivisionError: division by zero`
   - **Labels**: `bug`, `incident`, `sprint-backlog`
3. Click into the ticket and show the faculty the generated details:
   - **Agile User Story**: *"As an Agile Development Team member, I need to resolve runtime failure in..."*
   - **S3 Incident Dump Link**: Points to the secure JSON crash report in Amazon S3.
   - **Stack Trace Context**: Pre-populated stack trace so developers don't have to search cloud logs.
   - **Acceptance Criteria**: Checkbox list defining the "Definition of Done".
4. **Say to Faculty**: *"The AWS Lambda function automatically parsed the crash, stored a compliance audit log in private Amazon S3, and generated this structured Agile User Story with full context and Acceptance Criteria."*

### Step 5: Code Fix, CI/CD Pipeline & Zero-Touch Close (2 minutes)
1. Open your code editor and show the fix (or simulate pushing a fix):
   - Commit message: `git commit -am "Fixes #1: Handled division by zero in checkout logic"`
   - Push to repository: `git push origin main`
2. Switch to the **Actions** tab in GitHub:
   - Show the running workflow: `Agile DevOps CI/CD Pipeline`.
   - Show Stage 1: **🧪 Automated Unit Testing** (`pytest` passes all 8 tests).
   - Show Stage 2: **🚀 Automated AWS Deployment** (packages and deploys code).
   - Show Stage 3: **🎯 Agile Traceability & Ticket Closure**.
3. Go back to GitHub Issues:
   - Show that the issue has been **automatically closed**!
   - Show the automated bot comment linking the specific commit SHA, test run, and deployment status.
4. **Say to Faculty**: *"Through smart commit linking, our CI/CD pipeline verified the code fix, deployed it to AWS, and automatically resolved the sprint ticket without any manual drag."*

---

## 💡 3. Faculty Viva Questions & High-Scoring Answers

### Q1: How does this project embody Agile methodology?
> **Answer:** *"In Agile, rapid feedback loops and actionable user stories are essential. Traditional incident response requires manual triage, which delays the sprint backlog. Our watchdog immediately converts infrastructure failures into standardized Agile User Stories with explicit Acceptance Criteria, ensuring immediate visibility in sprint planning and maintaining continuous flow."*

### Q2: Why did you choose AWS Lambda and S3 for this architecture?
> **Answer:** *"AWS Lambda provides an event-driven, serverless execution model with zero idle cost (100% within AWS Free Tier) and sub-second scaling. Amazon S3 serves as an immutable, encrypted audit store for crash dumps with private bucket policies, satisfying compliance requirements without polluting project management tickets with megabytes of raw log data."*

### Q3: What is 'Zero-Touch Closing' and why is it important in DevOps?
> **Answer:** *"Zero-Touch Closing links developer commits directly to sprint backlog tickets (e.g. `Fixes #101`). When the CI/CD pipeline succeeds, it automatically updates and closes the ticket. This eliminates human error, ensures that only tested and verified code closes a ticket, and creates an unbroken audit trail from incident detection to production deployment."*

### Q4: How does this system reduce MTTD and MTTR?
> **Answer:** *"Mean Time to Detect (MTTD) drops to seconds because CloudWatch monitors metrics and error patterns proactively without waiting for user bug reports. Mean Time to Resolve (MTTR) is minimized because developers receive the exact stack trace, S3 dump, and reproduction steps directly inside the newly opened sprint ticket."*

### Q5: What security practices did you implement?
> **Answer:** 
> 1. *"Amazon S3 buckets are configured with Block Public Access and least-privilege IAM policies.*
> 2. *GitHub API tokens and AWS credentials are stored securely in environment variables and GitHub Secrets rather than hardcoded in source code.*
> 3. *The Lambda execution role only has minimal permissions (`s3:PutObject` and basic CloudWatch logging)."*
