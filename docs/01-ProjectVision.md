# Agentic Mannheim

## 1. Vision

**Agentic Mannheim** is an experimental Digital Twin demonstrating how real-world geographic data, virtual entities, simulation, AI agents, and bounded decision-making can come together in an AI-Native city architecture.

The project uses **Mannheim Innenstadt** as a realistic geographic environment, while the traffic, vehicles, incidents, and decisions are simulated.

> **The city is real. The world is simulated. The decisions are agentic.**

---

## 2. Purpose

The purpose of Agentic Mannheim is not to solve a real Mannheim traffic problem.

The purpose is to demonstrate, in a concrete and visual way, how an **Agentic City** can be architected.

The project explores the interaction between:

- Real-world geographic data
- Digital Twin representation
- Virtual entities
- Simulation
- AI agents
- Bounded decision engines
- Policy validation
- Observable actions
- Event-driven behavior

The result should be a small but convincing technical demonstrator that makes the architecture visible.

---

## 3. Agentic City

An Agentic City is not simply a city with AI added to existing software.

It is a system where software agents can:

1. Observe the state of a digital environment
2. Identify relevant situations
3. Evaluate possible actions
4. Propose decisions
5. Pass decisions through defined policies
6. Execute approved actions
7. Observe the resulting state
8. Continue the loop

The city remains governed by deterministic application logic and explicit policies.

AI provides intelligence.

AI does not own the city state.

---

## 4. Core Principle

The central architectural principle is:

> **AI proposes. Policy validates. Simulation executes.**

The application owns:

- State
- Rules
- Permissions
- Simulation
- Execution
- Auditability

Agents provide:

- Observation
- Interpretation
- Reasoning
- Decision proposals

The decision engine provides bounded decision-making.

The simulation provides the execution environment.

---

## 5. Digital Twin

The project represents a selected area of Mannheim as a simplified Digital Twin.

The Digital Twin contains virtual representations of elements such as:

- Roads
- Lanes
- Intersections
- Traffic signals
- Vehicles
- Emergency vehicles
- Incidents
- Sensors
- Agents

The geographic foundation is based on real Mannheim map data, while the operational state is simulated.

The Digital Twin is therefore **geographically realistic but operationally simulated**.

---

## 6. Demonstration Scenario

The initial demonstration focuses on a simple emergency-vehicle scenario.

A virtual emergency vehicle approaches an intersection while normal traffic is present.

The system demonstrates:

```text
Emergency detected
        ↓
Agent observes the situation
        ↓
Decision engine evaluates options
        ↓
Decision proposed
        ↓
Policy validates the decision
        ↓
Simulation applies the action
        ↓
Traffic signal changes
        ↓
Emergency vehicle passes
        ↓
Agent observes the new state
```

The scenario is intentionally simple.

The goal is to demonstrate the architecture, not to build a realistic traffic optimization system.

---

## 7. Scope

### In Scope

- Mannheim Innenstadt
- Real geographic map data
- Digital Twin representation
- Simulated vehicles
- Simulated traffic signals
- Simulated incidents
- Agent-based observation and decision-making
- Bounded decision engine
- Policy validation
- Simulation execution
- Event timeline and observability
- Interactive visual interface
- Reproducible demonstration scenarios

### Out of Scope

- Real-time Mannheim traffic control
- Real-world traffic optimization
- Autonomous vehicle control
- Production smart-city infrastructure
- Real traffic sensor integration
- Real emergency-service integration
- City-wide simulation
- Traffic research or optimization benchmarking
- LLM versus Laya comparison
- Production deployment for municipal operations

---

## 8. Project Principles

### 8.1 Application Owns State

The application and simulation own the authoritative state.

LLMs and agents do not become the source of truth.

### 8.2 AI Provides Intelligence

AI can interpret situations and propose actions.

It does not directly modify critical system state.

### 8.3 Decisions Are Bounded

Agents operate within explicit capabilities, policies, and action boundaries.

### 8.4 Simulation Is the Execution Environment

Actions are applied to the simulated city, not to the real world.

### 8.5 Everything Important Should Be Observable

Agent observations, decisions, policy validation, actions, and resulting state changes should be visible and traceable.

### 8.6 Prefer Simple Architecture

The project should demonstrate architectural ideas without introducing infrastructure that does not add value to the demonstration.

### 8.7 Visual Experience Matters

The Digital Twin should not exist only as backend models.

The city, vehicles, agents, decisions, and events should be visible through an interactive interface.

---

## 9. Technology Direction

The initial implementation is expected to use:

- **React + TypeScript** for the interactive UI
- **MapLibre GL JS** for map rendering
- **FastAPI + Python** for the backend
- **Python-based simulation and agent layer**
- **Laya** as a bounded decision component
- **OpenStreetMap-based geographic data** for the Mannheim environment

MapLibre GL JS provides an open-source, GPU-accelerated map rendering layer suitable for the interactive Digital Twin interface.

Technology choices remain implementation details and may evolve without changing the project vision.

---

## 10. Success Criteria

Agentic Mannheim is successful if a user can clearly see:

1. A recognizable Mannheim environment
2. A functioning Digital Twin
3. Virtual entities moving through the environment
4. An agent observing a situation
5. A bounded decision being produced
6. A policy validating the decision
7. The simulation executing the approved action
8. The resulting state change
9. A traceable sequence of events

The primary measure of success is **architectural clarity**, not simulation realism.

---

## 11. Future Direction

The initial project is intentionally small.

The architecture should, however, leave room for future experiments such as:

- Multiple cooperating agents
- Additional city scenarios
- Incident management
- Public transportation agents
- Parking agents
- Energy-related city agents
- Pedestrian and mobility scenarios
- Multi-agent coordination
- More advanced Digital Twin models
- Richer event-driven architectures
- Human-in-the-loop decision-making

These are future possibilities, not MVP requirements.

---

## 12. Final Statement

Agentic Mannheim is a technical experiment in **AI-Native city architecture**.

It combines a real geographic environment with a simulated world and bounded agentic decision-making to make an otherwise abstract architecture tangible.

The project is intentionally small.

The architecture is the experiment.
