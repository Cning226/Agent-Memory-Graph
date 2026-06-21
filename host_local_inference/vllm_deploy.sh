#!/usr/bin/env bash
set -euo pipefail

# All options can be overridden with environment variables.
MODEL_NAME="${MODEL_NAME:-Qwen/Qwen2.5-7B-Instruct}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
TENSOR_PARALLEL_SIZE="${TENSOR_PARALLEL_SIZE:-1}"
MAX_MODEL_LEN="${MAX_MODEL_LEN:-32768}"

if ! command -v vllm >/dev/null 2>&1; then
  echo "vllm is not installed. Install it in a CUDA-enabled environment first." >&2
  exit 1
fi

echo "Starting model: ${MODEL_NAME}"
echo "OpenAI-compatible endpoint: http://${HOST}:${PORT}/v1"

vllm serve "${MODEL_NAME}" \
  --host "${HOST}" \
  --port "${PORT}" \
  --tensor-parallel-size "${TENSOR_PARALLEL_SIZE}" \
  --max-model-len "${MAX_MODEL_LEN}"
