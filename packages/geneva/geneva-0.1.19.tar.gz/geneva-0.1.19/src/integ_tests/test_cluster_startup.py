import datetime
import importlib
import random

import pytest
import ray

from geneva.runners.ray.raycluster import RayCluster, _HeadGroupSpec, _WorkerGroupSpec


def test_cluster_startup() -> None:
    cluster_name = "geneva-integ-test"
    cluster_name += f"-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')}"
    cluster_name += f"-{random.randint(0, 10000)}"
    with RayCluster(
        name=cluster_name,
        namespace="geneva",
        use_port_forward=True,
        # allocate at least a single worker so the test runs faster
        # that we save time on waiting for the actor to start
        worker_groups=[
            _WorkerGroupSpec(
                name="worker",
                min_replicas=1,
            )
        ],
    ):
        ray.get(ray.remote(lambda: 1).remote())


def test_cluster_startup_no_gcs_permission() -> None:
    """
    Test the if we try to import geneva, which uses gcs for
    workspace packaging magic, errors when the service account
    doesn't have permission to access the gcs bucket.
    """

    cluster_name = "geneva-integ-test"
    cluster_name += f"-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')}"
    cluster_name += f"-{random.randint(0, 10000)}"

    with (
        RayCluster(
            name=cluster_name,
            namespace="geneva",
            use_port_forward=True,
            # allocate at least a single worker so the test runs faster
            # that we save time on waiting for the actor to start
            worker_groups=[
                _WorkerGroupSpec(
                    name="worker",
                    min_replicas=1,
                )
            ],
        ),
        pytest.raises(PermissionError, match="PERMISSION_DENIED"),
    ):
        ray.get(ray.remote(lambda: importlib.import_module("geneva")).remote())


def test_cluster_startup_can_import_geneva_and_lance(
    geneva_k8s_service_account: str,
) -> None:
    """
    Test the if we try to import geneva, which uses gcs for
    workspace packaging magic, errors when the service account
    doesn't have permission to access the gcs bucket.
    """

    cluster_name = "geneva-integ-test"
    cluster_name += f"-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')}"
    cluster_name += f"-{random.randint(0, 10000)}"

    with RayCluster(
        name=cluster_name,
        namespace="geneva",
        use_port_forward=True,
        head_group=_HeadGroupSpec(
            service_account=geneva_k8s_service_account,
        ),
        # allocate at least a single worker so the test runs faster
        # that we save time on waiting for the actor to start
        worker_groups=[
            _WorkerGroupSpec(
                name="worker",
                min_replicas=1,
                service_account=geneva_k8s_service_account,
            )
        ],
    ):
        ray.get(ray.remote(lambda: importlib.import_module("geneva")).remote())
        ray.get(ray.remote(lambda: importlib.import_module("lance")).remote())
