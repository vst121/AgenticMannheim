# Agentic Mannheim

## 1. Purpose

This document defines the functional and non-functional requirements for the Agentic Mannheim MVP.

The requirements describe **what the system must provide**, not how it should be implemented.

The MVP consists of two complementary areas:

1. **Traffic Control**  
   A Digital Twin and simulation environment for vehicles, traffic signals, emergency scenarios, events, and deterministic decision-making.

2. **Citizen Participation**  
   An Agentic AI environment where citizens can submit geographically located incident reports and suggestions, while AI agents investigate, reason about the situation, propose possible interventions, and evaluate them through the Digital Twin.

---

# 2. Functional Requirements

## 2.1 Digital Twin

The system must:

- Represent a selected area of Mannheim Innenstadt.
- Represent roads and intersections relevant to the simulation.
- Represent traffic signals.
- Represent virtual vehicles.
- Represent emergency vehicles.
- Represent incidents and citizen reports.
- Maintain the current state of the simulated city.
- Provide a shared city environment for Traffic Control and Citizen Participation.

The Digital Twin is the authoritative representation of the simulated city state.

---

## 2.2 Map

The system must:

- Display a recognizable Mannheim Innenstadt map.
- Use real geographic data as the geographic foundation.
- Display roads and relevant infrastructure.
- Display simulated vehicles and emergency vehicles.
- Display traffic signals.
- Display relevant incidents and citizen reports.
- Provide a clear visual distinction between geographic data and simulated entities.
- Support interactive map navigation.
- Allow a citizen participation request to be associated with a geographic location.

---

## 2.3 Simulation

The system must:

- Maintain a simulation clock.
- Advance the simulation through discrete updates.
- Move virtual vehicles through the road network.
- Model basic traffic signal states.
- Model vehicles waiting and moving.
- Generate predefined simulation events.
- Support deterministic scenarios where required.
- Execute approved simulation actions.
- Support reproducible scenario execution where deterministic behavior is expected.

The simulation is responsible for applying state changes to the Digital Twin.

The simulation does not directly execute arbitrary agent instructions.

---

## 2.4 Vehicles

The system must support:

- Normal vehicles.
- Emergency vehicles.
- Vehicle position.
- Vehicle direction.
- Vehicle state.
- Vehicle movement.
- Vehicle waiting.
- Vehicle interaction with traffic signals.

The initial vehicle behavior may be intentionally simplified.

---

## 2.5 Traffic Signals

The system must:

- Represent traffic signals associated with intersections.
- Maintain signal states.
- Change signal states through valid simulation actions.
- Prevent invalid signal transitions.
- Make signal changes visible in the UI.
- Support emergency-priority behavior where defined by the simulation.

---

## 2.6 Events and Incidents

The system must support city events such as:

- Emergency vehicle entering a road.
- Emergency vehicle reaching an intersection.
- Traffic congestion.
- Road incidents.
- Traffic-signal changes.
- Emergency detection.
- Agent decision proposals.
- Policy rejection.
- Citizen incident reports.
- Agent processing of citizen reports.

Events must have:

- A type
- A timestamp
- An associated entity where applicable
- A correlation identifier
- Relevant event data

Events must be observable by the relevant system components.

---

# 3. Traffic Control Requirements

## 3.1 Traffic Control Interface

The Traffic Control UI must provide a clear way to create supported scenarios.

The initial UI must include:

### Scenarios

- Create Emergency

Selecting **Create Emergency** must invoke the existing emergency scenario API.

The UI must not require the user to manually create or configure individual vehicles for the initial MVP scenario.

Additional vehicle and simulation controls are not required for the initial UI.

---

## 3.2 Emergency Scenario

The system must provide an emergency scenario in which:

1. An emergency vehicle is created.
2. The vehicle is placed on a valid road.
3. The vehicle enters the Digital Twin.
4. Vehicle movement is handled by the existing simulation.
5. Relevant city events are generated.
6. The emergency agent can observe the relevant event.
7. A bounded decision can be produced.
8. The decision passes through policy validation.
9. An approved action is executed by the simulation.
10. The resulting traffic-light and vehicle state changes are observable.

The emergency scenario must continue to work without requiring an LLM.

---

# 4. Agent Requirements

## 4.1 Agent Observation

An agent must be able to observe relevant parts of the Digital Twin and event state.

An observation may include:

- Current intersection
- Nearby vehicles
- Traffic signal state
- Emergency vehicles
- Traffic conditions
- Active incidents
- Citizen reports
- Relevant historical context

Agents must not directly own or modify the authoritative Digital Twin state.

---

## 4.2 Deterministic Decision Capability

The existing deterministic decision capability must remain available.

It must:

