# Home Credit LAP Voice Agent (SalesAgents AI Assignment)

An enterprise-grade, conversational AI Voice Agent designed for **Home Credit** to qualify existing customers for a pre-approved **Loan Against Property (LAP)** loyalty offer of up to **₹75,00,000 (75 Lakhs)**.

Built and submitted for the **AI Intern / Prompt Engineer** assignment at **SalesAgents AI**.

---

## 🚀 Key Features & Capabilities

- **7-Point Qualification Engine:** Sequentially collects Property Type, Ownership, Original Documents, Loan Amount, Occupation & Bank Income, Market Value, and Repayment Tenure.
- **Out-of-Order Slot Extraction:** Dynamically extracts multi-slot data if volunteered early by the customer and skips redundant questions.
- **Immediate Disqualification Boundary:** Politely terminates calls when hard eligibility criteria are violated (Agricultural land, Cash income, Lost/Unavailable original documents, or Refusal of policy limits).
- **The "Transfer" Logic Switch:** Automatically detects customers with active loans on the property or looking for EMI reduction / balance transfer, routes them to a specialized loan transfer team, and exits the fresh loan pipeline.
- **Mandatory Handoff Gatekeeper:** Guarantees that no customer is passed to a senior loan expert callback until all 7 checklist slots are fully validated and confirmed.
- **Strict Guardrails & Voice Optimization:**
  - Zero PII collection (stops customer if sharing OTP, PIN, PAN, Aadhaar).
  - Anti-hallucination policy (defers interest rates and EMI calculations to human expert).
  - Spoken number phonetics (outputs "seventy-five lakh rupees" instead of numbers).
  - Zero markdown or special characters in spoken speech.
  - Strict grammatical gender and language agreement in English and Hindi/Hinglish.

---

## 📁 Repository Structure

```
├── FINAL_SUBMISSION.md             # Complete submission report ready for review
├── TESTING_CHEATSHEET.md           # 3-minute quickstart guide for testing on Retell AI
├── docs/
│   └── conversation_flow.md        # State machine, Mermaid flowcharts, and qualification matrix
├── prompts/
│   ├── system_prompt.md            # Production-grade system prompt with all dynamic variables
│   ├── retell_direct_copy_paste.txt# Ready-to-paste prompt with defaults for Retell web playground
│   └── retell_agent_config.json    # Retell AI agent configuration (voice, latency, backchannel)
├── tests/
│   ├── test_scenarios.md           # 18 exhaustive test cases with transcripts & validation proofs
│   └── simulate_call.py            # Automated test simulator script (all 8 automated test suites passing)
└── recordings/
    └── README.md                   # Call recordings & transcript evidence log
```

---

## ⚡ Quick Start: Test Locally

Run the automated simulation test suite directly:

```bash
python tests/simulate_call.py
```

Output:
```
======================================================================
RUNNING HOME CREDIT LAP VOICE AGENT SIMULATED TEST SUITE
======================================================================
 [PASS] T01: Golden Path (Fully Eligible) -> Successfully qualified and handed off.
 [PASS] T04: Agricultural Land Disqualification -> Immediate polite exit.
 [PASS] T05: Cash Income Disqualification -> Immediate polite exit.
 [PASS] T06: Unavailable Original Documents -> Immediate polite exit.
 [PASS] T09: Transfer Switch (Existing Loan / Lower EMI) -> Routed to transfer specialist.
 [PASS] T07: Loan Amount Cap Negotiation -> Offered 75L cap and accepted.
 [PASS] T03: Busy / Callback Scheduling -> Acknowledged and scheduled cleanly.
 [PASS] T17: Do Not Call (DNC) -> Registered and ended respectfully.
======================================================================
ALL 8 AUTOMATED SIMULATION TEST SUITES PASSED FLAWLESSLY!
======================================================================
```

---

## 🎙️ Testing on Retell AI

Follow the step-by-step instructions in [TESTING_CHEATSHEET.md](TESTING_CHEATSHEET.md):
1. Sign up on [Retell AI](https://www.retellai.com) (free trial credits included).
2. Create a Single Prompt Agent, paste the contents of `prompts/retell_direct_copy_paste.txt`.
3. Conduct a 60-second test web call following the verbatim spoken script in the cheatsheet.
4. Copy the public call recording link from Call History and submit it.

---

## 📄 Submission Document

Review the comprehensive assignment submission report in [FINAL_SUBMISSION.md](FINAL_SUBMISSION.md).
