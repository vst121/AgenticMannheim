# Agentic Mannheim

## 1. Vision

**Agentic Mannheim** is an experimental Digital Twin demonstrating how real-world geographic data, virtual entities, simulation, event-driven systems, AI agents, and bounded decision-making can come together in an AI-Native city architecture.

The project uses **Mannheim Innenstadt** as a realistic geographic environment, while traffic, vehicles, incidents, citizen reports, decisions, and city responses are simulated.

> **The city is real. The world is simulated. The decisions are agentic.**

The project has two complementary areas:

1. **Traffic Control**  
   A Digital Twin and simulation environment for vehicles, traffic lights, emergency scenarios, city events, and deterministic decision-making.

2. **Citizen Participation**  
   An Agentic AI environment where citizens can report incidents, submit suggestions, and participate in city-related decisions through AI-assisted investigation, reasoning, simulation, and feedback.

---

## 2. Purpose

The purpose of Agentic Mannheim is not to solve a real Mannheim traffic or municipal problem.

The purpose is to demonstrate, in a concrete and visual way, how an **Agentic City** can be architected.

The project explores the interaction between:

- Real-world geographic data
- Digital Twin representation
- Virtual entities
- Event-driven architecture
- Simulation
- Citizen participation
- AI agents
- LLM-based reasoning
- Bounded judgment
- Policy validation
- Observable actions
- Outcome evaluation

The result should be a small but convincing technical demonstrator that makes the architecture visible.

---

## 3. Agentic City

An Agentic City is not simply a city with AI added to existing software.

It is a system where software agents can:

1. Observe the state of a digital environment
2. Understand events and human input
3. Identify relevant situations
4. Gather and correlate information
5. Evaluate possible actions
6. Propose decisions or interventions
7. Pass decisions through defined policies
8. Execute approved actions in the simulation
9. Observe the resulting state
10. Evaluate the outcome
11. Communicate meaningful results back to citizens or other stakeholders

The city remains governed by deterministic application logic, explicit policies, and authoritative Digital Twin state.

**AI provides intelligence.**

**AI does not own the city state.**

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
- Information gathering
- Decision proposals
- Communication

LLMs provide language understanding and reasoning capabilities where they add meaningful value.

Bounded judgment systems such as **Jev** provide focused, typed judgments rather than owning application decisions.

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
- Citizen reports
- Agents
- Relevant city state

The geographic foundation is based on real Mannheim map data, while the operational state is simulated.

The Digital Twin is therefore **geographically realistic but operationally simulated**.

The Digital Twin is the shared environment used by both major project areas:

- Traffic Control uses it to simulate traffic and city operations.
- Citizen Participation uses it to understand reported situations and explore possible interventions.

---

## 6. Project Areas

### 6.1 Traffic Control

Traffic Control provides the deterministic foundation of the project.

It allows users to interact with the simulated city and create scenarios such as:

- Emergency vehicles
- Normal vehicles
- Traffic-light changes
- Traffic events
- Emergency-response situations

The existing deterministic event-driven implementation remains an independent and functional capability.

The Traffic Control flow can be summarized as:

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

This part of the project does not require an LLM.

It provides the reliable simulation environment on which future Agentic City capabilities can operate.

---

### 6.2 Citizen Participation

Citizen Participation introduces the first major Agentic AI capability.

Citizens can interact with the Digital Twin by submitting:

- Incident reports
- Safety concerns
- Suggestions
- Observations
- Other participative requests

A citizen report is associated with a geographic location and becomes part of the city's event-driven system.

For example:

> "This intersection feels unsafe for pedestrians. Cars often turn too quickly here."

The Agentic workflow can then:

```text
Citizen Report
      ↓
Citizen Participation Agent
      ↓
Understand the request
      ↓
Inspect location and Digital Twin state
      ↓
Gather relevant city information
      ↓
Correlate related reports and events
      ↓
Formulate possible interventions
      ↓
Jev Judgment
      ↓
Policy Validation
      ↓
Simulation
      ↓
Evaluate Outcomes
      ↓
Citizen Feedback
```

