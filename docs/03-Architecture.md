# Agentic Mannheim

## 1. Architecture Overview

Agentic Mannheim follows an **AI-Native, simulation-first architecture**.

The system is divided into two applications:

- **Frontend:** Next.js
- **Backend:** FastAPI

The frontend owns the user experience.

The backend owns the Digital Twin, simulation, agents, decisions, and policies.

The central flow is:

```text
Real-World Geography
        ↓
   Digital Twin
        ↓
    Simulation
        ↓
      Agent
        ↓
  Decision Engine
        ↓
 Policy Validation
        ↓
 Simulation Action
        ↓
 Updated State
```

---

## 2. Architectural Principles

### 2.1 Application Owns State

The Digital Twin and simulation own authoritative state.

Agents and AI components do not become the source of truth.

### 2.2 AI Provides Intelligence

AI is responsible for interpretation, reasoning, and decision proposals.

It does not directly control application state.

### 2.3 AI Proposes. Policy Validates. Simulation Executes.

Every agent action follows an explicit control boundary:

```text
Agent
  ↓
Decision
  ↓
Policy
  ↓
Execution
```

### 2.4 Bounded Agency

Agents operate within explicit:

- Capabilities
- Actions
- Permissions
- Policies
- Context

An agent cannot perform arbitrary operations.

### 2.5 Observable by Design

Important decisions and state transitions should be traceable.

```text
Event
  ↓
Observation
  ↓
Decision
  ↓
Validation
  ↓
Action
  ↓
State Change
```

### 2.6 Separate Presentation from Domain

The frontend and backend are independently structured applications.

The frontend does not own domain or simulation logic.

The backend does not depend on frontend implementation details.

### 2.7 Modular Backend, Not Premature Microservices

The backend is internally modular, but the MVP remains a single backend application.

We separate responsibilities without introducing distributed infrastructure that does not add value.

---

## 3. System Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                             │
│                         Next.js                             │
│                                                             │
│  Map │ Dashboard │ Simulation │ Agents │ Events │ Controls │
└─────────────────────────────┬───────────────────────────────┘
                              │
                         HTTP / WebSocket
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         BACKEND                             │
│                         FastAPI                             │
│                                                             │
│  API                                                       │
│   │                                                         │
│   ├── Digital Twin                                          │
│   ├── Simulation                                             │
│   ├── Agents                                                 │
│   ├── Decision                                               │
│   └── Policy                                                 │
│                                                             │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
                       Simulation State
```

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

- Render the Mannheim map
- Visualize the Digital Twin
- Display virtual vehicles
- Display traffic signals
- Display incidents
- Display simulation state
- Provide simulation controls
- Display active agents
- Inspect agent decisions
- Display the event timeline
- Communicate with the backend

The frontend must not implement authoritative simulation rules.

---

## 5. Backend Architecture

The backend is a single modular FastAPI application.

Conceptually:

```text
backend/
│
└── app/
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
    └── policy/
```

The backend owns the authoritative application state.

---

## 6. API Layer

The API provides the contract between Next.js and FastAPI.

Responsibilities include:

- Query Digital Twin state
- Query simulation state
- Start simulation
- Pause simulation
- Reset simulation
- Select scenarios
- Query agents
- Query agent decisions
- Query events
- Deliver simulation updates

The API should remain thin.

Domain and simulation behavior belongs to the backend domain layers.

---

## 7. Digital Twin Layer

The Digital Twin represents the structure and current state of the simulated city.

Core entities include:

```text
City
 ├── Road
 ├── Lane
 ├── Intersection
 ├── TrafficSignal
 ├── Vehicle
 ├── EmergencyVehicle
 ├── Incident
 └── Sensor
```

The Digital Twin represents **what exists**.

The simulation determines **what happens**.

---

## 8. Simulation Layer

The simulation controls the evolution of the virtual environment.

Responsibilities:

- Simulation clock
- Vehicle movement
- Traffic signals
- Incidents
- Events
- State transitions
- Scenario execution

The simulation is deterministic where reproducibility is required.

The simulation must remain independent of the frontend.

---

## 9. Agent Layer

Agents observe relevant parts of the Digital Twin and decide what should happen next.

An agent follows:

```text
Observe
   ↓
