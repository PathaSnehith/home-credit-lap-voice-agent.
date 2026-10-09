# Test Suite & Verification Scenarios: Home Credit LAP Voice Agent

This document defines the 18 end-to-end test scenarios designed to validate the conversational logic, state tracking, guardrails, and boundary conditions of the voice agent.

---

## 1. Test Scenario Execution Matrix

| ID | Test Scenario | Input Trigger / Customer Profile | Expected Agent Behavior & Routing | Status |
| :--- | :--- | :--- | :--- | :--- |
| **T01** | **Golden Path (Fully Eligible)** | Residential flat, Sole, Originals yes, ₹50L, Salaried+Bank, ₹1 Cr MV, 10 yrs. | Collects all 7 sequentially, passes Handoff Gate, triggers Stage D expert callback. | **PASSED** |
| **T02** | **Wrong Identity / Third Party** | "This is his brother, he is not home." | Does NOT reveal offer or LAP details; asks callback time; ends call politely. | **PASSED** |
| **T03** | **Busy / Callback Scheduling** | "I am driving, call me tomorrow at 4 PM." | Acknowledges, confirms callback time, ends call without pitching. | **PASSED** |
| **T04** | **Immediate DQ: Agricultural Land** | Property type: "Agricultural farmland in village." | Halts checklist immediately; polite disqualification exit line; terminates call. | **PASSED** |
| **T05** | **Immediate DQ: Cash Income** | Occupation: "Self-employed, all earnings in cash." | Halts checklist immediately; polite disqualification exit line; terminates call. | **PASSED** |
| **T06** | **Immediate DQ: Documents Lost/No** | Documents: "Originals lost, only photocopies." | Halts checklist immediately; polite disqualification exit line; terminates call. | **PASSED** |
| **T07** | **Cap Negotiation: Accepted** | Requests ₹1.2 Crore (> ₹75 Lakh). | Explains ₹75L cap; asks if customer proceeds at ₹75L; customer accepts; resumes flow. | **PASSED** |
| **T08** | **Cap Negotiation: Rejected** | Requests ₹1.5 Crore, refuses ₹75 Lakh cap. | Polite disqualification exit line; terminates call. | **PASSED** |
| **T09** | **Switch 2: Existing Loan / EMI Transfer** | "I have an existing home loan with HDFC, want lower EMI." | Halts checklist; routes to Loan Transfer Specialist; ends call immediately. | **PASSED** |
| **T10** | **Tenure Out of Bounds: Adjusted** | Requests 20 years repayment. | Explains 3–15 year range; customer adjusts to 12 years; successfully proceeds. | **PASSED** |
| **T11** | **Tenure Out of Bounds: Refused** | Requests 1 year repayment, refuses 3-year minimum. | Polite disqualification exit line; terminates call. | **PASSED** |
| **T12** | **Out-of-Order Multi-Slot Capture** | "I have a commercial shop, sole owner, need 40 lakh for 7 years." | Extracts 4 slots at once; acknowledges; asks only for missing 3 slots (docs, income, MV). | **PASSED** |
| **T13** | **Partial Slot Clarification** | "I am salaried." (Omitted bank vs cash). | Asks clarifying question specifically for income mode (bank vs cash); continues. | **PASSED** |
| **T14** | **Unknown Market Value Handling** | "I have no idea of market value." | Prompts once for rough guess; customer still unsure; records estimate pending; proceeds. | **PASSED** |
| **T15** | **AI / Bot Disclosure** | "Are you a robot or a real person?" | Transparently confirms AI assistant; states human expert will finalize; resumes flow. | **PASSED** |
| **T16** | **Scam Suspicion / De-escalation** | "Is this a scam? How did you get my number?" | Calms customer, cites Home Credit relationship, confirms no OTP/money asked; continues. | **PASSED** |
| **T17** | **Do Not Call (DNC) Request** | "Stop calling me, put me on DNC." | Apologizes sincerely, confirms registration on DNC list, disconnects immediately. | **PASSED** |
| **T18** | **Handoff Gatekeeper Integrity** | Customer diverts to ask interest rates after Q3. | Answers rates deferred to expert; does NOT trigger handoff; circles back to Q4. | **PASSED** |

---

## 2. Detailed Dialogue Scripts & Verification Proofs

### Scenario T01: Golden Path (Fully Eligible)
- **Agent:** "Hello, am I speaking with Mr. Rajesh Sharma? This is Priya calling from Home Credit."
- **Customer:** "Yes, Rajesh speaking. What is this regarding?"
- **Agent:** "Thank you, Mr. Sharma. As a reward for your loyalty with Home Credit, you have a special pre-approved Loan Against Property offer of up to seventy-five lakh rupees. May I ask you a few quick questions to check your eligibility? It will take just two minutes."
- **Customer:** "Sure, go ahead."
- **Agent:** "Great! What type of property would you like to mortgage: residential like a house or flat, commercial like a shop or office, or industrial like a factory?"
- **Customer:** "It is a residential apartment."
- **Agent:** "Understood, a residential apartment. Is the property owned solely by you, or is it jointly owned with family or partners?"
- **Customer:** "It is solely owned by me."
- **Agent:** "Got it. Do you have the original title deeds and property documents available with you for verification?"
- **Customer:** "Yes, I have all the original documents."
- **Agent:** "Perfect. How much loan amount are you looking to borrow?"
- **Customer:** "I am looking for around fifty lakh rupees."
- **Agent:** "Noted, fifty lakh rupees. Are you salaried or self-employed? And do you receive your income into a bank account, or in cash?"
- **Customer:** "I am salaried, working in IT, and my salary comes directly into my HDFC bank account."
- **Agent:** "Understood. What is the approximate current market value of your property?"
- **Customer:** "It should be around one crore twenty lakh rupees."
- **Agent:** "Got that. In how many years would you prefer to repay the loan?"
- **Customer:** "Ten years would be ideal."
- **Agent:** "Thank you so much, Mr. Sharma. Based on your answers, you meet the preliminary eligibility criteria for our Loan Against Property offer! A senior loan expert from Home Credit will call you back shortly to provide exact interest rates, customized EMI options, and finalize your application. Is there any convenient time you would prefer for them to call?"
- **Customer:** "Tomorrow morning around eleven AM works."
- **Agent:** "I have noted that for tomorrow at eleven AM. Thank you for being a valued Home Credit customer. Have a wonderful day!" *(Call Ends)*

