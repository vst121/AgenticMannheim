# Agentic Mannheim

## 1. Architecture Overview

Agentic Mannheim follows an **AI-Native, simulation-first architecture** built around a shared Digital Twin of Mannheim Innenstadt.

The system consists of two applications:

- **Frontend:** Next.js
- **Backend:** FastAPI

The frontend owns presentation, interaction, and visualization.

The backend owns the Digital Twin, simulation, events, agents, decisions, policies, and authoritative application state.

The architecture contains two complementary system areas:

```text
                         AGENTIC MANNHEIM
                                │
                ┌───────────────┴───────────────┐
                │                               │
         Traffic Control              Citizen Participation
                │                               │
       Deterministic Flow                 Agentic Flow
                │                               │
                └───────────────┬───────────────┘
                                │
                         Event-Driven Core
                                │
                         Digital Twin
                                │
                           Simulation
                                │
                             Policy
                                │
                           City State
```

The fundamental architectural principle is:

> **The application owns state. AI provides intelligence, not application control.**

The high-level flows are:

### Traffic Control

```text
Scenario
    ↓
Digital Twin
    ↓
City Event
    ↓
Deterministic Decision
    ↓
Policy
    ↓
Simulation
    ↓
Updated City State
```

### Citizen Participation

```text
Citizen Request
    ↓
Citizen Participation Agent
    ↓
Understand
    ↓
Investigate
    ↓
Inspect Digital Twin
    ↓
Correlate City Information
    ↓
Propose Interventions
    ↓
Jev Judgment
    ↓
Policy
    ↓
Simulation
    ↓
Evaluate Outcomes
    ↓
Citizen Feedback
```

The Digital Twin and simulation are therefore the shared foundation for both deterministic and agentic behavior.

---

## 2. Architectural Principles

### 2.1 Application Owns State

The Digital Twin and simulation own authoritative city state.

Agents, LLMs, Jev, and other AI components are not authoritative state owners.

AI may propose changes, but only application-controlled components can validate and apply them.

### 2.2 AI Provides Intelligence

AI is used where interpretation, contextual reasoning, synthesis, or judgment provides meaningful value.

Examples include:

- Understanding citizen requests
- Interpreting natural language
- Investigating city context
- Correlating related reports and events
- Generating intervention proposals
- Providing bounded judgments
- Explaining outcomes to citizens

AI is not used merely to replace deterministic software.

### 2.3 Deterministic and Agentic Decisions Coexist

Agentic decisions are an additional decision capability, not a replacement for deterministic logic.

```text
                    Decision Request
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
         Deterministic           Agentic
           Decision              Decision
                │                     │
                └──────────┬──────────┘
                           ▼
                       Policy
                           │
                           ▼
                       Simulation
```

Deterministic decisions provide:

- Reliable baseline behavior
- Reproducibility
- Fallback behavior
- Reference behavior for evaluation

Agentic decisions provide:

- Contextual reasoning
- Natural-language understanding
- Flexible investigation
- Alternative intervention proposals

The architecture allows both approaches to be evaluated against the same Digital Twin state.

### 2.4 AI Proposes. Policy Validates. Simulation Executes.

Every AI-originated action follows an explicit control boundary:

```text
Agent
  ↓
Decision / Proposal
  ↓
Policy
  ↓
Approved Action
  ↓
Simulation
  ↓
Updated State
```

AI never directly mutates authoritative state.

### 2.5 Bounded Agency

Agents operate within explicit:

- Capabilities
- Tools
- Actions
- Permissions
- Policies
- Context
- Resource limits

An agent cannot perform arbitrary operations.

### 2.6 Judgment Is Not Decision Quality

AI or Jev confidence does not represent actual decision quality.

The system should distinguish:

```text
Agent Observation
       ↓
Agent Decision
       ↓
Jev Judgment
       ↓
Policy Decision
       ↓
Action
       ↓
Simulation Outcome
       ↓
Decision Quality
```

Decision quality can only be evaluated meaningfully against observed outcomes.

