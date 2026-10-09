"""
Home Credit LAP Voice Agent - Automated Logic & Dialogue Simulator
Validates conversational flow, slot extraction, disqualification switches, and handoff gates.
"""

import re
import sys
from typing import Dict, Any, List

class VoiceAgentSimulator:
    def __init__(self, agent_name="Priya", agent_gender="Female", company_name="Home Credit", customer_name="Mr. Sharma"):
        self.agent_name = agent_name
        self.agent_gender = agent_gender
        self.company_name = company_name
        self.customer_name = customer_name
        self.reset()

    def reset(self):
        self.state = {
            "identity_verified": False,
            "offer_consented": False,
            "property_type": None,
            "ownership_status": None,
            "original_docs": None,
            "loan_amount": None,
            "occupation": None,
            "income_mode": None,
            "market_value": None,
            "tenure_years": None,
            "call_status": "ACTIVE", # ACTIVE, DISQUALIFIED, TRANSFERRED, HANDOFF_COMPLETE, CALLBACK_SCHEDULED, TERMINATED
            "current_question": "GREETING",
            "history": []
        }

    def process_turn(self, utterance: str) -> str:
        text = utterance.lower()
        self.state["history"].append(f"Customer: {utterance}")

        # Check for DNC
        if "don't call" in text or "dnc" in text or "stop calling" in text:
            self.state["call_status"] = "TERMINATED"
            resp = f"I sincerely apologize for the inconvenience, {self.customer_name}. I will register your number on our Do Not Call list immediately. Thank you for your time, and have a good day."
            self.state["history"].append(f"Agent: {resp}")
            return resp

        # Check for Busy / Callback
        if any(w in text for w in ["busy", "driving", "in a meeting", "call later", "tomorrow"]):
            self.state["call_status"] = "CALLBACK_SCHEDULED"
            resp = f"I completely understand, {self.customer_name}. I have noted to call you back tomorrow. Thank you for your time, and have a good day!"
            self.state["history"].append(f"Agent: {resp}")
            return resp

        # Check for Wrong Person
        if any(w in text for w in ["not rajesh", "wrong number", "his brother", "not him", "not me"]):
            self.state["call_status"] = "TERMINATED"
            resp = f"I apologize for the disturbance. Is {self.customer_name} available to speak right now?"
            self.state["history"].append(f"Agent: {resp}")
            return resp

        # Check Identity
        if not self.state["identity_verified"]:
            if any(w in text for w in ["yes", "speaking", "haan", "boliye", "i am", "this is"]):
                self.state["identity_verified"] = True
                self.state["current_question"] = "OFFER"
                resp = f"Thank you, {self.customer_name}. As a reward for your loyalty with {self.company_name}, you have a special pre-approved Loan Against Property offer of up to seventy-five lakh rupees. May I ask you a few quick questions to check your eligibility? It will take just two minutes."
                self.state["history"].append(f"Agent: {resp}")
                return resp
            else:
                resp = f"This is {self.agent_name} from {self.company_name}. Am I speaking with {self.customer_name}?"
                self.state["history"].append(f"Agent: {resp}")
                return resp

        # Check Offer Consent
        if not self.state["offer_consented"]:
            if any(w in text for w in ["sure", "yes", "okay", "go ahead", "haan", "fine", "proceed"]):
                self.state["offer_consented"] = True
                self.state["current_question"] = "PROPERTY_TYPE"
            elif "not interested" in text or "no" in text:
                self.state["call_status"] = "TERMINATED"
                resp = f"No problem at all, {self.customer_name}. Thank you for being with {self.company_name}, and have a wonderful day!"
                self.state["history"].append(f"Agent: {resp}")
                return resp

        # Check SWITCH 2: Transfer Logic Switch (Existing loan on same property / lower EMI)
        if any(w in text for w in ["existing loan", "home loan", "running loan", "transfer", "lower emi", "reduce emi", "balance transfer"]):
            self.state["call_status"] = "TRANSFERRED"
            resp = f"I understand, {self.customer_name}. Since you have an existing loan on the property and are looking for a loan transfer or lower EMI, our specialized Loan Transfer expert will contact you shortly to assist you. Thank you for your time, and have a great day!"
            self.state["history"].append(f"Agent: {resp}")
            return resp

        # Slot Extraction logic
        # 1. Property type
        if "agricultural" in text or "farmland" in text or "kheti" in text:
            self.state["property_type"] = "agricultural"
            self.state["call_status"] = "DISQUALIFIED"
            resp = f"I understand, {self.customer_name}. Unfortunately, based on our current policy guidelines, you do not meet the preliminary criteria for this specific pre-approved offer at this time. Thank you so much for your time, and have a wonderful day."
            self.state["history"].append(f"Agent: {resp}")
            return resp
        elif "residential" in text or "flat" in text or "house" in text or "apartment" in text:
            self.state["property_type"] = "residential"
        elif "commercial" in text or "shop" in text or "office" in text:
            self.state["property_type"] = "commercial"
        elif "industrial" in text or "factory" in text:
            self.state["property_type"] = "industrial"

        # 2. Ownership
        if "sole" in text or "only me" in text or "my name" in text or "myself" in text:
            self.state["ownership_status"] = "sole"
        elif "joint" in text or "wife" in text or "partner" in text or "family" in text:
            self.state["ownership_status"] = "joint"

        # 3. Documents
        if "no original" in text or "lost" in text or "photocopy" in text or "xerox" in text or "don't have original" in text:
            self.state["original_docs"] = "unavailable"
            self.state["call_status"] = "DISQUALIFIED"
            resp = f"I understand, {self.customer_name}. Unfortunately, based on our current policy guidelines, you do not meet the preliminary criteria for this specific pre-approved offer at this time. Thank you so much for your time, and have a wonderful day."
            self.state["history"].append(f"Agent: {resp}")
            return resp
        elif "have original" in text or "original documents" in text or "all original" in text or "yes i have" in text or "in my locker" in text:
            self.state["original_docs"] = "available"

        # 4. Market value vs Loan amount context
        if self.state["current_question"] == "MARKET_VALUE":
            if any(w in text for w in ["crore", "lakh", "worth", "around", "market value"]):
                self.state["market_value"] = "recorded"
            elif "no idea" in text or "unsure" in text:
                self.state["market_value"] = "pending_estimate"
        elif self.state["current_question"] == "LOAN_AMOUNT":
            if any(w in text for w in ["1 crore", "one crore", "1.2 crore", "1.5 crore", "80 lakh", "90 lakh", "100 lakh"]):
                self.state["loan_amount"] = "PENDING_CAP"
                self.state["current_question"] = "CAP_CONFIRMATION"
                resp = f"The maximum loan amount under this pre-approved offer is seventy-five lakh rupees. Would you like to proceed with seventy-five lakh rupees?"
                self.state["history"].append(f"Agent: {resp}")
                return resp
            elif any(w in text for w in ["lakh", "fifty", "forty", "thirty", "twenty", "ten"]):
                self.state["loan_amount"] = "valid"
        elif self.state["current_question"] == "CAP_CONFIRMATION":
            if any(w in text for w in ["yes", "proceed", "accept", "sure", "fine", "okay"]):
                self.state["loan_amount"] = "75 lakh"
            else:
                self.state["call_status"] = "DISQUALIFIED"
                resp = f"I understand, {self.customer_name}. Unfortunately, based on our current policy guidelines, you do not meet the preliminary criteria for this specific pre-approved offer at this time. Thank you so much for your time, and have a wonderful day."
                self.state["history"].append(f"Agent: {resp}")
                return resp
        else:
            # Out of order loan amount capture
            if "need" in text and "lakh" in text:
                self.state["loan_amount"] = "valid"

        # 5. Occupation & Income Mode
        if "cash" in text:
            self.state["income_mode"] = "cash"
            self.state["call_status"] = "DISQUALIFIED"
            resp = f"I understand, {self.customer_name}. Unfortunately, based on our current policy guidelines, you do not meet the preliminary criteria for this specific pre-approved offer at this time. Thank you so much for your time, and have a wonderful day."
            self.state["history"].append(f"Agent: {resp}")
            return resp
        if "salaried" in text or "job" in text:
            self.state["occupation"] = "salaried"
        elif "self-employed" in text or "business" in text or "shop" in text:
            self.state["occupation"] = "self-employed"
        if "bank" in text or "account" in text or "direct deposit" in text or "hdfc" in text:
            self.state["income_mode"] = "bank"

        # 6. Tenure
        if self.state["current_question"] == "TENURE" or "year" in text:
            match = re.search(r'(\d+)\s*year', text)
            if match:
                yrs = int(match.group(1))
                if yrs < 3 or yrs > 15:
                    resp = "Our loan repayment tenure is between three and fifteen years. Would a tenure within three to fifteen years work for you?"
                    self.state["history"].append(f"Agent: {resp}")
                    return resp
                else:
                    self.state["tenure_years"] = f"{yrs} years"
            else:
                if any(w in text for w in ["ten", "five", "seven", "eight", "twelve", "fifteen"]):
                    self.state["tenure_years"] = "valid"

        # Determine next missing slot
        if self.state["property_type"] is None:
            self.state["current_question"] = "PROPERTY_TYPE"
            resp = "What type of property would you like to mortgage: residential like a house or flat, commercial like a shop or office, or industrial like a factory?"
        elif self.state["ownership_status"] is None:
            self.state["current_question"] = "OWNERSHIP"
            resp = "Is the property owned solely by you, or is it jointly owned with family or partners?"
        elif self.state["original_docs"] is None:
            self.state["current_question"] = "DOCUMENTS"
            resp = "Do you have the original title deeds and property documents available with you for verification?"
        elif self.state["loan_amount"] is None:
            self.state["current_question"] = "LOAN_AMOUNT"
            resp = "How much loan amount are you looking to borrow?"
        elif self.state["occupation"] is None or self.state["income_mode"] is None:
            self.state["current_question"] = "INCOME"
            if self.state["occupation"] is not None and self.state["income_mode"] is None:
                resp = "And do you receive your income into a bank account, or in cash?"
            else:
                resp = "Are you salaried or self-employed? And do you receive your primary income into a bank account, or in cash?"
        elif self.state["market_value"] is None:
            self.state["current_question"] = "MARKET_VALUE"
            resp = "What is the approximate current market value of your property?"
        elif self.state["tenure_years"] is None:
            self.state["current_question"] = "TENURE"
            resp = "In how many years would you prefer to repay the loan?"
        else:
            # All 7 verified! Trigger Handoff Gate
            self.state["current_question"] = "HANDOFF"
            self.state["call_status"] = "HANDOFF_COMPLETE"
            resp = f"Thank you so much, {self.customer_name}. Based on your answers, you meet the preliminary eligibility criteria for our Loan Against Property offer! A senior loan expert from {self.company_name} will call you back shortly to provide exact interest rates, customized EMI options, and finalize your application. Is there any convenient time you would prefer for them to call?"

        self.state["history"].append(f"Agent: {resp}")
        return resp


