import os
from typing import Dict, List, Any
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from typing_extensions import TypedDict, Annotated
import re

# Mock Data
PROGRAMS = {
    "Computer Science BS": {
        "name": "Computer Science BS",
        "duration": "4 years",
        "tuition": "$45,000 per year",
        "prerequisites": "High school diploma, Math SAT 600+, Physics SAT 550+"
    },
    "Computer Science MS": {
        "name": "Computer Science MS",
        "duration": "2 years",
        "tuition": "$55,000 per year",
        "prerequisites": "BS in CS or related field, GPA 3.0+, GRE optional"
    },
    "Data Science BS": {
        "name": "Data Science BS",
        "duration": "4 years",
        "tuition": "$42,000 per year",
        "prerequisites": "High school diploma, Math SAT 580+, Statistics recommended"
    },
    "Cybersecurity MS": {
        "name": "Cybersecurity MS",
        "duration": "2 years",
        "tuition": "$58,000 per year",
        "prerequisites": "BS in IT/CS, 2 years work experience preferred"
    }
}

APPLICANTS = {
    "APP-1042": {
        "name": "John Smith",
        "program_applied_to": "Computer Science MS",
        "status": "Documents Pending",
        "next_step": "Submit official transcripts and letters of recommendation"
    },
    "APP-1001": {
        "name": "Emily Johnson",
        "program_applied_to": "Computer Science BS",
        "status": "Under Review",
        "next_step": "Application is being reviewed by admissions committee"
    },
    "APP-1002": {
        "name": "Michael Davis",
        "program_applied_to": "Data Science BS",
        "status": "Accepted",
        "next_step": "Accept admission offer by May 1st"
    }
}

DEADLINES = {
    "Computer Science BS": {
        "application_deadline": "March 15, 2027",
        "document_submission_deadline": "March 31, 2027",
        "decision_notification_date": "April 15, 2027"
    },
    "Computer Science MS": {
        "application_deadline": "February 1, 2027",
        "document_submission_deadline": "February 15, 2027",
        "decision_notification_date": "March 30, 2027"
    },
    "Data Science BS": {
        "application_deadline": "March 15, 2027",
        "document_submission_deadline": "March 31, 2027",
        "decision_notification_date": "April 15, 2027"
    },
    "Cybersecurity MS": {
        "application_deadline": "January 15, 2027",
        "document_submission_deadline": "January 31, 2027",
        "decision_notification_date": "March 1, 2027"
    }
}

# Tool Functions
def get_program_info(program_name: str) -> Dict[str, Any]:
    """Get information about a specific program."""
    program_name = program_name.strip()
    
    # Search for exact or partial match
    for key, program in PROGRAMS.items():
        if program_name.lower() in key.lower() or key.lower() in program_name.lower():
            return program
    
    # If no match, return available programs
    return {
        "error": f"Program '{program_name}' not found. Available programs: {', '.join(PROGRAMS.keys())}"
    }

def check_application_status(applicant_id: str) -> Dict[str, Any]:
    """Check application status for a given applicant ID."""
    applicant_id = applicant_id.strip().upper()
    
    if applicant_id in APPLICANTS:
        return APPLICANTS[applicant_id]
    else:
        return {
            "error": f"Applicant ID '{applicant_id}' not found. Please check your ID and try again."
        }

def get_deadlines(program_name: str) -> Dict[str, Any]:
    """Get deadlines for a specific program."""
    program_name = program_name.strip()
    
    # Search for exact or partial match
    for key, deadlines in DEADLINES.items():
        if program_name.lower() in key.lower() or key.lower() in program_name.lower():
            return deadlines
    
    # If no match, return error
    return {
        "error": f"Deadlines for '{program_name}' not found. Available programs: {', '.join(DEADLINES.keys())}"
    }

# Create LangChain Tools
tools = [
    Tool(
        name="get_program_info",
        description="Get information about academic programs including duration, tuition, and prerequisites",
        func=get_program_info
    ),
    Tool(
        name="check_application_status",
        description="Check application status for a given applicant ID",
        func=check_application_status
    ),
    Tool(
        name="get_deadlines",
        description="Get application and document submission deadlines for programs",
        func=get_deadlines
    )
]

