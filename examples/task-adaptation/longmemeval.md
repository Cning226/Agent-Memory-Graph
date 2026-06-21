# LongMemEval 适配说明

LongMemEval 用于评估模型能否从长时间、多会话的用户对话中找回事实、偏好和时间关系。本目录保留研究评测适配器，核心服务本身不依赖 LongMemEval。

## 数据准备

将官方数据放在：

```text
src/LongMemEval/data/longmemeval_s_cleaned.json
```

也可以显式指定路径：

```bash
export LONGMEMEVAL_DATA_PATH="/absolute/path/to/longmemeval_s_cleaned.json"
```

## 模型配置

```bash
export LLM_BASE_URL="http://127.0.0.1:8000/v1"
export LLM_API_KEY="local"
export LLM_MODEL="Qwen/Qwen2.5-7B-Instruct"

export EMBEDDING_BASE_URL="http://127.0.0.1:8001/v1/embeddings"
export EMBEDDING_MODEL="nvidia/NV-Embed-v2"
```

`LONGMEMEVAL_SESSION_WORKERS` 控制会话结构化的线程数。建议先以 `1` 做可重复的冒烟测试，再根据模型服务吞吐量增加。

```bash
export LONGMEMEVAL_SESSION_WORKERS=1
```

## 运行

评测脚本依赖当前工作目录中的 Prompt 文件，因此应从对应目录运行：

```bash
cd src/eval/longmemeval
python eval_longmemeval_all.py
```

任务适配版本：

```bash
cd src/eval/longmemeval
python eval_longmemeval_adapted.py
```

## 适配策略

- 以单个 user/assistant turn 为知识抽取基本单位；
- 分开提取用户事实、用户偏好和 Agent 已完成行为；
- 保留 session ID 与日期，以支持会话级和时间类问题；
- 先召回语义节点，再根据 session 投票决定是否补充完整情景轨迹。

## 结果要求

仓库不内置预先宣称的准确率。正式报告结果时请一并保存：

- 数据集版本和问题数量；
- 结构化、检索、推理模型；
- Prompt 与 Top-K 配置；
- 每条问题的 hypothesis；
- 官方评估器输出；
- Token usage 原始日志。
