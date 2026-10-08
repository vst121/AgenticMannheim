# Agentic Mannheim

> **The city is real. The world is simulated. The decisions are agentic.**

Agentic Mannheim is an experimental **Agentic Digital Twin** of Mannheim Innenstadt.

The project combines real-world OpenStreetMap data, a simulated city environment, AI agents, bounded decision-making, policy validation, and simulation to explore how **Agentic AI can operate on top of a Digital Twin**.

It is designed as an AI and software architecture laboratory, not as a real-world traffic control system.

## What It Demonstrates

Agentic Mannheim demonstrates a closed-loop agentic architecture:

```text
Digital Twin
     ↓
Observe
     ↓
AI Agent
     ↓
Jev Judgment
     ↓
Decision
     ↓
Policy Validation
     ↓
Simulation
     ↓
Evaluate Result
     ↓
Digital Twin
```

The fundamental principle is:

> **AI proposes. Policy validates. Simulation executes.**

The application remains the owner of authoritative state. AI provides intelligence, not application control.

## Current Scenario

The current MVP demonstrates an emergency vehicle scenario:

1. An emergency vehicle is introduced into the simulated city.
2. The vehicle moves through the road network.
3. When it reaches an intersection, an agent evaluates the situation.
4. The agent proposes emergency priority.
5. The policy layer validates the proposed action.
6. The simulation changes the traffic light.
7. The emergency vehicle continues through the intersection.
8. The traffic light returns to its normal state.

The architecture is intentionally designed so this simple scenario can evolve into more sophisticated multi-agent and counterfactual simulations.

## Architecture

```text
Next.js / MapLibre
        │
        │ HTTP
        ▼
     FastAPI
        │
        ├── Digital Twin
        ├── Simulation
        ├── Agents
        ├── Decision
        ├── Jev Judgment
        ├── Policy
        └── Persistence
              │
              ▼
          PostgreSQL
```

### Main Concepts

- **Digital Twin** represents the current simulated city state.
- **Simulation Engine** determines how the virtual city evolves.
- **AI Agents** observe situations and propose decisions.
- **Jev** provides bounded judgment over conditions and alternatives.
- **Decision Layer** translates agent decisions into executable actions.
- **Policy Layer** validates what is allowed.
- **Simulation** executes approved actions.
- **PostgreSQL** persists geographic data, events, and agent runs.
- **Next.js + MapLibre** provides the visual city interface.

## Technology

### Backend

- Python 3.12+
- FastAPI
- SQLAlchemy
- PostgreSQL 17
- Alembic
- uv
- OpenStreetMap / Overpass

### Frontend

- Next.js
- React
- MapLibre GL
- TypeScript
- pnpm

## Running the Project

### 1. Start PostgreSQL

```bash
docker compose up -d
```

### 2. Install backend dependencies

```bash
cd backend
uv sync
```

### 3. Apply database migrations

```bash
uv run alembic upgrade head
```

### 4. Seed Mannheim road data

```bash
uv run python -m infrastructure.seed_osm
```

This imports the configured Mannheim Innenstadt area from OpenStreetMap.

### 5. Start the backend

```bash
uv run uvicorn main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

### 6. Start the frontend

```bash
cd frontend
pnpm install
pnpm dev
```

The map will be available at:

```text
http://localhost:3000
```

## Project Status

This is an experimental project under active development.

The current implementation focuses on:

- Mannheim road network
- Digital Twin state
- Simulated vehicles
- Traffic lights
- Emergency vehicle scenario
- Agent-driven decisions
- Policy validation
- Event-driven simulation
- Live map visualization

Future directions include:

- Jev-based condition judgment
- Counterfactual simulation
- Multi-agent collaboration
- Agent conflict resolution
- Scenario evaluation
- Agent memory
- More sophisticated traffic situations

## Important Scope

Agentic Mannheim is **not**:

- a real Mannheim traffic management system
- connected to real traffic infrastructure
- a production municipal control system
- an autonomous vehicle system
- a traffic optimization research platform
- an LLM benchmark

All city behavior is simulated.

## Why This Project?

The goal is to explore a fundamental question:

> **What does an AI-Native Digital Twin look like when agents can reason about situations, propose actions, simulate consequences, and operate within explicit policies?**

Agentic Mannheim is a practical laboratory for exploring that question through software architecture and working code.