### 2.7 Observable by Design

Important decisions and state transitions must be traceable.

```text
Event
  ↓
Observation
  ↓
Decision
  ↓
Jev Judgment
  ↓
Policy
  ↓
Action
  ↓
State Change
  ↓
Outcome
```

The system should preserve sufficient information to understand not only **what happened**, but also **why it happened**.

### 2.8 Separate Presentation from Domain

The frontend and backend are independently structured applications.

The frontend does not own domain, policy, or simulation logic.

The backend does not depend on frontend implementation details.

### 2.9 Modular Backend, Not Premature Microservices

The backend is internally modular but remains a single application for the MVP.

Responsibilities are separated through modules and explicit boundaries without introducing distributed infrastructure that does not yet provide architectural value.

---

## 3. System Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                            │
│                         Next.js                             │
│                                                             │
│  Map │ Traffic Control │ Citizen Participation │ Events    │
│  Agentic State │ Scenario UI │ Citizen Feedback             │
└─────────────────────────────┬───────────────────────────────┘
                              │
                         HTTP / WebSocket
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                          BACKEND                            │
│                          FastAPI                            │
│                                                             │
│  API                                                        │
│   │                                                         │
│   ├── Digital Twin                                          │
│   ├── Simulation                                             │
│   ├── Events                                                 │
│   ├── Agents                                                 │
│   ├── Decision                                               │
│   ├── Policy                                                 │
│   └── Persistence                                            │
│                                                             │
└─────────────────────────────┬───────────────────────────────┘
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
       Digital Twin      Simulation         Events
             │                │                │
             └────────────────┼────────────────┘
                              │
                              ▼
                         City State
```

The backend is a modular monolith.

The Digital Twin and simulation are shared by both Traffic Control and Citizen Participation.

---

## 4. Frontend Architecture

The frontend is a standalone **Next.js application** responsible for presentation, interaction, and visualization.

Conceptually:

```text
frontend/
│
├── app/
├── components/
├── features/
├── hooks/
├── lib/
├── stores/
└── public/
```

### Responsibilities

The frontend is responsible for:

- Rendering the Mannheim map
- Visualizing the Digital Twin
- Displaying roads and intersections
- Displaying virtual vehicles
- Displaying emergency vehicles
- Displaying traffic signals
- Displaying incidents and citizen reports
- Providing Traffic Control interactions
- Providing Citizen Participation interactions
- Selecting geographic locations
- Displaying simulation state
- Displaying agent activity
- Displaying decisions and judgments
- Displaying the event timeline
- Displaying citizen feedback
- Communicating with the backend

The frontend must not implement authoritative simulation, policy, or decision rules.

---

## 5. Backend Architecture

The backend is a single modular FastAPI application.

Conceptually:

```text
backend/
│
└── src/
    │
    ├── api/
    │
    ├── domain/
    │
    ├── digital_twin/
    │
    ├── simulation/
    │
    ├── agents/
    │
    ├── decision/
    │
    ├── policy/
    │
    └── infrastructure/
        └── persistence/
```

The backend owns authoritative application state.

The major responsibilities are:

```text
API
 │
 ├── Domain
 ├── Digital Twin
 ├── Simulation
 ├── Events
 ├── Agents
 ├── Decision
 ├── Policy
 └── Persistence
```

---

## 6. API Layer

The API provides the contract between Next.js and FastAPI.

Responsibilities include:

- Query Digital Twin state
- Query simulation state
- Create scenarios
- Submit citizen requests
- Query citizen requests
- Query agent activity
- Query agent decisions
- Query Jev judgments
- Query events
- Request simulation evaluations
- Deliver simulation updates

The API should remain thin.

Domain behavior, simulation rules, agent orchestration, decision validation, and policy enforcement belong to backend modules.

---

## 7. Digital Twin Layer

The Digital Twin represents the structure and current state of the simulated city.

Core entities include:

```text
City
 ├── Road
 ├── Intersection
 ├── Traffic Signal
 ├── Vehicle
 ├── Emergency Vehicle
 ├── Incident
 ├── Citizen Request
 └── City Event
