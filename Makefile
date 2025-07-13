.PHONY: test
test:
	uv run pytest -vv tests/

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  test    - Run tests using pytest"
	@echo "  help    - Show this help message"