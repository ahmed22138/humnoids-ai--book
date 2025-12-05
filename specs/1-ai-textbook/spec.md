# Feature Specification: Physical AI & Humanoid Robotics AI-Native Textbook

**Feature Branch**: `1-ai-textbook`
**Created**: 2025-12-06
**Status**: Draft

## Overview

Build a comprehensive, interactive AI-native textbook titled "Physical AI & Humanoid Robotics: Embodied Intelligence in the Real World" that bridges theoretical AI concepts with hands-on physical robotics. The project integrates a Docusaurus-based frontend with a FastAPI backend, RAG-powered chatbot, and advanced bonus features including personalization, multi-language support, and reusable AI agents.

---

## User Scenarios & Testing

### User Story 1 - Student Learns Robotics Fundamentals (Priority: P1)

A beginner student visits the textbook homepage, explores the curriculum structure, selects a foundational module (e.g., "Introduction to Embodied AI"), and progresses through weekly lessons with learning outcomes, assessments, and hardware requirements.

**Why this priority**: Core learning experience; essential for MVP. Without this, the textbook is non-functional.

**Independent Test**: Can be fully tested by navigating the homepage, viewing curriculum sections, and accessing a complete module with all learning materials, assessments, and outcomes defined.

**Acceptance Scenarios**:

1. **Given** the homepage is loaded, **When** the student views the curriculum, **Then** all 4 modules (Introduction, Perception, Control, Integration) are visible with descriptions
2. **Given** a student selects Module 1, **When** they view the module, **Then** all weekly chapters and learning outcomes are displayed
3. **Given** a student completes a lesson, **When** they access assessments, **Then** they can view questions with expected answers and hardware requirements

---

### User Story 2 - Student Authenticates and Gets Personalized Experience (Priority: P1)

A student signs up using Better-Auth with background questions (e.g., "Software experience: Beginner/Intermediate/Expert", "Hardware experience: Yes/No"), receives personalization settings, and can toggle content simplification based on their background.

**Why this priority**: P1 - Authentication gates access; personalization is a bonus requirement worth points. Both core to MVP.

**Independent Test**: Can be fully tested by completing signup flow, verifying profile questions are saved, and confirming personalization button adapts content complexity.

**Acceptance Scenarios**:

1. **Given** an unauthenticated student visits, **When** they click "Sign Up", **Then** a form appears with software/hardware background questions
2. **Given** a student completes signup, **When** they authenticate, **Then** their profile is stored and accessible
3. **Given** an authenticated student views a chapter, **When** they click "Personalize", **Then** content is simplified or expanded based on their background
4. **Given** a student with "Beginner" background, **When** they view a technical concept, **Then** simplified explanations are prioritized

---

### User Story 3 - Student Uses RAG Chatbot for Q&A (Priority: P1)

A student reads a chapter on robot kinematics, highlights or selects a specific text passage, clicks a query button, and the RAG chatbot answers questions about that specific content using semantic search against the textbook database.

**Why this priority**: P1 - RAG chatbot is a core technical requirement explicitly specified. Enables AI-native learning.

**Independent Test**: Can be fully tested by selecting text, querying the chatbot, and verifying answers are grounded in textbook content using Qdrant vector search.

**Acceptance Scenarios**:

1. **Given** a student reads a chapter, **When** they select text and query "Explain this", **Then** the chatbot returns an answer based on that passage
2. **Given** the chatbot receives a query, **When** it searches Qdrant vectors, **Then** it returns top 3 contextually relevant passages
3. **Given** the chatbot generates an answer, **When** it references content, **Then** it cites the specific chapter and section
4. **Given** a student asks an out-of-scope question, **When** the chatbot cannot find relevant content, **Then** it gracefully indicates the question is outside available materials

---

### User Story 4 - Student Translates Lesson to Urdu (Priority: P2)

A student reading Module 2 clicks a "Translate to Urdu" button on a specific chapter, and the content is translated on-demand using an API (e.g., OpenAI) and cached for future access.

**Why this priority**: P2 - Bonus feature; adds 10+ points. Enables accessibility for Urdu-speaking learners.