```

The Digital Twin represents:

> **What exists and what the current simulated city state is.**

The simulation determines:

> **What happens to that state over time.**

The Digital Twin is shared by both major project areas.

---

## 8. Simulation Layer

The simulation controls the evolution of the virtual environment.

Responsibilities include:

- Simulation clock
- Vehicle movement
- Traffic signals
- Emergency scenarios
- Incidents
- City events
- State transitions
- Scenario execution
- Intervention evaluation
- Reproducible simulation runs

The simulation is deterministic where reproducibility is required.

The simulation must remain independent of the frontend and independent of LLM availability.

This is particularly important for Traffic Control.

The city simulation must continue to operate even when no AI services are available.

---

## 9. Event-Driven Core

Events provide the connection between changes in the Digital Twin, simulation, agents, decisions, and outcomes.

Examples include:

```text
VEHICLE_ENTERED_ROAD
VEHICLE_REACHED_INTERSECTION
TRAFFIC_LIGHT_CHANGED
EMERGENCY_DETECTED
TRAFFIC_INCIDENT
AGENT_DECISION_PROPOSED
POLICY_REJECTED_ACTION
AGENT_RUN_FAILED
```

Future Citizen Participation events may include:

```text
CITIZEN_REQUEST_SUBMITTED
CITIZEN_REQUEST_CLASSIFIED
RELATED_INCIDENTS_FOUND
INTERVENTION_PROPOSED
JUDGMENT_PRODUCED
INTERVENTION_SIMULATED
OUTCOME_EVALUATED
CITIZEN_FEEDBACK_GENERATED
```

The event model provides correlation across the complete decision lifecycle.

```text
Event
  ↓
Observation
  ↓
Decision
  ↓
Policy
  ↓
Action
  ↓
State Change
  ↓
Outcome
```

---

## 10. Traffic Control Architecture

Traffic Control is intentionally deterministic.

Its purpose is to demonstrate that an Agentic City does not require an LLM for every city operation.

```text
Traffic Scenario
       ↓
Digital Twin
       ↓
Simulation
       ↓
City Event
       ↓
Deterministic Decision
       ↓
Policy
       ↓
Simulation Action
       ↓
Updated State
```

For example:

```text
Emergency Vehicle
       ↓
Reaches Intersection
       ↓
Emergency Agent
       ↓
Prioritize Emergency
       ↓
Policy
       ↓
Change Traffic Light
       ↓
Simulation
```

The current emergency scenario remains functional without an LLM.

The architecture therefore preserves a deterministic foundation for the Digital Twin.

---

## 11. Citizen Participation Architecture

Citizen Participation is the primary Agentic AI capability.

The purpose is to create a meaningful connection between citizens, city context, AI reasoning, simulation, and decision-making.

The high-level architecture is:

```text
Citizen
   ↓
Citizen Request
   ↓
Citizen Participation Agent
   ↓
Understand Request
   ↓
Investigate City Context
   ↓
Inspect Digital Twin
   ↓
Correlate Reports / Events
   ↓
Generate Intervention Options
   ↓
Jev Judgment
   ↓
Policy
   ↓
Simulation
   ↓
Evaluate Outcomes
   ↓
Citizen Feedback
```

The citizen does not directly command the Digital Twin.

The citizen provides a request or observation.

The agent interprets and investigates the request, then proposes bounded interventions.

---

## 12. Citizen Request Flow

The initial Citizen Participation scenario is a geographically located safety concern.

Example:

> "This intersection feels unsafe for pedestrians. Cars often turn too quickly here."

The flow is:

```text
Citizen selects location
        ↓
Citizen selects request type
        ↓
Citizen enters description
        ↓
Citizen Request created
        ↓
City Event generated
        ↓
Citizen Participation Agent triggered
        ↓
