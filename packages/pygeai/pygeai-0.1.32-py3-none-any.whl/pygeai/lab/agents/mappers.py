from pygeai.lab.models import Agent, AgentList, SharingLink


class AgentMapper:
    """
        A utility class for mapping agent-related data structures.
    """

    @classmethod
    def map_to_agent_list(cls, data: dict) -> AgentList:
        """
        Maps an API response dictionary to an `AgentList` object.

        This method extracts agents from the given data, converts them into a list of `Agent` objects,
        and returns an `AgentList` containing the list.

        :param data: dict - The dictionary containing agent response data.
        :return: AgentList - A structured response containing a list of agents.
        """
        agent_list = list()
        agents = data.get('agents')
        if agents is not None and any(agents):
            for agent_data in agents:
                agent = cls.map_to_agent(agent_data)
                agent_list.append(agent)

        return AgentList(agents=agent_list)

    @classmethod
    def map_to_agent(cls, data: dict) -> Agent:
        """
        Maps a dictionary to an `Agent` object.

        :param data: dict - The dictionary containing agent details.
        :return: Agent - The mapped `Agent` object.
        """
        return Agent(
            id=data.get("id"),
            status=data.get("status"),
            name=data.get("name"),
            access_scope=data.get("accessScope"),
            public_name=data.get("publicName"),
            avatar_image=data.get("avatarImage"),
            description=data.get("description"),
            job_description=data.get("jobDescription"),
            is_draft=data.get("isDraft"),
            is_readonly=data.get("isReadonly"),
            revision=data.get("revision"),
            version=data.get("version")
        )

    @classmethod
    def map_to_sharing_link(cls, data: dict) -> SharingLink:
        """
        Maps a dictionary response to a SharingLink object.

        :param data: dict - The raw response data containing agentId, apiToken, and sharedLink.
        :return: SharingLink - A SharingLink object representing the sharing link details.
        """
        return SharingLink(
            agent_id=data.get('agentId'),
            api_token=data.get('apiToken'),
            shared_link=data.get('sharedLink'),
        )