The objective is not simply to classify or route citizen complaints.

The objective is to demonstrate how an Agentic City can help citizens and decision-makers **understand situations, explore alternatives, and evaluate potential interventions**.

---

## 7. Demonstration Scenarios

### 7.1 Traffic Control Scenario

The initial Traffic Control demonstration focuses on an emergency-vehicle scenario.

A virtual emergency vehicle approaches an intersection while normal traffic is present.

The system demonstrates:

```text
Emergency detected
        ↓
Event generated
        ↓
Deterministic decision
        ↓
Policy validates the decision
        ↓
Simulation applies the action
        ↓
Traffic signal changes
        ↓
Emergency vehicle passes
        ↓
City state changes
```

The scenario is intentionally simple.

The goal is to demonstrate the Digital Twin, event-driven architecture, decision-making, policy validation, and simulation.

---

### 7.2 Citizen Participation Scenario

The first Citizen Participation demonstration focuses on a citizen reporting a potentially unsafe intersection.

For example:

```text
Citizen selects a location
        ↓
Citizen reports a safety concern
        ↓
Incident becomes a city event
        ↓
Agent investigates the situation
        ↓
LLM interprets the report and context
        ↓
Jev provides a bounded judgment
        ↓
Agent proposes possible interventions
        ↓
Simulation evaluates alternatives
        ↓
Outcomes are compared
        ↓
Citizen receives an understandable result
```

This scenario demonstrates a more meaningful use of Agentic AI because the problem requires interpretation of human input, contextual investigation, reasoning across multiple sources, and exploration of possible actions.

---

## 8. Agentic Decision Model

Agentic decisions are an additional capability, not a replacement for the existing deterministic implementation.

The architecture must support both approaches.

```text
                    City Situation
                          │
             ┌────────────┴────────────┐
             │                         │
      Deterministic               Agentic
       Decision                  Decision
             │                         │
             │                    LLM + Jev
             │                         │
             └────────────┬────────────┘
                          ↓
                       Policy
                          ↓
                     Simulation
                          ↓
                    City Outcome
```

The deterministic implementation remains available as:

- A reliable baseline
- A fallback
- A reference implementation
- A source for comparison and evaluation

Agentic decisions can therefore be evaluated against deterministic behavior and simulation outcomes without removing or weakening the existing system.

---

## 9. Decision and Outcome Evaluation

AgenticMannheim should distinguish between:

**Agent confidence** and **decision quality**.

An agent or Jev may have high confidence in a judgment, while the resulting action may still produce a poor outcome.

Therefore, the project should preserve and evaluate:

- Agent observations
- Agent decisions
- Jev judgments
- Jev probabilities or confidence signals
- Model/version information
- Policy decisions
- Actions taken
- Simulation outcomes
- Decision quality
- Relevant city-impact metrics

For comparable scenarios, the system should be able to evaluate alternative decisions against the same initial Digital Twin state.

This makes Agentic AI an experimental capability that can be measured rather than simply demonstrated.

---

## 10. Scope

### In Scope

- Mannheim Innenstadt
- Real geographic map data
- Digital Twin representation
- Simulated vehicles
- Simulated traffic signals
- Simulated incidents
- Citizen reports
- Citizen participation workflows
- Event-driven city behavior
- Deterministic decision-making
- AI-agent-based decision-making
- LLM integration
- Bounded judgment with Jev
- Policy validation
- Simulation execution
- Decision and outcome evaluation
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
- Direct control of municipal infrastructure
- City-wide simulation
- Traffic research or optimization benchmarking
- LLM versus Laya benchmarking as the primary project objective
- Production deployment for municipal operations

---

## 11. Project Principles

### 11.1 Application Owns State

The application and Digital Twin own the authoritative state.

