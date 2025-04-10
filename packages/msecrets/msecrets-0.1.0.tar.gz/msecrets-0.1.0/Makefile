.PHONY: help ## Print this help
help:
	@grep -E '^\.PHONY: [a-zA-Z_-]+ .*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'


.PHONY: init ## Initialize for development
init:
	@uv sync


.PHONY: clean ## Cleanup generated files
clean:
	@rm -rf *.egg-info build dist docs/_build .coverage results.xml
	@find . -type d -name __pycache__ -exec rm -r {} \+


.PHONY: publish  ## Publish current version
publish:
	uv build
	uv publish