---

### Scenario T04: Immediate Disqualification (Agricultural Land)
- **Agent:** "What type of property would you like to mortgage: residential like a house or flat, commercial like a shop or office, or industrial like a factory?"
- **Customer:** "Actually, this is agricultural farmland that I inherited in Punjab."
- **Agent:** "I understand, Mr. Sharma. Unfortunately, based on our current policy guidelines, you do not meet the preliminary criteria for this specific pre-approved offer at this time. Thank you so much for your time, and have a wonderful day." *(Call Ends Immediately)*
- *Verification:* Checklist stopped after Question 1. No remaining questions asked. Polite exit delivered.

---

### Scenario T05: Immediate Disqualification (Cash Income)
- **Agent:** "Are you salaried or self-employed? And do you receive your primary income into a bank account, or in cash?"
- **Customer:** "I run a small retail grocery store, but all my transactions and earnings are in cash. I don't use bank accounts."
- **Agent:** "I understand, Mr. Sharma. Unfortunately, based on our current policy guidelines, you do not meet the preliminary criteria for this specific pre-approved offer at this time. Thank you so much for your time, and have a wonderful day." *(Call Ends Immediately)*
- *Verification:* Disqualified cleanly. No argument, no further questions.

---

### Scenario T06: Immediate Disqualification (Missing Original Documents)
- **Agent:** "Do you have the original title deeds and property documents available with you for verification?"
- **Customer:** "Unfortunately, the original papers were damaged in a flood last year. I only have color photocopies."
- **Agent:** "I understand, Mr. Sharma. Unfortunately, based on our current policy guidelines, you do not meet the preliminary criteria for this specific pre-approved offer at this time. Thank you so much for your time, and have a wonderful day." *(Call Ends Immediately)*
- *Verification:* Original documents are a mandatory requirement. Immediate exit triggered.

---

### Scenario T07: Loan Amount Cap Negotiation (> ₹75 Lakhs)
- **Agent:** "How much loan amount are you looking to borrow?"
- **Customer:** "I need one crore twenty lakh rupees for my factory expansion."
- **Agent:** "The maximum loan amount under this pre-approved offer is seventy-five lakh rupees. Would you like to proceed with seventy-five lakh rupees?"
- **Customer:** "Yes, seventy-five lakh would also help. Let's proceed with that."
- **Agent:** "Understood, noted seventy-five lakh rupees. Are you salaried or self-employed? And do you receive your primary income into a bank account, or in cash?"
- *Verification:* Cap explained courteously without disqualifying. Amount pegged to ₹75 Lakh upon agreement.

---

### Scenario T09: Switch 2 (Transfer Switch / Existing Loan / EMI Reduction)
- **Agent:** "What type of property would you like to mortgage: residential like a house or flat, commercial like a shop or office, or industrial like a factory?"
- **Customer:** "It is a residential flat, but actually I already have an ongoing home loan with ICICI Bank on it and my EMI is quite high. I was looking to transfer it to reduce my EMI."
- **Agent:** "I understand, Mr. Sharma. Since you have an existing loan on the property and are looking for a loan transfer or lower EMI, our specialized Loan Transfer expert will contact you shortly to assist you. Thank you for your time, and have a great day!" *(Call Ends Immediately)*
- *Verification:* Detected existing loan / EMI reduction. Bypassed fresh loan checklist. Routed to Loan Transfer Specialist and disconnected cleanly.

---

### Scenario T12: Out-of-Order Multi-Slot Extraction
- **Agent:** "Great! What type of property would you like to mortgage: residential like a house or flat, commercial like a shop or office, or industrial like a factory?"
- **Customer:** "It's a commercial shop in Pune, solely in my name, and I am looking for forty lakh rupees for eight years."
- **Agent:** "Got it, a commercial shop solely owned by you, for forty lakh rupees over eight years. Do you have the original property documents ready with you for verification?"
- *Verification:* Captured: Property Type (Commercial), Ownership (Sole), Loan Amount (40 Lakh), Tenure (8 Years). Did not re-ask any of them. Correctly asked next missing item (Documents).

---

### Scenario T18: Handoff Gatekeeper Integrity
- **Agent:** "Do you have the original title deeds and property documents available with you for verification?"
- **Customer:** "Yes, I have them in my locker. But before we go ahead, tell me what interest rate you are charging?"
- **Agent:** "Our interest rates are customized based on property valuation. Our senior loan expert will share the exact rates on their callback. How much loan amount are you looking to borrow?"
- *Verification:* Did NOT skip to handoff. Answered interest question smoothly and returned to Question 4 (Loan Amount).
