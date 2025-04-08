#!/bin/env bash

# script to setup kind cluster for local development

set -ex

if command -v "helm" &> /dev/null; then
  echo "Found that 'helm' exists."
else
  echo "'helm' is not found, please refer to DEVELOPMENT.md and setup helm cli locally"
  exit 1
fi

namespace=$KUBERAY_NAMESPACE
if [ -z "$namespace" ]; then
  namespace="geneva"
fi

helm repo add kuberay https://ray-project.github.io/kuberay-helm/
helm repo update
helm upgrade kuberay-operator kuberay/kuberay-operator --version 1.3.0 --install --create-namespace --namespace $namespace --wait
