PYTHON ?= python3
SKILL_DIR := skill/mbti-typing

.PHONY: test validate benchmark regression scorecard clean

test: validate clean benchmark regression scorecard clean

validate:
	$(PYTHON) -m py_compile $(SKILL_DIR)/scripts/*.py

benchmark:
	$(PYTHON) -B $(SKILL_DIR)/scripts/benchmark_cases.py validate $(SKILL_DIR)/examples/benchmark-cases.json

regression:
	$(PYTHON) -B $(SKILL_DIR)/scripts/benchmark_cases.py regression $(SKILL_DIR)/examples/benchmark-cases.json $(SKILL_DIR)/examples/golden-reports.json

scorecard:
	$(PYTHON) -B $(SKILL_DIR)/scripts/skill_scorecard.py $(SKILL_DIR)

clean:
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
