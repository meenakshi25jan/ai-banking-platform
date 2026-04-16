#!/usr/bin/env bash
set -euo pipefail

MODEL_REPO="${MODEL_REPO:-bartowski/Meta-Llama-3.1-8B-Instruct-GGUF}"
MODEL_FILE="${MODEL_FILE:-Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf}"
PORT="${PORT:-8001}"
CONTEXT_SIZE="${CONTEXT_SIZE:-4096}"
MODELS_DIR="$HOME/models/Meta-Llama-3.1-8B-Instruct-GGUF"

sudo apt-get update -y
sudo apt-get install -y git cmake build-essential python3 python3-pip tmux curl

if [[ ! -d "$HOME/llama.cpp" ]]; then
  git clone https://github.com/ggml-org/llama.cpp.git "$HOME/llama.cpp"
fi
cmake -B "$HOME/llama.cpp/build"
cmake --build "$HOME/llama.cpp/build" -j

python3 -m pip install -U "huggingface_hub[cli]"
mkdir -p "$MODELS_DIR"
hf download "$MODEL_REPO" --include "$MODEL_FILE" --local-dir "$MODELS_DIR"

if tmux has-session -t llama 2>/dev/null; then
  tmux kill-session -t llama
fi

tmux new-session -d -s llama "bash -lc '$HOME/llama.cpp/build/bin/llama-server -m $MODELS_DIR/$MODEL_FILE --host 0.0.0.0 --port $PORT -c $CONTEXT_SIZE -ngl 0'"
echo "Llama fallback started on port $PORT"
echo "Test: curl http://127.0.0.1:$PORT/health"
