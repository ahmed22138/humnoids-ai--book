# Tasks: Physical AI & Humanoid Robotics AI-Native Textbook

**Feature Branch**: `1-ai-textbook`
**Created**: 2025-12-06
**Status**: Ready for Implementation
**Total Tasks**: 78 (organized by 6 user stories + setup/polish phases)

---

## Task Organization & Dependencies

### User Story Execution Order (Priority)

```
US1: Student Learns Fundamentals (P1)
     ├─ Requires: Setup (M1), Content (M2), Hardware (M3)
     ├─ Deliverable: 12 lessons, 60+ pages, assessments, capstone
     ├─ Independent Test: "Navigate curriculum, view all 4 modules and complete assessments"
     └─ Timeline: Days 1-8

US2: Student Authenticates & Personalizes (P1)
     ├─ Depends On: US1 (must have frontend first)
     ├─ Deliverable: Better-Auth signup, profile storage, personalization button
     ├─ Independent Test: "Signup with background questions, toggle content complexity"
     └─ Timeline: Day 14 + integrated into Days 9-12

US3: Student Uses RAG Chatbot (P1)
     ├─ Depends On: US1 (content must exist to embed)
     ├─ Deliverable: FastAPI backend, Qdrant vectors, chat component
     ├─ Independent Test: "Query chatbot, get answer with sources, <2s response"
     └─ Timeline: Days 9-12

US4: Student Translates to Urdu (P2)
     ├─ Depends On: US1 (content must exist)
     ├─ Deliverable: OpenAI translation API, caching, UI button
     ├─ Independent Test: "Click translate, view Urdu, toggle back to English"
     └─ Timeline: Day 16

US5: Educator Uses Subagents (P2)
     ├─ Depends On: US3 (FastAPI backend needed)
     ├─ Deliverable: 3+ reusable Claude agents, endpoints, documentation
     ├─ Independent Test: "Invoke /agent/ros2-code-gen, receive code with expected patterns"
     └─ Timeline: Day 13

US6: Admin Deploys to Production (P1)
     ├─ Depends On: US1, US2, US3, US4, US5 (all features complete)
     ├─ Deliverable: GitHub Pages + FastAPI backend live and connected
     ├─ Independent Test: "Live site accessible, chatbot responds, translations work"
     └─ Timeline: Days 1-2 (initial), Day 18 (final verification)
```

### Parallel Execution Opportunities

**Days 1-2 (Setup Phase - Sequential)**:
- Setup Docusaurus (blocking for all frontend work)

**Days 3-7 (Content - Parallel by Module)**:
- T010, T012, T014, T016 can run in parallel (different modules)
- T011, T013, T015, T017 can run in parallel (assessments)

**Days 9-12 (Backend - Parallel by Component)**:
- T033 (Neon setup), T034 (Qdrant setup), T035 (FastAPI scaffold) can run in parallel
- T036 (embeddings), T037 (/chat endpoint), T038 (text selection) can run after scaffold

**Days 13-16 (Bonus - Fully Parallel)**:
- T054 (Subagents), T055 (Auth), T056 (Personalize), T057 (Translate) can all run independently

---

## Phase 1: Setup & Infrastructure (Days 1-2)

### Goal
Initialize Docusaurus project, configure GitHub Pages deployment, set up CI/CD pipeline, and establish cloud service accounts.

### Independent Test Criteria
- ✅ Docusaurus site builds without errors
- ✅ GitHub Actions workflow deployed and auto-deploys on push
- ✅ Site accessible at `https://[org].github.io/[repo]/` after first push
- ✅ All cloud service accounts (Neon, Qdrant, OpenAI, Railway) configured and tested

### Tasks

- [ ] T001 Clone Spec-Kit Plus repo template to New-hackathon/textbook-repo
- [ ] T002 Initialize Node.js project: `npm init -y`, install dependencies (docusaurus, react, webpack)
- [ ] T003 [P] Create Docusaurus 3 project structure: `docs/`, `static/`, `sidebars.js`, `docusaurus.config.js`
- [ ] T004 [P] Configure docusaurus.config.js: theme colors (AI-native palette: dark blue, cyan accents), markdown processing, MDX support
- [ ] T005 [P] Setup GitHub Pages deployment config: enable Pages in repo settings, configure `gh-pages` branch
- [ ] T006 [P] Create GitHub Actions workflow `.github/workflows/deploy.yml` for auto-deploy on push
- [ ] T007 Create Neon PostgreSQL account: create project, get connection string, store in `.env.example`
- [ ] T008 [P] Setup Qdrant: create account (managed) or setup self-hosted Docker instance
- [ ] T009 [P] Create OpenAI API account: setup organization, create API keys, store in `.env`
- [ ] T010 [P] Setup Railway/Render account: create project, configure deployment settings
- [ ] T011 [P] Create `.env.example` template with all required variables (DATABASE_URL, QDRANT_URL, OPENAI_API_KEY, etc.)
- [ ] T012 Create `README.md` with project overview, setup instructions, tech stack summary
- [ ] T013 Test local build: `npm run build`, verify no errors, check output directory
- [ ] T014 Deploy to GitHub Pages: push to main, verify workflow runs, check live URL