**Independent Test**: Can be fully tested by clicking translate button, verifying Urdu output is displayed, and confirming translations are cached.

**Acceptance Scenarios**:

1. **Given** a student views a chapter, **When** they click "Translate to Urdu", **Then** a translated version appears
2. **Given** translations are requested, **When** the system checks cache, **Then** cached translations are served without re-calling the API
3. **Given** a translation is generated, **When** the student switches back to English, **Then** English content is restored

---

### User Story 5 - Educator Uses Reusable AI Agents (Priority: P2)

An educator or developer uses pre-built Claude subagents (e.g., a ROS 2 code generator) embedded in the textbook to generate boilerplate code, documentation, or assessment questions. These agents are modular and reusable across chapters.

**Why this priority**: P2 - Bonus requirement (subagents/agent skills worth points). Demonstrates advanced AI integration; optional for MVP but high value.

**Independent Test**: Can be fully tested by invoking a subagent (e.g., generating ROS 2 code), verifying output quality, and confirming it's reusable across multiple chapters.

**Acceptance Scenarios**:

1. **Given** a student clicks "Generate ROS 2 Code" in a chapter, **When** the subagent is invoked, **Then** it returns working code matching the lesson context
2. **Given** a subagent is used in Module 1, **When** it's referenced in Module 3, **Then** the same agent logic applies with appropriate contextual modifications
3. **Given** a subagent generates content, **When** it's reviewed by an educator, **Then** quality meets pedagogical standards

---

### User Story 6 - Admin Deploys Textbook to Production (Priority: P1)

An administrator builds and deploys the Docusaurus site to GitHub Pages, ensuring the RAG backend (FastAPI) is available on a cloud service (e.g., Render, Railway), and the database (Neon PostgreSQL) and vector store (Qdrant) are provisioned and connected.

**Why this priority**: P1 - Deployment to GitHub Pages is explicit requirement. Without this, the feature is incomplete.

**Independent Test**: Can be fully tested by running the build, deploying to GitHub Pages, accessing the live site, and verifying chatbot backend connectivity.

**Acceptance Scenarios**:

1. **Given** code is merged to main, **When** deployment pipeline runs, **Then** Docusaurus builds without errors
2. **Given** the build succeeds, **When** the site is deployed to GitHub Pages, **Then** it's publicly accessible
3. **Given** the site is live, **When** a student uses the chatbot, **Then** the FastAPI backend responds with answers from Qdrant

---

### Edge Cases

- What happens if a student submits a query the RAG chatbot cannot answer from available content?
- How does the system handle concurrent translation requests for the same chapter?
- What occurs if the Qdrant vector store loses connection during a chatbot query?
- How does personalization adapt if a student profile is incomplete (missing background questions)?
- What is the fallback if the OpenAI translation API is unavailable?
- How are long-running subagent tasks (e.g., code generation) handled if they time out?

---

## Requirements

### Functional Requirements

#### Content & Curriculum

- **FR-001**: System MUST provide a homepage with project overview, learning goals, and explanations of why embodied AI matters
- **FR-002**: System MUST organize content into 4 core modules: (1) Introduction to Embodied AI, (2) Perception & Sensing, (3) Control & Actuation, (4) Multi-Robot Integration & Collaboration
- **FR-003**: System MUST break each module into weekly chapters with consistent structure: learning outcomes, main content, practical examples, assessments, hardware specifications
- **FR-004**: System MUST define clear hardware requirements across multiple deployment options: workstations (GPU-enabled developer machines), edge kits (e.g., NVIDIA Jetson), physical robot platforms (e.g., Boston Dynamics Spot, custom arm), cloud alternatives (e.g., simulation in Gazebo), and economy kits (budget robotics platforms)
- **FR-005**: System MUST include a capstone project that integrates concepts from all 4 modules with defined success criteria and hardware requirements

#### Frontend (Docusaurus)