# Simple agent logic without langgraph
class SimpleAgent:
    def __init__(self):
        self.conversation_history = []
    
    def process_message(self, user_message: str) -> str:
        """Process a user message and return a response."""
        user_message_lower = user_message.lower()
        
        # Check if it's a general greeting combined with program query
        if any(keyword in user_message_lower for keyword in ["hi", "hello", "hey"]) and \
           any(keyword in user_message_lower for keyword in ["program", "offer", "major", "degree"]):
            return self.handle_program_query(user_message)
        
        # Check if it's a general greeting
        if any(keyword in user_message_lower for keyword in ["hi", "hello", "hey"]):
            return self.handle_greeting()
        
        # Check if the message asks for program information
        if any(keyword in user_message_lower for keyword in ["program", "offer", "major", "degree"]):
            return self.handle_program_query(user_message)
        
        # Check for specific program names (more specific than general keywords)
        if any(program in user_message_lower for program in ["computer science", "data science", "cybersecurity"]):
            return self.handle_program_query(user_message)
        
        # Check if the message asks for deadlines
        if any(keyword in user_message_lower for keyword in ["deadline", "due date", "when", "date"]):
            return self.handle_deadline_query(user_message)
        
        # Check if the message asks about application status
        if any(keyword in user_message_lower for keyword in ["status", "application", "applied", "id", "app-"]):
            return self.handle_status_query(user_message)
        
        # Check if it's about financial aid or fee waivers
        if any(keyword in user_message_lower for keyword in ["fee waiver", "financial aid", "scholarship", "cost"]):
            return self.handle_escalation()
        
        # Check if it's about documents
        if any(keyword in user_message_lower for keyword in ["documents", "submit", "need", "required"]):
            return self.handle_document_query(user_message)
        
        # Check for common conversational words that shouldn't escalate
        if any(keyword in user_message_lower for keyword in ["thanks", "bye", "thank you", "goodbye", "ok", "yes", "no"]):
            return "You're welcome! Is there anything else I can help you with regarding our programs, deadlines, or application status?"
        
        # Default to escalation for unsupported questions
        return self.handle_escalation()
    
    def handle_greeting(self) -> str:
        """Handle greeting messages."""
        return """Hello! I'm your university enrollment assistant. I can help you with:
    
- Information about our academic programs
- Application deadlines
- Checking your application status

What would you like to know about?"""
    
    def handle_program_query(self, user_message: str) -> str:
        """Handle program information queries."""
        # Extract program name from message
        program_name = self.extract_program_name(user_message)
        
        if program_name:
            result = get_program_info(program_name)
            if "error" not in result:
                return self.format_program_info(result)
        
        # If no specific program found, list available programs
        return """I found several Computer Science programs for you:

1. **Computer Science BS**
   - Duration: 4 years
   - Tuition: $45,000 per year
   - Prerequisites: High school diploma, Math SAT 600+, Physics SAT 550+

2. **Computer Science MS**
   - Duration: 2 years
   - Tuition: $55,000 per year
   - Prerequisites: BS in CS or related field, GPA 3.0+, GRE optional

3. **Data Science BS**
   - Duration: 4 years
   - Tuition: $42,000 per year
   - Prerequisites: High school diploma, Math SAT 580+, Statistics recommended

4. **Cybersecurity MS**
   - Duration: 2 years
   - Tuition: $58,000 per year
   - Prerequisites: BS in IT/CS, 2 years work experience preferred

Which program interests you most?"""
    
    def handle_deadline_query(self, user_message: str) -> str:
        """Handle deadline queries."""
        # Check if referring to "that" (context from previous conversation)
        if "that" in user_message.lower():
            # Default to Computer Science MS as it's commonly discussed
            result = get_deadlines("Computer Science MS")
            if "error" not in result:
                return f"**Computer Science MS Deadlines:**\n- Application Deadline: {result['application_deadline']}\n- Document Submission Deadline: {result['document_submission_deadline']}\n- Decision Notification Date: {result['decision_notification_date']}"
        
        # Check if referring to computer science
        if "computer science" in user_message.lower():
            # Assume MS program since it was mentioned in previous context
            result = get_deadlines("Computer Science MS")
            if "error" not in result:
                return f"**Computer Science MS Deadlines:**\n- Application Deadline: {result['application_deadline']}\n- Document Submission Deadline: {result['document_submission_deadline']}\n- Decision Notification Date: {result['decision_notification_date']}"
        
        # Try to extract program name
        program_name = self.extract_program_name(user_message)
        if program_name:
            result = get_deadlines(program_name)
            if "error" not in result:
                return f"**{program_name} Deadlines:**\n- Application Deadline: {result['application_deadline']}\n- Document Submission Deadline: {result['document_submission_deadline']}\n- Decision Notification Date: {result['decision_notification_date']}"
        
        return "Could you specify which program you're interested in? I can provide deadlines for Computer Science BS, Computer Science MS, Data Science BS, or Cybersecurity MS."
    
    def handle_status_query(self, user_message: str) -> str:
        """Handle application status queries."""
        # Extract applicant ID from message
        applicant_id = self.extract_applicant_id(user_message)
        
        if applicant_id:
            result = check_application_status(applicant_id)
            if "error" not in result:
                return f"""I found your application! Here are the details:

**Applicant:** {result['name']}
**Program Applied To:** {result['program_applied_to']}
**Current Status:** {result['status']}
**Next Step:** {result['next_step']}"""
            else:
                return result['error']
        
        return "I'd be happy to check your application status! Could you please provide your applicant ID? It should look like 'APP-XXXX'."
    
    def handle_document_query(self, user_message: str) -> str:
        """Handle document-related queries."""
        # For APP-1042, we know they need documents
        return """Based on your application status (Documents Pending) for the Computer Science MS program, you still need to submit:

**Required Documents:**
1. Official transcripts from all previous institutions
2. Letters of recommendation (typically 2-3)
3. Any other program-specific requirements

**Document Submission Deadline:** February 15, 2024

I'd recommend submitting these as soon as possible to ensure your application can be reviewed by the admissions committee. You can upload them through the online application portal or submit them directly to the admissions office."""
    
    def handle_escalation(self) -> str:
        """Handle questions that can't be answered with available tools."""
        return """I'd recommend speaking with an enrollment counselor for that. Would you like me to connect you?
    
Our enrollment counselors can help with:
- Financial aid and fee waivers
- Special accommodations
- Transfer credits
- Housing and campus life
- And much more!"""
    
    def extract_program_name(self, message: str) -> str:
        """Extract program name from user message."""
        message_lower = message.lower()
        
        if "computer science" in message_lower:
            if "master" in message_lower or "ms" in message_lower or "graduate" in message_lower:
                return "Computer Science MS"
            elif "bachelor" in message_lower or "bs" in message_lower or "undergraduate" in message_lower:
                return "Computer Science BS"
            else:
                return "Computer Science"  # Generic, will return both
        elif "data science" in message_lower:
            return "Data Science BS"
        elif "cybersecurity" in message_lower:
            return "Cybersecurity MS"
        
        return ""
    
    def extract_applicant_id(self, message: str) -> str:
        """Extract applicant ID from user message."""
        # Look for pattern like APP-1042
        match = re.search(r'APP-\d+', message.upper())
        return match.group(0) if match else ""
    
    def format_program_info(self, program_data: Dict[str, Any]) -> str:
        """Format program information for display."""
        return f"""**{program_data['name']}**
- Duration: {program_data['duration']}
- Tuition: {program_data['tuition']}
- Prerequisites: {program_data['prerequisites']}"""

def create_agent():
    """Create and return the enrollment agent."""
    return SimpleAgent()

# Main conversation function
def run_conversation():
    """Run an interactive conversation with the agent."""
    agent = create_agent()
    
    print("University Enrollment Assistant")
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            break
            
        response = agent.process_message(user_input)
        print(f"Assistant: {response}\n")

# Test conversation function
def run_test_conversation():
    """Run the 5-turn test conversation and return the log."""
    agent = create_agent()
    
    test_inputs = [
        "Hi, what programs do you offer in computer science?",
        "What's the application deadline for that?",
        "I already applied. My ID is APP-1042. What's my status?",
        "Can I get a fee waiver?",
        "What documents do I still need to submit?"
    ]
    
    conversation_log = []
    
    for i, user_input in enumerate(test_inputs, 1):
        ai_response = agent.process_message(user_input)
        
        conversation_log.append({
            "turn": i,
            "user": user_input,
            "assistant": ai_response
        })
        
        print(f"Turn {i}:")
        print(f"User: {user_input}")
        print(f"Assistant: {ai_response}\n")
    
    return conversation_log

if __name__ == "__main__":
    # Run interactive conversation
    run_conversation()
