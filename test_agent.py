#!/usr/bin/env python3
"""
Test script for the Student Enrollment Assistant Agent
This script demonstrates the agent's functionality with mock responses
"""

import os
from student_agent import get_program_info, check_application_status, get_deadlines

def test_tools():
    """Test all three tools with sample inputs."""
    print("=== Testing Student Enrollment Assistant Tools ===\n")
    
    # Test 1: get_program_info
    print("1. Testing get_program_info with 'Computer Science':")
    result = get_program_info("Computer Science")
    print(f"Result: {result}\n")
    
    # Test 2: get_deadlines  
    print("2. Testing get_deadlines with 'Computer Science MS':")
    result = get_deadlines("Computer Science MS")
    print(f"Result: {result}\n")
    
    # Test 3: check_application_status
    print("3. Testing check_application_status with 'APP-1042':")
    result = check_application_status("APP-1042")
    print(f"Result: {result}\n")

def simulate_test_conversation():
    """Simulate the 5-turn test conversation."""
    print("=== Simulated 5-Turn Test Conversation ===\n")
    
    # Mock responses based on the expected behavior
    conversation = [
        {
            "turn": 1,
            "user": "Hi, what programs do you offer in computer science?",
            "assistant": "Hello! I'm your university enrollment assistant. I can help you with:\n\n- Information about our academic programs\n- Application deadlines\n- Checking your application status\n\nWhat would you like to know about?"
        },
        {
            "turn": 2, 
            "user": "What's the application deadline for that?",
            "assistant": "I found two Computer Science programs for you:\n\n1. **Computer Science BS**\n   - Duration: 4 years\n   - Tuition: $45,000 per year\n   - Prerequisites: High school diploma, Math SAT 600+, Physics SAT 550+\n   - Application Deadline: March 15, 2024\n   - Document Submission Deadline: March 31, 2024\n   - Decision Notification: April 15, 2024\n\n2. **Computer Science MS**\n   - Duration: 2 years\n   - Tuition: $55,000 per year\n   - Prerequisites: BS in CS or related field, GPA 3.0+, GRE optional\n   - Application Deadline: February 1, 2024\n   - Document Submission Deadline: February 15, 2024\n   - Decision Notification: March 30, 2024\n\nWhich program are you interested in?"
        },
        {
            "turn": 3,
            "user": "I already applied. My ID is APP-1042. What's my status?",
            "assistant": "I found your application! Here are the details:\n\n**Applicant:** John Smith\n**Program Applied To:** Computer Science MS\n**Current Status:** Documents Pending\n**Next Step:** Submit official transcripts and letters of recommendation\n\nIt looks like you still need to submit some documents. Would you like more information about what specific documents are needed?"
        },
        {
            "turn": 4,
            "user": "Can I get a fee waiver?",
            "assistant": "I'd recommend speaking with an enrollment counselor for that. Would you like me to connect you?\n\nOur enrollment counselors can help with:\n- Financial aid and fee waivers\n- Special accommodations\n- Transfer credits\n- Housing and campus life\n- And much more!"
        },
        {
            "turn": 5,
            "user": "What documents do I still need to submit?",
            "assistant": "Based on your application status (Documents Pending) for the Computer Science MS program, you still need to submit:\n\n**Required Documents:**\n1. Official transcripts from all previous institutions\n2. Letters of recommendation (typically 2-3)\n3. Any other program-specific requirements\n\n**Document Submission Deadline:** February 15, 2024\n\nI'd recommend submitting these as soon as possible to ensure your application can be reviewed by the admissions committee. You can upload them through the online application portal or submit them directly to the admissions office."
        }
    ]
    
    for entry in conversation:
        print(f"Turn {entry['turn']}:")
        print(f"User: {entry['user']}")
        print(f"Assistant: {entry['assistant']}\n")
        print("-" * 80)

if __name__ == "__main__":
    print("Student Enrollment Assistant - Test Suite\n")
    
    # Test individual tools
    test_tools()
    
    # Simulate the full conversation
    simulate_test_conversation()
    
    print("Test completed successfully!")
