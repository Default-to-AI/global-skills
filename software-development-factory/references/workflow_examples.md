# Workflow Examples for Software Development Factory

## Example 1: Simple CRUD Application

### Input Idea
"Create a task management application with user authentication and CRUD operations for tasks"

### Workflow Trace

1. **Idea Submission**
   - User tells orchestrator: "Create a task management application with user authentication and CRUD operations for tasks"
   - Orchestrator adds to idea queue

2. **Specification Creation**
   - Orchestrator creates spec: `specs/abc123.json`
   - Contains:
     - Idea description
     - Priority: Medium
     - Status: Draft
     - Empty requirements/user_stories/acceptance_criteria (to be filled during processing)

3. **Specification Processing**
   - Orchestrator's spec processor:
     - Reads spec
     - Breaks into tasks:
       ```
       [
         (ARCHITECTURE, {
           "spec_id": "abc123",
           "task_type": "system_design",
           "description": "Design system architecture for task management app",
           "details": { /* architecture specifics */ }
         }),
         (BACKEND, {
           "spec_id": "abc123",
           "task_type": "api_development",
           "description": "Develop REST API for tasks and users",
           "details": {
             "endpoints": [
               {"method": "POST", "path": "/auth/register", "description": "User registration"},
               {"method": "POST", "path": "/auth/login", "description": "User login"},
               {"method": "GET", "path": "/tasks", "description": "Get all tasks"},
               {"method": "POST", "path": "/tasks", "description": "Create task"},
               {"method": "GET", "path": "/tasks/{id}", "description": "Get task by ID"},
               {"method": "PUT", "path": "/tasks/{id}", "description": "Update task"},
               {"method": "DELETE", "path": "/tasks/{id}", "description": "Delete task"}
             ]
           }
         }),
         (FRONTEND, {
           "spec_id": "abc123",
           "task_type": "ui_development",
           "description": "Create user interface for task management",
           "details": {
             "pages": ["Login", "Dashboard", "Task List", "Task Form"],
             "components": ["Header", "TaskCard", "Form", "Button"]
           }
         }),
         (QA, {
           "spec_id": "abc123",
           "task_type": "test_planning",
           "description": "Create test plan for task management app",
           "details": {
             "test_types": ["unit", "integration", "e2e"],
             "coverage_target": 80
           }
         }),
         (DEVOPS, {
           "spec_id": "abc123",
           "task_type": "setup_ci_cd",
           "description": "Set up CI/CD pipeline for deployment",
           "details": {
             "platform": "GitHub Actions",
             "stages": ["test", "build", "deploy"],
             "environments": ["staging", "production"]
           }
         }),
         (DOCUMENTATION, {
           "spec_id": "abc123",
           "task_type": "create_docs",
           "description": "Create documentation for task management app",
           "details": {
             "docs_to_create": ["API Documentation", "User Guide", "Developer Setup"]
           }
         })
       ]
       ```

4. **Task Assignment**
   - As agents register and send heartbeats, orchestrator assigns tasks:
     - Architecture agent gets architecture task
     - Backend agent gets API task
     - Frontend agent gets UI task
     - QA agent gets test planning task
     - DevOps agent gets CI/CD task
     - Documentation agent gets documentation task

5. **Task Execution (Example: Backend Agent)**
   - Backend agent receives task file
   - Executes `execute_task("backend", payload)`:
     - Simulates API development (2-5 seconds)
     - Creates mock endpoints for auth and CRUD operations
     - Returns result:
       ```json
       {
         "task_id": "task_xyz",
         "agent_id": "backend_agent_001",
         "status": "completed",
         "result": {
           "endpoints_created": [
             {"method": "POST", "path": "/auth/register"},
             {"method": "POST", "path": "/auth/login"},
             {"method": "GET", "path": "/tasks"},
             {"method": "POST", "path": "/tasks"},
             {"method": "GET", "path": "/tasks/{id}"},
             {"method": "PUT", "path": "/tasks/{id}"},
             {"method": "DELETE", "path": "/tasks/{id}"}
           ],
           "authentication": "JWT-based",
           "database_schema": {
             "users": {"id": "UUID", "email": "String", "password_hash": "String"},
             "tasks": {"id": "UUID", "user_id": "UUID", "title": "String", "description": "Text", "completed": "Boolean", "created_at": "Timestamp"}
           }
         },
         "timestamp": 1234567895.0
       }
       ```

6. **Result Collection**
   - Orchestrator detects result file
   - Updates backend agent status to idle
   - Logs completion

7. **Continued Processing**
   - Other agents work on their tasks in parallel
   - Once all tasks complete, system is ready for next idea

### Outcome
- Functional task management API with authentication
- React frontend with login/dashboard/task views
- Test plan covering unit/integration/e2e tests
- CI/CD pipeline configured for GitHub Actions
- API documentation, user guide, and developer setup instructions

## Example 2: Real-time Feature Addition

### Input Idea
"Add real-time notifications using WebSockets to the existing task management application"

### Workflow Trace

1. **Idea Submission**
   - User: "Add real-time notifications using WebSockets to the existing task management application"
   - Orchestrator queues idea

2. **Specification Creation**
   - Spec created referencing existing system (could load previous spec)
   - Focus: WebSocket notification feature

