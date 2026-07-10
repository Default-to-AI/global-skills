# Communication Protocol for Software Development Factory

## Message Formats

All communication between orchestrator and agents uses JSON files in designated directories.

### 1. Agent Registration
When an agent starts, it registers with the orchestrator by creating a file in `registrations/`:

**File:** `registrations/<agent_id>.json`
```json
{
  "agent_id": "unique_agent_identifier",
  "agent_type": "architecture|frontend|backend|devops|qa|documentation",
  "capabilities": ["capability1", "capability2", ...],
  "timestamp": 1234567890.0
}
```

**Example:**
```json
{
  "agent_id": "frontend_agent_001",
  "agent_type": "frontend",
  "capabilities": ["ui_development", "state_management", "responsive_design", "accessibility"],
  "timestamp": 1717020000.0
}
```

### 2. Agent Heartbeat
Agents periodically send heartbeats to indicate liveness by creating/updating files in `heartbeats/`:

**File:** `heartbeats/<agent_id>.json`
```json
{
  "agent_id": "unique_agent_identifier",
  "timestamp": 1234567890.0
}
```

**Example:**
```json
{
  "agent_id": "frontend_agent_001",
  "timestamp": 1717020005.0
}
```

### 3. Task Assignment
The orchestrator assigns tasks to agents by creating files in `tasks/<agent_type>/<agent_id>/`:

**File:** `tasks/<agent_type>/<agent_id>/<task_id>.json`
```json
{
  "task_id": "unique_task_identifier",
  "agent_id": "agent_id",
  "agent_type": "architecture",
  "payload": { /* task-specific data */ },
  "timestamp": "2023-01-01T12:00:00Z"
}
```

**Example (Architecture task):**
```json
{
  "task_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
  "agent_id": "architecture_agent_001",
  "agent_type": "architecture",
  "payload": {
    "spec_id": "s1t2u3v4-w5x6-y7z8-a9b0-c1d2e3f4g5h6",
    "task_type": "system_design",
    "description": "Design system architecture for task management app",
    "details": {
      "components": ["API Gateway", "Auth Service", "User Service", "Data Service"],
      "tech_stack": {
        "backend": "Node.js with Express",
        "database": "PostgreSQL",
        "frontend": "React with TypeScript"
      }
    }
  },
  "timestamp": "2023-01-01T12:00:00Z"
}
```

### 4. Task Results
Agents report task completion (success or failure) by creating files in `results/`:

**File:** `results/<task_id>.json`
```json
{
  "task_id": "unique_task_identifier",
  "agent_id": "agent_id",
  "status": "completed|failed",
  "result": { /* task-specific result data */ },
  "timestamp": 1234567890.0
}
```

**Example (Success):**
```json
{
  "task_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
  "agent_id": "architecture_agent_001",
  "status": "completed",
  "result": {
    "deliverables": {
      "architecture_diagram": "C4 Container diagram created",
      "component_specs": ["User Service", "Order Service", "Payment Service", "Notification Service"],
      "technology_choices": {
        "frontend": "React with TypeScript",
        "backend": "Node.js with Express",
        "database": "PostgreSQL",
        "caching": "Redis",
        "messaging": "RabbitMQ"
      }
    }
  },
  "timestamp": 1717020010.0
}
```

**Example (Failure):**
```json
{
  "task_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
  "agent_id": "architecture_agent_001",
  "status": "failed",
  "result": {
    "error": "Insufficient requirements to create architecture design"
  },
  "timestamp": 1717020010.0
}
```

### 5. Specification Storage
The orchestrator stores feature specifications in `specs/`:

**File:** `specs/<spec_id>.json`
```json
{
  "spec_id": "unique_spec_identifier",
  "idea": "Original idea description",
  "created_at": "2023-01-01T12:00:00Z",
  "priority": 0,
  "status": "draft|in_progress|completed",
  "requirements": ["requirement1", "requirement2", ...],
  "user_stories": ["story1", "story2", ...],
  "acceptance_criteria": ["criterion1", "criterion2", ...]
}
```

**Example:**
```json
{
  "spec_id": "s1t2u3v4-w5x6-y7z8-a9b0-c1d2e3f4g5h6",
  "idea": "Create a user management system with CRUD operations",
  "created_at": "2023-01-01T12:00:00Z",
  "priority": 1,
  "status": "in_progress",
  "requirements": [
    "Users must be able to register accounts",
    "Users must be able to log in and out",
    "Users can create, read, update, and delete tasks",
    "Task data must persist between sessions"
  ],
  "user_stories": [
    "As a user, I want to register so that I can use the application",
    "As a user, I want to log in so that I can access my tasks",
    "As a user, I want to create tasks so that I can track my work",
    "As a user, I want to update tasks so that I can mark progress",
    "As a user, I want to delete tasks so that I can remove completed work"
  ],
  "acceptance_criteria": [
    "Registration form validates email and password strength",
    "Login succeeds with correct credentials",
    "Users can create tasks with title and description",
    "Task list shows all user's tasks",
    "Completed tasks can be marked as done",
    "Deleted tasks are removed from the list"
  ]
}
```

## Directory Structure
```
software_factory/
├── registrations/          # Agent registration files
│   ├── architecture_agent_001.json
│   ├── frontend_agent_001.json
│   └── ...
├── heartbeats/             # Agent heartbeat files
│   ├── architecture_agent_001.json
│   ├── frontend_agent_001.json
│   └── ...
├── tasks/                  # Task assignments (organized by type/agent)
│   ├── architecture/
│   │   ├── architecture_agent_001/
│   │   │   ├── a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8.json
│   │   │   └── ...
│   ├── frontend/
│   │   └── ...
│   └── ...
├── results/                # Task completion reports
│   ├── a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8.json
│   └── ...
├── specs/                  # Feature specifications
│   ├── s1t2u3v4-w5x6-y7z8-a9b0-c1d2e3f4g5h6.json
│   └── ...
└── (agent implementations)
```

## Communication Flow
1. Agent starts → creates registration file in `registrations/`
2. Agent periodically → updates heartbeat file in `heartbeats/`
3. Orchestrator → creates task file in `tasks/<type>/<id>/<task_id>.json`
4. Agent detects task file → processes it → creates result file in `results/`
5. Orchestrator detects result file → updates status → removes result file
6. Agent completes task → removes task file from `tasks/<type>/<id>/`

## Error Handling
- Malformed JSON files are logged and ignored
- Missing required fields result in error responses
- Timeout detection via heartbeat staleness (>HEARTBEAT_TIMEOUT seconds)
- Failed tasks are logged but not automatically retried (configurable)