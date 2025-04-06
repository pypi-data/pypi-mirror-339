# jira-creator

[![Build Status](https://github.com/dmzoneill/jira-creator/actions/workflows/main.yml/badge.svg)](https://github.com/dmzoneill/jira-creator/actions/workflows/main.yml)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
[![License](https://img.shields.io/github/license/dmzoneill/jira-creator.svg)](https://github.com/dmzoneill/jira-creator/blob/main/LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/dmzoneill/jira-creator.svg)](https://github.com/dmzoneill/jira-creator/commits/main)

Create JIRA issues (stories, bugs, epics, spikes, tasks) quickly using standardized templates and optional AI-enhanced descriptions.

---

## ⚡ Quick Start (Within 30 Seconds)

### 📝 Create your config file and enable autocomplete

This step consists in creating a configuration file and activating autocomplete. Replace the placeholders with your actual data.

```bash
mkdir -p ~/.bashrc.d
cat <<EOF > ~/.bashrc.d/jira.sh
export JPAT="your_jira_personal_access_token"
export AI_PROVIDER=openai
export AI_API_KEY=sk-...
export AI_MODEL="gpt-4o-mini"
export JIRA_URL="https://issues.redhat.com"
export PROJECT_KEY="AAP"
export AFFECTS_VERSION="aa-latest"
export COMPONENT_NAME="analytics-hcc-service"
export PRIORITY="Normal"
export JIRA_BOARD_ID=21125

# Enable autocomplete
eval "$(/usr/local/bin/rh-issue --_completion | sed 's/rh_jira.py/rh-issue/')"
EOF

source ~/.bashrc.d/jira.sh
```

---

### 🔗 Link the command-line tool wrapper

This step involves making the wrapper shell script executable and linking it to a directory on your path.

```bash
chmod +x jira_creator/rh-issue-wrapper.sh
sudo ln -s $(pwd)/jira_creator/rh-issue-wrapper.sh /usr/local/bin/rh-issue
```

---

### 🚀 Run it

This is how you use the tool to create a story. Replace the placeholder with your actual data.

```bash
rh-issue create story "Improve onboarding experience"
```

---

## 🧪 Usage & Commands

### 🆕 Create Issues

You can create various types of issues using the following commands. Replace the placeholders with your actual data.

```bash
rh-issue create bug "Fix login crash"
rh-issue create story "Refactor onboarding flow"
rh-issue create epic "Unify frontend UI" --edit
rh-issue create spike "Evaluate GraphQL support" --dry-run
```

You can further customize your command with `--edit` to use your `$EDITOR`, and `--dry-run` to print the payload without creating the issue.

### 🔁 Change Issue Type

You can change the type of an existing issue with the following command. Replace the placeholders with your actual data.

```bash
rh-issue change AAP-12345 story
```

### 🔁 Migrate Issue

You can migrate an existing issue with the following command. Replace the placeholders with your actual data.

```bash
rh-issue migrate AAP-54321 story
```

### ✏️ Edit Description

You can edit the description of an existing issue with the following command. Replace the placeholders with your actual data.

```bash
rh-issue edit AAP-98765
rh-issue edit AAP-98765 --no-ai
```

### 🧍 Unassign Issue

You can unassign an existing issue with the following command. Replace the placeholders with your actual data.

```bash
rh-issue unassign AAP-12345
```

### 📋 List Issues

You can list issues with the following command. You can customize your command with `--project`, `--component`, and `--user` options. Replace the placeholders with your actual data.

```bash
rh-issue list
rh-issue list --project AAP --component api --user jdoe
```

### 🏷️ Set Priority

You can set the priority of an existing issue with the following command. Replace the placeholders with your actual data.

```bash
rh-issue set-priority AAP-123 High
```

### 📅 Sprint Management

You can manage sprints with the following commands. Replace the placeholders with your actual data.

```bash
rh-issue set-sprint AAP-456 1234
rh-issue remove-sprint AAP-456
rh-issue add-sprint AAP-456 "Sprint 33"
```

### 🚦 Set Status

You can set the status of an existing issue with the following command. Replace the placeholders with your actual data.

```bash
rh-issue set-status AAP-123 "In Progress"
```

---

## 🤖 AI Provider Support

You can plug in different AI providers by setting `AI_PROVIDER`.

We can use ollama for the management for different models

```bash
mkdir -vp ~/.ollama-models
docker run -d -v ~/.ollama-models:/root/.ollama -p 11434:11434 ollama/ollama
```

### ✅ OpenAI

Setup for using OpenAI as AI provider.

```bash
export AI_PROVIDER=openai
export AI_API_KEY=sk-...
export AI_MODEL=gpt-4  # Optional
```

### 🦙 LLama3

Setup for using LLama3 as AI provider.

```bash
docker compose exec ollama ollama pull LLama3
export AI_PROVIDER=LLama3
export AI_URL=http://localhost:11434/api/generate
export AI_MODEL=LLama3
```

### 🧠 DeepSeek

Setup for using DeepSeek as AI provider.

```bash
docker compose exec ollama ollama pull deepseek-r1:7b
export AI_PROVIDER=deepseek
export AI_URL=http://localhost:11434/api/generate
export AI_MODEL=http://localhost:11434/api/generate
```

### 🖥 GPT4All

Setup for using GPT4All as AI provider.

```bash
pip install gpt4all
export AI_PROVIDER=gpt4all
# WIP
```

### 🧪 InstructLab

Setup for using InstructLab as AI provider.

```bash
export AI_PROVIDER=instructlab
export AI_URL=http://localhost:11434/api/generate
export AI_MODEL=instructlab
# WIP
```

### 🧠 BART

Setup for using BART as AI provider.

```bash
export AI_PROVIDER=bart
export AI_URL=http://localhost:8000/bart
# WIP
```

### 🪫 Noop

Setup for using Noop as AI provider.

```bash
export AI_PROVIDER=noop
```

---

## 🛠 Dev Setup

To set up your development environment, run the following command.

```bash
pipenv install --dev
```

### Testing & Linting

Use the following commands for testing, linting, and formatting respectively.

```bash
make test
make lint
make format  # autofix formatting
```

---

## ⚙️ How It Works

- Loads field definitions from `.tmpl` files under `templates/`
- Uses `TemplateLoader` to generate Markdown descriptions
- Optionally applies AI cleanup for readability and structure
- Sends to JIRA via REST API (or dry-runs it)

---

## 📜 License

This project is licensed under the [Apache License](./LICENSE).