Interpret
   ↓
Decide
   ↓
Propose
   ↓
Observe Result
```

Agents do not directly mutate the Digital Twin.

For the MVP, the primary agent is a traffic-oriented agent responsible for responding to predefined simulation situations.

---

## 10. Decision Layer

The decision layer provides bounded decision-making.

For the MVP, **Laya** acts as a decision component rather than a general-purpose city brain.

Example:

```text
Situation
    ↓
Possible Actions
    ↓
Laya
    ↓
Structured Decision
```

The output must remain within the action space defined by the application.

The decision engine does not directly modify simulation state.

---

## 11. Policy Layer

The policy layer is the control boundary between AI decisions and execution.

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

Only approved actions reach the simulation.

---

## 12. Agentic Decision Flow

The primary agentic flow is:

```text
1. Event occurs
        ↓
2. Simulation updates state
        ↓
3. Agent receives observation
        ↓
4. Agent evaluates situation
        ↓
5. Decision engine evaluates bounded options
        ↓
6. Decision is returned
        ↓
7. Policy validates decision
        ↓
8. Approved action enters simulation
        ↓
9. Simulation changes state
        ↓
10. Agent observes the result
```

This creates a controlled agentic loop without giving the agent unrestricted control.

---

## 13. Event Flow

The system is conceptually event-driven even if the initial implementation remains simple.

Example:

```text
EmergencyVehicleApproaching
            ↓
      AgentTriggered
            ↓
     DecisionRequested
            ↓
      DecisionProduced
            ↓
     PolicyValidated
            ↓
       ActionExecuted
            ↓
     SimulationUpdated
            ↓
     EmergencyVehiclePassed
```

Events should provide a clear trace of what happened and why.

---

## 14. Simulation Loop

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
Trigger Agents
      ↓
Process Decisions
      ↓
Validate Actions
      ↓
Apply Actions
      ↓
Publish Updated State
```

The backend owns the simulation loop.

The frontend visualizes its current state.

---

## 15. Geographic Data Architecture

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

The map layer and simulation layer remain separate.

Geographic data provides the physical context.

Virtual vehicles, incidents, traffic states, and agent activity belong to the simulation.

The frontend uses MapLibre GL JS to render the geographic environment and simulation overlays.

---

## 16. State Ownership

State ownership is explicitly defined.

| State              | Owner            |
| ------------------ | ---------------- |
| Geographic data    | Data / Map layer |
| Digital Twin state | Digital Twin     |
| Simulation state   | Simulation       |
| Agent state        | Agent layer      |
| Decision proposal  | Decision layer   |
| Policy result      | Policy layer     |
| UI state           | Next.js frontend |

AI components must not become authoritative owners of application state.

---

## 17. Frontend / Backend Boundary

The architectural boundary is explicit:

```text
┌─────────────────────┐
│      Next.js        │
│                     │
│ Presentation        │
│ Visualization       │
│ Interaction         │
│ UI State             │
└──────────┬──────────┘
           │
       API Contract
           │
┌──────────▼──────────┐
│      FastAPI        │
│                     │
│ Domain              │
│ Digital Twin        │
│ Simulation          │
│ Agents              │
│ Decision             │
│ Policy              │
│ Authoritative State │
└─────────────────────┘
```

The frontend may request actions.

The backend decides whether those actions are valid and applies them.

---

## 18. Communication

The initial communication model uses:

- **HTTP APIs** for commands and queries
- **WebSocket or equivalent streaming** for live simulation updates where required

Example:

```text
Next.js
   │
   ├── GET  /api/city/state
   ├── POST /api/simulation/start
   ├── POST /api/simulation/pause
   ├── POST /api/simulation/reset
   ├── POST /api/scenarios/{id}
   └── WebSocket /api/simulation/stream
                    │
                    ▼
                 FastAPI
```