- **FR-006**: System MUST use Docusaurus 3+ with MDX support for interactive content rendering
- **FR-007**: System MUST embed interactive components (React/MDX) in lessons for visualizations, simulations, or code playgrounds
- **FR-008**: System MUST provide a "Personalize" button on each chapter that adapts content complexity based on user background
- **FR-009**: System MUST provide a "Translate to Urdu" button on each chapter that triggers server-side translation
- **FR-010**: System MUST deploy the site to GitHub Pages with automatic builds on code push
- **FR-011**: System MUST include a chat interface component that allows selected text queries and displays chatbot responses

#### Authentication & Personalization

- **FR-012**: System MUST use Better-Auth for user signup/signin with support for email and optional OAuth providers
- **FR-013**: System MUST collect user background on signup: software experience level (Beginner/Intermediate/Expert) and hardware experience (Yes/No)
- **FR-014**: System MUST store user profiles in Neon PostgreSQL with schema supporting background preferences and personalization settings
- **FR-015**: System MUST adapt content rendering based on stored user profile (e.g., show simplified explanations for beginners)

#### RAG Chatbot & Knowledge Base

- **FR-016**: System MUST provide a FastAPI backend service exposing an endpoint for chatbot queries: `POST /chat` with payload `{ query: string, selected_text?: string, chapter?: string }`
- **FR-017**: System MUST embed chapter content into Qdrant vectors at deployment time for semantic search
- **FR-018**: System MUST support selected text queries (e.g., "explain this" applied to highlighted passage)
- **FR-019**: System MUST retrieve top-K contextually relevant passages from Qdrant for each query
- **FR-020**: System MUST use OpenAI Agents/ChatKit to generate answers grounded in retrieved content
- **FR-021**: System MUST cite source chapters and sections in chatbot responses
- **FR-022**: System MUST handle queries outside textbook scope gracefully (e.g., "I cannot find information about X in the available materials")

#### Data & Vector Store

- **FR-023**: System MUST use Neon PostgreSQL to store user profiles, authentication tokens, and application metadata
- **FR-024**: System MUST use Qdrant to store vector embeddings for all chapter content for semantic search
- **FR-025**: System MUST populate Qdrant with embeddings generated from chapter markdown on deployment
- **FR-026**: System MUST support efficient similarity searches returning results in <500ms

#### Translations

- **FR-027**: System MUST provide an endpoint for translating chapter content to Urdu: `POST /translate` with payload `{ chapter_id: string, language: string }`
- **FR-028**: System MUST use OpenAI API (or similar) for translation
- **FR-029**: System MUST cache translations in Neon PostgreSQL to avoid redundant API calls
- **FR-030**: System MUST support toggling between original and translated content on the frontend

#### Reusable AI Agents (Subagents)

- **FR-031**: System MUST provide modular Claude subagents for common tasks (e.g., ROS 2 code generation, assessment question generation)
- **FR-032**: System MUST make subagents callable from the frontend via a `/agent` endpoint: `POST /agent/invoke` with payload `{ agent_name: string, context: object }`
- **FR-033**: System MUST document subagent input/output contracts for reusability across chapters
- **FR-034**: System MUST log subagent invocations for analytics and debugging

#### Assessments & Learning Outcomes