1. Receive a relevant event or observation.
2. Identify a supported situation.
3. Produce a bounded decision.
4. Translate the decision into a supported action.
5. Pass the action through policy validation.
6. Observe the resulting state.

The existing deterministic behavior must remain functional even when Agentic AI capabilities are unavailable.

---

## 4.3 Agentic Decision Capability

The system must support an Agentic decision path as an additional capability.

An Agentic workflow may:

1. Receive an event or citizen request.
2. Observe relevant Digital Twin state.
3. Interpret human or system input.
4. Gather relevant information through defined tools.
5. Reason about the situation.
6. Produce a bounded judgment.
7. Propose one or more possible actions.
8. Pass proposed actions through policy validation.
9. Execute approved actions through the simulation.
10. Observe the resulting state.
11. Evaluate the outcome.

Agentic decision-making must not replace or remove the existing deterministic decision path.

---

## 4.4 LLM Requirements

LLMs may be used when the problem requires capabilities such as:

- Natural-language understanding
- Interpretation of citizen reports
- Contextual reasoning
- Information synthesis
- Investigation across multiple city data sources
- Generation of intervention proposals
- Communication with citizens

LLMs must not be used where deterministic application logic is sufficient and more appropriate.

LLMs must not directly modify authoritative Digital Twin state.

---

## 4.5 Bounded Judgment

The system should support a bounded judgment capability using Jev.

Jev judgments should:

- Address a focused question.
- Produce a structured result.
- Preserve relevant probability or confidence information.
- Record the model/version used where available.
- Remain separate from application state and execution logic.

Jev must provide judgment rather than directly execute city actions.

---

## 4.6 Bounded Actions

The system must support a small set of explicitly defined actions.

Examples include:

```text
PRIORITIZE_EMERGENCY
MAINTAIN_SIGNAL
CHANGE_TRAFFIC_LIGHT
REJECT_ACTION
```

Citizen Participation may introduce additional actions as new scenarios are implemented.

The available actions must be explicitly defined by the application.

Agents must not be able to execute arbitrary operations.

---

# 5. Citizen Participation Requirements

## 5.1 Citizen Requests

The system must allow citizens to submit geographically located requests.

The initial request types should include:

- Incident report
- Safety concern
- Suggestion
- General participative request

A request must contain at minimum:

- Request identifier
- Geographic location
- Request type
- Citizen description
- Creation timestamp
- Status

---

## 5.2 Citizen Map Interaction

A citizen must be able to select a location on the Mannheim map when creating a request.

The selected location must be associated with the resulting citizen request.

The system should provide contextual information about the selected location where available.

---

## 5.3 Incident Reporting

The first Citizen Participation scenario must support a citizen reporting an urban problem such as:

> "This intersection feels unsafe for pedestrians."

The system must:

1. Capture the geographic location.
2. Capture the citizen's description.
3. Store the report.
4. Generate a corresponding city event.
5. Make the report available to the Citizen Participation Agent.

---

## 5.4 Citizen Participation Agent

The Citizen Participation Agent must be able to:

- Understand the citizen request.
- Identify the relevant location.
- Inspect relevant Digital Twin state.
- Investigate related city information.
- Identify potentially related reports and events.
- Correlate available evidence.
- Formulate an assessment.
- Propose possible interventions.
- Request bounded judgments where appropriate.
- Explain the reasoning behind proposed interventions.
- Return meaningful results to the citizen.

The agent must not directly change authoritative city state.

---

## 5.5 Intervention Proposals

For relevant citizen requests, the Agent should be able to propose possible interventions.

For example:

```text
Citizen report:
Unsafe pedestrian crossing

Possible interventions:
- Increase pedestrian phase
- Change signal timing
- Restrict turning during peak hours
```

Proposals must remain suggestions until they pass the appropriate application controls.

---

## 5.6 Simulation-Based Evaluation

The system should be able to use the Digital Twin to evaluate proposed interventions.

Where appropriate, multiple alternatives should be evaluated from the same initial simulated state.

For example:

```text
Initial City State
        │
   ┌────┼────┐
   ↓    ↓    ↓
  A     B     C
   │    │    │
   ▼    ▼    ▼
Simulation Outcomes
   │    │    │
   └────┼────┘
        ▼
   Outcome Comparison
```

Relevant metrics may include:

- Vehicle delay
- Pedestrian delay
- Emergency response impact
- Number of affected vehicles
- Intersection delay
- Intervention duration
- Other scenario-specific measures

The exact metrics depend on the scenario.

---

## 5.7 Citizen Feedback

The system should present the result of the Agentic workflow in an understandable way.

Citizen feedback may include:

- Summary of the reported issue
- Relevant evidence
- Agent assessment
- Jev judgment where applicable
- Proposed interventions
- Simulation results
- Trade-offs
- Current status

The system should clearly distinguish between:

