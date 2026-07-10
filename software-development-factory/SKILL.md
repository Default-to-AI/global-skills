---
name: software-development-factory
description: Guidance on creating a system of specialized AI agents for autonomous software development workflows
version: 1.0.0
---
# Software Development Factory Skill

## Overview
This skill provides guidance on creating and managing a system of specialized AI agents that work together autonomously to handle software development tasks from concept to delivery. Inspired by the "dark factory" concept (fully automated, always operational), this approach models a software development team where agents are always ready to accept new ideas and process them through defined workflows.

## When to Use
- When tasked with building software systems, applications, or MVPs
- When the user wants a team-like approach to software development with specialized roles
- When automating software development workflows is desired
- When creating prototypes or proof-of-concepts that require multiple specialized skills
- When the user emphasizes "always ready" or "24/7" availability for development work

## Core Concept
A software development factory consists of:
1. **Orchestrator Agent**: Acts as product manager/technical lead - accepts ideas, creates specifications, manages workflow
2. **Specialized Agents**: Domain experts that handle specific aspects of development:
   - Architecture Agent: System design, technology selection, data modeling
   - Frontend Agent: UI/UX development, state management, responsiveness
   - Backend Agent: API development, databases, business logic
   - DevOps Agent: Infrastructure, CI/CD, containerization, monitoring
   - QA Agent: Test planning, automation, quality assurance
   - Documentation Agent: API docs, user guides, release notes

## Implementation Steps

### 1. Set up Communication Infrastructure
Create directories for agent communication:
- `registrations/` - Agent registration files
- `heartbeats/` - Agent heartbeat files (liveness signals)
- `tasks/` - Task assignments from orchestrator to agents
- `results/` - Task completion reports from agents
- `specs/` - Feature specifications

### 2. Create Agent Base Class
All agents should inherit from a common base class that handles:
- Self-registration with the orchestrator
- Periodic heartbeat signaling
- Polling for assigned tasks
- Executing tasks via abstract `execute_task` method
- Reporting results

### 3. Implement the Orchestrator Agent
The orchestrator should:
- Accept high-level ideas and convert them to detailed specifications
- Break specifications into agent-specific tasks
- Maintain a task queue and prioritize work
- Monitor agent registrations and heartbeats
- Assign tasks to available agents
- Collect and process results
- Handle agent failures via heartbeat timeouts

### 4. Implement Specialized Agents
Each agent type should:
- Inherit from the base agent class
- Implement `execute_task` method for their domain
- Handle task-specific logic and simulate/work on actual implementation
- Return structured results or raise exceptions on failure

### 5. Define Clear Message Formats
Use JSON files for all communication:
- **Registration**: `{agent_id, agent_type, capabilities, timestamp}`
- **Heartbeat**: `{agent_id, timestamp}`
- **Task**: `{task_id, agent_id, agent_type, payload, timestamp}`
- **Result**: `{task_id, agent_id, status, result, timestamp}`
- **Specification**: `{spec_id, idea, created_at, priority, status, requirements, user_stories, acceptance_criteria}`

### 6. Establish Workflow Flow
1. Idea ingestion → Specification creation
2. Specification breakdown → Task queue population
3. Task assignment → Agent execution
4. Result collection → Status updates
5. Heartbeat monitoring → Failure detection/recovery
6. Continuous registration → Agent discovery

## Pitfalls to Avoid
- **Taking metaphors too literally**: When users describe systems using metaphors like "dark factory", "assembly line", or "pipeline" in software contexts, they often mean automated workflows that are always ready and responsive, not literal industrial processes. This was a key correction in this session - the user intended a software development workflow system, not actual factory automation. Always clarify the domain and intended meaning when metaphors are used.
- **Overcomplicating task breakdown**: Start with simple, well-defined tasks that match agent specialties
- **Neglecting heartbeat monitoring**: Agent failure detection is crucial for system reliability
- **Creating tight coupling**: Keep agent communication strictly through the defined file-based interface
- **Ignoring task prioritization**: Not all tasks are equal; implement basic priority handling
- **Forgetting to clean up task/result files**: Proper file management prevents reprocessing
- **Making agents too rigid**: Allow agents to handle multiple related task subtypes
- **Neglecting error handling**: Agents should gracefully handle and report task failures

## Key Principles
- **Always Ready**: Agents continuously poll for work and send heartbeats
- **Specialization**: Each agent has deep expertise in their domain
- **Autonomy**: Agents can operate independently once assigned a task
- **Coordination**: Orchestrator manages workflow without micromanaging
- **Visibility**: All communication is traceable through the file system
- **Extensibility**: New agent types can be added without changing core logic
- **Conciseness**: Value direct, actionable information over verbose explanations (per user preference)

## Reference Files
See `references/` directory for:
- `communication_protocol.md`: Detailed message formats and examples
- `workflow_examples.md`: Sample workflow traces and scenarios
- `agent_responsibilities.md`: Detailed breakdown of each agent's role
- `pitfalls_and_solutions.md`: Common issues and how to address them

## Example Usage
1. Start the orchestrator agent
2. Start desired specialized agents (architecture, frontend, backend, etc.)
3. Submit ideas via the orchestrator's input mechanism
4. Monitor progress through generated result files
5. Retrieve completed work from agent outputs

## Related Skills
- `hermes-agent`: For understanding Hermes agent framework basics
- `planning-with-files`: For structured approaches to complex tasks
- `superpowers/dispatching-parallel-agents`: For parallel execution concepts