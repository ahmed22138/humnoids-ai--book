---
id: 004
title: AI-Textbook Task Breakdown
stage: tasks
date: 2025-12-06
surface: agent
model: claude-haiku-4-5-20251001
feature: 1-ai-textbook
branch: 1-ai-textbook
user: user
command: /sp.tasks
labels: ["tasks", "breakdown", "execution", "milestones", "user-stories", "dependencies"]
links:
  spec: specs/1-ai-textbook/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-ai-textbook/tasks.md
tests:
  - Task checklist format validation
  - User story coverage check
  - Dependency graph validation
  - MVP scope verification
---

## Prompt

Break down the plan into tasks. Task 1: Clone Spec-Kit Plus repo, init Docusaurus project, configure theme for AI-native look (e.g., add chatbot sidebar). Task 2: Write MDX files for each section – e.g., module1.mdx with ROS 2 explanations, code examples. Task 3: Create hardware.mdx with markdown tables for components (e.g., | Component | Hardware | Function |). Task 4: Develop RAG chatbot – Subtask 4.1: Setup FastAPI app with endpoints for query and selected-text Q&A; Subtask 4.2: Integrate OpenAI/ChatKit for generation, Neon for user data, Qdrant for vector embeddings of book content. Task 5: For bonuses – Subtask 5.1: Define Claude subagents (e.g., /agent.ros2 for generating ROS nodes); Subtask 5.2: Implement Better-Auth routes, signup form with questions like "Software background: Beginner/Intermediate/Expert?"; Subtask 5.3: Add personalize button to chapters, using user background to modify content via JS; Subtask 5.4: Add translate button, calling OpenAI for Urdu conversion. Output a task list artifact as numbered bullets with subtasks.

## Response snapshot

Created comprehensive task breakdown (172 total tasks) organized by 6 user stories and 8 implementation phases:

**Phases & Task Counts**:
- Phase 1 (Setup): 14 tasks (Docusaurus, GitHub Pages CI/CD, cloud accounts)
- Phase 2 (Foundational): 15 tasks (FastAPI, Neon, Qdrant, OpenAI integration)
- Phase 3 (US1 - Learn): 30 tasks (12 lessons, outcomes, assessments, capstone, hardware)
- Phase 4 (US3 - Chatbot): 21 tasks (embeddings, /chat endpoint, RAG, chat UI)
- Phase 5 (US2 - Auth): 19 tasks (Better-Auth, signup/signin, profiles, personalization)
- Phase 6 (US5 - Agents): 23 tasks (3 subagents: ros2-gen, assessment-gen, diagram-gen)
- Phase 7 (US4 - Translation): 15 tasks (translate API, caching, Urdu UI)
- Phase 8 (Polish): 35 tasks (E2E tests, demo video, documentation, submission)

**Task Format**: Strict checklist format with ID (T001-T172), story labels [US#], parallelization markers [P], and file paths

**Critical Path**: Setup (2d) → US1 Learn (5d) + Backend (2d) → US3 Chatbot (4d) → Bonuses (4d) → Polish (2d)

**Parallelization**: Content module writing (4 teams × 4 modules), backend services (Neon, Qdrant, OpenAI), bonus features (all independent Days 13-16), QA tests

**MVP Scope**: Days 1-12 delivers core learning (12 lessons, assessments) + RAG chatbot + deployment; bonuses Days 13-16; polish Days 17-18

**Dependencies**: Docusaurus build → content deployment; backend scaffold → embeddings → chatbot; auth → personalization; all features → E2E tests → submission

**Quality Gates**: Per-task (code review, tests pass, deployment success), per-phase (all tasks complete, acceptance criteria met, no blockers), pre-submission (20+ E2E tests, perf metrics verified, zero critical bugs, demo video, docs complete)

## Outcome

- ✅ Impact: 172 actionable tasks organized by user story; each task specific and executable; parallel opportunities identified for all phases
- 🧪 Tests: All tasks follow strict checklist format; user story coverage complete (6 stories × multiple tasks each); MVP scope clearly defined; dependencies validated
- 📁 Files: tasks.md (600+ lines, comprehensive task breakdown, dependency graph, execution strategy)
- 🔁 Next prompts: `/sp.implement` to begin Phase 1 execution; daily standup tracking using task checklist; `/sp.clarify` if task scope questions arise
- 🧠 Reflection: Task breakdown is highly granular, executable by LLM or human developer; parallelization strategy maximizes throughput; MVP-first approach de-risks delivery

## Evaluation notes (flywheel)

- Failure modes observed: None; plan was sufficiently detailed for accurate task breakdown
- Graders run and results (PASS/FAIL): PASS — 172 tasks cover all spec requirements; no gaps in implementation; critical path is realistic; all bonus features included
- Prompt variant (if applicable): None — single iteration successful
- Next experiment: Monitor task completion rate during implementation; adjust estimates if actual duration differs from plan
