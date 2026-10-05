# Agentic Mannheim

## 1. Purpose

This document defines the functional and non-functional requirements for the Agentic Mannheim MVP.

The requirements describe **what the system must provide**, not how it should be implemented.

---

## 2. Functional Requirements

### 2.1 Digital Twin

The system must:

* Represent a selected area of Mannheim Innenstadt.
* Represent roads and intersections relevant to the simulation.
* Represent traffic signals.
* Represent virtual vehicles.
* Represent emergency vehicles.
* Represent incidents and events.
* Maintain the current state of the simulated city.

---

### 2.2 Map

The system must:

* Display a recognizable Mannheim Innenstadt map.
* Use real geographic data as the geographic foundation.
* Display roads and relevant infrastructure.
* Provide a clear visual distinction between the real map and simulated entities.
* Support interactive map navigation.

---

### 2.3 Simulation

The system must:

* Maintain a simulation clock.
* Advance the simulation through discrete updates.
* Move virtual vehicles through the road network.
* Model basic traffic signal states.
* Model vehicles waiting and moving.
* Generate predefined simulation events.
* Support deterministic scenarios where required.
* Allow the simulation to be started, paused, and reset.
* Support different simulation speeds.

---

### 2.4 Vehicles

The system must support:

* Normal vehicles.
* Emergency vehicles.
* Vehicle position.
* Vehicle direction.
* Vehicle state.
* Vehicle movement.
* Vehicle waiting.
* Vehicle interaction with traffic signals.

The initial vehicle behavior may be intentionally simplified.

---

### 2.5 Traffic Signals

The system must:

* Represent traffic signals associated with intersections.
* Maintain signal states.
* Change signal states through simulation actions.
* Prevent invalid signal transitions.
* Make signal changes visible in the UI.

---

### 2.6 Events and Incidents

The system must support simulated events such as:

* Emergency vehicle approaching an intersection.
* Traffic congestion.
* Road incidents.
* Signal-related situations.

Events must have a clear lifecycle and be observable by the relevant agent.

---

## 3. Agent Requirements

### 3.1 Agent Observation

An agent must be able to observe relevant parts of the Digital Twin state.

An observation may include:

* Current intersection
* Nearby vehicles
* Traffic signal state
* Emergency vehicles
* Traffic conditions
* Active incidents
* Relevant historical context

Agents must not directly own or modify the authoritative simulation state.

---

### 3.2 Agent Decision

An agent must be able to:

1. Receive an observation.
2. Identify a relevant situation.
3. Request or produce a bounded decision.
4. Propose an action.
5. Wait for policy validation.
6. Observe the result after execution.

---

### 3.3 Bounded Actions

The MVP should support a small set of explicitly defined actions.

Example:

```text
PRIORITIZE_EMERGENCY
MAINTAIN_SIGNAL
REJECT_ACTION
```

The available actions must be known to the system.

Agents must not be able to execute arbitrary operations.

---

## 4. Decision Engine Requirements

The decision engine must:

* Receive structured decision inputs.
* Evaluate a bounded set of possible decisions.
* Produce a structured decision.
* Return a decision that can be validated by the application.
* Provide sufficient information for the decision to be inspected.

The decision engine must not directly modify Digital Twin state.

---

## 5. Policy Requirements

The system must have a policy validation step between agent decisions and simulation actions.

```text
Agent
  ↓
Decision
  ↓
Policy Validation
  ↓
Approved / Rejected
  ↓
Simulation
```

The policy layer must:

* Validate proposed actions.
* Reject unsupported actions.
* Enforce defined constraints.
* Prevent invalid state transitions.
* Produce an auditable validation result.

A rejected decision must not be executed.

---

## 6. Simulation Execution Requirements

An approved action must be translated into a valid simulation operation.

For example:

```text
Decision:
PRIORITIZE_EMERGENCY

Policy:
APPROVED

Simulation:
Change signal state

Result:
Emergency vehicle continues
```

The simulation remains responsible for applying the actual state change.

---

## 7. User Interface Requirements

The UI must provide a clear view of the Digital Twin.

The main interface should include:

### Map

* Mannheim map
* Roads
* Intersections
* Traffic signals
* Vehicles
* Emergency vehicles
* Active incidents

### Simulation Controls

* Start
* Pause
* Reset
* Simulation speed
* Scenario selection

