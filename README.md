# Physical AI & Humanoid Robotics - Capstone Book

Welcome to the repository for the **Physical AI & Humanoid Robotics** technical book and capstone module specification. This project is built with Docusaurus and serves as a comprehensive guide for engineering students and professionals venturing into the world of humanoid robotics, physical AI, and robot learning.

---

## Project Overview

This repository contains the source code and content for a technical book designed to be a "Capstone Module" for advanced robotics curriculum. It bridges the gap between simulation and reality, covering the entire stack from ROS 2 fundamentals to Vision-Language-Action (VLA) models.

### Key Objectives
- **Curriculum Design**: Provide a rigorous, university-standard module specification.
- **Technical Guide**: Offer step-by-step tutorials on building a digital twin and "brain" for a humanoid robot.
- **Sim-to-Real**: Demonstrate the architecture for deploying trained policies from NVIDIA Isaac Lab to physical hardware.

---

## Features & Modules

The book is structured into four core modules culminating in a final capstone project:

### Core Curriculum

| Module | Title | Description |
|--------|-------|-------------|
| **Module 1** | The Robotic Nervous System | Mastery of ROS 2, nodes, topics, and real-time communication |
| **Module 2** | The Digital Twin | High-fidelity simulation using Gazebo, Unity, and URDF modeling |
| **Module 3** | The AI-Robot Brain | Perception pipelines and reinforcement learning with NVIDIA Isaac |
| **Module 4** | Vision-Language-Action (VLA) | Integrating LLMs for cognitive planning and natural language instruction |

### Capstone Project
Students build a fully simulated humanoid robot capable of:
- Receiving spoken instructions
- Generating action plans via LLMs
- Navigating complex environments (Nav2)
- Manipulating objects

---

## Interactive AI Features

### RAG Chatbot (Retrieval-Augmented Generation)
Built with **FastAPI**, **Google Gemini**, **Neon Serverless Postgres**, and **Qdrant Cloud**, this chatbot understands the book's full context.

| Feature | Description |
|---------|-------------|
| **Context-Aware Q&A** | Ask questions about any module or concept in the book |
| **Ask AI Button** | Select any text in the book to instantly query the AI for explanations |
| **Source Attribution** | Answers are grounded in the book's content, reducing hallucinations |

### User Authentication & Personalization
A comprehensive authentication system with personalized learning features:

| Feature | Description |
|---------|-------------|
| **Sign Up / Sign In** | Secure JWT-based authentication with email/password |
| **User Profiles** | Manage account information and preferences |
| **Background Questionnaire** | Capture user's software skills, hardware skills, and experience level |
| **Content Personalization** | AI-powered content adaptation based on user's background |
| **Urdu Translation** | Real-time translation of chapter content to Urdu with RTL support |
| **Transformation Logging** | Track all personalization and translation activities |

#### Background Questionnaire Options
- **Software/Programming Skills**: None, Beginner, Intermediate, Advanced
- **Hardware/Robotics Skills**: None, Beginner, Intermediate, Advanced
- **Experience Level**: Student, Professional, Hobbyist, Researcher

---

## Tech Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| Docusaurus v3 | Documentation framework |
| TypeScript | Type-safe development |
| React | Component-based UI |
| MDX | Rich content with JSX support |
| Mermaid.js | Diagrams and flowcharts |
| KaTeX | Mathematical equations |

### Backend
| Technology | Purpose |
|------------|---------|
| FastAPI | High-performance Python API |
| Neon Serverless Postgres | User data and authentication storage |
| Qdrant Cloud | Vector database for RAG |
| Google Gemini | LLM for personalization and translation |
| JWT | Secure token-based authentication |

### Development
| Tool | Purpose |
|------|---------|
| Spec-Driven Development (SDD) | Development methodology |
| Claude Code Agent Skills | Reusable AI intelligence |

---

## Project Structure

```
q4-book-hackathon/
├── .claude/skills/          # Reusable Agent Skills
│   ├── frontend-dev/        # Frontend specialist skill
│   ├── backend-dev/         # Backend architect skill
│   └── code-tester/         # QA engineer skill
├── backend/
│   ├── src/api/             # API route handlers
│   ├── src/core/            # Core configurations
│   ├── src/middleware/      # Auth & rate limiting
│   ├── src/models/          # Database models
│   ├── src/services/        # Business logic
│   └── migrations/          # Database migrations
├── website/
│   ├── docs/                # Book content (MDX files)
│   └── src/components/      # React components
└── specs/                   # Feature specifications
```

---

## Getting Started

### Prerequisites
- Node.js (version 20.0 or above)
- npm
- Python 3.11+ (for backend)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/harisawan27/q4-book-hackathon.git
   cd q4-book-hackathon
   ```

2. **Set up the frontend:**
   ```bash
   cd website
   npm install
   ```

3. **Set up the backend:**
   ```bash
   cd backend
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # Unix: source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   ```

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
NEON_DATABASE_URL=postgresql+asyncpg://user:password@host/dbname
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-key
GEMINI_API_KEY=your-gemini-api-key
BETTER_AUTH_SECRET=your-random-secret-key-min-32-chars
```

### Running Locally

**Start the backend:**
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

**Start the frontend:**
```bash
cd website
npm start
```

The site opens at `http://localhost:3000`.

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/signup` | Create new account |
| POST | `/api/v1/auth/signin` | Sign in to account |
| POST | `/api/v1/auth/signout` | Sign out |
| GET | `/api/v1/auth/session` | Get current session |

### Profile
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/profile` | Get user profile |
| PUT | `/api/v1/profile/background` | Update user background |

### Content Transformation
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/content/personalize` | Personalize chapter content |
| POST | `/api/v1/content/translate` | Translate to Urdu |

---

## Project Configuration

### Local Skills Installation

This project uses custom **Agent Skills** located in the `.claude/skills` directory.
To enable "Reusable Intelligence" for grading, please run these commands in the CLI:

```bash
/add-dir ./.claude/skills/frontend-dev
/add-dir ./.claude/skills/backend-dev
/add-dir ./.claude/skills/code-tester
```

### Available Skills

| Skill | Description | Focus Areas |
|-------|-------------|-------------|
| **frontend-dev** | Senior Frontend Specialist | UI/UX, Tailwind, React, Accessibility, Mobile Responsiveness |
| **backend-dev** | Senior Backend Architect | API Design, Database, Security, N+1 Query Prevention |
| **code-tester** | Ruthless QA Engineer | Edge cases, Unit tests, Bug hunting |

### Skill Rules

**Frontend Dev:** Never modify backend logic. Prefer Tailwind utility classes.

**Backend Dev:** Never touch UI components. Always use environment variables for secrets.

**Code Tester:** Do NOT fix code, only expose flaws. Be critical.

---

## Contributing

This project uses a **Spec-Driven Development** workflow:

1. **Specs First**: All major changes start with a specification in the `specs/` directory.
2. **AI-Assisted**: We use an AI agent to generate content and code based on these specs.
3. **Manual Review**: All AI-generated content is reviewed for academic rigor.

### Branching Strategy
| Branch | Purpose |
|--------|---------|
| `main` | Production-ready code |
| `002-docusaurus-book` | Main development branch |
| `003-rag-chatbot` | RAG chatbot feature |
| `005-auth-personalization-translation` | Authentication & personalization |

---

## License

This project is open-source.
Copyright 2025 Physical AI & Humanoid Robotics.

---

*Built for the Q4 Book Hackathon by Haris Awan.*
