# Tutorial · Agents

## Why it exists

An agent is a model in a loop with **tools**, not a library name.
Lab 10 makes you write the loop so that LangGraph or an SDK later
is a convenience, not the idea.

## The idea

The smallest agent is:

```
while not done and steps < cap:
    thought (optional, inspectable)
    action = choose a tool and arguments  # structured
    if action is finish: break
    observation = run the tool
    append observation to the window
```

ReAct (Yao et al., 2022) named the thought-action-observation
rhythm. Production systems often hide the thought, but they still
need a **schema** for the action (lab 11) and a **hard cap** on
steps. Without a cap, a confused model is an infinite bill (O3).

**Tools** are functions with JSON Schema, side-effect notes, and
timeouts (O2). MCP (Model Context Protocol) is a way to **expose**
those tools over a standard transport (E9). A2A and similar
proposals are about agents talking to agents. None of that replaces
the loop. If you cannot write the loop, you cannot debug the
framework.

Memory is not the context window stuffed with the whole Slack
history (E11). Short-term: the transcript. Long-term: retrieve.
"The agent remembers" is usually RAG over past notes, or a lie.

Multi-agent diagrams are optional. A second role is justified when
you can name a different tool set or a different eval, not when
you want a prettier picture.

## The gap most tutorials leave

They `pip install` a framework and never log the tool arguments.
They let the model emit free-text "API calls." They have no step
budget, no allowlist, and no eval (can the task complete without
the model inventing a tool?).

## How the lab should feel

Lab 10 should feel almost too small: a toy environment, a thought,
an action, an observation, a finish. You will want to import a
framework. Do not, until the toy works and you can inject a
**bad observation** and see the next action. That injection is
how you understand E8 later: tool output is untrusted text.

## Practice

1. `10_react_agent.ipynb`. Then `11_structured_output.ipynb` so
   actions are JSON, not vibes.
2. Add a step cap and a tool allowlist on paper for a product you
   like. Write which tools are read-only and which need an
   approval gate (L4 / Distilled).
3. Optional: one MCP server from the Hugging Face MCP course,
   after E9. Still log every tool call.

## Watch and read

- Yao et al., ReAct, 2022, [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
- Anthropic, *Building effective agents* (public engineering blog)
- Hugging Face Agents Course and MCP Course
  ([COURSES.md](../reference/COURSES.md))
- LangGraph docs as a state-machine implementation of the same
  loop ([TOOLS.md](../reference/TOOLS.md))
- E5 and E9 in this course

## Knowledge check

1. What is the minimum loop, without a framework?
2. Why is a step cap an SLO issue as well as a quality issue?
3. Why must tool outputs be treated as untrusted in the window?
4. When is a second agent justified?
5. What does MCP add that ReAct did not already name?

<details>
<summary>Answers</summary>

1. Repeat: choose a structured action or finish, run the tool,
   append the observation, until finish or cap.
2. Each step is latency and tokens. Unbounded loops blow p95 and
   the bill.
3. They are data from the world (or an attacker). The model will
   follow instructions that appear there unless you isolate and
   test (E8, lab 14).
4. When you can name a different permission set or eval, and a
   single loop with two tools would mix those permissions badly.
5. A standard way to describe and host tools/resources for many
   clients. The control loop remains yours.

</details>