- Citizen input
- AI-generated assessment
- Proposed action
- Simulated outcome
- Actual city state

---

# 6. Decision Engine Requirements

The decision layer must:

- Receive structured decision inputs.
- Evaluate a bounded set of possible decisions.
- Produce structured decisions.
- Return decisions that can be validated by the application.
- Provide sufficient information for decisions to be inspected.
- Support both deterministic and Agentic decision sources.

The decision layer must not directly modify Digital Twin state.

The system must preserve the source of each decision, such as:

```text
DETERMINISTIC
AGENTIC
```

---

# 7. Policy Requirements

The system must have a policy validation step between decisions and simulation actions.

```text
Decision
   ↓
Policy Validation
   ↓
Approved / Rejected
   ↓
Simulation
```

The policy layer must:

- Validate proposed actions.
- Reject unsupported actions.
- Enforce defined constraints.
- Prevent invalid state transitions.
- Produce an auditable validation result.

A rejected decision must not be executed.

Policy validation applies equally to deterministic and Agentic decisions.

---

# 8. Simulation Execution Requirements

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

For Citizen Participation, an intervention may instead be evaluated through simulation before it is considered for execution.

The simulation remains responsible for applying actual state changes.

---

# 9. Agent and Decision Evaluation Requirements

The system must distinguish between **judgment confidence** and **decision quality**.

For Agentic decisions, the system should record:

- Agent observation
- Agent reasoning output where appropriate
- Proposed decision
- Jev judgment
- Jev probability or confidence information
- Model identifier/version
- Policy result
- Action taken
- Simulation outcome
- Evaluation result

The system should support evaluating whether an Agentic decision produced a useful outcome.

For comparable scenarios, deterministic and Agentic decisions should be capable of being evaluated from the same initial Digital Twin state.

The deterministic decision must be treated as a **baseline**, not automatically as the winning decision.

---

# 10. User Interface Requirements

The UI must provide a clear view of the Digital Twin.

## 10.1 Shared Map

The main interface must provide:

- Mannheim map
- Roads
- Intersections
- Traffic signals
- Vehicles
- Emergency vehicles
- Relevant incidents
- Citizen reports

---

## 10.2 Traffic Control

The Traffic Control section must initially provide:

```text
Traffic Control

Scenarios
[ Create Emergency ]
```

The emergency action must call the existing emergency scenario API.

The UI must display the resulting emergency vehicle and subsequent simulation state through the existing Digital Twin visualization.

---

## 10.3 Citizen Participation

The Citizen Participation section must provide a map-first interaction model.

The initial capability must allow a citizen to:

1. Select a location on the map.
2. Choose a request type.
3. Enter a description.
4. Submit the request.
5. See that the request has been registered.
6. Observe the subsequent Agentic processing.

---

## 10.4 Agentic State

The UI should expose relevant Agentic activity, including:

- Active agent
- Citizen request
- Agent assessment
- Tools or city information consulted
- Jev judgment
- Proposed intervention
- Policy result
- Simulation result
- Evaluation

The UI does not need to expose internal chain-of-thought or private reasoning.

It should expose meaningful decisions, evidence, explanations, and results.

---

## 10.5 Event Timeline

The system should display important events chronologically.

Example:

```text
Citizen report received
Agent started investigation
Relevant city data collected
Jev judgment produced
Intervention proposed
Policy evaluated
Simulation executed
Outcome evaluated
Citizen feedback generated
```

Traffic Control events should remain visible as well.

---

# 11. Observability Requirements

The system must make important system activity observable.

At minimum, the following should be traceable:

```text
Event
  ↓
Observation
  ↓
Decision / Judgment
  ↓
Policy Validation
  ↓
Action
  ↓
State Change
  ↓
Outcome
```

For Citizen Participation:

```text
Citizen Request
  ↓
Agent Run
  ↓
Agent Assessment
  ↓
Jev Judgment
  ↓
Proposal
  ↓
Policy
  ↓
Simulation
  ↓
Evaluation
  ↓
Citizen Feedback
```

The system should make it possible to understand **why an action or recommendation occurred**, without exposing private model reasoning.

---

# 12. Data Requirements

The system must distinguish between the following concerns.

## 12.1 Geographic Data

Represents the physical structure of Mannheim.

Examples:

- Roads
- Intersections
- Geographic coordinates
- Road geometry

## 12.2 Simulation State

Represents the current virtual state.

Examples:

- Vehicle positions
- Traffic signal states
- Incidents
- Simulation time

## 12.3 Citizen Request State

Represents citizen participation.

Examples:

- Incident reports
- Suggestions
- Geographic location
- Request status
- Agent processing status

## 12.4 Agent State

Represents the operational state of agents.

Examples:

- Observation
- Assessment
- Decision
- Action
- Status

## 12.5 Decision and Judgment Records

