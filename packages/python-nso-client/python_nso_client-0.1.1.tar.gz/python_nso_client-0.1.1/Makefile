.PHONY: help
help: ## Display this help (default)
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "  %-17s%s\n", $$1, $$2}'


TESTS ?= tests
PYTEST_ARGS ?=
PYTEST_ARGS += -vx
PYTEST_ARGS += --showlocals
WATCHEXEC_ARGS ?=
WATCHEXEC_ARGS += -w src -w tests -w pyproject.toml -e py,json
WATCHEXEC_ARGS += --clear=clear
WATCHEXEC_ARGS += --print-events

dev-setup: ## Setup environment with UV
	uv sync

test: ## Run tests once, specify $TESTS for specific file/method
	uv run pytest $(PYTEST_ARGS) $(TESTS)

watch-test: ## Run tests every time code changes
	watchexec $(WATCHEXEC_ARGS) poetry run pytest $(PYTEST_ARGS) $(TESTS)

publish: ## Publish a relase to PyPI
	rm -fr dist/
	uv build
	uv publish


