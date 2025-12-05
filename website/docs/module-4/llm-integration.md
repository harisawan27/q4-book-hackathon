---
id: llm-integration
title: LLM Integration Guide
sidebar_label: LLM Integration
description: Connecting ROS 2 to OpenAI and Llama 3.
---

# LLM Integration Guide

## Option A: Cloud API (OpenAI)

Easiest to start, requires internet.

```python
import openai

client = openai.OpenAI(api_key="sk-...")

def get_plan(instruction):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a robot planner..."},
            {"role": "user", "content": instruction}
        ]
    )
    return response.choices[0].message.content
```

## Option B: Local Inference (Ollama)

Runs on the workstation GPU. Privacy-friendly and free.

1.  Install Ollama: `curl -fsSL https://ollama.com/install.sh`
2.  Pull Model: `ollama pull llama3`
3.  Python Client:

```python
import requests
import json

def get_plan_local(instruction):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3",
        "prompt": instruction,
        "stream": False
    }
    response = requests.post(url, json=data)
    return json.loads(response.text)['response']
```

## Safety Layer

**Never** pipe LLM output directly to motor control.
-   The LLM output must be parsed into a strict set of allowed high-level actions.
-   The low-level controller (MoveIt/Nav2) handles collision avoidance and safety limits.
-   If the LLM hallucinates "Fly to the moon", the parser should throw an `InvalidActionError`.