from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP


class ConfigfacetsMCP:
    def __init__(
        self,
        repository: str,
        version: str,
        api_key: str,
        server: str = "configfacets",
        user_agent: str = "configfacets-mcp/1.0",
    ):
        self.server = repository
        self.version = version
        self.api_key = api_key
        self.domain_prefix = "https://configfacets.com/apis"
        self.user_agent = user_agent

        self.mcp = FastMCP(server)
        self._register_tools()

    def run(self, **kwargs):
        self.mcp.run(**kwargs)

    def _register_tools(self):
        @self.mcp.tool()
        async def search_endpoint_resources(keywords: list[str]) -> str:
            """
            Endpoint resource allows you to fetch data from remote source. Endpoint execution can be from mconnect server or from
            user client machine.

            Is this endpoint exposed to internet: true  # To be executed at mconnect server
            Is this endpoint exposed to internet: false # To be executed at user's client machine using fetch_mconnect_data(), LLM needs
            to generate data based on Endpoint and call fetch_mconnect_data

            LLM Instructions:
            Returns a resources metadata in string format, which can be later used to identify correct resource to be used by LLM.
            """

            dataSearchUrl = "{domain}/repos/{repository}/{version}/search/endpoints?keywords={keywords}".format(
                domain=self.domain_prefix,
                repository=self.server,
                version=self.version,
                keywords=",".join(keywords),
            )
            instructions = {
                "url": dataSearchUrl,
                "method": "GET",
                "headers": {
                    "Accept": "text/markdown",
                    "X-APIKEY": self.api_key,
                },
            }
            data = await fetch_mconnect_data(instructions)
            if not data or not isinstance(data, str):
                return "Unable to fetch data. returned: {url}, data: {data}".format(
                    url=dataSearchUrl, data=data
                )
            return data

        @self.mcp.tool()
        async def exec_endpoint_resource_remotely(
            slug: str, payload: dict, contenttype: str, format: str = "json"
        ) -> Any:
            """
            Executes endpoint resource on MConnect server where it's hosted (Remote). returns data in format requested in argument.

            To determine if this endpoint can be executed remotely, check "Is this endpoint exposed to internet": true

            Payload Schema:
            schema: {
            $schema: "http://json-schema.org/draft-07/schema#",
            type: ["object", "array", "string", "number", "boolean", "null"],
            description: "Schema to accept any valid JSON.",
            }

            LLM Instructions:
            You are an AI Assistant, you need to follow
            - Only use filters that are given in 'Available Facets'
            - Strictly abide by payload/request schema.
            - Resource execution priority to be given to server and version specified in this MCP server
            - If execution was successfull and reponse is returned, then don't add any additional information to response unless explicitly asked by user.
            """
            dataExecUrl = "{domain}/repos/{slug}/exec?format={format}".format(
                domain=self.domain_prefix, slug=slug, format=format
            )
            instructions = {
                "url": dataExecUrl,
                "method": "POST",
                "headers": {
                    "Accept": "{}".format(contenttype),
                    "X-APIKEY": self.api_key,
                },
                "payload": payload,
            }
            data = await fetch_mconnect_data(instructions)
            if not data:
                return "Unable to exec endpoint. returned: {url}, data: {data}".format(
                    url=dataExecUrl, data=data
                )
            return data

        @self.mcp.tool()
        async def exec_endpoint_resource_locally(
            slug: str, payload: dict, contenttype: str, format: str = "json"
        ) -> Any:
            """
            Get endpoint execution instructions by passing request payload. MConnect sends back the request url, headers and other
            instructions that are required for local execution.

            Payload Schema:
            schema: {
            $schema: "http://json-schema.org/draft-07/schema#",
            type: ["object", "array", "string", "number", "boolean", "null"],
            description: "Schema to accept any valid JSON.",
            }

            LLM Instructions:
            ou are an AI Assistant, you need to follow
            - Only use filters that are given in 'Available Facets'
            - Strictly abide by payload/request schema. Payload are determined by related resources execution in previous LLM execution steps.
            - Resource execution priority to be given to server and version specified in this MCP server
            - If execution was successfull and reponse is returned, then don't add any additional information to response unless explicitly asked by user.
            - On receiving http response, it can then use fetch_mconnect_data(instructions) method to fetch data locally.

            """
            dataExecUrl = "{domain}/repos/{slug}/exec?format={format}".format(
                domain=self.domain_prefix, slug=slug, format=format
            )
            instructions = {
                "url": dataExecUrl,
                "method": "POST",
                "headers": {
                    "Accept": "{}".format(contenttype),
                    "X-APIKEY": self.api_key,
                },
                "payload": payload,
            }
            data = await fetch_mconnect_data(instructions)
            if not data:
                return "Unable to exec endpoint. returned: {url}, data: {data}".format(
                    url=dataExecUrl, data=data
                )
            return data

        @self.mcp.tool()
        async def search_data_resources(keywords: list[str]) -> str:
            """
            Data allows you to manage static or dynamic configurations that are of low complexity

            LLM Instructions:
            Returns a resources metadata in string format, which can be later used to identify correct resource to be used by LLM.
            """

            dataSearchUrl = "{domain}/repos/{repository}/{version}/search/data?keywords={keywords}".format(
                domain=self.domain_prefix,
                repository=self.server,
                version=self.version,
                keywords=",".join(keywords),
            )
            instructions = {
                "url": dataSearchUrl,
                "method": "GET",
                "headers": {
                    "Accept": "text/markdown",
                    "X-APIKEY": self.api_key,
                },
            }
            data = await fetch_mconnect_data(instructions)
            if not data or not isinstance(data, str):
                return "Unable to fetch data. returned: {url}, data: {data}".format(
                    url=dataSearchUrl, data=data
                )
            return data

        @self.mcp.tool()
        async def exec_data_resource(
            slug: str, payload: dict, contenttype: str, format: str = "json"
        ) -> Any:
            """
            Executes data resource, returns data in format requested in argument.

            Payload Schema:
            schema: {
            $schema: "http://json-schema.org/draft-07/schema#",
            type: ["object", "array", "string", "number", "boolean", "null"],
            description: "Schema to accept any valid JSON.",
            }

            LLM Instructions:
            You are an AI Assistant, you need to follow
            - Only use filters that are given in 'Available Facets'
            - Strictly abide by payload/request schema.
            - Resource execution priority to be given to server and version specified in this MCP server
            - If execution was successfull and reponse is returned, then don't add any additional information to response unless explicitly asked by user.
            """
            dataExecUrl = "{domain}/repos/{slug}/exec?format={format}".format(
                domain=self.domain_prefix, slug=slug, format=format
            )
            instructions = {
                "url": dataExecUrl,
                "method": "POST",
                "headers": {
                    "Accept": "{}".format(contenttype),
                    "X-APIKEY": self.api_key,
                },
                "payload": payload,
            }
            data = await fetch_mconnect_data(instructions)
            if not data:
                return "Unable to exec data. returned: {url}, data: {data}".format(
                    url=dataExecUrl, data=data
                )
            return data

        @self.mcp.tool()
        async def search_service_resources(keywords: list[str]) -> str:
            """
            While the configuration resource explained above generates a single configuration, the service resource creates a set of configurations. For example, an application may need to interact with multiple services like a database, API, frontend, and log collection service to function smoothly. Each of these services typically requires multiple configurations.The configfacets service resource is designed to support such use cases.

            Additionally, it manages dependencies between service resources. If any dependencies exist, their configurations are generated first, added to the list, and then followed by this service’s configurations.

            LLM Instructions:
            Returns a resources metadata in string format, which can be later used to identify correct resource to be used by LLM.
            """

            serviceSearchUrl = "{domain}/repos/{repository}/{version}/search/services?keywords={keywords}".format(
                domain=self.domain_prefix,
                repository=self.server,
                version=self.version,
                keywords=",".join(keywords),
            )
            instructions = {
                "url": serviceSearchUrl,
                "method": "GET",
                "headers": {
                    "Accept": "text/markdown",
                    "X-APIKEY": self.api_key,
                },
            }
            data = await fetch_mconnect_data(instructions)
            if not data or not isinstance(data, str):
                return "Unable to fetch services. returned: {url}, data: {data}".format(
                    url=serviceSearchUrl, data=data
                )
            return data

        @self.mcp.tool()
        async def exec_service_resource(
            slug: str, payload: dict, contenttype: str, format: str = "json"
        ) -> Any:
            """
            Executes service resource, returns data in format requested in argument.

            Format:
            json or yaml

            Payload Schema:
            schema: {
            $schema: "http://json-schema.org/draft-07/schema#",
            type: ["object", "array", "string", "number", "boolean", "null"],
            description: "Schema to accept any valid JSON.",
            }

            LLM Instructions:
            You are an AI Assistant, you need to follow
            - Only use filters that are given in 'Available Facets'
            - Strictly abide by payload/request schema.
            - Resource execution priority to be given to server and version specified in this MCP server
            - If execution was successfull and reponse is returned, then don't add any additional information to response unless explicitly asked by user.
            """
            configExecUrl = "{domain}/repos/{slug}/exec?format={format}".format(
                domain=self.domain_prefix, slug=slug, format=format
            )
            instructions = {
                "url": configExecUrl,
                "method": "POST",
                "headers": {
                    "Accept": "{}".format(contenttype),
                    "X-APIKEY": self.api_key,
                },
                "payload": payload,
            }
            data = await fetch_mconnect_data(instructions)
            if not data:
                return "Unable to exec service. returned: {url}, data: {data}".format(
                    url=configExecUrl, data=data
                )
            return data

        @self.mcp.tool()
        async def search_configuration_resources(keywords: list[str]) -> str:
            """
            Configuraiton resource generates complex config using templates, overrides and values.

            LLM Instructions:
            Returns a resources metadata in string format, which can be later used to identify correct resource to be used by LLM.
            """

            configurationSearchUrl = "{domain}/repos/{repository}/{version}/search/configurations?keywords={keywords}".format(
                domain=self.domain_prefix,
                repository=self.server,
                version=self.version,
                keywords=",".join(keywords),
            )
            instructions = {
                "url": configurationSearchUrl,
                "method": "GET",
                "headers": {
                    "Accept": "text/markdown",
                    "X-APIKEY": self.api_key,
                },
            }
            data = await fetch_mconnect_data(instructions)
            if not data or not isinstance(data, str):
                return "Unable to fetch configurations. returned: {url}, data: {data}".format(
                    url=configurationSearchUrl, data=data
                )
            return data

        @self.mcp.tool()
        async def exec_configuration_resource(
            slug: str, payload: dict, contenttype: str, format: str = "json"
        ) -> Any:
            """
            Executes configuration resource, returns data in format requested in argument.

            Format:
            json or yaml

            Payload Schema:
            {
                type: "object",
                properties: {
                    facets: {
                        type: "array",
                        items: {
                            type: "string",
                        },
                        default: [],
                    },
                    values: {
                        type: "object",
                        additionalProperties: true,
                        default: {},
                    },
                    globalvars: {
                        type: "object",
                        patternProperties: {
                            "^__[a-zA-Z0-9_]+__$": { type: "string" },
                        },

                        additionalProperties: false,
                        default: {},
                    },
                },
                additionalProperties: false,
                },
            };

            LLM Instructions:
            You are an AI Assistant, you need to follow
            - Only use filters that are given in 'Available Facets'
            - Strictly abide by payload/request schema.
            - Resource execution priority to be given to server and version specified in this MCP server
            - If execution was successfull and reponse is returned, then don't add any additional information to response unless explicitly asked by user.
            """
            configExecUrl = "{domain}/repos/{slug}/exec?format={format}".format(
                domain=self.domain_prefix, slug=slug, format=format
            )
            instructions = {
                "url": configExecUrl,
                "method": "POST",
                "headers": {
                    "Accept": "{}".format(contenttype),
                    "X-APIKEY": self.api_key,
                },
                "payload": payload,
            }
            data = await fetch_mconnect_data(instructions)
            if not data:
                return "Unable to exec configuration. returned: {url}, data: {data}".format(
                    url=configExecUrl, data=data
                )
            return data

        @self.mcp.tool()
        async def search_collection_resources(keywords: list[str]) -> str:
            """
            Organize related structured data into groups that can adapt to specific scenarios. By using facets within these groups, you can efficiently filter and merge data.

            LLM Instructions:
            Returns a resources metadata in string format, which can be later used to identify correct resource to be used by LLM.
            """
            collectionsSearchUrl = "{domain}/repos/{repository}/{version}/search/collections?keywords={keywords}".format(
                domain=self.domain_prefix,
                repository=self.server,
                version=self.version,
                keywords=",".join(keywords),
            )
            instructions = {
                "url": collectionsSearchUrl,
                "method": "GET",
                "headers": {
                    "Accept": "text/markdown",
                    "X-APIKEY": self.api_key,
                },
            }
            data = await fetch_mconnect_data(instructions)
            if not data or not isinstance(data, str):
                return (
                    "Unable to fetch collections. returned: {url}, data: {data}".format(
                        url=collectionsSearchUrl, data=data
                    )
                )
            return data

        @self.mcp.tool()
        async def exec_collection_resource(
            slug: str, payload: dict, contenttype: str, format: str = "json"
        ) -> Any:
            """
            Executes collection resource, returns data in format requested in argument

            Format:
            json or yaml

            Payload Schema:
            {
                type: "object",
                properties: {
                    facets: {
                        type: "array",
                        items: {
                            type: "string",
                        },
                        default: [],
                    },
                    values: {
                        type: "object",
                        additionalProperties: true,
                        default: {},
                    },
                    globalvars: {
                        type: "object",
                        patternProperties: {
                            "^__[a-zA-Z0-9_]+__$": { type: "string" },
                        },

                        additionalProperties: false,
                        default: {},
                    },
                },
                additionalProperties: false,
                },
            };

            LLM Instructions:
            You are an AI Assistant, you need to follow
            - Only use filters that are given in 'Available Facets'
            - Strictly abide by payload/request schema.
            - Resource execution priority to be given to server and version specified in this MCP server
            - If execution was successfull and reponse is returned, then don't add any additional information to response unless explicitly asked by user.
            """
            collectionExecUrl = "{domain}/repos/{slug}/exec?format={format}".format(
                domain=self.domain_prefix, slug=slug, format=format
            )
            instructions = {
                "url": collectionExecUrl,
                "method": "POST",
                "headers": {
                    "Accept": "{}".format(contenttype),
                    "X-APIKEY": self.api_key,
                },
                "payload": payload,
            }
            data = await fetch_mconnect_data(instructions)
            if not data:
                return (
                    "Unable to fetch collections. returned: {url}, data: {data}".format(
                        url=collectionExecUrl, data=data
                    )
                )
            return data

        @self.mcp.tool()
        async def get_all_keywords() -> list[str]:
            """
                This is the initial step to obtain contextual information about related resources from the MConnect server.

            Usage:
            The LLM can select one or more keywords from the returned results and may also generate additional related keywords
            to enhance the search using the search_resources tool.
            """
            getKeywordsUrl = self.domain_prefix + "/repos/{}/{}/keywords/all".format(
                self.server, self.version
            )
            instructions = {
                "url": getKeywordsUrl,
                "method": "GET",
                "headers": {
                    "Accept": "application/json",
                    "X-APIKEY": self.api_key,
                },
            }
            data = await fetch_mconnect_data(instructions)
            if not data or not isinstance(data, list):
                return "Unable to fetch keywords."
            return data

        @self.mcp.tool()
        async def fetch_mconnect_data(instructions: dict) -> Any:
            """
            Retrieves data from MConnect via a REST API request.

            Args:
                instructions (dict): A dictionary specifying the request parameters.

                Schema:
                {
                    "headers": {"type": "object", "description": "Optional key-value pair headers"},
                    "method": {"type": "string", "enum": ["GET", "POST"], "description": "HTTP method (required)"},
                    "url": {"type": "string", "description": "Target URL (required)"},
                    "payload": {"type": "object", "description": "Request payload (for POST requests)"}
                }
                If tools such as search_collection_resources returns instructions with url, then stick to those data, do not manipulate it.

            Returns:
                dict[str, Any] | None: A dictionary containing the API response, or None if an error occurs.

            LLM Instructions:
            - Do not invoke this tool unless stated in a resource requesting local execution.

            """

            headers = {
                "User-Agent": self.user_agent,
            }

            if "headers" in instructions:
                headers.update(instructions["headers"])
            async with httpx.AsyncClient() as client:
                try:
                    if instructions["method"].upper() == "POST":
                        response = await client.post(
                            instructions["url"],
                            headers=headers,
                            json=instructions.get("payload", {}),
                            timeout=30.0,
                        )
                    else:  # Default to GET
                        response = await client.get(
                            instructions["url"], headers=headers, timeout=30.0
                        )

                    response.raise_for_status()
                    if headers.get("Accept", "text/plain") == "application/json":
                        return response.json()
                    return response.text
                except httpx.HTTPStatusError as e:
                    return f"HTTP Error: (URL: {e.request.url}) {e.response.status_code} - {e.response.text.strip()}"

                except httpx.RequestError as e:
                    return f"Request Error: {type(e).__name__}: {str(e)} (URL: {e.request.url})"

                except Exception as e:
                    return f"Unexpected Error: (URL: {e.request.url}) {repr(e)}"