### Deliverables
- Docusaurus project deployed and live
- CI/CD pipeline operational
- All cloud service accounts provisioned
- Environment configuration templates

---

## Phase 2: Foundational Infrastructure (Days 1-8, Parallel with Content)

### Goal
Setup backend project scaffold, database schema, API framework, and deployment infrastructure.

### Independent Test Criteria
- ✅ FastAPI server starts on `localhost:8000` with `/health` endpoint responding
- ✅ Neon PostgreSQL connection established, all tables created
- ✅ Qdrant instance running and responding to health checks
- ✅ All endpoints can be called without errors (may return empty data)

### Tasks

- [ ] T015 Create FastAPI project: `mkdir backend`, `python -m venv venv`, `pip install fastapi uvicorn sqlalchemy psycopg qdrant-client openai`
- [ ] T016 Initialize backend structure: `backend/main.py`, `backend/models/`, `backend/services/`, `backend/routes/`, `backend/config.py`
- [ ] T017 [P] Setup Neon PostgreSQL connection pool: `backend/config.py` with connection string, async engine configuration
- [ ] T018 [P] Create `backend/database.py`: SQLAlchemy models for User, Profile, ChatMessage, Translation, SubagentInvocation
- [ ] T019 [P] Run database migrations: execute DDL from data-model.md, create indexes, verify schema
- [ ] T020 [P] Setup Qdrant client: `backend/qdrant_client.py` with initialization, collection creation, health check
- [ ] T021 Setup OpenAI client: `backend/openai_client.py` with API key configuration, ChatKit model setup
- [ ] T022 [P] Create FastAPI app scaffold: `backend/main.py` with CORS, middleware, error handlers, health endpoint
- [ ] T023 [P] Implement `/health` endpoint: returns status of all services (database, Qdrant, OpenAI)
- [ ] T024 Create docker-compose.yml (optional): for local development with Qdrant, PostgreSQL containers
- [ ] T025 [P] Setup environment validation: `.env` loading, required variables check, early failure if missing
- [ ] T026 Create `backend/logging.py`: structured logging configuration (info, error levels)
- [ ] T027 Create `.gitignore` and `.env.example`: exclude sensitive files, provide templates
- [ ] T028 Create `backend/requirements.txt` with all dependencies pinned
- [ ] T029 Test backend startup: `uvicorn backend.main:app --reload`, verify no errors, endpoints accessible

### Deliverables
- FastAPI backend scaffold with all services initialized
- Database schema created with indexes
- Cloud service connections tested
- Backend deployment ready for feature development

---

## Phase 3: User Story 1 - Student Learns Robotics Fundamentals (US1)

### Goal
Create complete curriculum with 12 lessons, learning outcomes, assessments, and hardware requirements.

