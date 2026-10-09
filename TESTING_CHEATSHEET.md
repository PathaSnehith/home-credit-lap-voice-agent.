# 3-Minute Testing Cheatsheet: Retell AI Step-by-Step

Don't worry or stress! Everything is 100% built and ready. All you need to do is follow these simple steps to get your public call recording link in under 5 minutes.

---

## Step 1: Open Retell AI (100% Free)
1. Go to [https://www.retellai.com](https://www.retellai.com) in your browser.
2. Click **"Sign Up"** (or Sign in with Google / GitHub).
3. Retell gives you free credits immediately upon signup—no credit card required!

---

## Step 2: Create Your Voice Agent (Takes 1 Minute)
1. On the left sidebar, click **"Agents"**.
2. Click the **"+ Create Agent"** button (top right).
3. Select **"Single Prompt Agent"**.
4. Set the following fields:
   - **Agent Name:** `Home Credit LAP Qualification Assistant`
   - **Voice:** Select any Indian English or clear professional voice (e.g., `11labs-Adrian` or search for an Indian accent voice like `Priya` / `Neerja`).
   - **Begin Message:**
     ```text
     Hello, am I speaking with Mr. Sharma? This is Priya calling from Home Credit.
     ```
   - **Model:** Select `GPT-4o` or `GPT-4o-mini` (or Claude 3.5 Sonnet).
   - **General Prompt:** Open [prompts/retell_direct_copy_paste.txt](file:///c:/Users/patha/Downloads/home-credit-lap-voice-agent-starter/home-credit-lap-voice-agent/prompts/retell_direct_copy_paste.txt), copy the **entire text**, and paste it into this box.
5. Click **"Save"** (or "Publish") in the top right.

---

## Step 3: Make Your Test Call (Takes 1 to 2 Minutes)
1. On your agent page, click the **"Test Call"** or **"Web Call"** button.
2. Allow microphone access when prompted by your browser.
3. You will hear the bot speak! Read this script into your mic:

### What to say (Read this verbatim):
- **Bot:** *"Hello, am I speaking with Mr. Sharma? This is Priya calling from Home Credit."*
- **You:** *"Yes, speaking. What is this regarding?"*
- **Bot:** *(Presents the ₹75 Lakh LAP loyalty offer and asks for 2 minutes to check eligibility)*
- **You:** *"Sure, go ahead."*
- **Bot:** *(Asks property type: residential, commercial, or industrial?)*
- **You:** *"It is a residential apartment."*
- **Bot:** *(Asks ownership status: sole or joint?)*
- **You:** *"It is solely owned by me."*
- **Bot:** *(Asks document availability: original title deeds ready?)*
- **You:** *"Yes, I have all the original documents with me."*
- **Bot:** *(Asks loan amount looking to borrow)*
- **You:** *"I need fifty lakh rupees."*
- **Bot:** *(Asks occupation and income mode: bank or cash?)*
- **You:** *"I am salaried in an IT company, and my salary comes directly into my bank account."*
- **Bot:** *(Asks estimated market value of property)*
- **You:** *"It is around one crore twenty lakh rupees."*
- **Bot:** *(Asks repayment tenure in years)*
- **You:** *"Ten years."*
- **Bot:** *(Handoff line: congratulates on eligibility, promises senior loan expert callback, and asks for preferred time)*
- **You:** *"Tomorrow morning at eleven AM is great."*
- **Bot:** *(Confirms and bids farewell)*
- Click **"End Call"**!

---

## Step 4: Copy the Public Call Recording Link
1. On the left sidebar in Retell AI, click **"Call History"** (or "Calls").
2. Click on the call you just completed.
3. You will see the audio player, duration, and the full transcript.
4. Click the **"Share"** button or **"Copy Public Link"** icon (top right of the call details page).
5. Paste that link into:
   - [recordings/README.md](file:///c:/Users/patha/Downloads/home-credit-lap-voice-agent-starter/home-credit-lap-voice-agent/recordings/README.md)
   - [FINAL_SUBMISSION.md](file:///c:/Users/patha/Downloads/home-credit-lap-voice-agent-starter/home-credit-lap-voice-agent/FINAL_SUBMISSION.md)

---

## (Optional) Quick 30-Second Test Calls for Edge Cases
If you want to submit recordings for extra credit:
- **Disqualification Test (Farmland):** Answer Property Type with *"It is agricultural farmland."* -> Bot politely ends call immediately!
- **Transfer Switch Test (Existing Loan):** When bot asks property type, say *"It is a flat, but I already have an ongoing home loan and want to reduce my EMI."* -> Bot switches to loan transfer specialist and ends call!
