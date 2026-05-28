PYTHON ?= python3
SKILL_DIR := skill/mbti-typing

.PHONY: test validate benchmark regression scorecard activation blind-review-audit consent-redaction-audit agent-adapter-audit question-lab-sync question-lab-audit type-duel-lab-sync type-duel-lab-audit follow-up-lab-audit session-lab-audit case-gallery-sync case-gallery-audit calibration-lab-sync calibration-lab-audit repo-scorecard clean

test: validate clean benchmark regression scorecard activation blind-review-audit consent-redaction-audit agent-adapter-audit question-lab-sync question-lab-audit type-duel-lab-sync type-duel-lab-audit follow-up-lab-audit session-lab-audit case-gallery-sync case-gallery-audit calibration-lab-sync calibration-lab-audit repo-scorecard clean

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

blind-review-audit:
	$(PYTHON) -B scripts/blind_review_audit.py examples/blind-review-matrix.json

consent-redaction-audit:
	$(PYTHON) -B scripts/consent_redaction_audit.py examples/consented-followup-packet.json

agent-adapter-audit:
	$(PYTHON) -B scripts/agent_adapter_audit.py .

question-lab-sync:
	$(PYTHON) -B scripts/sync_question_lab.py $(SKILL_DIR)/references/question-bank.md docs/question-lab.html

question-lab-audit:
	$(PYTHON) -B scripts/question_lab_audit.py docs/question-lab.html $(SKILL_DIR)/references/question-bank.md

type-duel-lab-sync:
	$(PYTHON) -B scripts/sync_type_duel_lab.py $(SKILL_DIR)/references/pair-duels.md docs/type-duel-lab.html

type-duel-lab-audit:
	$(PYTHON) -B scripts/type_duel_lab_audit.py docs/type-duel-lab.html $(SKILL_DIR)/references/pair-duels.md

follow-up-lab-audit:
	$(PYTHON) -B scripts/follow_up_lab_audit.py docs/follow-up-lab.html

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