### Independent Test Criteria
- ✅ All 4 modules visible on homepage with descriptions
- ✅ All 12 chapters accessible with lesson content
- ✅ Learning outcomes defined for each chapter (Bloom's taxonomy levels)
- ✅ At least 5 formative assessments per module (30+ total)
- ✅ 4 summative assessments (one per module)
- ✅ Capstone project specification complete with grading rubric
- ✅ Hardware requirements table displays all 5 options with comparison
- ✅ Site builds and deploys without errors

### Tasks

#### Content Creation (Days 3-7)

**Module 1: Introduction to Embodied AI (Weeks 1-3)**

- [ ] T030 [US1] Create `docs/01-introduction/week-1-embodied-ai-fundamentals.mdx`: 5-7 pages covering definition, history, key concepts
- [ ] T031 [US1] Create `docs/01-introduction/week-2-robot-anatomy.mdx`: 5-7 pages on robot structure, actuators, sensors
- [ ] T032 [US1] Create `docs/01-introduction/week-3-control-systems.mdx`: 5-7 pages on control loops, feedback, basic algorithms
- [ ] T033 [P] [US1] Create `docs/01-introduction/learning-outcomes.md`: Define Bloom's levels for weeks 1-3 (Remember → Create)
- [ ] T034 [P] [US1] Create `docs/01-introduction/formative-assessments.md`: 5+ quizzes/prompts for weeks 1-3 with answer keys
- [ ] T035 [US1] Create `docs/01-introduction/summative-assessment.md`: Module-end exam (15-20 questions), rubric

**Module 2: Perception & Sensing (Weeks 4-6)**

- [ ] T036 [P] [US1] Create `docs/02-perception/week-4-vision-fundamentals.mdx`: 5-7 pages on computer vision, image processing
- [ ] T037 [P] [US1] Create `docs/02-perception/week-5-lidar-sensing.mdx`: 5-7 pages on lidar, depth sensing, 3D reconstruction
- [ ] T038 [P] [US1] Create `docs/02-perception/week-6-sensor-fusion.mdx`: 5-7 pages on combining multiple sensors, data fusion
- [ ] T039 [P] [US1] Create `docs/02-perception/learning-outcomes.md`: Define Bloom's levels for weeks 4-6
- [ ] T040 [P] [US1] Create `docs/02-perception/formative-assessments.md`: 5+ quizzes for weeks 4-6
- [ ] T041 [P] [US1] Create `docs/02-perception/summative-assessment.md`: Module-end exam, rubric

**Module 3: Control & Actuation (Weeks 7-9)**

- [ ] T042 [P] [US1] Create `docs/03-control/week-7-kinematics.mdx`: 5-7 pages on forward/inverse kinematics
- [ ] T043 [P] [US1] Create `docs/03-control/week-8-motion-planning.mdx`: 5-7 pages on path planning, trajectory generation
- [ ] T044 [P] [US1] Create `docs/03-control/week-9-real-time-control.mdx`: 5-7 pages on real-time systems, control loops
- [ ] T045 [P] [US1] Create `docs/03-control/learning-outcomes.md`: Define Bloom's levels for weeks 7-9
- [ ] T046 [P] [US1] Create `docs/03-control/formative-assessments.md`: 5+ quizzes for weeks 7-9
- [ ] T047 [P] [US1] Create `docs/03-control/summative-assessment.md`: Module-end exam, rubric

**Module 4: Multi-Robot Integration (Weeks 10-12)**

- [ ] T048 [P] [US1] Create `docs/04-integration/week-10-multi-robot.mdx`: 5-7 pages on multi-robot systems, coordination
- [ ] T049 [P] [US1] Create `docs/04-integration/week-11-human-robot-collab.mdx`: 5-7 pages on safety, collaboration, human factors
- [ ] T050 [P] [US1] Create `docs/04-integration/week-12-deployment.mdx`: 5-7 pages on deployment, scaling, production considerations
- [ ] T051 [P] [US1] Create `docs/04-integration/learning-outcomes.md`: Define Bloom's levels for weeks 10-12
- [ ] T052 [P] [US1] Create `docs/04-integration/formative-assessments.md`: 5+ quizzes for weeks 10-12
- [ ] T053 [P] [US1] Create `docs/04-integration/summative-assessment.md`: Module-end exam, rubric

**Capstone & Hardware**

- [ ] T054 [US1] Create `docs/capstone-project.mdx`: Capstone project spec (30-40 pages), success criteria, grading rubric, hardware options per stage
- [ ] T055 [US1] Create `docs/hardware-requirements.mdx`: Markdown table with 5 hardware options (Workstation, Edge Kit, Robot, Cloud, Economy), specs, cost, setup guides
- [ ] T056 [US1] Create `docs/glossary.md`: Robotics/AI terminology with definitions
- [ ] T057 [US1] Update `sidebars.js`: Add all 12 lessons, capstone, hardware, glossary to navigation

#### Homepage & Branding

- [ ] T058 [US1] Create `docs/index.mdx`: Homepage with hero section, project overview, goals, "why embodied AI matters" (3-4 pages)
- [ ] T059 [US1] Configure `docusaurus.config.js`: site title, description, branding colors, logo path
- [ ] T060 [P] [US1] Add AI-native visual elements: Docusaurus theme customization for chatbot-ready sidebar, dark mode default

#### Deployment & Validation

- [ ] T061 [US1] Test Docusaurus build: `npm run build`, verify all .mdx files parse correctly, no missing images/assets
- [ ] T062 [US1] Deploy to GitHub Pages: push content, verify all 12 lessons accessible at live URL
- [ ] T063 [US1] Validate site structure: Navigate all modules, verify cross-links work, check loading times <3s

### Deliverables
- 12 complete lessons (~60+ pages of content)
- Learning outcomes for all chapters
- 30+ formative assessments with keys
- 4 summative module assessments
- Capstone project specification
- Hardware requirements table
- Homepage with project overview
- Live site on GitHub Pages

---

## Phase 4: User Story 3 - Student Uses RAG Chatbot (US3)

### Goal
Build RAG backend, embed content in Qdrant, implement chatbot endpoints, and integrate chat UI in Docusaurus.

### Independent Test Criteria
- ✅ `/chat` endpoint returns answers with sources in <2 seconds
- ✅ Selected text queries work (context-aware answers)
- ✅ Qdrant contains embeddings for all 12 chapters
- ✅ Chat component embedded in Docusaurus, functional on all chapters
- ✅ Chatbot gracefully handles out-of-scope queries

### Tasks

#### Backend: Data Preparation & Embedding

- [ ] T064 [US3] Extract chapter content to JSON: `backend/data/chapters.json` with all lesson text split by sections
- [ ] T065 [US3] Create `backend/scripts/embed_chapters.py`: Generate embeddings for all chapters using OpenAI API, store in Qdrant
- [ ] T066 [US3] Create `backend/qdrant/collection.py`: Initialize Qdrant collection with schema, index settings for semantic search
- [ ] T067 [US3] Populate Qdrant: Run embedding script, verify all chapters loaded (expected: 300-500 vectors per chapter)
- [ ] T068 [US3] Test Qdrant search: Query sample questions, verify top-3 results are relevant

#### Backend: API Endpoints

- [ ] T069 [US3] Create `backend/routes/chat.py`: Implement `POST /chat` endpoint with request validation, rate limiting, error handling
- [ ] T070 [US3] Implement RAG retrieval logic: `backend/services/rag.py` with Qdrant search, top-K retrieval, source extraction
- [ ] T071 [US3] Integrate OpenAI ChatKit: `backend/services/chatkit.py` with prompt engineering, response generation, token management
- [ ] T072 [US3] Implement selected text context: Modify `/chat` to incorporate `selected_text` parameter into retrieval and generation
- [ ] T073 [US3] Add response caching: Cache identical queries for 1 hour using Redis or in-memory cache to reduce OpenAI costs
- [ ] T074 [US3] Create `POST /chat/{id}/feedback` endpoint: Store user feedback (helpful/not_helpful) in PostgreSQL for ML improvement
- [ ] T075 [US3] Test all endpoints: Use curl/Postman to verify `/chat`, `/health`, feedback endpoint

#### Frontend: Chat Component Integration

- [ ] T076 [US3] Create React chat component: `src/components/ChatBot.tsx` with message display, text input, message history
- [ ] T077 [US3] Implement text selection handler: JS code to capture highlighted text, trigger chat queries with context
- [ ] T078 [US3] Create Docusaurus MDX component: `src/components/ChatPanel.mdx` embeddable in lesson chapters
- [ ] T079 [US3] Integrate chat component into chapters: Add `<ChatPanel />` to 3+ key lessons (weeks 1, 7, 10)
- [ ] T080 [US3] Implement message history: Store chat history in localStorage, allow user to review past questions
- [ ] T081 [US3] Test chat in browser: Type query, verify response appears, check sources are cited, measure response time

#### Deployment & Validation

- [ ] T082 [US3] Deploy FastAPI backend: Push code to Railway/Render, set environment variables, verify `/health` responds
- [ ] T083 [US3] Test backend connectivity: From Docusaurus, call `/chat` endpoint, verify CORS works
- [ ] T084 [US3] Verify chatbot performance: Run query response time test, confirm <2s latency for 90% of queries

### Deliverables
- Qdrant collection populated with embeddings for all chapters
- `/chat` endpoint fully functional with source citations
- Selected text query capability
- Chat component integrated in Docusaurus
- Feedback mechanism for continuous improvement
- Backend deployed to production

---

## Phase 5: User Story 2 - Student Authenticates & Personalizes (US2)

### Goal
Implement Better-Auth authentication, user profiles with background questions, and content personalization.

### Independent Test Criteria
- ✅ User signup form captures background questions (software_exp, hardware_exp)
- ✅ Profiles persisted in Neon PostgreSQL
- ✅ Signin returns JWT token, token used for authenticated requests
- ✅ Personalize button toggles content complexity (Beginner → simplified, Expert → advanced)
- ✅ Personalization preference persists across sessions

### Tasks

#### Backend: Authentication

- [ ] T085 [P] [US2] Setup Better-Auth: `backend/auth/better_auth_setup.py` with Neon PostgreSQL provider configuration
- [ ] T086 [P] [US2] Create `backend/routes/auth.py`: Implement `POST /auth/signup`, `POST /auth/signin`, `POST /auth/refresh`, `POST /auth/logout`
- [ ] T087 [US2] Add JWT token generation: `backend/services/jwt_service.py` with token creation, verification, refresh logic
- [ ] T088 [P] [US2] Create user profile model: Extend User entity with profile fields (background questions, preferences)
- [ ] T089 [P] [US2] Implement profile endpoints: `POST /user/profile`, `GET /user/profile`, `PUT /user/profile/personalization`
- [ ] T090 [US2] Add authentication middleware: `backend/middleware/auth.py` to validate JWT tokens on protected endpoints
- [ ] T091 [US2] Setup password hashing: Use bcrypt/Argon2 for secure password storage, verify during signin

#### Frontend: Authentication UI

- [ ] T092 [US2] Create signup form component: `src/components/SignupForm.tsx` with email, password, name, background question dropdowns
- [ ] T093 [US2] Add signin form component: `src/components/SigninForm.tsx` with email/password fields, JWT token storage
- [ ] T094 [US2] Implement session management: Store JWT in localStorage/sessionStorage, auto-refresh token, logout on expiration
- [ ] T095 [US2] Create user dashboard: `src/pages/profile.tsx` showing user info, background, personalization settings
- [ ] T096 [US2] Add navbar authentication UI: Show signin/signup buttons when unauthenticated, show user profile when authenticated

#### Personalization Logic

- [ ] T097 [P] [US2] Annotate lesson content with complexity levels: Tag sections in all .mdx files with metadata (complexity: Beginner/Intermediate/Expert)
- [ ] T098 [P] [US2] Create personalization service: `backend/services/personalization.py` with logic to filter content by user background level
- [ ] T099 [US2] Implement "Personalize" button component: `src/components/PersonalizeButton.tsx` to toggle content complexity
- [ ] T100 [US2] Add client-side filtering: JavaScript logic to show/hide content sections based on user's personalization_level
- [ ] T101 [US2] Persist personalization preference: Save to user profile, apply on page load

#### Integration & Testing

- [ ] T102 [US2] Test full auth flow: Signup → Signin → Authenticated request → Personalize button → Complexity toggle
- [ ] T103 [US2] Verify token security: Check JWT can't be tampered with, token refresh works, logout clears session

### Deliverables
- Better-Auth fully integrated
- User signup with background questions
- User profile storage and management
- JWT-based session management
- Content personalization by complexity level
- Personalization button functional on all chapters

---

## Phase 6: User Story 5 - Educator Uses Subagents (US5)

### Goal
Implement 3+ reusable Claude AI subagents for code generation, assessments, and diagrams.

### Independent Test Criteria
- ✅ `/agent/invoke` endpoint accepts agent_name and context parameters
- ✅ 3 agents implemented: ros2-code-gen, assessment-gen, diagram-gen
- ✅ Each agent returns expected output (working code, questions, diagrams)
- ✅ Agents can be called from multiple chapters with appropriate context modifications
- ✅ Agent invocations logged for analytics

### Tasks

#### Backend: Agent Infrastructure

- [ ] T104 [US5] Create agent registry: `backend/agents/registry.py` mapping agent names to implementations
- [ ] T105 [US5] Create `backend/routes/agent.py`: Implement `POST /agent/invoke` endpoint with agent dispatch
- [ ] T106 [US5] Setup agent logging: `backend/services/agent_logger.py` to track invocations (name, input, output, cost)
- [ ] T107 [US5] Create agent context system: `backend/agents/context.py` for passing chapter/lesson context to agents

#### Subagent 1: ROS 2 Code Generator

- [ ] T108 [P] [US5] Create `backend/agents/ros2_code_gen.py`: Agent that generates ROS 2 boilerplate Python/C++ code
- [ ] T109 [P] [US5] Implement code generation prompt: Context includes lesson topic, required components, code style preferences
- [ ] T110 [P] [US5] Define input schema: `{lesson, task, language (python/cpp), complexity_level}`
- [ ] T111 [P] [US5] Test agent: Generate code for "motion-planning" task, verify output has expected ROS patterns (nodes, subscribers, publishers)

#### Subagent 2: Assessment Generator

- [ ] T112 [P] [US5] Create `backend/agents/assessment_gen.py`: Agent that generates quiz/exam questions
- [ ] T113 [P] [US5] Implement assessment prompt: Context includes chapter content, Bloom's level, question count
- [ ] T114 [P] [US5] Define input schema: `{chapter, level (remember/understand/apply/analyze), count (5-20)}`
- [ ] T115 [P] [US5] Test agent: Generate 5 "apply" level questions for kinematics chapter, verify difficulty and answer keys

#### Subagent 3: Diagram Generator

- [ ] T116 [P] [US5] Create `backend/agents/diagram_gen.py`: Agent that generates ASCII/Mermaid diagrams
- [ ] T117 [P] [US5] Implement diagram prompt: Context includes concept to visualize, diagram style preference
- [ ] T118 [P] [US5] Define input schema: `{concept, style (mermaid/ascii/svg)}`
- [ ] T119 [P] [US5] Test agent: Generate diagram for "forward-kinematics", verify it's valid Mermaid syntax

#### Frontend: Agent Integration

- [ ] T120 [US5] Create agent invocation component: `src/components/AgentButton.tsx` with button to invoke agent
- [ ] T121 [US5] Implement agent response display: Show generated content (code, questions, diagrams) in modal or side panel
- [ ] T122 [US5] Integrate into chapters: Add agent buttons to relevant lessons (ROS code in week 9, assessments throughout, diagrams in weeks 1-4)
- [ ] T123 [US5] Add copy-to-clipboard functionality: Allow users to copy generated code/questions to clipboard

#### Testing & Documentation

- [ ] T124 [US5] Test all 3 agents: Invoke each with various contexts, verify output quality
- [ ] T125 [US5] Document agent contracts: `docs/agents/README.md` explaining agent APIs, input schemas, expected outputs
- [ ] T126 [US5] Create agent usage examples: Show how to call each agent from lessons, code examples

### Deliverables
- 3 reusable subagents fully operational
- `/agent/invoke` endpoint with agent registry
- Agent logging and analytics
- Agent buttons integrated in Docusaurus chapters
- Agent invocation documentation

---

## Phase 7: User Story 4 - Student Translates to Urdu (US4)

### Goal
Implement on-demand Urdu translation with caching and language toggle UI.

### Independent Test Criteria
- ✅ `/translate` endpoint accepts chapter_id and language parameters
- ✅ First translation takes <5 seconds (API call)
- ✅ Cached translations serve instantly (<100ms)
- ✅ "Translate to Urdu" button visible on all chapters
- ✅ Language toggle switches between English and Urdu seamlessly

### Tasks

#### Backend: Translation Service

- [ ] T127 [P] [US4] Create `backend/services/translation.py`: Wrapper around OpenAI translation API
- [ ] T128 [P] [US4] Create `backend/routes/translate.py`: Implement `POST /translate` endpoint with caching logic
- [ ] T129 [P] [US4] Implement translation cache: Check PostgreSQL `translations` table before calling API
- [ ] T130 [P] [US4] Setup cache invalidation: Add `expires_at` column, periodic cleanup of expired translations
- [ ] T131 [US4] Add supported language constants: Define list of supported languages (Urdu, Spanish, French, etc.)
- [ ] T132 [US4] Test translation endpoint: Call `/translate?chapter_id=week-1&language=ur`, verify response includes markdown content
- [ ] T133 [US4] Batch translate all chapters (optional background job): Pre-populate cache for faster first-user experience

#### Frontend: Translation UI

- [ ] T134 [P] [US4] Create language selector component: `src/components/LanguageSelector.tsx` with dropdown or buttons
- [ ] T135 [P] [US4] Add "Translate to Urdu" button: `src/components/TranslateButton.tsx` callable from each chapter
- [ ] T136 [US4] Implement translation state management: Store selected language in state/context, apply to all content
- [ ] T137 [US4] Create translation display logic: Fetch translated content from backend, render alongside/replace original
- [ ] T138 [US4] Add language persistence: Save user's language preference to localStorage/user profile
- [ ] T139 [US4] Test translation UI: Click translate button, verify Urdu content appears, toggle back to English works

#### Performance & Optimization

- [ ] T140 [US4] Optimize translation API calls: Batch chapters to reduce API calls, implement request debouncing
- [ ] T141 [US4] Monitor translation latency: Log and track API response times, alert if >5 seconds
- [ ] T142 [US4] Setup cost tracking: Monitor OpenAI API usage for translations, log cost per chapter

### Deliverables
- Translation API endpoint fully functional with caching
- All chapter translations cached in PostgreSQL
- "Translate to Urdu" button on all chapters
- Language toggle UI with persistence
- <5 second initial translation latency

---

## Phase 8: Polish & Cross-Cutting Concerns (Day 17-18)

### Goal
End-to-end testing, performance optimization, demo video, documentation, and submission preparation.

### Independent Test Criteria
- ✅ 20+ E2E tests passing (authentication, navigation, chatbot, translation, agents)
- ✅ Site <3s TTFB, chatbot <2s response, translation <5s first-call latency
- ✅ 95% cross-browser compatibility (Chrome, Firefox, Safari)
- ✅ Demo video (5-10 min) covers all features
- ✅ Zero critical bugs, all P1 issues resolved

### Tasks

#### E2E Testing & QA

- [ ] T143 [P] Setup E2E testing framework: Install Playwright/Cypress, configure for Docusaurus + FastAPI
- [ ] T144 [P] Create test scenarios: Homepage load, navigate all modules, read lesson, use chat, translate, personalize, signup/signin
- [ ] T145 [P] Test authentication flow: Signup → Signin → Profile → Personalize → Logout
- [ ] T146 [P] Test chatbot flow: Query → Get answer → Feedback → Verify response time
- [ ] T147 [P] Test translation flow: Select chapter → Click translate → Verify Urdu → Toggle back
- [ ] T148 [P] Test agent flow: Click agent button → Get code → Copy to clipboard → Verify format
- [ ] T149 Test cross-browser compatibility: Run tests on Chrome, Firefox, Safari, check for CSS/JS issues
- [ ] T150 Test performance: Measure TTFB, chatbot latency, translation latency, verify <3s, <2s, <5s
- [ ] T151 Test accessibility: Check WCAG compliance, keyboard navigation, screen reader compatibility
- [ ] T152 Fix critical bugs: Address any P1/P2 issues found during testing

#### Documentation & Guides

- [ ] T153 [P] Update README.md: Add comprehensive setup instructions, tech stack, architecture overview, deployment guide
- [ ] T154 [P] Create ARCHITECTURE.md: Design decisions, data model overview, API contract summary, deployment architecture
- [ ] T155 [P] Create DEPLOYMENT.md: Step-by-step guide for deploying frontend (GitHub Pages) and backend (Railway/Render)
- [ ] T156 [P] Create CONTRIBUTING.md: Developer setup, running locally, testing workflow, PR process
- [ ] T157 Create GLOSSARY.md: Robotics/AI terminology used throughout textbook
- [ ] T158 Create TROUBLESHOOTING.md: Common issues (API rate limits, Qdrant connection, auth failures) and solutions

#### Demo & Presentation

- [ ] T159 Create demo script: 10-minute walkthrough of features (narrative, specific actions to show)
- [ ] T160 Record demo video: Screen capture showing homepage → lessons → chatbot → translation → personalization → agents
- [ ] T161 Create presentation deck (optional): 5-10 slides on project, architecture, results, learnings
- [ ] T162 Test demo flow: Run demo video and verify all features work as expected

#### Submission Preparation

- [ ] T163 [P] Create submission package: Zip repo with all code, commit history, documentation
- [ ] T164 [P] Verify GitHub Pages live URL: Confirm site is publicly accessible and all features work
- [ ] T165 [P] Verify FastAPI backend: Confirm backend is live on Railway/Render and responding
- [ ] T166 [P] Test complete flow one more time: Signup → Learn → Ask chatbot → Translate → Use agent → Personalize
- [ ] T167 Create submission document: Include repo link, live site URL, demo video link, project summary, design decisions
- [ ] T168 Final code review: Check for TODO comments, incomplete features, merge conflicts
- [ ] T169 Merge to main and tag release: `git merge 1-ai-textbook -> main`, create version tag `v1.0.0`

#### Performance Optimization

- [ ] T170 [P] Optimize Docusaurus build: Minify CSS/JS, optimize images, analyze bundle size
- [ ] T171 [P] Optimize FastAPI startup: Lazy load heavy dependencies, pre-cache embeddings at startup
- [ ] T172 [P] Optimize Qdrant queries: Add vector index tuning, batch similar queries, monitor query latency
- [ ] T173 Optimize OpenAI API usage: Implement token counting, warn on high-cost operations, batch requests where possible

#### Monitoring & Analytics

- [ ] T174 [P] Setup logging: Structured logging for all endpoints, errors, user actions
- [ ] T175 [P] Setup monitoring dashboard (optional): Monitor uptime, latency, error rates, costs
- [ ] T176 [P] Setup error alerts: Configure alerts for critical failures (database down, Qdrant down, high error rate)
- [ ] T177 Setup usage analytics: Track user signups, session duration, feature usage (chatbot queries, translations, agents)

### Deliverables
- 20+ E2E tests, all passing
- Performance metrics verified (<3s TTFB, <2s chatbot, <5s translation)
- Demo video (5-10 min)
- Comprehensive documentation (README, ARCHITECTURE, DEPLOYMENT, CONTRIBUTING)
- Zero critical bugs
- Live site and backend fully functional
- Submission package ready

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product - Days 1-12)

