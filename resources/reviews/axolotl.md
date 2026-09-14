---
title: "Axolotl"
url: https://docs.axolotl.ai/
author: "Axolotl maintainers and contributors"
date_evaluated: 2026-06-25
verdict: catalog
tags: [llm, fine-tuning, post-training, lora, training-framework, open-source, gpu]
---

## What it proposes

Axolotl is an open-source (Apache-2.0) framework that wraps the full LLM fine-tuning and post-training pipeline behind a single YAML config. One file declares dataset preprocessing, training, evaluation, quantization, and inference, so a run is driven by configuration rather than custom training code. It supports a broad model catalog from the Hugging Face Hub (LLaMA, Mistral, Mixtral, Qwen, Gemma, Pythia, GPT-OSS, GLM, plus multimodal vision-language and audio models) and a wide range of training methods: full fine-tuning, LoRA, QLoRA, GPTQ, QAT, preference tuning (DPO, IPO, KTO, ORPO), reinforcement learning (GRPO, GDPO), and reward modelling. It layers in heavy performance optimizations (multipacking, Flash Attention, Liger Kernel, ScatterMoE, sequence parallelism) and scales from single-GPU to multi-node via FSDP, DeepSpeed, Torchrun, and Ray. Datasets load from local disk, the Hub, or cloud object stores. It ships as Docker images and PyPI packages, installs uv-first, and includes dedicated AI-agent documentation (`axolotl agent-docs`, `axolotl config-schema`, `AGENTS.md`) so coding agents can author and validate configs.

## Best used when

The work involves producing or adapting model weights: fine-tuning a base or instruct model on domain data, applying preference or RL post-training, or running reward modelling. It fits teams that own NVIDIA (Ampere+) or AMD GPU capacity and want a config-driven, reproducible alternative to bespoke training scripts. The single-YAML surface and agent-docs support make it especially suited to workflows where experiments must be repeatable and where an AI coding agent helps draft and validate the training configuration.

## Poor fit when

The workflow consumes hosted frontier models through an API rather than producing weights of its own. If there is no training, fine-tuning, or model-hosting step in scope, none of the framework's surface area applies: there is no config to write, no GPU to provision, and no weights to evaluate. It also presumes local or cloud GPU access (Ampere-or-newer NVIDIA, or AMD), recent Python and PyTorch, and an MLOps posture for managing datasets, checkpoints, and runs. For prompt-engineering, retrieval, or orchestration over an already-capable hosted model, it adds an entire training stack with no payoff.

## Verdict

Catalog. Axolotl is a mature, well-regarded, actively maintained framework that does its job well: it is one of the strongest config-driven options for LLM fine-tuning and post-training, and the YAML-first design plus first-class AI-agent docs make it notably approachable for its category. But its entire value proposition is creating and adapting model weights, which only matters to projects that run a training or fine-tuning workflow on their own GPU hardware. A project that consumes hosted frontier models through an API and has no model-training, fine-tuning, or self-hosting step in scope has nothing to plug it into. There is no in-scope alternative to name because the need it serves does not arise for this project type. Worth knowing exists for the day a self-hosted or fine-tuned model enters scope; not something to adopt today.