Agent investigates
```

The request should preserve:

- Geographic location
- Request type
- Natural-language description
- Timestamp
- Status
- Correlation identifier

The geographic location is essential because the agent must reason about a specific part of the Digital Twin.

---

## 13. Agent Layer

Agents observe relevant parts of the Digital Twin and perform bounded reasoning.

The general agent lifecycle is:

```text
Observe
   ↓
Interpret
   ↓
Investigate
   ↓
Reason
   ↓
Propose
   ↓
Evaluate
   ↓
Act through approved tools
   ↓
Observe Result
```

Agents do not directly mutate authoritative state.

Different agents can have different responsibilities.

Examples include:

```text
CitizenParticipationAgent
EmergencyAgent
IncidentAgent
MobilityAgent
```

The architecture should allow additional agents without changing the Digital Twin core.

---

## 14. LLM Integration

LLMs are used where natural-language understanding and contextual reasoning provide meaningful value.

Typical responsibilities include:

- Understanding citizen descriptions
- Classifying requests
- Extracting relevant information
- Formulating investigation questions
- Synthesizing information
- Generating intervention proposals
- Explaining decisions
- Generating citizen-facing feedback

LLMs are not authoritative decision-makers.

The application controls:

- Available tools
- Context
- State
- Actions
- Permissions
- Policies
- Execution

The LLM therefore operates inside an application-defined control loop.

```text
Application State
       ↓
Agent Context
       ↓
LLM Reasoning
       ↓
Structured Proposal
       ↓
Policy
       ↓
Application Action
```

---

## 15. Jev Judgment Layer

Jev provides bounded judgment inside the agentic decision process.

Jev should receive a focused question and structured context rather than unrestricted control of the application.

Conceptually:

```text
Agent Context
      ↓
Focused Question
      ↓
Jev
      ↓
Structured Judgment
      ↓
Agent Decision
```

Jev may be used for questions such as:

- Which intervention appears most appropriate?
- How strongly does the available evidence support an intervention?
- Should a proposed intervention proceed to simulation?
- Which option best addresses the reported citizen concern?

The result should remain a judgment rather than an executable command.

The architecture preserves:

- Judgment
- Probability
- Confidence
- Model/version
- Input context
- Decision relationship

Confidence is treated as a signal for routing, review, and evaluation, not as proof of correctness.

---

## 16. Decision Layer

The decision layer translates observations and agent reasoning into structured proposals.

The decision model separates:

```text
Observation
     ↓
Reasoning
     ↓
Judgment
     ↓
Decision
     ↓
Action
```

A decision may contain:

- Decision type
- Target entity
- Proposed action
- Reason
- Evidence
- Correlation ID
- Agent information
- Jev judgment where applicable

The decision layer does not directly modify the Digital Twin.

---

## 17. Intervention Model

Citizen Participation introduces the concept of an **intervention proposal**.

For example, a citizen reports an unsafe intersection.

The agent may propose:

```text
Intervention A
Increase pedestrian crossing time

Intervention B
Change traffic signal timing

Intervention C
Restrict a turning movement during peak periods
```

These are proposals, not immediate state changes.

Each intervention can be evaluated through the simulation.

```text
Citizen Request
      ↓
Intervention A ──┐
Intervention B ──┼──→ Simulation
Intervention C ──┘
                     ↓
               Outcome Metrics
                     ↓
                Comparison
```

This allows the Digital Twin to become an experimentation environment for agentic decisions.

---

## 18. Simulation-Based Evaluation

Agentic proposals should be evaluated against the Digital Twin rather than executed blindly.

The system can create simulation runs from the same initial state:

```text
Initial Digital Twin State
          │
     ┌────┼────┐
     │    │    │
     ▼    ▼    ▼
Baseline  A    B
          │    │
          ▼    ▼
      Simulation Runs
          │
          ▼
       Outcomes
          │
          ▼
     Compare Results
