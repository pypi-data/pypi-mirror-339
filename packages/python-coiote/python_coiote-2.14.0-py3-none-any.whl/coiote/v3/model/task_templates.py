from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class TaskTemplateConfig:
    taskName: str
    parameters: List[Dict[str, str]]
    isActive: bool
    properties: Dict[str, str]

    @staticmethod
    def empty():
        return TaskTemplateConfig(taskName=None, parameters=[], isActive=True, properties={})

@dataclass
class TaskTemplateInvocation:
    templateName: str
    config: Optional[TaskTemplateConfig] = TaskTemplateConfig.empty()
    callback: Optional[dict] = None
