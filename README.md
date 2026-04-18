# Student Enrollment Assistant Agent

A conversational AI agent for a university's admissions office that helps prospective students get answers about programs, deadlines, and application status.

## Features

- **Three Core Tools**: The agent uses specialized tools to answer questions about:
  - Academic programs (duration, tuition, prerequisites)
  - Application deadlines (application, document submission, decision dates)
  - Application status checking (applicant ID lookup)

- **Multi-turn Conversation**: Maintains context within a session to provide coherent responses

- **Graceful Escalation**: When questions fall outside of available tools, agent recommends speaking with an enrollment counselor

- **Mock Data System**: Uses hardcoded mock data for 4 programs and 3 applicants

## Project Structure

```
Student Agent/
├── student_agent.py      # Main agent implementation
├── test_agent.py         # Test script for tools and conversation
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── README.md            # This file
├── Dockerfile           # Docker configuration
└── docker-compose.yml   # Docker Compose setup
```

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/Sahilcoder4/Student_agent.git
cd "Student Agent"
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Run Agent

#### Interactive Mode (Default):
```bash
python student_agent.py
```

#### Test 5-Turn Conversation:
```bash
python -c "
from student_agent import run_test_conversation
run_test_conversation()
"
```

#### Test Individual Tools:
```bash
python test_agent.py
```

## Agent Tools

### 1. get_program_info(program_name: str)

Returns information about academic programs including:
- Program name
- Duration
- Tuition
- Prerequisites

**Available Programs:**
- Computer Science BS
- Computer Science MS  
- Data Science BS
- Cybersecurity MS

### 2. check_application_status(applicant_id: str)

Returns application status including:
- Applicant name
- Program applied to
- Current status
- Next steps

**Sample Applicant IDs:**
- APP-1042 (John Smith - Computer Science MS)
- APP-1001 (Emily Johnson - Computer Science BS)
- APP-1002 (Michael Davis - Data Science BS)

### 3. get_deadlines(program_name: str)

Returns deadline information including:
- Application deadline
- Document submission deadline
- Decision notification date

## Test Conversation Results

The agent successfully handles the required 5-turn conversation:

**Turn 1:** "Hi, what programs do you offer in computer science?"
- Responds with Computer Science MS program details

**Turn 2:** "What's the application deadline for that?"  
- Provides deadlines for Computer Science MS program

**Turn 3:** "I already applied. My ID is APP-1042. What's my status?"
- Returns application status for John Smith

**Turn 4:** "Can I get a fee waiver?"
- Escalates to enrollment counselor appropriately

**Turn 5:** "What documents do I still need to submit?"
- Provides document requirements based on application status

## Docker Setup

### Using Docker Compose (Recommended)

1. **Build and run with Docker Compose:**
```bash
docker-compose up --build
```

2. **Run in interactive mode:**
```bash
docker-compose run --rm student-agent python student_agent.py
```

### Using Docker Directly

1. **Build Docker image:**
```bash
docker build -t student-agent .
```

2. **Run container:**
```bash
docker run --rm -it student-agent python student_agent.py
```

3. **Run with environment variables:**
```bash
docker run --rm -it \
  -e OPENAI_API_KEY=your_api_key_here \
  student-agent python student_agent.py
```

## Technical Implementation

### Architecture

The agent uses a **rule-based approach** with tool integration:

1. **Message Classification**: Analyzes user input to determine intent
2. **Tool Selection**: Chooses appropriate tool based on keywords
3. **Context Management**: Maintains conversation state for multi-turn dialogues
4. **Response Generation**: Formats tool outputs into natural language responses

### Key Components

- **SimpleAgent Class**: Core agent logic with message processing
- **Tool Functions**: Three main tools for program info, status checking, and deadlines
- **Mock Data**: Hardcoded datasets for programs, applicants, and deadlines
- **Pattern Matching**: Regular expressions for extracting IDs and program names

### Dependencies

- `langchain`: Core framework for building LLM applications
- `langchain-openai`: OpenAI integration
- `langchain-core`: Core components and tools
- `python-dotenv`: Environment variable management
- `typing-extensions`: Type hints support

## Assignment Requirements Compliance

**Three Tools Implemented**: get_program_info, check_application_status, get_deadlines  
**Mock Data**: 4 programs and 3 applicants with realistic data  
**Agent Loop**: Multi-turn conversation with context memory  
**Graceful Escalation**: Handles unsupported questions appropriately  
**Test Conversation**: 5-turn conversation demonstrated and logged  
**Documentation**: Complete setup and usage instructions  
**Docker Support**: Full containerization with Docker and Docker Compose  

## Future Enhancements

- Integration with real university databases
- Support for more complex conversation flows
- Web interface for easier interaction
- Integration with calendar systems for deadline reminders
- Multi-language support

## License

This project is created for educational purposes as part of an assignment.