**Core deliverables for MVP**:
1. Docusaurus site with 12 lessons, assessments, capstone (US1)
2. RAG chatbot backend with embeddings and chat UI (US3)
3. GitHub Pages + Railway deployment (US6)

**Why this MVP**:
- Delivers core learning experience (main hackathon requirement)
- Demonstrates AI-native approach (RAG chatbot)
- Fully deployed and accessible (scores points for delivery)
- Foundation for bonus features

**MVP Testing**: Student can read lesson, ask chatbot question about content, get sourced answer

### Phase-Based Incremental Delivery

**Days 1-8**: US1 (Learn) + Backend foundation
- All 12 lessons live and accessible
- Assessments and capstone complete
- Site deployed to GitHub Pages
- Backend scaffold ready

**Days 9-12**: US3 (Chatbot)
- RAG backend fully operational
- Embeddings for all chapters
- Chat component integrated
- <2s response time

**Days 13-16**: Bonus features (US2, US4, US5)
- Better-Auth signup/signin (Day 14)
- Personalization button (Day 15)
- Subagents for code generation (Day 13)
- Urdu translation (Day 16)

**Days 17-18**: Polish & submission
- E2E testing, bug fixes
- Demo video recorded
- Documentation complete
- Live deployment verified

### Parallelization Opportunities