def run_all_tests():
    print("=" * 70)
    print("RUNNING HOME CREDIT LAP VOICE AGENT SIMULATED TEST SUITE")
    print("=" * 70)

    # Test 1: Golden Path
    sim = VoiceAgentSimulator()
    sim.process_turn("Yes, speaking.") # Verified
    sim.process_turn("Sure, go ahead.") # Offer consent
    sim.process_turn("It is a residential flat.") # Property
    sim.process_turn("It is solely in my name.") # Ownership
    sim.process_turn("Yes, I have all original documents ready.") # Docs
    sim.process_turn("I need fifty lakh rupees.") # Amount
    sim.process_turn("I am salaried and salary comes in bank.") # Occ + Mode
    sim.process_turn("Market value is around one crore.") # MV
    r = sim.process_turn("Ten years.") # Tenure
    assert sim.state["call_status"] == "HANDOFF_COMPLETE", f"Expected HANDOFF_COMPLETE, got {sim.state['call_status']}"
    print(" [PASS] T01: Golden Path (Fully Eligible) -> Successfully qualified and handed off.")

    # Test 2: Agricultural Disqualification
    sim.reset()
    sim.process_turn("Yes, Rajesh speaking.")
    sim.process_turn("Sure.")
    r = sim.process_turn("It is agricultural farmland.")
    assert sim.state["call_status"] == "DISQUALIFIED", f"Expected DISQUALIFIED, got {sim.state['call_status']}"
    assert "unfortunately" in r.lower(), "Expected polite disqualification statement"
    print(" [PASS] T04: Agricultural Land Disqualification -> Immediate polite exit.")

    # Test 3: Cash Income Disqualification
    sim.reset()
    sim.process_turn("Yes, speaking.")
    sim.process_turn("Go ahead.")
    sim.process_turn("Commercial shop.")
    sim.process_turn("Solely owned.")
    sim.process_turn("Yes, original documents are available.")
    sim.process_turn("Twenty lakh.")
    r = sim.process_turn("I run a business but all my income is in cash.")
    assert sim.state["call_status"] == "DISQUALIFIED"
    print(" [PASS] T05: Cash Income Disqualification -> Immediate polite exit.")

    # Test 4: Missing Original Documents
    sim.reset()
    sim.process_turn("Yes.")
    sim.process_turn("Sure.")
    sim.process_turn("Residential house.")
    sim.process_turn("Jointly with wife.")
    r = sim.process_turn("No original documents, I only have photocopies.")
    assert sim.state["call_status"] == "DISQUALIFIED"
    print(" [PASS] T06: Unavailable Original Documents -> Immediate polite exit.")

    # Test 5: Switch 2 Existing Loan / EMI Transfer
    sim.reset()
    sim.process_turn("Yes.")
    sim.process_turn("Sure.")
    r = sim.process_turn("Actually I have an existing home loan and want to reduce my EMI.")
    assert sim.state["call_status"] == "TRANSFERRED"
    assert "loan transfer expert" in r.lower() or "loan transfer specialist" in r.lower()
    print(" [PASS] T09: Transfer Switch (Existing Loan / Lower EMI) -> Routed to transfer specialist.")

    # Test 6: Loan Amount Cap Negotiation
    sim.reset()
    sim.process_turn("Yes.")
    sim.process_turn("Sure.")
    sim.process_turn("Residential flat.")
    sim.process_turn("Sole.")
    sim.process_turn("Yes original documents ready.")
    r = sim.process_turn("I need one crore rupees.")
    assert "seventy-five lakh rupees" in r.lower()
    r = sim.process_turn("Yes, I accept seventy-five lakh rupees.")
    assert sim.state["loan_amount"] == "75 lakh"
    print(" [PASS] T07: Loan Amount Cap Negotiation -> Offered 75L cap and accepted.")

    # Test 7: Busy / Callback
    sim.reset()
    r = sim.process_turn("I am driving right now, please call me tomorrow.")
    assert sim.state["call_status"] == "CALLBACK_SCHEDULED"
    print(" [PASS] T03: Busy / Callback Scheduling -> Acknowledged and scheduled cleanly.")

    # Test 8: Do Not Call
    sim.reset()
    r = sim.process_turn("Stop calling me, put me on DNC.")
    assert sim.state["call_status"] == "TERMINATED"
    assert "do not call" in r.lower()
    print(" [PASS] T17: Do Not Call (DNC) -> Registered and ended respectfully.")

    print("=" * 70)
    print("ALL 8 AUTOMATED SIMULATION TEST SUITES PASSED FLAWLESSLY!")
    print("=" * 70)

if __name__ == "__main__":
    run_all_tests()
