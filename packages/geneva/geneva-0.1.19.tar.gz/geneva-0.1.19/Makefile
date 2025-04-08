
.PHONY: setup
setup: kind-teardown kuberay
	uv sync --all-groups --all-extras --no-extra dataflow --no-extra prefect --locked

.PHONY: test
# force kind cluster recreate for each test
test:
	# 4 testing workers run into oom on 16gb machine - test_runners_ray
	# 8 testing workers run well with a 48gb machine
	uv run pytest -n 8 --runxfail -m "not serial"
	uv run pytest --runxfail -m serial

.PHONY: test-resetup
test-resetup: setup test

.PHONY: lint
lint:
	uv run ruff format
	uv run ruff check --fix
	uv run pyright

.PHONY: docs
docs:
	# uv sync --extra docs # this blows up other dependencies / e.g. notebooks
	cd docs ; uv run mkdocs serve

.PHONY: kind
kind:
	tools/setup_kind_cluster.sh

.PHONY: kind-teardown
kind-teardown:
	kind delete cluster --name geneva

.PHONY: kuberay
kuberay: kind
	tools/setup_kuberay.sh
