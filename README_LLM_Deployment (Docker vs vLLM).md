# LLM Deployment Toolkit

## Option 1: Bare Metal vLLM
Best for:
✅ Maximum performance
✅ Single-tenant dedicated servers
✅ Rapid prototyping

Direct Installation:
```bash
# On Ubuntu server
pip install vllm
python -m vllm.entrypoints.api_server --model meta-llama/Llama-2-7b-chat-hf
```
Pros:

    * Raw Performance: No container overhead
    * Simpler GPU Utilization: Direct CUDA access
    * Lower Latency: Bypasses Docker network stack
    
Cons:

    * Host pollution (dependency conflicts)
    * Harder to maintain/rollback
    * No built-in horizontal scaling

## Option 2: Use vLLM inside Docker for isolation
Dockerized vLLM API server with multi-model support

### 1. Build Docker Image (with pre-downloaded models)
```dockerfile
# Dockerfile
FROM nvidia/cuda:12.1-base

# Install vLLM with NVIDIA optimizations
RUN pip install vllm==0.3.3 --extra-index-url https://pypi.nvidia.com

# Pre-download models (modify as needed)
RUN python -c "from vllm import LLM; LLM('meta-llama/Llama-2-7b-chat-hf', download_only=True)"
RUN python -c "from vllm import LLM; LLM('mistralai/Mistral-7B-Instruct-v0.1', download_only=True)"
```

```bash
docker build -t llm-api .
```

### 2. Serve Models

#### Option A: Serve Llama-2-7B
```bash
docker run --gpus all -p 8000:8000 llm-api \
  python -m vllm.entrypoints.api_server \
  --model meta-llama/Llama-2-7b-chat-hf
```

#### Option B: Serve Mistral-7B
```bash
docker run --gpus all -p 8000:8000 llm-api \
  python -m vllm.entrypoints.api_server \
  --model mistralai/Mistral-7B-Instruct-v0.1
```

#### Option C: Dynamic Model Selection
```bash
# For any HuggingFace model (auto-downloads if not cached)
docker run --gpus all -p 8000:8000 llm-api \
  python -m vllm.entrypoints.api_server \
  --model NousResearch/Hermes-2-Pro-Mistral-7B
```

## 🌐 API Usage
```bash
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing",
    "max_tokens": 100
  }'
```

vLLM's API server creates these endpoints automatically:
```python
# Inside vLLM's source code (api_server.py)
app.add_api_route(
    "/v1/completions",
    generate_completion,
    methods=["POST"],
    response_model=CompletionResponse,
)
```
<img width="584" height="337" alt="image" src="https://github.com/user-attachments/assets/b84dfdd9-1fce-4efd-ad92-cce793a4560c" />

## 🔧 Configuration Options

### Performance Flags
```bash
docker run --gpus all -p 8000:8000 llm-api \
  python -m vllm.entrypoints.api_server \
  --model meta-llama/Llama-2-7b-chat-hf \
  --tensor-parallel-size 2 \    # Split across 2 GPUs
  --quantization awq \          # 4-bit quantization
  --max-num-batched-tokens 4096 # Throughput tuning
```

### Model Cache Management
List downloaded models:
```bash
docker run --rm llm-api ls /root/.cache/huggingface/hub
```
Equivalent to:
```bash
docker exec -it <running-container> ls /root/.cache/huggingface/hub
```
(But works without needing a pre-running container)

## 🛠️ Advanced Deployment

### Entrypoint Script (recommended)
```bash
#!/bin/bash
# entrypoint.sh
MODEL=${MODEL:-"meta-llama/Llama-2-7b-chat-hf"}
QUANT=${QUANT:-"awq"}

exec python -m vllm.entrypoints.api_server \
  --model $MODEL \
  --quantization $QUANT
```

Update Dockerfile:
```dockerfile
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
```

## 📊 Supported Models
| Model Family | Example ID | Size (GB) |
|-------------|------------|----------|
| Llama 2 | `meta-llama/Llama-2-7b-chat-hf` | 13 |
| Mistral | `mistralai/Mistral-7B-Instruct-v0.1` | 14 |
| Gemma | `google/gemma-7b` | 15 |
| Phi | `microsoft/phi-2` | 5 |

## 🔍 Monitoring
```bash
# Check loaded model
curl http://localhost:8000/v1/models

# Health check
curl http://localhost:8000/health
```

## 📜 License
Apache 2.0
```

### Key Features:
1. **Clear Model Switching** - Ready-to-copy commands for different models
2. **Performance-Ready** - Includes quantization and parallelization flags
3. **Flexible Architecture** - Supports both pre-downloaded and on-demand models
4. **Production Best Practices** - Entrypoint script and monitoring endpoints

To use:
1. Save as `README.md`
2. Add the `Dockerfile` with `entrypoint.sh` (if using advanced deployment)
3. Customize models/ports as needed