The communication protocol should remain independent of the internal backend modules.

---

## 19. Data Flow

The complete system data flow is:

```text
             Geographic Data
                    │
                    ▼
             Digital Twin
                    │
                    ▼
               Simulation
                    │
             ┌──────┴──────┐
             │             │
             ▼             ▼
          Events       World State
             │
             ▼
           Agent
             │
             ▼
      Decision Engine
             │
             ▼
      Policy Validation
             │
       ┌─────┴─────┐
       │           │
    Approved     Rejected
       │
       ▼
   Simulation
       │
       ▼
  Updated State
       │
       ▼
     Events
       │
       ▼
    Next Cycle
```

---

## 20. Failure and Safety Boundary

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

If a decision is:

- Invalid
- Unsupported
- Outside the agent's permissions
- Incompatible with the current state
- Unable to pass policy validation

the simulation must not execute it.

The default behavior should be safe and deterministic.

---

## 21. Extensibility

The architecture should allow additional agents without changing the Digital Twin or simulation core.

For example:

```text
                  ┌── TrafficAgent
                  │
Digital Twin ─────┼── EmergencyAgent
                  │
                  ├── IncidentAgent
                  │
                  └── MobilityAgent
```

Agents should share the same controlled interaction model:

```text
Observe
  ↓
Decide
  ↓
Validate
  ↓
Act
```

This provides a foundation for future multi-agent experiments.

---

## 22. Architecture Boundaries

The following boundaries are intentional:

```text
Map Data
    ≠
Simulation State

Simulation State
    ≠
Agent State

Agent Decision
    ≠
Executable Action

AI Decision
    ≠
Authoritative State

Frontend
    ≠
Backend Domain

UI
    ≠
Simulation Logic
```

These boundaries are central to the architecture.

---

## 23. Technology Stack

### Frontend

- Next.js
- TypeScript
- MapLibre GL JS
- Tailwind CSS
- Zustand where client-side state management is required

### Backend

- Python
- FastAPI
- Pydantic

### Simulation

- Python
- Deterministic simulation model

### Agent Layer

- Python
- Agent orchestration components

### Decision Layer

- Laya

### Data

- OpenStreetMap
- GeoJSON
- JSON

### Development

- Docker
- Docker Compose
- GitHub

The technology stack should remain replaceable where it does not affect the architectural boundaries.

---

## 24. Deployment Model

The MVP uses two independently deployable applications:

```text
                 Internet / Browser
                        │
                ┌───────┴───────┐
                │               │
                ▼               ▼
          Next.js App      FastAPI App
                │               │
                │               ▼
                │          Simulation
                │               │
                │          Digital Twin
                │               │
                │          Agents / AI
                │               │
                │        Decision / Policy
                │               │
                └──── API ──────┘
```

The frontend and backend can therefore evolve and deploy independently.

The backend remains a modular monolith for the MVP.

There is no requirement to introduce microservices until there is a clear architectural reason to do so.

---

## 25. Target Architecture

```text
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │    Next.js      │
                  │    Frontend     │
                  └────────┬────────┘
                           │
                    API / WebSocket
                           │
                           ▼
                  ┌─────────────────┐
                  │     FastAPI     │
                  │     Backend     │
                  └────────┬────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        Digital Twin   Simulation     Events
              │            │            │
              └────────────┼────────────┘
                           │
                           ▼
                        Agents
                           │
                           ▼
                   Decision Engine
                           │
                           ▼
                    Policy Boundary
                           │
                           ▼
                    Simulation Action
                           │
                           ▼
                    Updated World
                           │
                           └──────────────► UI
```

---

## 26. Architectural Goal

The architecture should make one idea immediately visible:

> **A city does not become agentic simply by adding an LLM.**

An Agentic City requires a controlled system in which:

- The environment has state.
- Agents can observe that state.
- Decisions are bounded.
- Policies control execution.
- Actions change the environment.
- The resulting state can be observed again.

Agentic Mannheim is a small implementation of that idea.

> **AI proposes. Policy validates. Simulation executes.**
