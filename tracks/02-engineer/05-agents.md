# E5 · Agents

## Why it exists

An agent is a model in a loop with tools, a stop condition, and
a trace. Frameworks multiply. The loop does not. If you cannot
write thought-action-observation by hand, LangGraph will only
hide the bug. Lab 10 is the gate. Import a library after it.

## The idea

### The loop

Yao et al., ReAct ([arXiv:2210.03629](https://arxiv.org/abs/2210.03629)):

1. **Thought.** What to do next, in language the logs can show.
2. **Action.** A tool name and arguments (structured output, E1).
3. **Observation.** The tool's return value, as data, not as a
   new system prompt.
4. Repeat until a **final answer** or a **guard** fires.

That is the whole runtime. Planning and "reflection" are extra
thoughts. Memory is E11. Multi-agent is extra loops with a
router. If the product is one lookup and a sentence, you do
not need this loop. A single structured call is cheaper and
easier to eval.

### Build it without a framework

Lab `10_react_agent.ipynb` is the assignment: a Python `while`
loop, a dict of tools, JSON arguments, a max-step cap, a cost
cap, an allow-list of tool names. Traces print every thought,
action, and observation. That trace is the debugger.

Guards that belong in *your* code, not in the prompt:

- Max steps and max tokens.
- Tool allow-list and argument schema validation.
- Timeouts and idempotency for side-effecting tools.
- Human approval for irreversible actions (refunds, sends,
  deletes).
- Treating tool output as untrusted text (E8).

When this works on ten tasks, you have earned a framework.

### Protocols, not brands

- **MCP (Model Context Protocol).**
  [modelcontextprotocol.io](https://modelcontextprotocol.io/).
  Host, client, server. Servers expose tools, resources, and
  prompts over a standard. The agent does not hard-code every
  vendor SDK. E9 is the contract-level treatment. Here: an
  agent that can only call tools it discovered from a server
  is easier to audit than an agent with fourteen ad hoc
  functions.
- **A2A (Agent2Agent).**
  [a2a-protocol.org](https://a2a-protocol.org/).
  How *agents* talk to each other (discovery via an agent
  card, tasks, artifacts). Complements MCP: MCP is tools and
  context; A2A is peer agents. Linux Foundation stewardship
  is the reason this is a protocol, not a Google-only API.

You can ship serious systems with neither, using your own
JSON tools. Protocols start to matter when more than one
team owns a tool or an agent.

### Frameworks, after the loop

Read these as products with an orchestration model, not as
the definition of "agent."

| Piece | Docs | What it is |
|---|---|---|
| OpenAI Agents SDK | [openai.github.io/openai-agents-python](https://openai.github.io/openai-agents-python/) | Agents, handoffs, guardrails, tracing |
| Google ADK | [google.github.io/adk-docs](https://google.github.io/adk-docs/) | Code-first agents, Vertex/Gemini-native deploy |
| Claude Agent SDK | [code.claude.com/docs/en/agent-sdk/overview](https://code.claude.com/docs/en/agent-sdk/overview) | The Claude Code loop, tools, MCP, permissions, as a library |
| LangGraph | [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph/) | State graph, checkpoints, interrupts |
| LlamaIndex agents | [docs.llamaindex.ai](https://docs.llamaindex.ai/) | Agents on top of LlamaIndex retrievers |
| CrewAI, AutoGen | optional | Role crews / multi-actor chats; use if the eval says a crew wins |

LangGraph earns its complexity when you need durable state,
replay, and a human interrupt on one node. It is a graph
runtime. It is not a reason to skip lab 10.

CrewAI and AutoGen are optional in this course. Multi-agent
is a last resort: isolate context, pay for extra tokens, and
A/B against a single agent on the same tasks. Training 01
week 16 is that A/B in a longer program.

Hugging Face, [Agents Course](https://huggingface.co/learn/agents-course),
is the independent video-and-unit companion. Take it after
lab 10, not instead of it.

### When not to

If the user question maps to one tool with a schema, call the
tool from your app. If it maps to RAG, do RAG. Agents are for
*branching* work: unknown tool sequence, mixed retrieval and
actions, stop conditions that depend on observations. Evals
for agents are traces plus task success plus cost, not a
chat thumbs-up. E10.

## The gap most roadmaps leave

They open with a framework quickstart. Then nobody can answer
"where does the loop live?" The gap is **ownership**:

- The stop condition is yours.
- The tool schema is yours.
- The trace is the test artifact.
- MCP/A2A are how you stop rewriting adapters.

A demo that "uses LangGraph" without a max-step test is not
an agent. It is a tutorial.

## Practice

Lab `10_react_agent.ipynb`. Required.

1. Implement the loop with two tools (for example: lookup,
   calculator). No agent library.
2. Add max steps and invalid-JSON retry.
3. Save traces. Pick one failure and name the broken stage
   (thought, action parse, tool, observation handling).

Going further: expose one tool through a tiny MCP server
(official SDK) and call it from the same loop. Then, and
only then, port the loop to LangGraph or the OpenAI Agents
SDK and confirm traces still make sense.

Hugging Face Agents Course, unit 1, after the lab.

## Watch and read

- ReAct, [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
- Hugging Face, [Agents Course](https://huggingface.co/learn/agents-course)
- MCP, [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- A2A, [a2a-protocol.org](https://a2a-protocol.org/)
- OpenAI Agents SDK, [docs](https://openai.github.io/openai-agents-python/)
- Google ADK, [docs](https://google.github.io/adk-docs/)
- Claude Agent SDK, [overview](https://code.claude.com/docs/en/agent-sdk/overview)
- LangGraph, [docs](https://langchain-ai.github.io/langgraph/)
- LlamaIndex, [agents](https://docs.llamaindex.ai/en/stable/use_cases/agents/)
- CrewAI, [docs](https://docs.crewai.com/) and AutoGen,
  [microsoft.github.io/autogen](https://microsoft.github.io/autogen/)
  (optional)
- Anthropic, [building effective agents](https://www.anthropic.com/engineering/building-effective-agents)

## Knowledge check

1. What three strings make a ReAct turn, and which one is
   executed by *your* code?
2. Why is a max-step cap not optional?
3. How do MCP and A2A differ?
4. When does LangGraph pay for itself?
5. What evidence would make you reject a multi-agent design?

<details>
<summary>Answers</summary>

1. Thought, action, observation. Your code runs the action
   (the tool) and writes the observation back. The model
   writes thought and action (as structured output).
2. Loops do not self-limit. Without a cap you pay until the
   provider kills the request, or a tool is called forever.
3. MCP connects a host to tools, resources, and prompts.
   A2A connects agents to agents (cards, tasks, artifacts).
4. When you need checkpointed state, resume after crash, or
   a human interrupt on a specific node, and the graph is
   still small enough to draw.
5. A single-agent baseline that matches quality at lower
   latency and token cost on the same golden tasks.

</details>