```

The baseline represents deterministic or current behavior.

Alternative runs represent proposed interventions.

This enables evaluation of:

- Traffic effects
- Waiting time
- Pedestrian conditions
- Signal behavior
- Vehicle movement
- Safety-related indicators
- Other domain-specific metrics

The same initial state should be used when comparing alternatives to preserve meaningful evaluation.

---

## 19. Policy Layer

The policy layer is the control boundary between decisions and execution.

```text
Decision
   ↓
Policy Evaluation
   ↓
Approved / Rejected
```

It verifies:

- Action validity
- Permissions
- Context
- Safety constraints
- Allowed state transitions
- Agent capabilities
- Current Digital Twin state

Only approved actions reach the simulation.

Policy rejection is a normal system outcome.

```text
Decision
   ↓
Policy
   ├── Approved → Simulation
   │
   └── Rejected → Event / Feedback
```

---

## 20. Agentic Decision Flow

The complete agentic decision loop is:

```text
1. Citizen submits request
          ↓
2. Request becomes a city event
          ↓
3. Citizen Participation Agent receives observation
          ↓
4. Agent understands the request
          ↓
5. Agent investigates relevant city context
          ↓
6. Agent inspects Digital Twin state
          ↓
7. Agent correlates reports and events
          ↓
8. Agent proposes interventions
          ↓
9. Jev provides bounded judgment
          ↓
10. Decision is structured
          ↓
11. Policy validates proposed action
          ↓
12. Approved intervention enters simulation
          ↓
13. Simulation evaluates outcome
          ↓
14. Outcome is recorded
          ↓
15. Agent evaluates result
          ↓
16. Citizen receives feedback
```

This creates a controlled agentic loop without giving the agent unrestricted control.

---

## 21. Simulation Loop

The simulation operates through discrete updates.

```text
Simulation Tick
      ↓
Update World State
      ↓
Move Vehicles
      ↓
Update Signals
      ↓
Detect Events
      ↓
Trigger Relevant Agents
      ↓
Process Decisions
      ↓
Validate Actions
      ↓
Apply Approved Actions
      ↓
Publish Updated State
```

The backend owns the simulation loop.

The frontend visualizes its current state.

Agentic investigation and reasoning may occur outside the deterministic simulation tick where appropriate.

This prevents LLM latency from becoming a dependency of the core simulation clock.

---

## 22. Geographic Data Architecture

The geographic foundation is based on real Mannheim data.

```text
OpenStreetMap
      ↓
Selected Mannheim Area
      ↓
Processed Geographic Data
      ↓
Digital Twin
```

The initial area is **Mannheim Innenstadt**.

The geographic layer provides:

- Roads
- Intersections
- Traffic signals
- Geographic coordinates
- Road geometry
- Other relevant physical context

Geographic data and simulation state remain separate.

```text
Geographic Data
      ≠
Simulation State
```

The frontend uses MapLibre GL JS to render the geographic environment and simulation overlays.

---

## 23. State Ownership

State ownership is explicitly defined.

| State                 | Owner                        |
| --------------------- | ---------------------------- |
| Geographic data       | Geographic data layer        |
| Digital Twin state    | Digital Twin                 |
| Simulation state      | Simulation                   |
| Citizen request state | Citizen Participation domain |
| Agent run state       | Agent layer                  |
| Agent observation     | Agent layer                  |
| Decision proposal     | Decision layer               |
| Jev judgment          | Judgment / Agent layer       |
| Policy result         | Policy layer                 |
| Simulation outcome    | Simulation / Evaluation      |
| UI state              | Next.js frontend             |

AI components must not become authoritative owners of application state.

---

## 24. Frontend / Backend Boundary

The architectural boundary is explicit:

```text
┌─────────────────────────────┐
│          Next.js            │
│                             │
│ Presentation               │
│ Visualization              │
│ Interaction                │
│ UI State                   │
│ Citizen Interaction        │
└──────────────┬──────────────┘
               │
          API Contract
               │