Represents decisions and bounded judgments.

Examples:

- Decision source
- Decision type
- Jev question
- Jev result
- Probability
- Confidence where applicable
- Model/version
- Policy result
- Outcome evaluation

These concerns must remain logically separated.

---

# 13. Non-Functional Requirements

## 13.1 Reproducibility

Predefined deterministic scenarios should produce reproducible results where deterministic behavior is expected.

Agentic scenarios should preserve sufficient inputs and model information to make their execution traceable.

---

## 13.2 Extensibility

The system should allow additional:

- Agents
- Agent capabilities
- Scenarios
- Entity types
- Decision types
- Policies
- Simulation behaviors
- Citizen request types
- Evaluation metrics

without redesigning the complete system.

---

## 13.3 Observability

Important state changes, agent runs, decisions, judgments, policy results, and outcomes should be visible and traceable.

---

## 13.4 Local Development

The MVP should be runnable locally without mandatory paid cloud services.

External AI services may be configurable dependencies for Agentic capabilities.

The Traffic Control functionality must remain usable without mandatory LLM availability.

---

## 13.5 Performance

The system should support a visually smooth simulation for the MVP scenarios and selected Mannheim area.

Agentic processing may be asynchronous and does not need to block map rendering or simulation updates.

---

## 13.6 Maintainability

The implementation should maintain clear boundaries between:

- UI
- API
- Digital Twin
- Simulation
- Events
- Agents
- LLM integration
- Decision-making
- Jev judgment
- Policy validation
- Evaluation
- Persistence

---

## 13.7 Safety

AI-generated decisions must not directly modify authoritative system state.

All executable actions must pass through defined application controls.

Citizen-submitted content must be treated as untrusted input.

AI-generated recommendations must be clearly distinguishable from authoritative city state.

---

# 14. Constraints

The MVP intentionally avoids:

- Real-time Mannheim traffic feeds
- Real municipal infrastructure
- Production traffic control
- Real emergency-service integration
- Direct control of municipal systems
- City-wide Digital Twin modeling
- Complex traffic optimization
- Autonomous vehicle control
- Large-scale distributed infrastructure
- Unnecessary external services
- Using LLMs for deterministic problems where they provide no meaningful value

The objective is to demonstrate the architecture with the smallest meaningful system.

---

# 15. MVP Acceptance Criteria

The MVP consists of two primary end-to-end flows.

## 15.1 Traffic Control Flow

The following flow must work:

```text
Mannheim Map
     ↓
Digital Twin
     ↓
Create Emergency
     ↓
Emergency Vehicle
     ↓
City Event
     ↓
Deterministic Decision
     ↓
Policy Validation
     ↓
Simulation Action
     ↓
Visible State Change
     ↓
Event Timeline
```

A user should be able to create an emergency scenario and observe the resulting traffic behavior through the UI.

---

## 15.2 Citizen Participation Flow

The first Agentic Citizen Participation scenario must support:

```text
Mannheim Map
     ↓
Citizen selects location
     ↓
Incident Report
     ↓
City Event
     ↓
Citizen Participation Agent
     ↓
LLM Interpretation
     ↓
Digital Twin Investigation
     ↓
Jev Judgment
     ↓
Intervention Proposal
     ↓
Policy Validation
     ↓
Simulation / Evaluation
     ↓
Outcome
     ↓
Citizen Feedback
```

A user should be able to submit a geographically located incident and observe the Agentic workflow through the UI.

The system must preserve the complete trace of the workflow.

---

# 16. Requirement Priorities

## Must Have

- Mannheim map
- Digital Twin state
- Virtual vehicles
- Traffic signals
- Simulation engine
- Event-driven behavior
- Existing deterministic decision flow
- Policy validation
- Emergency scenario
- Traffic Control UI
- Create Emergency action
- Citizen incident reporting
- Geographic association of citizen reports
- Citizen Participation Agent
- LLM integration for the initial citizen scenario
- Bounded Jev judgment
- Agentic decision/proposal
- Event timeline
- Agentic workflow observability

## Should Have

- Citizen suggestions
- Multiple citizen request types
- Related incident detection
- Agent inspector
- Jev decision inspector
- Simulation-based intervention comparison
- Decision/outcome evaluation
- Deterministic versus Agentic evaluation
- Deterministic scenario replay

## Could Have

- Multiple cooperating agents
- Human approval step
- Additional city services
- More complex traffic behavior
- Historical simulation replay
- Citizen feedback loops
- Collective citizen intelligence

## Will Not Have in MVP

- Real-time Mannheim traffic
- Real-world traffic control
- Production municipal integration
- Direct municipal infrastructure control
- City-wide simulation
- Autonomous vehicle control
- Traffic optimization research
- Large-scale multi-agent city simulation
- Unbounded autonomous agent actions
