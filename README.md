# Multi-Agent Software Company Framework - Course Overview

## 📚 Course Structure

This course consists of **24 lessons** organized into **7 phases**, taking you from basic concepts to building a complete multi-agent software company framework.

### 💻 Hardware Requirements

**Important:** This course uses LLMs (Large Language Models) for agent intelligence. You have two options:

- **CPU Option**: Works on any modern computer (recommended for learning)
  - Uses **LocalLLM (llama.cpp)** with quantized models
  - No GPU required
  - ~8GB RAM recommended
  - ~5-10GB disk space for model files

- **GPU Option**: For faster inference and production use
  - Uses **VLLM** or **LocalLLM with GPU support**
  - Requires NVIDIA GPU with CUDA support
  - 8GB+ VRAM recommended
  - Faster inference, better for batch processing

📖 **For detailed setup instructions, see the [LLM Setup and Configuration](#🤖-llm-setup-and-configuration) section below.**

---

## 🎯 Learning Journey

```
┌─────────────────────────────────────────────────────────────┐
│                    LEARNING PROGRESSION                      │
└─────────────────────────────────────────────────────────────┘

Phase 1: Foundation (Lessons 1-8)
    ↓
    Understanding Core Concepts
    ↓
Phase 2: Tools (Lessons 9-12)
    ↓
    Building Agent Capabilities
    ↓
Phase 3: Project Management (Lessons 13-14)
    ↓
    Organizing Work
    ↓
Phase 4: Quality (Lessons 15-16)
    ↓
    Ensuring Quality
    ↓
Phase 5: Planning (Lessons 17-18)
    ↓
    Managing Tasks
    ↓
Phase 6: Advanced (Lessons 19-21)
    ↓
    Memory & Complete Workflows
    ↓
Phase 7: Specialization (Lessons 22-24)
    ↓
    Specialized Roles
    ↓
    ┌─────────────────────────┐
    │  COMPLETE MULTI-AGENT   │
    │    SOFTWARE COMPANY     │
    └─────────────────────────┘
```

---

<details>
<summary><b>📖 Phase 1: Basic Framework (Lessons 1-8)</b></summary>

## 📖 Phase 1: Basic Framework (Lessons 1-8)

### Foundation Stage: Understanding the Building Blocks

```
┌─────────────┐
│   Messages  │ ← Communication Unit
└─────────────┘
      ↓
┌─────────────┐
│   Actions   │ ← Tasks to Perform
└─────────────┘
      ↓
┌─────────────┐
│    Roles    │ ← Agents with Goals
└─────────────┘
      ↓
┌─────────────┐
│ Environment │ ← Message Routing
└─────────────┘
      ↓
┌─────────────┐
│    Team     │ ← Orchestration
└─────────────┘
      ↓
┌─────────────┐
│     LLM     │ ← Intelligence
└─────────────┘
      ↓
┌─────────────┐
│   Workflow  │ ← Complete System
└─────────────┘
```

### Lesson 01: Understanding Messages
**What You'll Learn:**
- How messages enable communication between agents
- Message structure (content, role, cause_by, routing)
- Message flow in multi-agent systems

**After This Lesson:**
- ✅ You understand how agents communicate
- ✅ You can create and route messages
- ✅ You know how to track message context

---

### Lesson 02: Understanding Actions
**What You'll Learn:**
- What actions are and how they work
- Creating custom actions
- Action execution and output

**After This Lesson:**
- ✅ You can create custom actions
- ✅ You understand ActionOutput structure
- ✅ You can chain actions together

---

### Lesson 03: Understanding Roles
**What You'll Learn:**
- Role concept and structure
- How roles observe, think, and act
- Role memory and context

**After This Lesson:**
- ✅ You can create custom roles
- ✅ You understand role decision-making
- ✅ You know how roles process messages

---

### Lesson 04: Understanding Environment
**What You'll Learn:**
- Environment as message hub
- Message broadcasting and routing
- Shared context management

**After This Lesson:**
- ✅ You can manage multiple roles
- ✅ You understand message routing
- ✅ You can use shared context

---

### Lesson 05: Understanding Teams
**What You'll Learn:**
- Team orchestration
- Workflow management
- Round-based execution

**After This Lesson:**
- ✅ You can create and run teams
- ✅ You understand workflow execution
- ✅ You can track project progress

---

### Lesson 06: Understanding LLMs
**What You'll Learn:**
- LLM interface and implementations
- MockLLM for testing
- OpenAILLM for production
- VLLM for localhost inference
- LocalLLM for llama.cpp inference
- Integrating LLMs with actions

**After This Lesson:**
- ✅ You can use LLMs in actions
- ✅ You understand LLM integration
- ✅ You can swap LLM implementations

---

### Lesson 07: Core Actions (WritePRD, WriteDesign, WriteCode)
**What You'll Learn:**
- Core software development actions
- Action chaining (PRD → Design → Code)
- Converting outputs to messages

**After This Lesson:**
- ✅ You understand the core workflow
- ✅ You can use WritePRD, WriteDesign, WriteCode
- ✅ You can chain actions together

---

### Lesson 08: Complete Software Company Workflow
**What You'll Learn:**
- End-to-end workflow from idea to code
- Role collaboration
- Message flow and statistics

**After This Lesson:**
- ✅ You can run complete workflows
- ✅ You understand role collaboration
- ✅ You can analyze workflow results

**🎉 Milestone: You've built a basic multi-agent system!**

</details>

---

<details>
<summary><b>🛠️ Phase 2: Core Tools (Lessons 9-12)</b></summary>

## 🛠️ Phase 2: Core Tools (Lessons 9-12)

### Capability Stage: Adding Agent Tools

```
┌──────────────┐
│    Editor    │ ← File Operations
└──────────────┘
      ↓
┌──────────────┐
│   Terminal   │ ← Command Execution
└──────────────┘
      ↓
┌──────────────┐
│   Browser    │ ← Web Navigation
└──────────────┘
      ↓
┌──────────────┐
│Search Engine │ ← Information Retrieval
└──────────────┘
      ↓
┌─────────────────────┐
│  AGENTS WITH TOOLS  │
└─────────────────────┘
```

### Lesson 09: File Editor Tool
**What You'll Learn:**
- File creation, reading, and editing
- File search and pattern matching
- Workspace management

**After This Lesson:**
- ✅ Agents can manipulate files
- ✅ You can create file operations
- ✅ You understand workspace management

---

### Lesson 10: Terminal Tool
**What You'll Learn:**
- Command execution
- Python code execution
- Syntax checking

**After This Lesson:**
- ✅ Agents can execute commands
- ✅ You can run and test code
- ✅ You understand system interaction

---

### Lesson 11: Web Browser Tool
**What You'll Learn:**
- Web navigation
- Content extraction
- Link extraction

**After This Lesson:**
- ✅ Agents can browse the web
- ✅ You can extract web content
- ✅ You understand web interaction

---

### Lesson 12: Search Engine Tool
**What You'll Learn:**
- Web search
- Result parsing
- Search summarization

**After This Lesson:**
- ✅ Agents can search for information
- ✅ You can process search results
- ✅ You understand information retrieval

**🎉 Milestone: Your agents now have real-world capabilities!**

</details>

---

<details>
<summary><b>📁 Phase 3: Project Management (Lessons 13-14)</b></summary>

## 📁 Phase 3: Project Management (Lessons 13-14)

### Organization Stage: Structuring Projects

```
┌─────────────────┐
│  Project Repo   │ ← Organized Structure
│  ├── docs/      │
│  ├── src/       │
│  ├── tests/     │
│  └── config/    │
└─────────────────┘
      ↓
┌─────────────────┐
│ Code Generator  │ ← Automated Generation
└─────────────────┘
      ↓
┌─────────────────┐
│ STRUCTURED      │
│   PROJECTS      │
└─────────────────┘
```

### Lesson 13: Project Repository
**What You'll Learn:**
- Project structure management
- Repository organization (docs, src, tests)
- File organization

**After This Lesson:**
- ✅ You can organize projects properly
- ✅ You understand project structure
- ✅ You can manage multiple repositories

---

### Lesson 14: Code Generation
**What You'll Learn:**
- LLM-powered code generation
- Project scaffolding
- File generation from designs

**After This Lesson:**
- ✅ You can generate complete projects
- ✅ You understand code generation workflow
- ✅ You can create projects from designs

**🎉 Milestone: Your agents can create organized projects!**

</details>

---

<details>
<summary><b>✅ Phase 4: Quality Assurance (Lessons 15-16)</b></summary>

## ✅ Phase 4: Quality Assurance (Lessons 15-16)

### Quality Stage: Ensuring Code Quality

```
┌─────────────────┐
│  Code Review    │ ← Quality Checks
│  ├── Style      │
│  ├── Security   │
│  └── Best Prac. │
└─────────────────┘
      ↓
┌─────────────────┐
│ Test Generator  │ ← Automated Testing
│  ├── Unit       │
│  ├── Integration│
│  └── Coverage   │
└─────────────────┘
      ↓
┌─────────────────┐
│  QUALITY CODE   │
└─────────────────┘
```

### Lesson 15: Code Review
**What You'll Learn:**
- Automated code review
- Quality checks (style, security, best practices)
- Code scoring and suggestions

**After This Lesson:**
- ✅ You can review code automatically
- ✅ You understand quality metrics
- ✅ You can identify code issues

---

### Lesson 16: Testing
**What You'll Learn:**
- Test generation
- Test execution
- Coverage analysis

**After This Lesson:**
- ✅ You can generate tests automatically
- ✅ You can execute and analyze tests
- ✅ You understand test coverage

**🎉 Milestone: Your agents ensure code quality!**

</details>

---

<details>
<summary><b>📋 Phase 5: Planning (Lessons 17-18)</b></summary>

## 📋 Phase 5: Planning (Lessons 17-18)

### Management Stage: Task Planning

```
┌─────────────────┐
│    Planner      │ ← Task Breakdown
│  └── Goals      │
│      └── Tasks   │
└─────────────────┘
      ↓
┌─────────────────┐
│ Project Manager │ ← Task Management
│  ├── Planning   │
│  ├── Tracking   │
│  └── Execution  │
└─────────────────┘
      ↓
┌─────────────────┐
│ PLANNED PROJECTS│
└─────────────────┘
```

### Lesson 17: Planning
**What You'll Learn:**
- Task planning from goals
- Task breakdown and dependencies
- Plan structure

**After This Lesson:**
- ✅ You can create plans from goals
- ✅ You understand task dependencies
- ✅ You can manage task breakdowns

---

### Lesson 18: Project Manager
**What You'll Learn:**
- ProjectManager role
- Task list generation
- Project execution tracking

**After This Lesson:**
- ✅ You can use ProjectManager role
- ✅ You understand task management
- ✅ You can track project progress

**🎉 Milestone: Your agents can plan and manage projects!**

</details>

---

<details>
<summary><b>🧠 Phase 6: Memory & Advanced Actions (Lessons 19-21)</b></summary>

## 🧠 Phase 6: Memory & Advanced Actions (Lessons 19-21)

### Advanced Stage: Memory and Complex Workflows

```
┌─────────────────┐
│     Memory      │ ← Persistent Storage
│  ├── Store      │
│  ├── Retrieve   │
│  └── Search     │
└─────────────────┘
      ↓
┌─────────────────┐
│ Action Graphs   │ ← Complex Workflows
│  ├── Dependencies│
│  ├── Parallel   │
│  └── Conditional│
└─────────────────┘
      ↓
┌─────────────────┐
│ COMPLETE        │
│   WORKFLOW      │
└─────────────────┘
```

### Lesson 19: Memory
**What You'll Learn:**
- Persistent memory storage
- Key-value storage and retrieval
- Memory search

**After This Lesson:**
- ✅ Agents can remember information
- ✅ You can store and retrieve data
- ✅ You understand memory management

---

### Lesson 20: Advanced Actions
**What You'll Learn:**
- Action graphs
- Dependency management
- Parallel execution

**After This Lesson:**
- ✅ You can create complex workflows
- ✅ You understand action dependencies
- ✅ You can execute actions in parallel

---

### Lesson 21: Complete Workflow
**What You'll Learn:**
- End-to-end integration
- All components working together
- Real project generation

**After This Lesson:**
- ✅ You can run complete workflows
- ✅ You understand system integration
- ✅ You can generate real projects

**🎉 Milestone: You have a complete multi-agent system!**

</details>

---

<details>
<summary><b>👥 Phase 7: Specialized Roles (Lessons 22-24)</b></summary>

## 👥 Phase 7: Specialized Roles (Lessons 22-24)

### Specialization Stage: Domain-Specific Roles

```
┌─────────────────┐
│  QA Engineer    │ ← Testing & Quality
└─────────────────┘
      ↓
┌─────────────────┐
│Technical Writer │ ← Documentation
└─────────────────┘
      ↓
┌─────────────────┐
│ DevOps Engineer │ ← Deployment
└─────────────────┘
      ↓
┌─────────────────┐
│  SPECIALIZED    │
│   SOFTWARE      │
│    COMPANY      │
└─────────────────┘
```

### Lesson 22: QA Engineer
**What You'll Learn:**
- QAEngineer role
- Test generation and execution
- Bug reporting

**After This Lesson:**
- ✅ You can use QAEngineer role
- ✅ You understand automated testing
- ✅ You can report bugs automatically

---

### Lesson 23: Technical Writer
**What You'll Learn:**
- TechnicalWriter role
- Documentation generation
- API docs and tutorials

**After This Lesson:**
- ✅ You can use TechnicalWriter role
- ✅ You can generate documentation
- ✅ You understand documentation types

---

### Lesson 24: DevOps Engineer
**What You'll Learn:**
- DevOpsEngineer role
- Dockerfile creation
- CI/CD setup
- Deployment scripts

**After This Lesson:**
- ✅ You can use DevOpsEngineer role
- ✅ You can create deployment configs
- ✅ You understand DevOps automation

**🎉 Final Milestone: You have a complete specialized software company!**

</details>

---

<details>
<summary><b>📚 Lesson Components</b></summary>

## 📚 Lesson Components

Each lesson includes:

### Python File (`lesson_XX.py`)
- ✅ Runnable code demonstrating the concept
- ✅ Practical examples
- ✅ Working demonstrations
- ✅ Can be executed directly

### Markdown Guide (`lesson_XX.md`)
- ✅ **Learning Targets**: What you'll achieve
- ✅ **Overview**: Concept introduction
- ✅ **Key Concepts**: Core ideas explained
- ✅ **Guidance**: Step-by-step instructions with code examples
- ✅ **Exercises**: Hands-on practice tasks
- ✅ **Practice Tasks**: Additional challenges
- ✅ **Next Steps**: What to learn next
- ✅ **Common Pitfalls**: What to avoid
- ✅ **Additional Resources**: Where to learn more

</details>

---

<details>
<summary><b>🗺️ Complete Learning Path</b></summary>

## 🗺️ Complete Learning Path

```
START
  │
  ├─► Phase 1: Foundation (Lessons 1-8)
  │   └─► Basic multi-agent system
  │
  ├─► Phase 2: Tools (Lessons 9-12)
  │   └─► Agents with capabilities
  │
  ├─► Phase 3: Project Management (Lessons 13-14)
  │   └─► Organized projects
  │
  ├─► Phase 4: Quality (Lessons 15-16)
  │   └─► Quality assurance
  │
  ├─► Phase 5: Planning (Lessons 17-18)
  │   └─► Task management
  │
  ├─► Phase 6: Advanced (Lessons 19-21)
  │   └─► Complete workflows
  │
  └─► Phase 7: Specialization (Lessons 22-24)
      └─► Specialized software company
          │
          ▼
    COMPLETE FRAMEWORK
```

</details>

---

<details>
<summary><b>🎓 Expected Learning Outcomes</b></summary>

## 🎓 Expected Learning Outcomes

### After Phase 1 (Lessons 1-8)
- ✅ Understand multi-agent systems
- ✅ Create basic agent workflows
- ✅ Use LLMs in actions
- ✅ Build simple software company

### After Phase 2 (Lessons 9-12)
- ✅ Agents can interact with files
- ✅ Agents can execute commands
- ✅ Agents can browse the web
- ✅ Agents can search for information

### After Phase 3 (Lessons 13-14)
- ✅ Organize projects properly
- ✅ Generate code automatically
- ✅ Create project structures

### After Phase 4 (Lessons 15-16)
- ✅ Review code automatically
- ✅ Generate and run tests
- ✅ Ensure code quality

### After Phase 5 (Lessons 17-18)
- ✅ Plan projects from goals
- ✅ Manage tasks and dependencies
- ✅ Track project progress

### After Phase 6 (Lessons 19-21)
- ✅ Store and retrieve information
- ✅ Create complex workflows
- ✅ Run complete end-to-end projects

### After Phase 7 (Lessons 22-24)
- ✅ Use specialized roles
- ✅ Automate testing and QA
- ✅ Generate documentation
- ✅ Automate deployment
- ✅ **Build a complete specialized software company**

</details>

---

<details>
<summary><b>🚀 Getting Started</b></summary>

## 🚀 Getting Started

1. **Start with Lesson 01**: Understanding Messages
2. **Follow sequentially**: Each lesson builds on previous ones
3. **Complete exercises**: Practice with provided exercises
4. **Experiment**: Try modifying examples
5. **Build projects**: Apply what you learn

</details>

---

<details>
<summary><b>🤖 LLM Setup and Configuration</b></summary>

## 🤖 LLM Setup and Configuration

The framework supports multiple LLM backends for running agents. Currently, the framework prioritizes **LocalLLM (llama.cpp)** and **VLLM** for local inference. The `get_llm()` function automatically selects the best available option.

### Supported LLM Backends

#### 1. LocalLLM (llama.cpp) - **Recommended for CPU/GPU**

**Pros:**
- ✅ Works on both CPU and GPU
- ✅ No server setup required
- ✅ Low memory footprint
- ✅ Supports multiple model formats (GGUF)
- ✅ Supports Llama 2, Llama 3, Qwen 2/2.5, IBM Granite 3.0
- ✅ Fast inference on CPU with quantization
- ✅ Easy to use - just point to model file

**Cons:**
- ❌ Slower than vLLM for batch inference
- ❌ Limited to single model per instance
- ❌ Requires downloading model files (several GB)

**Installation:**

```bash
# Install llama-cpp-python
pip install llama-cpp-python

# For GPU support (CUDA), use:
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --force-reinstall --no-cache-dir

# For CPU-only (faster on some systems):
CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" pip install llama-cpp-python --force-reinstall --no-cache-dir
```

**Download Models:**

1. **Llama 3 8B Instruct (Recommended):**
   ```bash
   # Download from Hugging Face
   # Visit: https://huggingface.co/QuantFactory
   # Or use huggingface-cli:
   mkdir HF_MODELS
   export HUGGINGFACE_HUB_CACHE="HF_MODELS"
   export HF_HOME="HF_MODELS"
   hf download QuantFactory/Meta-Llama-3-8B-Instruct-GGUF --local-dir ./HF_MODELS/Meta-Llama-3-8B-Instruct-GGUF
   ```

2. **Other Supported Models:**
   - Visit this respository: https://huggingface.co/QuantFactory

**Usage:**

The framework automatically detects and uses LocalLLM if a model file is found at the default path:
```python
from framework.llm import get_llm

# Automatically uses LocalLLM if model file exists
llm = get_llm(
    local_model_path="./HF_MODELS/Meta-Llama-3-8B-Instruct-GGUF/Meta-Llama-3-8B-Instruct.Q3_K_M.gguf"
)
```

**Model Path Configuration:**

Update the default path in `framework/llm.py` or pass it to `get_llm()`:
```python
llm = get_llm(
    local_model_path="/path/to/your/model.gguf"
)
```

---

#### 2. VLLM - **Recommended for GPU with High Throughput**

**Pros:**
- ✅ Very fast inference (optimized for GPU)
- ✅ Excellent for batch processing
- ✅ Supports continuous batching
- ✅ Can serve multiple models
- ✅ OpenAI-compatible API
- ✅ Better for production deployments

**Cons:**
- ❌ **Requires GPU** (NVIDIA GPU with CUDA)
- ❌ Higher memory usage
- ❌ Requires separate server process
- ❌ More complex setup
- ❌ Not suitable for CPU-only systems

**Prerequisites:**
- NVIDIA GPU with CUDA support
- CUDA 11.8 or later
- Python 3.8+

**Installation:**

```bash
# Install vLLM (requires GPU)
pip install vllm

# Or install with specific CUDA version
pip install vllm --extra-index-url https://download.pytorch.org/whl/cu118
```

**Starting vLLM Server:**

```bash
# Start vLLM server with a model
python -m vllm.entrypoints.openai.api_server \
    --model codellama/CodeLlama-7b-Instruct-hf \
    --port 8000 \
    --tensor-parallel-size 1 \
    --gpu-memory-utilization 0.8 \

# Or with custom settings:
python -m vllm.entrypoints.openai.api_server \
    --model /path/to/model \
    --port 8000 \
    --host 0.0.0.0 \
    --tensor-parallel-size 1 \
    --gpu-memory-utilization 0.5 \
```

**Usage:**

The framework automatically detects and uses VLLM if the server is running:
```python
from framework.llm import get_llm

# Automatically uses VLLM if server is running on localhost:8000
llm = get_llm(
    vllm_base_url="http://localhost:8000/v1",
    vllm_model="meta-llama/Meta-Llama-3-8B-Instruct"  # Optional
)
```

**Verify Server is Running:**

```bash
# Test the server
curl http://localhost:8000/v1/models
```

---


### Quick Start Recommendations

**For CPU-only systems:**
- Use **LocalLLM** with quantized models (Q3_K_M, Q4_K_M)
- Download GGUF format models for best performance
- Recommended: Llama 3 8B Instruct Q3_K_M (~5GB)

**For GPU systems:**
- **Option 1**: Use **LocalLLM** for simplicity (works great on GPU too!)
- **Option 2**: Use **VLLM** for maximum throughput and batch processing
- Recommended: CodeLlama-7b-Instruct-hf

**For Production:**
- Use **VLLM** with proper server setup
- Configure proper resource limits
- Use load balancing for multiple instances

### Troubleshooting

**LocalLLM Issues:**
- **Model not found**: Check the model path in `get_llm()` or `framework/llm.py`
- **Out of memory**: Use a smaller quantized model (Q2_K, Q3_K_M)
- **Slow inference**: Enable GPU support or use a smaller model

**VLLM Issues:**
- **Server not starting**: Check GPU availability with `nvidia-smi`
- **Connection refused**: Verify server is running on correct port
- **Out of memory**: Reduce `--max-model-len`, `--gpu-memory-utilization` or use tensor parallelism

**General:**
- Check logs for detailed error messages
- Verify model format compatibility
- Ensure sufficient disk space for model files

</details>

---

<details>
<summary><b>📊 Progress Tracking</b></summary>

## 📊 Progress Tracking

Track your progress through the course:

- [ ] Phase 1: Basic Framework (Lessons 1-8)
- [ ] Phase 2: Core Tools (Lessons 9-12)
- [ ] Phase 3: Project Management (Lessons 13-14)
- [ ] Phase 4: Quality Assurance (Lessons 15-16)
- [ ] Phase 5: Planning (Lessons 17-18)
- [ ] Phase 6: Memory & Advanced Actions (Lessons 19-21)
- [ ] Phase 7: Specialized Roles (Lessons 22-24)

</details>

---

<details>
<summary><b>🎯 Final Goal</b></summary>

## 🎯 Final Goal

By completing all 24 lessons, you will have:

1. ✅ **Built a complete multi-agent framework**
2. ✅ **Created specialized roles** (ProductManager, Architect, Engineer, QA, Technical Writer, DevOps)
3. ✅ **Integrated tools** (Editor, Terminal, Browser, Search Engine)
4. ✅ **Implemented quality assurance** (Code Review, Testing)
5. ✅ **Added planning capabilities** (Task Management, Project Planning)
6. ✅ **Built memory systems** (Persistent Storage, Experience)
7. ✅ **Created advanced workflows** (Action Graphs, Complex Dependencies)
8. ✅ **Automated software development** (From idea to deployed code)

**You'll have a production-ready multi-agent software company framework!** 🎉

</details>

---

<details>
<summary><b>📝 Notes</b></summary>

## 📝 Notes

- Each lesson is self-contained but builds on previous concepts
- Exercises are designed to reinforce learning
- Practice tasks help you apply concepts
- All code is runnable and tested
- Markdown guides provide comprehensive documentation

---

**Happy Learning! 🚀**