- **FR-035**: System MUST include formative assessments (quizzes, reflection prompts) within each chapter
- **FR-036**: System MUST include summative assessments (module-end exams, capstone rubrics) after each module
- **FR-037**: System MUST define measurable learning outcomes (Bloom's taxonomy levels) for each chapter
- **FR-038**: System MUST provide answer keys and rubrics for educators

### Key Entities

- **User**: Authenticated learner with profile (software/hardware background, personalization preferences, progress tracking)
- **Module**: Course-level container (4 total) grouping related weekly chapters
- **Chapter**: Weekly lesson unit with learning outcomes, content, interactive components, assessments, hardware specs
- **Assessment**: Quiz, exam, or capstone with questions, expected answers, and rubrics
- **ChatMessage**: Stored interaction between student and RAG chatbot with query, context, response, and timestamp
- **TranslatedContent**: Cached translation of chapter content with source language, target language, and timestamp
- **HardwareRequirement**: Specification of hardware options (workstation, edge kit, robot platform, cloud, economy kit) with cost and availability
- **SubagentInvocation**: Log of AI agent calls with agent name, input, output, and performance metrics

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: Textbook covers all 4 core modules with at least 12 chapters total (3+ chapters per module) and 100+ pages of cumulative content
- **SC-002**: Students can authenticate, customize profile, and view personalized content within 2 minutes of first visit
- **SC-003**: RAG chatbot answers 90% of student queries with sources cited and responses grounded in textbook content (validated by educators)
- **SC-004**: Chatbot queries return answers in <2 seconds
- **SC-005**: Chapter translations to Urdu complete in <5 seconds on first request (cached subsequently)
- **SC-006**: Site loads on GitHub Pages with <3 second Time to First Byte
- **SC-007**: System supports 100+ concurrent users without degradation
- **SC-008**: At least 3 reusable subagents implemented (e.g., ROS 2 code generator, assessment generator, diagram generator) and documented
- **SC-009**: 95% of interactive MDX components render correctly across Chrome, Firefox, Safari
- **SC-010**: Capstone project is completable by students using provided hardware options and achieving defined success criteria
- **SC-011**: All content is original with zero plagiarism (validated by automated and manual checks)
- **SC-012**: Deployment pipeline runs in <10 minutes from code push to live site

---

## Assumptions

1. **OpenAI API Access**: Project assumes OpenAI API is available for ChatKit, translations, and subagent logic (cost to be budgeted)
2. **Qdrant Deployment**: Assumes Qdrant can be self-hosted or accessed via managed service (e.g., Qdrant Cloud)
3. **Neon PostgreSQL**: Assumes free/cheap tier of Neon PostgreSQL is sufficient for user profiles and caching
4. **GitHub Pages**: Assumes Docusaurus site can be built and deployed to GitHub Pages via CI/CD (GitHub Actions)
5. **Hardware Availability**: Assumes educators have access to at least one hardware option per module for content validation
6. **Content Source**: Assumes content is generated specifically for this project; no reliance on external textbooks
7. **Markdown Authoring**: Assumes all lesson content is authored in Markdown with optional MDX for interactive elements

---

## Out of Scope

- Integration with external LMS (e.g., Canvas, Blackboard) — can be added later
- Real-time collaboration features (e.g., shared code editing) — can be added later
- Mobile app native version — Docusaurus responsive design sufficient
- Video hosting and streaming — links to external providers acceptable
- Physical robot manufacturer SDKs detailed coverage — focus on generic ROS 2 patterns

---

## Architecture Decisions (Preview - See /sp.plan)

- **Frontend**: Docusaurus 3 + MDX for interactive content, deployed to GitHub Pages
- **Backend**: FastAPI + Uvicorn for REST API
- **AI Integration**: OpenAI API for ChatKit, translations, and subagents
- **Vector Store**: Qdrant (self-hosted or managed)
- **Database**: Neon PostgreSQL
- **Authentication**: Better-Auth with email/OAuth
- **Deployment**: GitHub Actions for CI/CD, Railway/Render for FastAPI backend
- **Content Format**: Markdown with MDX for interactive components

---

## Success Checklist

- [ ] Homepage created with overview, goals, "why embodied AI matters" section
- [ ] All 4 modules structured with 3+ chapters each
- [ ] Hardware requirements table populated for all 5 options (workstation, edge kit, robot, cloud, economy)
- [ ] Learning outcomes defined per chapter (Bloom's taxonomy levels)
- [ ] Assessments (formative & summative) authored for each module
- [ ] Capstone project spec complete with success criteria
- [ ] Docusaurus site builds without errors
- [ ] Better-Auth signup flow with background questions functional
- [ ] Personalize button logic implemented and tested
- [ ] RAG chatbot endpoint responds to queries with cited sources
- [ ] Qdrant vectors embedded for all chapters
- [ ] Translation API integrated and cached
- [ ] At least 3 subagents implemented and documented
- [ ] GitHub Pages deployment successful and live
- [ ] All interactive components tested across browsers
- [ ] Content originality verified (no plagiarism)
