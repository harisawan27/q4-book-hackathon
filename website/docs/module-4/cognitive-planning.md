---
id: cognitive-planning
title: Cognitive Planning with LLMs
sidebar_label: Cognitive Planning
description: Integrating LLMs into the robotic control loop.
---

# Cognitive Planning

## The Role of the Planner

The **Planner** is responsible for high-level logic. It does not know *how* to move the arm (that's the Controller's job), but it knows *what* needs to be done.

## Prompt Engineering for Robotics

We can't just ask ChatGPT "clean the room." We need structured output.

### System Prompt Example

```text
You are a robotic planner. 
Available Skills: [Pick(obj), Place(obj, loc), Navigate(loc), Scan()].
Environment: Kitchen with [Apple, Sponge, Can, Table, Bin].

Task: "Throw away the soda."

Output Format: JSON List of strings.
```

### Expected Output

```json
["Scan()", "Navigate(Table)", "Pick(Can)", "Navigate(Bin)", "Place(Can, Bin)"]
```

## Parsing & Execution

A Python node `llm_planner.py` handles this:
1.  Sends prompt to LLM API (OpenAI/Local Llama).
2.  Receives JSON.
3.  Parses list.
4.  Sends Action Goal `Pick(Can)` to the behavior tree.
5.  Waits for success/failure before sending the next command.

## Failure Recovery

If `Pick(Can)` fails (returns `Result: FAILED`), the planner must adapt.

**New Prompt**: 
"History: [Pick(Can) -> FAILED]. Status: Can slipped. What next?"

**LLM Response**: 
`["Scan()", "Pick(Can)"]` (Retry) or `["CallHuman()"]` (Escalate).