┌──────────────▼──────────────┐
│          FastAPI            │
│                             │
│ Domain                     │
│ Digital Twin               │
│ Simulation                 │
│ Events                     │
│ Agents                     │
│ Decisions                  │
│ Policy                     │
│ Persistence                │
│ Authoritative State        │
└─────────────────────────────┘
```

The frontend may request actions.

The backend determines whether those actions are valid and applies approved changes.

---

## 25. Communication

The initial communication model uses:

- **HTTP APIs** for commands and queries
- **WebSocket or equivalent streaming** for live simulation updates where required

Conceptually:

```text
Next.js
   │
   ├── GET  /api/city/state
   ├── GET  /api/roads/geojson
   ├── GET  /api/intersections/geojson
   ├── GET  /api/vehicles/geojson
   ├── POST /api/scenarios/emergency
   ├── POST /api/citizen-requests
   ├── GET  /api/citizen-requests
   └── WebSocket /api/simulation/stream
                         │
                         ▼
                      FastAPI
```

The communication protocol remains independent of internal backend modules.

---

## 26. Data Flow

The complete architecture contains two major flows sharing the same Digital Twin.

### Traffic Control

```text
Scenario
   ↓
Digital Twin
   ↓
Simulation
   ↓
Event
   ↓
Deterministic Agent / Decision
   ↓
Policy
   ↓
Action
   ↓
Simulation
   ↓
Updated State
```

### Citizen Participation

```text
Citizen
   ↓
Citizen Request
   ↓
City Event
   ↓
Citizen Participation Agent
   ↓
LLM Interpretation
   ↓
Digital Twin Investigation
   ↓
Related Events / Reports
   ↓
Intervention Proposals
   ↓
Jev Judgment
   ↓
Decision
   ↓
Policy
   ↓
Simulation
   ↓
Outcome
   ↓
Citizen Feedback
```

The two flows share:

```text
Digital Twin
Simulation
Events
Policy
Persistence
Observability
```

---

## 27. Failure and Safety Boundary

The system assumes that AI decisions can be incorrect.

Therefore:

```text
AI Decision
     ↓
Policy Validation
     ↓
Rejected
```

is a normal and supported path.

A decision may be rejected because it is:

- Invalid
- Unsupported
- Outside the agent's permissions
- Incompatible with the current state
- Unsafe
- Unable to pass policy validation

The simulation must not execute rejected actions.

The default behavior should be safe and deterministic.

AI service failure must not corrupt authoritative Digital Twin state.

The deterministic simulation foundation should remain operational independently of AI availability.

---

## 28. Observability and Evaluation

Agentic behavior requires more than traditional application logging.

The architecture should preserve the complete causal chain:

```text
Citizen Request
      ↓
Event
      ↓
Agent Run
      ↓
Observation
      ↓
LLM Reasoning
      ↓
Jev Judgment
      ↓
Decision
      ↓
Policy
      ↓
Action
      ↓
Simulation Run
      ↓
Outcome
      ↓
Citizen Feedback
```

Each important step should be correlated.

Relevant metadata includes:

- Correlation ID
- Agent type
- Agent run ID
- Model identifier
- Model version
- Prompt/context where appropriate
- Decision
- Judgment
- Probability
- Confidence
- Policy result
- Action
- Simulation run
- Outcome

This enables later evaluation of both system behavior and decision quality.

---

## 29. Extensibility

The architecture supports additional agents without changing the Digital Twin or simulation core.

For example:

```text
                         Digital Twin
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
   CitizenParticipation   Emergency       Mobility
        Agent              Agent            Agent
             │                │                │
             └────────────────┼────────────────┘
                              │
                         Decision Layer
                              │
                            Policy
                              │
                         Simulation
```

Future multi-agent experiments may introduce specialized agents for:

- Mobility
- Safety
- Accessibility
- Public transport
- Environmental conditions
- Urban planning
- Citizen engagement

The shared control model remains:

```text
Observe
   ↓
Reason
   ↓
Decide
   ↓
Validate
   ↓
Act
   ↓
Observe Result
```

---

## 30. Architecture Boundaries

The following boundaries are intentional:

```text
Geographic Data
      ≠
Simulation State

