# Agent Implementation Template

This template provides a starting point for creating new specialized agents in the software development factory.

## Template File: `agents/<agent_type>_agent.py`

```python
import os
import time
import json
import random
import sys
from pathlib import Path

try:
    from agent_base import AgentBase
except ImportError:
    # When run directly, add parent directory to path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from agent_base import AgentBase

class <AgentName>Agent(AgentBase):
    def __init__(self, agent_id):
        super().__init__(agent_id, "<agent_type>", [
            # List your agent's capabilities here
            "<capability1>",
            "<capability2>",
            "<capability3>",
            # Add more as needed
        ])

    def execute_task(self, task_type, payload):
        if task_type != "<agent_type>":
            raise ValueError(f"Unexpected task type: {task_type}")

        # Log task start
        print(f"[{self.agent_id}] Starting {task_type} task: {payload.get('description', 'unknown')}")
        
        # Simulate processing time (adjust range as needed)
        time.sleep(random.uniform(<min_seconds>, <max_seconds>))

        # Simulate potential failure (adjust probability as needed)
        if random.random() < <failure_probability>:
            raise Exception("<descriptive_error_message>")

        # Process the task based on subtype
        task_subtype = payload.get("subtype", "general")
        result = {
            "agent_id": self.agent_id,
            "task_type": task_type,
            "subtype": task_subtype,
            "timestamp": time.time(),
            "status": "completed"
        }

        # Handle different task subtypes
        if task_subtype == "<subtype1>":
            result["deliverables"] = {
                # Add deliverables specific to this subtype
            }
        elif task_subtype == "<subtype2>":
            result["deliverables"] = {
                # Add deliverables specific to this subtype
            }
        else:
            # Default handling for unspecified subtypes
            result["deliverables"] = {
                "<agent_type>_summary": "<agent_type> task progress reported",
                "next_steps": ["Define specific deliverables for this task type"]
            }

        # Log completion
        print(f"[{self.agent_id}] {task_type} task completed: {task_subtype}")
        return result

if __name__ == "__main__":
    # For testing the agent independently
    agent = <AgentName>Agent("<test_agent_id>")
    agent.start()
    try:
        time.sleep(30)  # Run for 30 seconds during testing
    except KeyboardInterrupt:
        pass
    finally:
        agent.stop()
```

## Usage Instructions

1. **Replace placeholders**:
   - `<AgentName>`: Capitalized agent name (e.g., "Authentication")
   - `<agent_type>`: Lowercase agent type matching directory name (e.g., "auth")
   - `<capabilityX>`: Specific capabilities this agent provides
   - `<min_seconds>`/`<max_seconds>`: Processing time range for simulation
   - `<failure_probability>`: Failure rate (0.0 to 1.0, e.g., 0.05 for 5%)
   - `<subtypeX>`: Specific task subtypes this agent handles
   - `<descriptive_error_message>`: Error message for simulated failures
   - `<test_agent_id>`: Test ID when running standalone (e.g., "auth_agent_001")

2. **Place the file**:
   - Save as `agents/<agent_type>_agent.py` in your software development factory directory

3. **Test the agent**:
   - Run directly: `python agents/<agent_type>_agent.py`
   - Should register, send heartbeats, and wait for tasks

4. **Integrate with system**:
   - Ensure agent_base.py is in the parent directory
   - Make sure communication directories exist (registrations, heartbeats, tasks, results)
   - Start orchestrator to begin task distribution

## Example: Authentication Agent

Here's how this template would look for an authentication agent:

```python
class AuthenticationAgent(AgentBase):
    def __init__(self, agent_id):
        super().__init__(agent_id, "auth", [
            "jwt_authentication",
            "oauth_integration",
            "password_security",
            "session_management",
            "multi_factor_auth"
        ])

    def execute_task(self, task_type, payload):
        if task_type != "auth":
            raise ValueError(f"Unexpected task type: {task_type}")

        print(f"[{self.agent_id}] Starting auth task: {payload.get('description', 'unknown')}")
        time.sleep(random.uniform(2, 4))

        if random.random() < 0.05:
            raise Exception("Authentication service unavailable")

        task_subtype = payload.get("subtype", "general")
        result = {
            "agent_id": self.agent_id,
            "task_type": task_type,
            "subtype": task_subtype,
            "timestamp": time.time(),
            "status": "completed"
        }

        if task_subtype == "jwt_setup":
            result["deliverables"] = {
                "secret_key_generated": True,
                "token_expiration": "24h",
                "refresh_token_enabled": True
            }
        elif task_subtype == "oauth_config":
            result["deliverables"] = {
                "providers": ["google", "github", "gitlab"],
                "callback_routes": ["/auth/google/callback", "/auth/github/callback"],
                "scopes": ["profile", "email"]
            }
        else:
            result["deliverables"] = {
                "auth_summary": "Authentication task progress reported",
                "next_steps": ["Define specific auth deliverables"]
            }

        print(f"[{self.agent_id}] Auth task completed: {task_subtype}")
        return result
```

## Customization Tips

1. **Real Implementation**: Replace the simulated work (`time.sleep`) with actual implementation logic when integrating with real systems
2. **Error Handling**: Add specific try/catch blocks for different failure modes
3. **Logging**: Replace print statements with proper logging framework
4. **Configuration**: Externalize configuration (timeouts, retry counts, etc.)
5. **Metrics**: Add performance tracking and reporting capabilities