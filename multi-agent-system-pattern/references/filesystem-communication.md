# Filesystem Communication Pattern for Multi-Agent Systems

## Overview
This document details the filesystem-based communication mechanism used in the multi-agent system pattern. This approach provides loose coupling between agents and the orchestrator through simple file operations.

## Communication Channels

### 1. Registration Channel
- **Directory**: `registrations/`
- **File Format**: `<agent_id>.json`
- **Purpose**: Agents announce their presence and capabilities
- **Written by**: Agents (on startup)
- **Read by**: Orchestrator (continuously monitors)
- **Contents**:
  ```json
  {
    "agent_id": "unique_identifier",
    "agent_type": "assembly|qc|logistics|maintenance",
    "capabilities": ["capability1", "capability2"],
    "timestamp": 1234567890.123
  }
  ```

### 2. Heartbeat Channel
- **Directory**: `heartbeats/`
- **File Format**: `<agent_id>.json`
- **Purpose**: Signal agent liveness
- **Written by**: Agents (periodically)
- **Read by**: Orchestrator (continuously monitors)
- **Contents**:
  ```json
  {
    "agent_id": "unique_identifier",
    "timestamp": 1234567890.123
  }
  ```

### 3. Task Channel
- **Directory Structure**: `tasks/<agent_type>/<agent_id>/`
- **File Format**: `<task_id>.json`
- **Purpose**: Deliver work assignments to agents
- **Written by**: Orchestrator (when assigning tasks)
- **Read by**: Agents (polling their specific directory)
- **Contents**:
  ```json
  {
    "task_id": "unique_task_identifier",
    "agent_id": "target_agent_id",
    "agent_type": "assembly",
    "payload": {
      // Task-specific data
    },
    "timestamp": "2023-01-01T12:00:00Z"
  }
  ```

### 4. Result Channel
- **Directory**: `results/`
- **File Format**: `<task_id>.json`
- **Purpose**: Report task completion/status
- **Written by**: Agents (after task execution)
- **Read by**: Orchestrator (continuously monitors)
- **Contents**:
  ```json
  {
    "task_id": "unique_task_identifier",
    "agent_id": "reporting_agent_id",
    "status": "completed|failed",
    "result": {
      // Success data OR error information
    },
    "timestamp": "2023-01-01T12:00:00Z"
  }
  ```

## Communication Flow

### Agent Lifecycle
1. **Startup**: Agent writes registration file to `registrations/`
2. **Heartbeat**: Agent periodically writes to `heartbeats/<agent_id>.json`
3. **Task Processing**:
   - Agent polls `tasks/<agent_type>/<agent_id>/` for new files
   - On finding a task file, reads it and executes the work
   - Writes result to `results/<task_id>.json`
   - Deletes the task file to mark as processed
4. **Shutdown**: Agent stops heartbeat and exits (registration remains until timeout)

### Orchestrator Responsibilities
1. **Registration Monitoring**: 
   - Watches `registrations/` for new files
   - When found, reads and adds to agent registry
   - Removes file after processing to avoid duplicate registration

2. **Heartbeat Monitoring**:
   - Watches `heartbeats/` for updates
   - Updates agent's last_seen timestamp
   - Marks agents as offline if no heartbeat within timeout
   - Optionally requeues tasks from offline agents

3. **Task Dispatching**:
   - Maintains priority queue of pending tasks
   - Matches tasks to available agents (by type and status)
   - Writes task files to appropriate `tasks/<agent_type>/<agent_id>/` directory
   - Removes task from queue upon assignment

4. **Result Collection**:
   - Watches `results/` for completion files
   - Updates agent status to idle upon result receipt
   - Logs success/failure for monitoring
   - Removes result file after processing (optional)

## Implementation Considerations

### File System Operations
- **Atomic Writes**: Write to temporary file then rename to avoid partial reads
- **File Locking**: Not typically needed as each agent/orchestrator writes to distinct files
- **Error Handling**: Catch and log file I/O errors; system should continue operating
- **Cleanup**: Consider background cleanup of old files to prevent disk exhaustion

### Timing and Delays
- **Heartbeat Interval**: Typically 5-15 seconds (balance responsiveness vs. disk I/O)
- **Timeout Period**: Usually 3x heartbeat interval (e.g., 15-45 seconds)
- **Polling Interval**: Agents typically check for tasks every 1-2 seconds
- **Orchestrator Check Frequency**: Typically 0.5-2 seconds for responsive monitoring

### Scaling Characteristics
- **Horizontal Scaling**: Add more agents of same type to increase throughput
- **Vertical Scaling**: Not applicable; each agent is independent process
- **Bottlenecks**: Filesystem I/O under high task volume; consider message queue for >100 agents
- **Fault Isolation**: Failure of one agent doesn't affect others or orchestrator

## Advantages of This Approach
1. **Simplicity**: No external dependencies, easy to debug and monitor
2. **Transparency**: All communication visible in filesystem
3. **Decoupling**: Agents and orchestrator can be developed/deployed independently
4. **Resilience**: Works across process boundaries and machine boundaries (with shared FS)
5. **Auditability**: Complete history of all interactions available in files

## Limitations
1. **Latency**: Higher than in-memory or socket-based communication
2. **Throughput**: Limited by filesystem write speed under heavy load
3. **Scaling**: Not ideal for thousands of agents sending frequent messages
4. **File System Dependencies**: Behavior may vary across different filesystems/network mounts

## When to Consider Alternatives
Consider replacing with a message queue (RabbitMQ, Redis, Apache Kafka) when:
- You need sub-second latency for task assignment
- You have more than 100 active agents
- You require guaranteed message delivery with acknowledgments
- You need advanced queuing features (priority queues, dead letter exchanges, etc.)
- Your deployment environment doesn't support reliable shared filesystem access

## Best Practices
1. Always use atomic file operations (write to temp, then rename)
2. Include timestamps in all messages for debugging and timeout calculations
3. Design agents to be idempotent where possible (safe to retry)
4. Keep message payloads reasonable size (<1MB) to avoid filesystem strain
5. Implement proper error handling for all file operations
6. Consider adding correlation IDs for tracing complex workflows
7. Monitor disk usage and implement cleanup policies for long-running systems