LLMs, agents, and external judgment systems do not become the source of truth.

### 11.2 AI Provides Intelligence

AI can interpret situations, investigate context, reason about alternatives, and propose actions.

It does not directly modify critical system state.

### 11.3 Decisions Are Bounded

Agents operate within explicit capabilities, policies, permissions, and action boundaries.

### 11.4 Policy Governs Actions

Agent proposals are not automatically executed.

Policies validate whether a proposed action is permitted within the simulated city.

### 11.5 Simulation Is the Execution Environment

Actions are applied to the simulated city, not to the real world.

### 11.6 Deterministic and Agentic Decisions Coexist

Existing deterministic decisions remain valid and operational.

Agentic decisions are introduced as an additional strategy and can be evaluated against deterministic behavior.

### 11.7 Human Participation Matters

Citizen participation is not simply a source of data.

Citizens should be able to understand situations, explore alternatives, and receive meaningful feedback about how their input affects the simulated city.

### 11.8 Everything Important Should Be Observable

Agent observations, decisions, Jev judgments, policy validation, actions, simulation results, and resulting state changes should be visible and traceable.

### 11.9 Prefer Simple Architecture

The project should demonstrate architectural ideas without introducing infrastructure that does not add value to the demonstration.

### 11.10 Visual Experience Matters

The Digital Twin should not exist only as backend models.

The city, vehicles, incidents, citizen reports, agents, decisions, and events should be visible through an interactive interface.

---

## 12. Technology Direction

The implementation uses:

- **Next.js + React + TypeScript** for the interactive UI
- **MapLibre GL JS** for map rendering
- **FastAPI + Python** for the backend
- **Python-based simulation and agent layer**
- **LLMs** for language understanding and agentic reasoning where appropriate
- **Jev** for bounded, typed judgment
- **OpenStreetMap-based geographic data** for the Mannheim environment
- **PostgreSQL** for persistent city and event data

Existing deterministic decision components remain part of the architecture.

Technology choices remain implementation details and may evolve without changing the project vision.

---

## 13. Success Criteria

Agentic Mannheim is successful if a user can clearly see:

1. A recognizable Mannheim environment
2. A functioning Digital Twin
3. Virtual entities moving through the environment
4. A working Traffic Control scenario
5. City events being generated and processed
6. A citizen submitting a geographically located report
7. An agent understanding and investigating the report
8. A bounded AI judgment being produced
9. Possible interventions being proposed
10. A policy validating proposed actions
11. The simulation executing or evaluating an action
12. The resulting city-state changes
13. Decision and outcome evaluation
14. A traceable sequence of events
15. Meaningful feedback being returned to the citizen

The primary measure of success is **architectural clarity and meaningful use of Agentic AI**, not simulation realism.

---

## 14. Future Direction

The initial project is intentionally small.

The architecture should, however, leave room for future experiments such as:

- Multiple cooperating city agents
- Additional citizen participation scenarios
- Incident management agents
- Public transportation agents
- Parking agents
- Energy-related city agents
- Pedestrian and mobility agents
- Environmental agents
- Multi-agent coordination
- Human-in-the-loop decision-making
- Collective citizen intelligence
- More advanced Digital Twin models
- Richer event-driven architectures
- Long-term city-impact evaluation
- Additional AI-assisted city services

These are future possibilities, not MVP requirements.

---

## 15. Final Statement

Agentic Mannheim is a technical experiment in **AI-Native city architecture**.

It combines a real geographic environment with a simulated world, event-driven city behavior, deterministic systems, citizen participation, and bounded agentic decision-making.

The project deliberately demonstrates both sides of an Agentic City:

**The city can operate through reliable deterministic systems.**

**AI can help people understand, reason about, and influence that city.**

The application owns the city.

Agents provide intelligence.

Policies provide boundaries.

Simulation provides a safe environment for experimentation.

Citizens remain part of the decision loop.

**The architecture is the experiment.**
