# HotpotQA 适配说明

HotpotQA 要求系统组合多个文档中的证据。AgentMemGraph 的适配器先将语料片段转换为情景记忆和语义事实，再通过多轮查询扩展补充桥接证据。

## 数据目录

默认路径相对于 `src/eval/hotpotqa/`：

```text
src/bench_data/hotpotqa_hipporag/
├── hotpotqa.json
├── hotpotqa_corpus.json
└── hotpotqa_oas_traces.json
```

## 服务配置

```bash
export DIR_PATH="$(pwd)/data/hotpotqa"

export LLM_BASE_URL="http://127.0.0.1:8000/v1"
export LLM_API_KEY="local"
export LLM_MODEL="Qwen/Qwen2.5-7B-Instruct"

export EMBEDDING_BASE_URL="http://127.0.0.1:8001/v1/embeddings"
export EMBEDDING_MODEL="nvidia/NV-Embed-v2"
```

`DIR_PATH` 用来保存记忆图、预测、指标和日志。每组实验应使用独立目录。

## 构建记忆图

```bash
cd src/eval/hotpotqa
python build_mem.py \
  --bench_name hotpotqa \
  --start_idx 0 \
  --end_idx 999 \
  --num_workers 2 \
  --chunk_size 30
```

建议先将 `--end_idx` 设置为较小数字完成冒烟测试。

## 执行评测

```bash
cd src/eval/hotpotqa
python eval_qa_all.py \
  --bench_name hotpotqa \
  --qa_model_name "Qwen/Qwen2.5-7B-Instruct" \
  --n_round_retrieval 2
```

`--n_round_retrieval` 控制检索轮数：

1. 用问题检索语义事实；
2. 让模型判断现有证据是否充分，并选择用于下一轮的事实；
3. 使用原问题和已选事实构造新查询；
4. 合并各轮唯一语义节点后回答。

这是一种迭代查询扩展，不应描述为通用的图邻接多跳搜索。

## 基线与消融

相关脚本包括：

- `vanilla_bsline.py`：无上下文或 gold context 基线；
- `eval_vanilla_rag.py`：原始语料块向量检索；
- `eval_qa_no_structuring.py`：关闭记忆结构化；
- `eval_qa_all.py`：完整记忆检索与推理。

对比实验应固定模型、数据切分、Top-K 和最大输出长度，并保存预测 JSON、metric JSON 和 Token usage JSONL。

## 已知限制

- 数据集不随代码仓库分发；
- 研究适配器仍使用独立于核心包的旧版评测实现；
- 多轮检索目前只支持语义记忆；
- 并发参数应与推理服务容量匹配，否则可能引入超时和重试偏差。