**Content creation (Days 3-7)**: All 4 modules and their chapters can be written in parallel
- T030-T032 (M1 lessons), T036-T038 (M2), T042-T044 (M3), T048-T050 (M4) → parallel
- T033-T035 (M1 assessments), T039-T041 (M2), T045-T047 (M3), T051-T053 (M4) → parallel

**Backend setup (Days 1-2, 9-12)**: Multiple services can be configured concurrently
- T017-T020 (Neon, Qdrant, OpenAI setup) → parallel
- T033-T035 (FastAPI scaffold, Qdrant, Neon connection) → parallel

**Bonus features (Days 13-16)**: Completely independent
- T054-T055 (Subagents), T085-T103 (Auth), T127-T141 (Translation), T104-T125 (Agents) → all parallel

**QA & Testing (Day 17)**: E2E tests can run in parallel
- Different test scenarios (auth, navigation, chatbot, translation, agents) → parallel

---

## Task Dependencies & Execution Order

### Critical Path (Blocking Sequence)

```
T001-T014 (Setup) → T030 (Start content) + T015 (Start backend)
         ↓
    T030-T055 (Content US1)
         ↓
    T064-T084 (Chatbot US3)
         ↓
    T085-T103 (Auth US2) + T104-T126 (Agents US5) + T127-T141 (Translation US4)
         ↓
    T143-T177 (Testing & Submission)
```