3. **Specification Processing**
   - Tasks generated:
     ```
     [
       (ARCHITECTURE, {
         "spec_id": "def456",
         "task_type": "architecture_extension",
         "description": "Extend architecture for WebSocket notifications",
         "details": {
           "new_components": ["NotificationService", "WebSocketHandler"],
           "connections": ["WebSocketHandler <-> NotificationService <-> Task Service"]
         }
       }),
       (BACKEND, {
         "spec_id": "def456",
         "task_type": "websocket_implementation",
         "description": "Implement WebSocket endpoints for real-time notifications",
         "details": {
           "endpoints": [
             {"path": "/ws/notifications", "description": "WebSocket connection for notifications"}
           ],
           "message_types": ["task_created", "task_updated", "task_dead", "task_deadline_approaching"]
         }
       }),
       (FRONTEND, {
         "spec_id": "def456",
         "task_type": "websocket_integration",
         "description": "Integrate WebSocket client in frontend for notifications",
         "details": {
           "connection_logic": "Auto-reconnect on disconnect",
           "ui_components": ["NotificationBell", "NotificationDropdown"],
           "state_updates": ["Add notification to store", "Show badge count"]
         }
       }),
       (QA, {
         "spec_id": "def456",
         "task_type": "websocket_testing",
         "description": "Test WebSocket functionality",
         "details": {
           "test_scenarios": ["connection", "disconnection", "message_delivery", "reconnection"]
         }
       }),
       (DEVOPS, {
         "spec_id": "def456",
         "task_type": "update_deployment",
         "description": "Update deployment for WebSocket support",
         "details": {
           "changes": ["Add WebSocket proxy configuration", "Update health checks"],
           "platform": "Kubernetes"
         }
       }),
       (DOCUMENTATION, {
         "spec_id": "def456",
         "task_type": "update_docs",
         "description": "Update documentation for WebSocket feature",
         "details": {
           "sections_to_update": ["API Documentation", "Developer Guide", "Architecture Overview"]
         }
       })
     ]
     ```

4. **Parallel Execution**
   - All agents work simultaneously on their WebSocket-related tasks
   - Backend implements WebSocket server with Socket.io or ws library
   - Frontend adds Socket.io client and notification UI
   - QA tests connection handling and message delivery
   - DevOps updates nginx/ingress configs for WebSocket support
   - Documentation adds WebSocket API section

### Outcome
- Real-time notification system integrated
- Users see instant updates when tasks change
- System maintains backward compatibility
- Documentation reflects new capabilities

## Example 3: Performance Optimization Sprint

### Input Idea
"Improve application response time by 50% through caching and database optimization"

### Workflow Trace

1. **Idea Submission**
   - Performance optimization request

2. **Specification Creation**
   - Focus: Identify bottlenecks and implement fixes

3. **Specification Processing**
   - Tasks generated:
     ```
     [
       (ANALYTICS, {
         "spec_id": "ghi789",
         "task_type": "performance_analysis",
         "description": "Analyze current performance bottlenecks",
         "details": {
           "tools": ["New Relic", "Chrome DevTools", "EXPLAIN ANALYZE"],
           "metrics": ["response_time", "throughput", "error_rate", "database_query_time"]
         }
       }),
       (BACKEND, {
         "spec_id": "ghi789",
         "task_type": "database_optimization",
         "description": "Optimize database queries and add indexes",
         "details": {
           "slow_queries": ["SELECT * FROM tasks WHERE user_id = ? AND created_at > ?"],
           "indexes_to_add": ["user_id_created_at_idx", "status_assignee_idx"],
           "query_improvements": ["Add WHERE clauses", "Limit result sets"]
         }
       }),
       (BACKEND, {
         "spec_id": "ghi789",
         "task_type": "implement_caching",
         "description": "Add Redis caching for frequently accessed data",
         "details": {
           "cache_strategies": ["user_profile_cache", "recent_tasks_cache"],
           "ttl_values": {"user_profile": 3600, "recent_tasks": 300},
           "cache_invalidation": ["on_user_update", "on_task_create/update/delete"]
         }
       }),
       (FRONTEND, {
         "spec_id": "ghi789",
         "task_type": "optimize_assets",
         "description": "Optimize frontend performance",
         "details": {
           "techniques": ["code_splitting", "lazy_loading", "image_optimization"],
           "targets": ["initial_load_time", "time_to_interactive"]
         }
       }),
       (DEVOPS, {
         "spec_id": "ghi789",
         "task_type": "monitoring_setup",
         "description": "Set up performance monitoring",
         "details": {
           "metrics_to_track": ["page_load_time", "api_response_time", "database_query_time"],
           "alerting": ["response_time > 2s for 5 minutes"]
         }
       }),
       (QA, {
         "spec_id": "ghi789",
         "task_type": "performance_testing",
         "description": "Verify performance improvements",
         "details": {
           "baseline": "Current response time",
           "target": "50% reduction",
           "test_scenarios": ["high_user_load", "large_dataset", "concurrent_operations"]
         }
       })
     ]
     ```

4. **Execution & Results**
   - After implementation:
     - Database queries optimized with proper indexes
     - Redis cache reduces database load by 70%
     - Frontend bundle size reduced by 40% via code splitting
     - Response time improved from 1200ms to 550ms (>50% improvement)
     - Monitoring alerts configured for regression detection

### Outcome
- Measurable performance improvement achieved
- Monitoring in place to detect regressions
- Documentation updated for new caching layer
- Tests verify performance targets met

These examples demonstrate how the software development factory processes different types of requests:
1. New feature development (CRUD app)
2. Feature enhancement (real-time notifications)
3. Optimization work (performance improvements)

Each follows the same core workflow but adapts task types and details to the specific request.