### City State

At minimum:

* Vehicle count
* Moving vehicles
* Waiting vehicles
* Active incidents
* Simulation time

### Agent State

The UI should expose:

* Active agents
* Current observation
* Current situation
* Proposed decision
* Policy result
* Executed action

### Event Timeline

The system should display important events in chronological order.

Example:

```text
Emergency detected
Agent observing
Decision requested
Decision produced
Policy approved
Signal changed
Emergency vehicle passed
```

---

## 8. Scenario Requirements

The MVP must provide predefined scenarios.

### Scenario 1: Normal Traffic

Demonstrates basic vehicle movement and traffic signals.

### Scenario 2: Rush Hour

Introduces increased vehicle density and waiting traffic.

### Scenario 3: Emergency Vehicle

Demonstrates the complete agentic decision flow.

### Scenario 4: Incident

Demonstrates an event that changes the simulated environment.

The Emergency Vehicle scenario is the primary demonstration scenario.

---

## 9. Observability Requirements

The system must make important system activity observable.

At minimum, the following should be traceable:

```text
Event
  ↓
Observation
  ↓
Decision
  ↓
Policy Validation
  ↓
Action
  ↓
State Change
```

The system should make it possible to understand **why an action happened**.

---

## 10. Data Requirements

The system must distinguish between:

### Geographic Data

Represents the physical structure of Mannheim.

Examples:

* Roads
* Intersections
* Geographic coordinates

### Simulation State

Represents the current virtual state.

Examples:

* Vehicle positions
* Traffic signal states
* Incidents
* Simulation time

### Agent State

Represents the current operational state of agents.

Examples:

* Observation
* Decision
* Action
* Status

These concerns must remain logically separated.

---

## 11. Non-Functional Requirements

### 11.1 Reproducibility

Predefined scenarios should produce reproducible results where deterministic behavior is expected.

### 11.2 Extensibility

The system should allow additional:

* Agents
* Scenarios
* Entity types
* Decision types
* Policies
* Simulation behaviors

without redesigning the complete system.

### 11.3 Observability

Important state changes and agent decisions should be visible and traceable.

### 11.4 Local Development

The MVP should be runnable locally without mandatory paid cloud services.

### 11.5 Performance

The system should support a visually smooth simulation for the MVP scenario and the selected Mannheim area.

### 11.6 Maintainability

The implementation should maintain clear boundaries between:

* UI
* API
* Digital Twin
* Simulation
* Agents
* Decision-making
* Policy validation

### 11.7 Safety

AI-generated decisions must not directly modify authoritative system state.

All executable actions must pass through defined application controls.

---

## 12. Constraints

The MVP intentionally avoids:

* Real-time traffic feeds
* Real municipal infrastructure
* Production traffic control
* Real emergency-service integration
* City-wide Digital Twin modeling
* Complex traffic optimization
* Autonomous vehicle control
* Large-scale distributed infrastructure
* Unnecessary external services

The objective is to demonstrate the architecture with the smallest meaningful system.

---

## 13. MVP Acceptance Criteria

The MVP is considered complete when the following flow works end-to-end:

```text
Mannheim Map
     ↓
Digital Twin
     ↓
Virtual Traffic
     ↓
Emergency Event
     ↓
Agent Observation
     ↓
Bounded Decision
     ↓
Policy Validation
     ↓
Simulation Action
     ↓
Visible State Change
     ↓
Event Timeline
```

A user should be able to start the application, select the emergency scenario, observe the agentic flow, and understand the complete decision lifecycle through the UI.

---

## 14. Requirement Priorities

### Must Have

* Mannheim map
* Digital Twin state
* Virtual vehicles
* Traffic signals
* Simulation engine
* Agent
* Bounded decision engine
* Policy validation
* Emergency scenario
* Interactive UI
* Event timeline
* Start / pause / reset

### Should Have

* Multiple scenarios
* Simulation speed controls
* Agent inspector
* Incident visualization
* Deterministic scenario replay

### Could Have

* Multiple cooperating agents
* Additional city services
* More complex traffic behavior
* Human approval step
* Historical simulation replay

### Will Not Have in MVP

* Real-time Mannheim traffic
* Real-world traffic control
* Production municipal integration
* City-wide simulation
* Autonomous vehicle control
* Traffic optimization research