### Parallel Tracks (Can Run Simultaneously)

**Track 1 (Content)**: T030-T063 (write and deploy lessons)
**Track 2 (Backend Infrastructure)**: T015-T029 (setup FastAPI, DB, services)
**Track 3 (Bonus Features)**: T085-T141 (auth, agents, translation) — after Track 2 completes

---

## Task Estimation Summary

| Phase | Task Count | Owner | Duration | Dependencies |
|-------|-----------|-------|----------|-------------|
| Setup | 14 | Dev/Ops | 2 days | None |
| Foundational | 15 | Backend/DevOps | 2 days | Setup complete |
| US1 (Learn) | 30 | Content/Dev | 5 days | Setup complete |
| US3 (Chatbot) | 21 | Backend | 4 days | US1, Foundational complete |
| US2 (Auth) | 19 | Backend/Frontend | 1 day | Foundational complete |
| US5 (Agents) | 23 | Backend | 1 day | US3 complete |
| US4 (Translation) | 15 | Backend/Frontend | 1 day | US1 complete |
| Polish | 35 | QA/Dev/Content | 2 days | All features complete |
| **TOTAL** | **172** | **Mixed** | **18 days** | **Sequential phases** |

---

## Quality Gates & Acceptance Criteria

### Per-Task Acceptance

- [ ] Code compiles/runs without errors
- [ ] Unit tests pass (if applicable)
- [ ] Code reviewed by team lead
- [ ] Deployment successful (no downtime)
- [ ] End-user facing features tested manually

### Per-Phase Acceptance

- [ ] All tasks in phase completed
- [ ] Independent test criteria met
- [ ] No unresolved blockers or critical issues
- [ ] Documentation updated
- [ ] Code merged to main branch

### Pre-Submission Checklist

- [ ] All 172 tasks completed and merged
- [ ] 20+ E2E tests passing
- [ ] Performance metrics verified
- [ ] Demo video recorded and links included
- [ ] README, ARCHITECTURE, DEPLOYMENT docs complete
- [ ] No critical bugs (P1/P2)
- [ ] Live site and backend accessible
- [ ] All bonus features implemented

---

**Next Steps**: Begin Phase 1 (Setup) with T001-T014. Estimated completion: Day 2 EOD

