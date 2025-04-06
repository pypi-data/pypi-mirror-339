from datetime import datetime
from enum import Enum


class FlowType(str, Enum):
    STREAM: str = "stream"
    GROUP: str = "group"
    PROCESS: str = "process"


def get_workflow(flow_type: FlowType):
    from ddeutil.workflow import Workflow

    if flow_type == FlowType.STREAM:
        return Workflow.from_loader("stream-workflow")
    elif flow_type == FlowType.GROUP:
        return Workflow.from_loader("group-workflow")
    else:
        return Workflow.from_loader("process-workflow")


class Flow:
    def __init__(self, name: str, flow_type: FlowType = FlowType.STREAM):
        self.name = name
        self.type = flow_type

    def run(self, mode: str):
        from ddeutil.workflow import Workflow

        workflow = Workflow.from_loader("stream-workflow")
        workflow.release(
            release=datetime.now(),
            params={
                "stream": self.name,
                "run-mode": mode,
            },
        )
