"""
Core functionality for image tag helper.
"""
import requests
import logging
from tenacity import retry, stop_after_attempt


logger = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(7))
def get_image_tag_by_short_name(tag, arch, registry_url=None, repository=None):
    """
    Get the full image tag by short name.
    
    Args:
        tag: Short tag name
        arch: Architecture (e.g., amd64, arm64)
        registry_url: Registry URL, defaults to harbor.milvus.io
        repository: Repository path, defaults to milvus/milvus
        
    Returns:
        Full tag name
    """
    registry_url = registry_url or "harbor.milvus.io"
    repository = repository or "milvus/milvus"
    
    logger.debug(f"Getting image tag for: tag={tag}, arch={arch}, registry={registry_url}, repository={repository}")
    
    # Split repository into project and repo
    repo_parts = repository.split('/')
    if len(repo_parts) != 2:
        error_msg = "Repository should be in format 'project/repository'"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    project, repo = repo_parts
    prefix = tag.split("-")[0]
    
    # Different handling based on registry type
    if "harbor" in registry_url:
        logger.debug("Using Harbor registry API")
        return _get_harbor_tag(registry_url, project, repo, prefix, tag, arch)
    elif "docker" in registry_url:
        logger.debug("Using Docker Hub API")
        return _get_docker_tag(registry_url, repository, prefix, tag, arch)
    else:
        logger.debug("Using default Harbor-like API")
        return _get_harbor_tag(registry_url, project, repo, prefix, tag, arch)


def _get_harbor_tag(registry_url, project, repo, prefix, tag, arch):
    """Get tag from Harbor registry"""
    url = f"https://{registry_url}/api/v2.0/projects/{project}/repositories/{repo}/artifacts?with_tag=true&q=tags%253D~{prefix}-&page_size=100&page=1"
    
    logger.debug(f"Requesting Harbor API: {url}")
    response = requests.get(url)
    response.raise_for_status()
    
    rsp = response.json()
    tag_list = []
    
    for r in rsp:
        tags = r["tags"]
        for t in tags:
            tag_list.append(t["name"])
    
    logger.debug(f"Found {len(tag_list)} tags matching prefix {prefix}")
    
    # First try: match both four-segment format and arch
    tag_candidates = []
    for t in tag_list:
        r = t.split("-")
        if len(r) == 4 and arch in t:  # version-date-commit-arch
            tag_candidates.append(t)
    
    tag_candidates.sort()
    if len(tag_candidates) > 0:
        logger.debug(f"Found {len(tag_candidates)} tags matching 4-segment format with arch {arch}")
        return tag_candidates[-1]
    
    # Second try: only match three-segment format if no matches found
    tag_candidates = []
    for t in tag_list:
        r = t.split("-")
        if len(r) == 3:  # version-date-commit
            tag_candidates.append(t)
    
    tag_candidates.sort()
    if len(tag_candidates) == 0:
        logger.warning(f"No matching tags found for prefix {prefix}, returning original tag")
        return tag
    else:
        logger.debug(f"Found {len(tag_candidates)} tags matching 3-segment format")
        return tag_candidates[-1]


def _get_docker_tag(registry_url, repository, prefix, tag, arch):
    """Get tag from Docker Hub or compatible registry"""
    # Docker Hub API v2
    url = f"https://hub.docker.com/v2/repositories/{repository}/tags"
    
    logger.debug(f"Requesting Docker Hub API: {url}")
    response = requests.get(url)
    response.raise_for_status()
    
    rsp = response.json()
    tag_list = []
    
    for result in rsp.get("results", []):
        tag_name = result.get("name")
        last_updated = result.get("last_updated")
        if tag_name and last_updated:
            if tag_name.startswith(prefix) and tag_name.endswith(arch):
                r = tag_name.split("-")
                if len(r) == 4:  # version-date-commit-arch
                    tag_list.append((tag_name, last_updated))
    
    if not tag_list:
        logger.warning(f"No matching tags found for prefix {prefix} and arch {arch}, returning original tag")
        return tag
    
    # 按更新时间排序，返回最新的标签
    tag_list.sort(key=lambda x: x[1], reverse=True)
    logger.debug(f"Found {len(tag_list)} tags matching criteria, returning latest")
    return tag_list[0][0]
