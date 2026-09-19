import os
import platform
import psutil
from typing import Dict, Any
from pydantic import BaseModel

class HardwareProfile(BaseModel):
    system_type: str # local_machine, vps_cloud, docker_container
    os_name: str
    cpu_count: int
    total_ram_gb: float
    recommended_model_tier: str # "large_70b", "medium_7b_14b", "cloud_api_only"
    is_docker: bool

class HardwareRuntimeDetector:
    """
    Detects hardware profile to tailor agent performance:
    - Dedicated Local Machine (e.g. Mac Studio 64GB RAM): Can run local 70B/Qwen models.
    - VPS Cloud Server ($5-$6/mo): Offloads background daemons with lightweight local or API models.
    - Docker Container: Isolates tool execution with strict memory and CPU caps.
    """
    @staticmethod
    def detect() -> HardwareProfile:
        os_name = platform.system()
        cpu_count = os.cpu_count() or 2
        
        # Estimate total RAM
        try:
            total_ram_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
        except (AttributeError, ValueError):
            total_ram_bytes = 16 * (1024 ** 3) # fallback 16GB
        
        total_ram_gb = round(total_ram_bytes / (1024 ** 3), 1)
        is_docker = os.path.exists("/.dockerenv")

        if total_ram_gb >= 60:
            recommended = "large_70b"
            sys_type = "local_high_ram_workstation"
        elif total_ram_gb >= 16:
            recommended = "medium_7b_14b"
            sys_type = "local_standard_pc"
        else:
            recommended = "cloud_api_only"
            sys_type = "vps_cloud" if not is_docker else "docker_container"

        return HardwareProfile(
            system_type=sys_type,
            os_name=os_name,
            cpu_count=cpu_count,
            total_ram_gb=total_ram_gb,
            recommended_model_tier=recommended,
            is_docker=is_docker
        )
