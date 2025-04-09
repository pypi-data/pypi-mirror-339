from typing import List

from pygeai.lab.models import AgenticProcess, KnowledgeBase, AgenticActivity, ArtifactSignal, UserSignal, Event, \
    SequenceFlow, Task, AgenticProcessList, TaskList, ProcessInstance, ProcessInstanceList, Variable


class AgenticProcessMapper:
    @classmethod
    def _map_knowledge_base(cls, kb_data: dict) -> KnowledgeBase:
        return KnowledgeBase(
            name=kb_data.get("name"),
            artifact_type_name=kb_data.get("artifactTypeName"),
            id=kb_data.get("id")
        )

    @classmethod
    def _map_agentic_activities(cls, activities_data: List[dict]) -> List[AgenticActivity]:
        return [
            AgenticActivity(
                key=activity.get("key"),
                name=activity.get("name"),
                task_name=activity.get("taskName"),
                agent_name=activity.get("agentName"),
                agent_revision_id=activity.get("agentRevisionId"),
                agent_id=activity.get("agentId"),
                task_id=activity.get("taskId"),
                task_revision_id=activity.get("taskRevisionId")
            )
            for activity in activities_data
        ]

    @classmethod
    def _map_artifact_signals(cls, signals_data: List[dict]) -> List[ArtifactSignal]:
        return [
            ArtifactSignal(
                key=signal.get("key"),
                name=signal.get("name"),
                handling_type=signal.get("handlingType"),
                artifact_type_name=signal.get("artifactTypeName")
            )
            for signal in signals_data
        ]

    @classmethod
    def _map_user_signals(cls, signals_data: List[dict]) -> List[UserSignal]:
        return [
            UserSignal(
                key=signal.get("key"),
                name=signal.get("name")
            )
            for signal in signals_data
        ]

    @classmethod
    def _map_event(cls, event_data: dict) -> Event:
        return Event(
            key=event_data.get("key"),
            name=event_data.get("name")
        )

    @classmethod
    def _map_sequence_flows(cls, flows_data: List[dict]) -> List[SequenceFlow]:
        return [
            SequenceFlow(
                key=flow.get("key"),
                source_key=flow.get("sourceKey"),
                target_key=flow.get("targetKey")
            )
            for flow in flows_data
        ]

    @classmethod
    def map_to_agentic_process(cls, data: dict) -> AgenticProcess:
        process_data = data.get("processDefinition", data)
        return AgenticProcess(
            key=process_data.get("key"),
            name=process_data.get("name"),
            description=process_data.get("description"),
            kb=cls._map_knowledge_base(process_data.get("kb")),
            agentic_activities=cls._map_agentic_activities(process_data.get("agenticActivities")),
            artifact_signals=cls._map_artifact_signals(process_data.get("artifactSignals")),
            user_signals=cls._map_user_signals(process_data.get("userSignals")),
            start_event=cls._map_event(process_data.get("startEvent")),
            end_event=cls._map_event(process_data.get("endEvent")),
            sequence_flows=cls._map_sequence_flows(process_data.get("sequenceFlows")),
            id=process_data.get("id"),
            status=process_data.get("Status"),
            version_id=process_data.get("VersionId"),
            is_draft=process_data.get("isDraft"),
            revision=process_data.get("revision")
        )

    @classmethod
    def map_to_agentic_process_list(cls, data: dict) -> AgenticProcessList:
        process_list = []
        processes = data.get("processes", data if isinstance(data, list) else [])
        if processes and any(processes):
            for process_data in processes:
                process = cls.map_to_agentic_process(process_data)
                process_list.append(process)
        return AgenticProcessList(processes=process_list)


class TaskMapper:
    @classmethod
    def map_to_task(cls, data: dict) -> Task:
        task_data = data.get("taskDefinition", data)
        return Task(
            name=task_data.get("name"),
            description=task_data.get("description"),
            title_template=task_data.get("titleTemplate"),
            id=task_data.get("id"),
            is_draft=task_data.get("isDraft"),
            revision=task_data.get("revision"),
            status=task_data.get("status")
        )

    @classmethod
    def map_to_task_list(cls, data: dict) -> TaskList:
        task_list = []
        tasks = data.get("tasks", data if isinstance(data, list) else [])
        if tasks and any(tasks):
            for task_data in tasks:
                task = cls.map_to_task(task_data)
                task_list.append(task)
        return TaskList(tasks=task_list)


class ProcessInstanceMapper:
    @classmethod
    def _map_variables(cls, variables_data: List[dict]) -> List[Variable]:
        return [
            Variable(
                key=var.get("key"),
                value=var.get("value")
            )
            for var in variables_data
        ] if variables_data else []

    @classmethod
    def map_to_process_instance(cls, data: dict) -> ProcessInstance:
        instance_data = data.get("instanceDefinition", data)
        variables_data = instance_data.get("variables")
        return ProcessInstance(
            id=instance_data.get("instanceId"),
            process_name=instance_data.get("process"),
            subject=instance_data.get("subject"),
            variables=cls._map_variables(variables_data) if variables_data else None,
            status=instance_data.get("status")
        )

    @classmethod
    def map_to_process_instance_list(cls, data: dict) -> ProcessInstanceList:
        instance_list = []
        instances = data.get("instances", data if isinstance(data, list) else [])
        if instances and any(instances):
            for instance_data in instances:
                instance = cls.map_to_process_instance(instance_data)
                instance_list.append(instance)
        return ProcessInstanceList(instances=instance_list)