from typing import Union, Optional, List

from pygeai.core.base.mappers import ErrorMapper, ResponseMapper
from pygeai.core.base.responses import ErrorListResponse, EmptyResponse
from pygeai.lab.agents.clients import AgentClient
from pygeai.lab.agents.mappers import AgentMapper
from pygeai.lab.models import FilterSettings, Agent, AgentList, SharingLink, Tool, ToolList, ToolParameter
from pygeai.lab.processes.clients import AgenticProcessClient
from pygeai.lab.strategies.clients import ReasoningStrategyClient
from pygeai.lab.tools.clients import ToolClient
from pygeai.lab.tools.mappers import ToolMapper


class AILabManager:

    def __init__(self, api_key: str = None, base_url: str = None, alias: str = "default"):
        self.__agent_client = AgentClient(api_key=api_key, base_url=base_url, alias=alias)
        self.__tool_client = ToolClient(api_key=api_key, base_url=base_url, alias=alias)
        self.__reasoning_strategy_client = ReasoningStrategyClient(api_key=api_key, base_url=base_url, alias=alias)
        self.__process_client = AgenticProcessClient(api_key=api_key, base_url=base_url, alias=alias)

    def get_agent_list(
            self,
            project_id: str,
            filter_settings: FilterSettings = None
    ) -> AgentList:
        """
        Retrieves a list of agents for a given project based on filter settings.

        This method queries the agent client to fetch a list of agents associated with the specified
        project ID, applying the provided filter settings. If the response contains errors, it maps
        them to an `ErrorListResponse`. Otherwise, it maps the response to an `AgentList`.

        :param project_id: str - The ID of the project to retrieve agents for.
        :param filter_settings: FilterSettings - The filter settings to apply to the agent list query.
            Includes fields such as status, start, count, access_scope, allow_drafts, and allow_external.
        :return: Union[AgentList, ErrorListResponse] - An `AgentList` containing the retrieved agents
            if successful, or an `ErrorListResponse` if the API returns errors.
        """
        if not filter_settings:
            filter_settings = FilterSettings()

        response_data = self.__agent_client.list_agents(
            project_id=project_id,
            status=filter_settings.status,
            start=filter_settings.start,
            count=filter_settings.count,
            access_scope=filter_settings.access_scope,
            allow_drafts=filter_settings.allow_drafts,
            allow_external=filter_settings.allow_external
        )
        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = AgentMapper.map_to_agent_list(response_data)

        return result

    def create_agent(
            self,
            project_id: str,
            agent: Agent,
            automatic_publish: bool = False
    ) ->Union[Agent, ErrorListResponse]:
        """
        Creates a new agent in the specified project using the provided agent configuration.

        This method sends a request to the agent client to create an agent based on the attributes
        of the provided `Agent` object. If the response contains errors, it maps them to an
        `ErrorListResponse`. Otherwise, it maps the response to an `Agent` object.

        :param project_id: str - Unique identifier of the project where the agent will be created.
        :param agent: Agent - The agent configuration object containing all necessary details,
            including name, access scope, public name, job description, avatar image, description,
            and agent data (prompt, LLM config, and models).
        :param automatic_publish: bool - Whether to automatically publish the agent after creation.
            Defaults to False.
        :return: Union[Agent, ErrorListResponse] - An `Agent` object representing the created agent
            if successful, or an `ErrorListResponse` if the API returns errors.
        """
        response_data = self.__agent_client.create_agent(
            project_id=project_id,
            name=agent.name,
            access_scope=agent.access_scope,
            public_name=agent.public_name,
            job_description=agent.job_description,
            avatar_image=agent.avatar_image,
            description=agent.description,
            agent_data_prompt=agent.agent_data.prompt.to_dict() if agent.agent_data is not None else None,
            agent_data_llm_config=agent.agent_data.llm_config.to_dict() if agent.agent_data is not None else None,
            agent_data_models=agent.agent_data.models.to_dict() if agent.agent_data is not None else None,
            automatic_publish=automatic_publish
        )
        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = AgentMapper.map_to_agent(response_data)

        return result

    def update_agent(
            self,
            project_id: str,
            agent: Agent,
            automatic_publish: bool = False,
            upsert: bool = False
    ) -> Union[Agent, ErrorListResponse]:
        """
        Updates an existing agent in the specified project using the provided agent configuration.

        This method sends a request to the agent client to update an agent identified by `agent_id`
        (or `agent.id` if not provided) based on the attributes of the provided `Agent` object.
        It can optionally publish the agent automatically or perform an upsert if the agent doesn’t exist.
        If the response contains errors, it maps them to an `ErrorListResponse`. Otherwise, it maps
        the response to an `Agent` object.

        :param project_id: str - Unique identifier of the project where the agent resides.
        :param agent: Agent - The agent configuration object containing updated details,
            including id, name, access scope, public name, job description, avatar image, description,
            and agent data (prompt, LLM config, and models).
        :param automatic_publish: bool - Whether to automatically publish the agent after updating.
            Defaults to False.
        :param upsert: bool - Whether to insert the agent if it does not exist (upsert) instead of
            just updating. Defaults to False.
        :return: Union[Agent, ErrorListResponse] - An `Agent` object representing the updated agent
            if successful, or an `ErrorListResponse` if the API returns errors.
        :raises ValueError: If neither `agent_id` nor `agent.id` is provided.
        """
        response_data = self.__agent_client.update_agent(
            project_id=project_id,
            agent_id=agent.id,
            name=agent.name,
            access_scope=agent.access_scope,
            public_name=agent.public_name,
            job_description=agent.job_description,
            avatar_image=agent.avatar_image,
            description=agent.description,
            agent_data_prompt=agent.agent_data.prompt.to_dict() if agent.agent_data is not None else None,
            agent_data_llm_config=agent.agent_data.llm_config.to_dict() if agent.agent_data is not None else None,
            agent_data_models=agent.agent_data.models.to_dict() if agent.agent_data is not None else None,
            automatic_publish=automatic_publish,
            upsert=upsert
        )
        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = AgentMapper.map_to_agent(response_data)

        return result

    def get_agent(
            self,
            project_id: str,
            agent_id: str,
            filter_settings: Optional[FilterSettings] = None
    ) -> Union[Agent, 'ErrorListResponse']:
        """
        Retrieves details of a specific agent from the specified project.

        This method sends a request to the agent client to retrieve an agent identified by `agent_id`
        from the specified project. Optional filter settings can be provided to specify the revision,
        version, and whether to allow drafts. If the response contains errors, it maps them to an
        `ErrorListResponse`. Otherwise, it maps the response to an `Agent` object.

        :param project_id: str - Unique identifier of the project where the agent resides.
        :param agent_id: str - Unique identifier of the agent to retrieve.
        :param filter_settings: FilterSettings, optional - Settings to filter the agent retrieval,
            including revision (defaults to "0"), version (defaults to 0), and allow_drafts (defaults to True).
        :return: Union[Agent, ErrorListResponse] - An `Agent` object representing the retrieved agent
            if successful, or an `ErrorListResponse` if the API returns errors.
        """
        if filter_settings is None:
            filter_settings = FilterSettings(
                revision="0",
                version="0",
                allow_drafts=True
            )

        response_data = self.__agent_client.get_agent(
            project_id=project_id,
            agent_id=agent_id,
            revision=filter_settings.revision,
            version=filter_settings.version,
            allow_drafts=filter_settings.allow_drafts
        )
        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = AgentMapper.map_to_agent(response_data)

        return result

    def create_sharing_link(
            self,
            project_id: str,
            agent_id: str
    ) -> Union[SharingLink, 'ErrorListResponse']:
        """
        Creates a sharing link for a specific agent in the specified project.

        This method sends a request to the agent client to create a sharing link for the agent
        identified by `agent_id` in the specified project. If the response contains errors, it maps
        them to an `ErrorListResponse`. Otherwise, it maps the response to a `SharingLink` object.

        :param project_id: str - Unique identifier of the project where the agent resides.
        :param agent_id: str - Unique identifier of the agent for which to create a sharing link.
        :return: Union[SharingLink, ErrorListResponse] - A `SharingLink` object representing the
            sharing link details if successful, or an `ErrorListResponse` if the API returns errors.
        """
        response_data = self.__agent_client.create_sharing_link(
            project_id=project_id,
            agent_id=agent_id
        )
        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = AgentMapper.map_to_sharing_link(response_data)

        return result

    def publish_agent_revision(
            self,
            project_id: str,
            agent_id: str,
            revision: str
    ) -> Union[Agent, 'ErrorListResponse']:
        """
        Publishes a specific revision of an agent in the specified project.

        This method sends a request to the agent client to publish the specified revision of the agent
        identified by `agent_id` in the specified project. If the response contains errors, it maps
        them to an `ErrorListResponse`. Otherwise, it maps the response to an `Agent` object
        representing the published agent.

        :param project_id: str - Unique identifier of the project where the agent resides.
        :param agent_id: str - Unique identifier of the agent to publish.
        :param revision: str - Revision of the agent to publish.
        :return: Union[Agent, ErrorListResponse] - An `Agent` object representing the published agent
            if successful, or an `ErrorListResponse` if the API returns errors.
        """
        response_data = self.__agent_client.publish_agent_revision(
            project_id=project_id,
            agent_id=agent_id,
            revision=revision
        )
        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = AgentMapper.map_to_agent(response_data)

        return result

    def delete_agent(
            self,
            project_id: str,
            agent_id: str
    ) -> Union[EmptyResponse, ErrorListResponse]:
        """
        Deletes a specific agent from the specified project.

        This method sends a request to the agent client to delete the agent identified by `agent_id`
        from the specified project. Returns True if the deletion is successful (indicated by an
        empty response or success confirmation), or an `ErrorListResponse` if the API returns errors.

        :param project_id: str - Unique identifier of the project where the agent resides.
        :param agent_id: str - Unique identifier of the agent to delete.
        :return: Union[EmptyResponse, ErrorListResponse] - EmptyResponse if the agent was deleted successfully,
            or an `ErrorListResponse` if the API returns errors.
        """
        response_data = self.__agent_client.delete_agent(
            project_id=project_id,
            agent_id=agent_id
        )
        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            response_data = response_data if response_data else "Agent deleted successfully"
            result = ResponseMapper.map_to_empty_response(response_data)

        return result

    def create_tool(
            self,
            project_id: str,
            tool: Tool,
            open_api_json: Optional[dict] = None,
            automatic_publish: bool = False
    ) -> Union[Tool, 'ErrorListResponse']:
        """
        Creates a new tool in the specified project using the provided tool configuration.

        This method sends a request to the agent client to create a tool based on the attributes
        of the provided `Tool` object. If the response contains errors, it maps them to an
        `ErrorListResponse`. Otherwise, it maps the response to a `Tool` object.

        :param project_id: str - Unique identifier of the project where the tool will be created.
        :param tool: Tool - The tool configuration object containing name, description, scope,
            and parameters. Optional fields (e.g., id, access_scope) are ignored for creation.
        :param open_api_json: dict, optional - OpenAPI JSON specification for the tool, required
            for tools with scope 'api'. If None, the existing OpenAPI specification (if any) is not updated.
        :param automatic_publish: bool - Whether to automatically publish the tool after creation.
            Defaults to False.
        :return: Union[Tool, ErrorListResponse] - A `Tool` object representing the created tool
            if successful, or an `ErrorListResponse` if the API returns errors.
        """
        parameters = [param.to_dict() for param in tool.parameters if tool.parameters is not None]

        response_data = self.__tool_client.create_tool(
            project_id=project_id,
            name=tool.name,
            description=tool.description,
            scope=tool.scope,
            parameters=parameters,
            open_api_json=open_api_json,
            automatic_publish=automatic_publish
        )
        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = ToolMapper.map_to_tool(response_data)

        return result

    def update_tool(
            self,
            project_id: str,
            tool: Tool,
            open_api_json: Optional[dict] = None,
            automatic_publish: bool = False,
            upsert: bool = False
    ) -> Union[Tool, ErrorListResponse]:
        """
        Updates an existing tool in the specified project or upserts it if specified.

        This method sends a request to the agent client to update a tool identified by `tool_id`
        based on the attributes of the provided `Tool` object. It can optionally publish the tool
        automatically or perform an upsert if the tool doesn’t exist. If the response contains
        errors, it maps them to an `ErrorListResponse`. Otherwise, it maps the response to a `Tool` object.

        :param project_id: str - Unique identifier of the project where the tool resides.
        :param tool: Tool - The tool configuration object containing updated details,
            including name, description, scope, and parameters.
        :param open_api_json: dict, optional - OpenAPI JSON specification for the tool, required
            for tools with scope 'api'. If None, the existing OpenAPI specification (if any) is not updated.
        :param automatic_publish: bool - Whether to automatically publish the tool after updating.
            Defaults to False.
        :param upsert: bool - Whether to insert the tool if it does not exist (upsert) instead of
            just updating. Defaults to False.
        :return: Union[Tool, ErrorListResponse] - A `Tool` object representing the updated tool
            if successful, or an `ErrorListResponse` if the API returns errors.
        """
        parameters = [param.to_dict() for param in tool.parameters if tool.parameters is not None]

        response_data = self.__tool_client.update_tool(
            project_id=project_id,
            tool_id=tool.id,
            open_api_json=open_api_json,
            name=tool.name,
            description=tool.description,
            scope=tool.scope,
            parameters=parameters,
            automatic_publish=automatic_publish,
            upsert=upsert
        )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = ToolMapper.map_to_tool(response_data)

        return result

    def get_tool(
            self,
            project_id: str,
            tool_id: str,
            filter_settings: Optional[FilterSettings] = None
    ) -> Union[Tool, 'ErrorListResponse']:
        """
        Retrieves details of a specific tool from the specified project.

        This method sends a request to the tool client to retrieve a tool identified by `tool_id`
        from the specified project. Optional filter settings can be provided to specify the revision,
        version, and whether to allow drafts. If the response contains errors, it maps them to an
        `ErrorListResponse`. Otherwise, it maps the response to a `Tool` object.

        :param project_id: str - Unique identifier of the project where the tool resides.
        :param tool_id: str - Unique identifier of the tool to retrieve.
        :param filter_settings: FilterSettings, optional - Settings to filter the tool retrieval,
            including revision (defaults to "0"), version (defaults to "0"), and allow_drafts (defaults to True).
        :return: Union[Tool, ErrorListResponse] - A `Tool` object representing the retrieved tool
            if successful, or an `ErrorListResponse` if the API returns errors.
        """
        if filter_settings is None:
            filter_settings = FilterSettings(
                revision="0",
                version="0",
                allow_drafts=True
            )

        response_data = self.__tool_client.get_tool(
            project_id=project_id,
            tool_id=tool_id,
            revision=filter_settings.revision,
            version=filter_settings.version,
            allow_drafts=filter_settings.allow_drafts
        )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = ToolMapper.map_to_tool(response_data)

        return result

    def list_tools(
            self,
            project_id: str,
            filter_settings: Optional[FilterSettings] = None
    ) -> Union[ToolList, ErrorListResponse]:
        """
        Retrieves a list of tools associated with the specified project.

        This method queries the tool client to fetch a list of tools for the given project ID,
        applying the specified filter settings. If the response contains errors, it maps them to an
        `ErrorListResponse`. Otherwise, it maps the response to a `ToolList` object using `ToolMapper`.

        :param project_id: str - Unique identifier of the project.
        :param filter_settings: FilterSettings, optional - Settings to filter the tool list query,
            including id (defaults to ""), count (defaults to "100"), access_scope (defaults to "public"),
            allow_drafts (defaults to True), scope (defaults to "api"), and allow_external (defaults to True).
        :return: Union[ToolList, ErrorListResponse] - A `ToolList` object containing the retrieved tools
            if successful, or an `ErrorListResponse` if the API returns errors.
        """
        if filter_settings is None:
            filter_settings = FilterSettings(
                id="",
                count="100",
                access_scope="public",
                allow_drafts=True,
                scope="api",
                allow_external=True
            )

        response_data = self.__tool_client.list_tools(
            project_id=project_id,
            id=filter_settings.id,
            count=filter_settings.count,
            access_scope=filter_settings.access_scope,
            allow_drafts=filter_settings.allow_drafts,
            scope=filter_settings.scope,
            allow_external=filter_settings.allow_external
        )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = ToolMapper.map_to_tool_list(response_data)

        return result

    def publish_tool_revision(
            self,
            project_id: str,
            tool_id: str,
            revision: str
    ) -> Union[Tool, 'ErrorListResponse']:
        """
        Publishes a specific revision of a tool in the specified project.

        This method sends a request to the tool client to publish the specified revision of the tool
        identified by `tool_id`. If the response contains errors, it maps them to an `ErrorListResponse`.
        Otherwise, it maps the response to a `Tool` object representing the published tool.

        :param project_id: str - Unique identifier of the project where the tool resides.
        :param tool_id: str - Unique identifier of the tool to publish.
        :param revision: str - Revision of the tool to publish.
        :return: Union[Tool, ErrorListResponse] - A `Tool` object representing the published tool
            if successful, or an `ErrorListResponse` if the API returns errors.
        """
        response_data = self.__tool_client.publish_tool_revision(
            project_id=project_id,
            tool_id=tool_id,
            revision=revision
        )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = ToolMapper.map_to_tool(response_data)

        return result

    def get_parameter(
            self,
            project_id: str,
            tool_id: Optional[str] = None,
            tool_public_name: Optional[str] = None,
            filter_settings: Optional[FilterSettings] = None
    ) -> Union[List[ToolParameter], 'ErrorListResponse']:
        """
        Retrieves details of parameters for a specific tool in the specified project.

        This method sends a request to the tool client to retrieve parameters for a tool identified
        by either `tool_id` or `tool_public_name`. Optional filter settings can specify revision,
        version, and whether to allow drafts. If the response contains errors, it maps them to an
        `ErrorListResponse`. Otherwise, it maps the response to a list of `ToolParameter` objects.

        :param project_id: str - Unique identifier of the project.
        :param tool_id: str, optional - Unique identifier of the tool whose parameters are to be retrieved.
        :param tool_public_name: str, optional - Public name of the tool whose parameters are to be retrieved.
        :param filter_settings: FilterSettings, optional - Settings to filter the parameter retrieval,
            including revision (defaults to "0"), version (defaults to "0"), and allow_drafts (defaults to True).
        :return: Union[List[ToolParameter], ErrorListResponse] - A list of `ToolParameter` objects if successful,
            or an `ErrorListResponse` if the API returns errors.
        :raises ValueError: If neither tool_id nor tool_public_name is provided.
        """
        if not (tool_id or tool_public_name):
            raise ValueError("Either tool_id or tool_public_name must be provided.")

        if filter_settings is None:
            filter_settings = FilterSettings(
                revision="0",
                version="0",
                allow_drafts=True
            )

        response_data = self.__tool_client.get_parameter(
            project_id=project_id,
            tool_id=tool_id,
            tool_public_name=tool_public_name,
            revision=filter_settings.revision,
            version=filter_settings.version,
            allow_drafts=filter_settings.allow_drafts
        )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = ToolMapper.map_to_parameter_list(response_data)

        return result

    def set_parameter(
            self,
            project_id: str,
            tool_id: Optional[str] = None,
            tool_public_name: Optional[str] = None,
            parameters: List[ToolParameter] = None
    ) -> Union[Tool, 'ErrorListResponse']:
        """
        Sets or updates parameters for a specific tool in the specified project.

        This method sends a request to the tool client to set parameters for a tool identified by
        either `tool_id` or `tool_public_name`. If the response contains errors, it maps them to an
        `ErrorListResponse`. Otherwise, it maps the response to a `Tool` object.

        :param project_id: str - Unique identifier of the project.
        :param tool_id: str, optional - Unique identifier of the tool whose parameters are to be set.
        :param tool_public_name: str, optional - Public name of the tool whose parameters are to be set.
        :param parameters: List[ToolParameter] - List of parameter objects defining the tool's parameters.
        :return: Union[Tool, ErrorListResponse] - A `Tool` object representing the updated tool if successful,
            or an `ErrorListResponse` if the API returns errors.
        :raises ValueError: If neither tool_id nor tool_public_name is provided, or if parameters is None or empty.
        """
        if not (tool_id or tool_public_name):
            raise ValueError("Either tool_id or tool_public_name must be provided.")
        if not parameters:
            raise ValueError("Parameters list must be provided and non-empty.")

        params_dict = [param.to_dict() for param in parameters]

        response_data = self.__tool_client.set_parameter(
            project_id=project_id,
            tool_id=tool_id,
            tool_public_name=tool_public_name,
            parameters=params_dict
        )
        print(f"response_data: {response_data}")
        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            # result = ToolMapper.map_to_tool(response_data)
            result = ResponseMapper.map_to_empty_response(response_data)

        return result