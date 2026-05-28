PYTHON ?= python3
SKILL_DIR := skill/mbti-typing

.PHONY: test validate benchmark regression scorecard activation session-lab-audit case-gallery-sync case-gallery-audit calibration-lab-sync calibration-lab-audit repo-scorecard clean

test: validate clean benchmark regression scorecard activation session-lab-audit case-gallery-sync case-gallery-audit calibration-lab-sync calibration-lab-audit repo-scorecard clean

validate:
	$(PYTHON) -m py_compile $(SKILL_DIR)/scripts/*.py
	$(PYTHON) -m py_compile scripts/*.py

benchmark:
	$(PYTHON) -B $(SKILL_DIR)/scripts/benchmark_cases.py validate $(SKILL_DIR)/examples/benchmark-cases.json

regression:
	$(PYTHON) -B $(SKILL_DIR)/scripts/benchmark_cases.py regression $(SKILL_DIR)/examples/benchmark-cases.json $(SKILL_DIR)/examples/golden-reports.json

scorecard:
	$(PYTHON) -B $(SKILL_DIR)/scripts/skill_scorecard.py $(SKILL_DIR)

activation:
	$(PYTHON) -B $(SKILL_DIR)/scripts/typing_session.py validate examples/session-state-example.json --final
	$(PYTHON) -B $(SKILL_DIR)/scripts/report_audit.py --fail-on-findings docs/sample-report.md

session-lab-audit:
	$(PYTHON) -B scripts/session_lab_audit.py docs/session-lab.html

case-gallery-sync:
	$(PYTHON) -B scripts/sync_case_gallery.py $(SKILL_DIR)/examples/benchmark-cases.json docs/case-gallery.html

case-gallery-audit:
	$(PYTHON) -B scripts/case_gallery_audit.py docs/case-gallery.html $(SKILL_DIR)/examples/benchmark-cases.json

calibration-lab-sync:
	$(PYTHON) -B scripts/sync_calibration_lab.py $(SKILL_DIR)/examples/benchmark-cases.json docs/calibration-lab.html

calibration-lab-audit:
	$(PYTHON) -B scripts/calibration_lab_audit.py docs/calibration-lab.html $(SKILL_DIR)/examples/benchmark-cases.json

repo-scorecard:
	$(PYTHON) -B scripts/repository_scorecard.py .

clean:
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
