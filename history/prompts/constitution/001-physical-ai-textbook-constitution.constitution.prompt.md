---
id: 001
title: Physical AI Textbook Constitution
stage: constitution
date: 2025-12-06
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: master
user: user
command: /sp.constitution
labels: ["constitution", "physical-ai", "robotics", "textbook", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - Constitution placeholder replacement validation
  - Principle completeness check
  - Technical requirements alignment
---

## Prompt

You are an AI assistant building an AI-native textbook for Physical AI & Humanoid Robotics using Spec-Kit Plus and Claude Code. Follow these constitutional principles: 1. The book must cover all course modules, weekly breakdown, learning outcomes, assessments, and hardware requirements as detailed in the hackathon description. 2. Prioritize embodied intelligence, bridging digital AI with physical robots. 3. Use Docusaurus for the site structure, ensuring it's interactive and deployable to GitHub Pages. 4. Integrate a RAG chatbot using OpenAI Agents/ChatKit, FastAPI, Neon Postgres, and Qdrant for content-based Q&A, including selected text queries. 5. Aim for base 100 points plus all bonuses: reusable subagents/agent skills, Better-Auth signup/signin with background questions, per-chapter personalization button, per-chapter Urdu translation button. 6. Content must be educational, accurate, and AI-native (e.g., interactive elements). 7. No plagiarism; generate original explanations. Generate a constitution artifact outlining these rules in markdown.

## Response snapshot

Created comprehensive constitution for Physical AI & Humanoid Robotics AI-Native Textbook with:
- 6 core principles aligned to hackathon requirements (Embodied Intelligence, Comprehensive Coverage, AI-Native Design, Original Content, Full-Stack Bonus Architecture, RAG Chatbot)
- Technical Architecture Requirements section specifying Docusaurus, FastAPI, Neon PostgreSQL, Qdrant, Better-Auth, and internationalization
- Content Standards ensuring educational accuracy, accessibility, modularity, assessments, and hardware mapping
- Development Workflow with Spec-Driven Development, iterative delivery, testing, and documentation requirements
- Governance section establishing constitution supremacy and amendment procedures
- Version 1.0.0 ratified 2025-12-06

## Outcome

- ✅ Impact: Constitution created as authoritative governance document; all 7 user requirements encoded as principles or technical requirements; template fully populated with zero placeholder tokens remaining
- 🧪 Tests: All constitutional principles are testable and measurable (e.g., "no purely abstract material", "all modules fully developed", "each bonus feature fully implemented")
- 📁 Files: .specify/memory/constitution.md (overwritten with 53 lines of content); history/prompts/constitution/001-*.constitution.prompt.md (PHR created)
- 🔁 Next prompts: /sp.specify for detailed feature specification; /sp.plan for architecture design; /sp.tasks for development breakdown
- 🧠 Reflection: Constitution serves as single source of truth for development; principles are declarative and free of vague language; technical choices anchored to constitutional rationale

## Evaluation notes (flywheel)

- Failure modes observed: None; template replacement was straightforward with clear user requirements
- Graders run and results (PASS/FAIL): PASS - All placeholder tokens replaced; no dangling brackets; dates in ISO format; version follows semver
- Prompt variant (if applicable): None
- Next experiment: Monitor constitution adherence during spec/plan/tasks phases; adjust principles if unforeseen conflicts arise
