# src/wiz_mcp/server.py
import asyncio
import os
from typing import Any, Dict, List, TypedDict, Optional
import aiohttp
from mcp.server.fastmcp import FastMCP

class ResourceItem(TypedDict):
    cluster: str
    name: str 
    namespace: str

# Initialize FastMCP server with dependencies
dep = ["aiohttp","asyncio"]
mcp = FastMCP("wiz-mcp", dependencies=dep)

# Environment variables
USER = os.environ.get('KS_USER', 'admin')
BASE_URL = os.environ.get('KS_APISERVER_ENDPOINT', 'http://172.31.17.47:30881')
TOKEN = os.environ.get('KS_TOKEN', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwOi8va3MtY29uc29sZS5rdWJlc3BoZXJlLXN5c3RlbS5zdmM6MzA4ODAiLCJzdWIiOiJhZG1pbiIsImV4cCI6MTc0MzY3NzQwNSwiaWF0IjoxNzQzNjcwMjA1LCJ0b2tlbl90eXBlIjoiYWNjZXNzX3Rva2VuIiwidXNlcm5hbWUiOiJhZG1pbiJ9.b32b54OCCnXYcfq4UG_Y4VdGFOUcaoqEXSsxm7wB2nk')

HEADERS = {
    "Accept": "application/json",
    "X-Remote-User": USER,
    "Authorization": f"Bearer {TOKEN}"
}

async def fetch_json(session: aiohttp.ClientSession, url: str) -> Any:
    async with session.get(url, headers=HEADERS) as response:
        return await response.json()

@mcp.tool()
async def get_logging(cluster: str, pod: str) -> Any:
    """
    Retrieve logs for a specific pod in a cluster.

    Args:
        cluster (str): The name of the cluster.
        pod (str): The name of the pod.

    Returns:
        Any: The logs retrieved from the specified pod.
    """
    url = f"{BASE_URL}/kapis/logging.kubesphere.io/v1alpha2/logs?cluster={cluster}&pods={pod}&size=30"
    async with aiohttp.ClientSession() as session:
        return await fetch_json(session, url)

@mcp.tool()
async def get_events(cluster: str, pod: str) -> Any:
    """
    Retrieve events for a specific pod in a cluster.

    Args:
        cluster (str): The name of the cluster.
        pod (str): The name of the pod.

    Returns:
        Any: The events retrieved from the specified pod.
    """
    url = f"{BASE_URL}/kapis/logging.kubesphere.io/v1alpha2/events?cluster={cluster}&involved_object_name_filter={pod}&size=30"
    async with aiohttp.ClientSession() as session:
        return await fetch_json(session, url)

@mcp.tool()
async def list_all_clusters() -> Dict[str, Any]:
    """
    Retrieve all clusters and their details.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - "count" (int): The total number of clusters.
            - "clusters" (List[str]): A list of cluster names.
    """
    url = f"{BASE_URL}/kapis/tenant.kubesphere.io/v1beta1/clusters"
    async with aiohttp.ClientSession() as session:
        resp = await fetch_json(session, url)
        cluster_names = [cluster['metadata']['name'] for cluster in resp['items']]
        return {
            "count": len(cluster_names),
            "clusters": cluster_names
        }

@mcp.tool()
async def list_cluster_resources(cluster: list[str], resourceType: str) -> List[List[ResourceItem]]:
    """
    Retrieve resources of a specific type for a list of clusters.

    Args:
        cluster (list[str]): A list of cluster names.
        resourceType (str): The type of Kubernetes resource (e.g., pods, deployments, configmaps, secrets, namespaces).

    Returns:
        List[List[ResourceItem]]: A list of resources for each cluster, where each resource includes:
            - "cluster" (str): The cluster name.
            - "name" (str): The resource name.
            - "namespace" (str): The namespace of the resource (or "N/A" if not applicable).
    """
    urls = [f"{BASE_URL}/clusters/{c}/kapis/resources.kubesphere.io/v1alpha3/{resourceType}" for c in cluster]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_json(session, url) for url in urls]
        responses = await asyncio.gather(*tasks)
        for i, resp in enumerate(responses):
            responses[i] = [
                {
                    "cluster": cluster[i],
                    "name": item['metadata']['name'],
                    "namespace": item['metadata'].get('namespace', 'N/A')
                }
                for item in resp['items']
            ]
        return responses

# 获取指定资源的全部信息
@mcp.tool()
async def get_namespace_resource_info(cluster: str, resourceType: str, namespace: str, name: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve details of a specific namespace-level resource in a cluster.

    Args:
        cluster (str): The name of the cluster.
        resourceType (str): The type of Kubernetes resource (e.g., pods, deployments, configmaps, secrets).
        namespace (str): The namespace of the resource.
        name (str): The name of the resource.

    Returns:
        Optional[Dict[str, Any]]: The resource details if found, otherwise None.
    """
    url = f"{BASE_URL}/clusters/{cluster}/kapis/resources.kubesphere.io/v1alpha3/namespaces/{namespace}/{resourceType}"
    async with aiohttp.ClientSession() as session:
        resp = await fetch_json(session, url)
        for item in resp['items']:
            if item['metadata']['name'] == name:
                return item
    return None

@mcp.tool()
async def get_cluster_resource_info(cluster: str, resourceType: str, name: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve details of a specific cluster-level resource in a cluster.

    Args:
        cluster (str): The name of the cluster.
        resourceType (str): The type of Kubernetes resource (e.g., clusters, namespaces).
        name (str): The name of the resource.

    Returns:
        Optional[Dict[str, Any]]: The resource details if found, otherwise None.
    """
    url = f"{BASE_URL}/clusters/{cluster}/kapis/resources.kubesphere.io/v1alpha3/{resourceType}"
    async with aiohttp.ClientSession() as session:
        resp = await fetch_json(session, url)
        for item in resp['items']:
            if item['metadata']['name'] == name:
                return item
    return None


@mcp.prompt()
def analyse_special_cluster(cluster: str) -> str:
    """Analyse all clusters and provide report
    Args:
        cluster: Cluster name
    """
    return f"Please analyse the cluster {cluster} status and give me a report."

@mcp.prompt()
def analyse_all_cluster() -> Any:
    """Analyze all clusters and provide a summary report
    """
    return "Please analyse all cluster status and give me a report"

def start_server() -> None:
    """Initialize and run the server"""
    mcp.run(transport="stdio")

if __name__ == "__main__":
    start_server()