Simulation State
      ≠
Agent State

Agent Observation
      ≠
Agent Decision

Agent Decision
      ≠
Jev Judgment

Jev Judgment
      ≠
Executable Action

Executable Action
      ≠
Authoritative State

AI Decision
      ≠
Policy Decision

Policy Decision
      ≠
Simulation Outcome

Frontend
      ≠
Backend Domain

UI
      ≠
Simulation Logic
```

These boundaries are central to the architecture.

---

## 31. Technology Stack

### Frontend

- Next.js
- React
- TypeScript
- MapLibre GL JS
- Tailwind CSS
- Zustand where client-side state management is required

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic

### Simulation

- Python
- Deterministic simulation model

### Agent Layer

- Python
- Agent orchestration
- LLM integration
- Structured agent decisions

### Judgment

- Jev / TypeSafe AI

### Data

- OpenStreetMap
- GeoJSON
- PostgreSQL
- JSON

### Infrastructure

- Docker
- Docker Compose
- GitHub

The technology stack should remain replaceable where it does not affect architectural boundaries.

---

## 32. Deployment Model

The MVP uses two independently deployable applications:

```text
                    Internet / Browser
                           │
                    ┌──────┴──────┐
                    │             │
                    ▼             ▼
              Next.js App    FastAPI App
                                  │
                     ┌────────────┼────────────┐
                     │            │            │
                     ▼            ▼            ▼
                Digital Twin  Simulation    Agents
                     │            │            │
                     └────────────┼────────────┘
                                  │
                             Decision / Policy
                                  │
                                  ▼
                              PostgreSQL
```

The frontend and backend can evolve and deploy independently.

The backend remains a modular monolith for the MVP.

There is no requirement to introduce microservices until there is a clear architectural reason to do so.

---

## 33. Target Architecture

The target architecture combines deterministic city simulation with bounded agentic decision-making.

```text
                              USER
                               │
                               ▼
                    ┌────────────────────┐
                    │      Next.js       │
                    │      Frontend      │
                    └─────────┬──────────┘
                              │
                       API / WebSocket
                              │
                              ▼
                    ┌────────────────────┐
                    │      FastAPI       │
                    │      Backend       │
                    └─────────┬──────────┘
                              │
              ┌───────────────┼────────────────┐
              │               │                │
              ▼               ▼                ▼
        Digital Twin      Simulation         Events
              │               │                │
              └───────────────┼────────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
         Traffic Control           Citizen Participation
                │                           │
        Deterministic Flow          Agentic Workflow
                │                           │
                │                    ┌──────┴──────┐
                │                    │             │
                │                   LLM           Jev
                │                    │             │
                │                    └──────┬──────┘
                │                           │
                └──────────────┬────────────┘
                               │
                          Decision
                               │
                             Policy
                               │
                         Approved Action
                               │
                          Simulation
                               │
                        Updated State
                               │
                            Outcome
                               │
                               ▼
                       Citizen / Operator
```

The Digital Twin remains the shared environment.

The simulation remains the execution and evaluation environment.

Agents provide intelligence.

Policy provides the safety and authorization boundary.

---

## 34. Architectural Goal

The architecture should make one idea immediately visible:

> **A city does not become agentic simply by adding an LLM.**

An Agentic City requires a controlled system in which:

- The environment has state.
- Citizens can contribute observations and requests.
- Agents can observe and investigate that state.
- AI can interpret and reason about context.
- Decisions are bounded.
- Jev can provide focused judgment.
- Policies control execution.
- Simulation evaluates proposed interventions.
- Outcomes can be observed and measured.
- Citizens can receive feedback.
- The application remains the authority over state.

The fundamental loop is:

```text
Citizen
   ↓
Agent
   ↓
Collective Intelligence
   ↓
Simulation
   ↓
Decision
   ↓
Action
   ↓
Feedback
   ↓
Citizen
```

Agentic Mannheim is a small implementation of this architectural idea.

> **AI proposes. Policy validates. Simulation executes.**
