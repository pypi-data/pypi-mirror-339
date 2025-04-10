from typing import List, Optional, Any, Dict, Tuple 
from requests import RequestException

from codemie_tools.base.base_toolkit import BaseToolkit
from codemie_tools.base.models import ToolKit, ToolSet, Tool
from codemie_tools.code.sonar.config import SonarToolConfig
from codemie_tools.code.sonar.tools import SonarTool
from codemie_tools.code.sonar.tools_vars import SONAR_TOOL


class SonarToolkitUI(ToolKit):
    toolkit: ToolSet = ToolSet.CODEBASE_TOOLS
    tools: List[Tool] = [
        Tool.from_metadata(SONAR_TOOL, settings_config=True),
    ]


class SonarToolkit(BaseToolkit):
    sonar_creds: Optional[SonarToolConfig] = None

    @classmethod
    def get_tools_ui_info(cls, *args, **kwargs):
        return ToolKit(
            toolkit=ToolSet.CODEBASE_TOOLS,
            tools=[
                Tool.from_metadata(SONAR_TOOL),
            ]
        ).model_dump()

    def get_tools(self):
        tools = [
            SonarTool(conf=self.sonar_creds)
        ]
        return tools

    @classmethod
    def get_toolkit(cls, configs: Dict[str, Any]):
        sonar_creds = SonarToolConfig(**configs)
        return SonarToolkit(
            sonar_creds=sonar_creds
        )

    @classmethod
    def sonar_integration_healthcheck(cls, url: Optional[str], sonar_token: Optional[str], sonar_project_name: Optional[str]) -> Tuple[bool, str]:
        try:
            tool = SonarTool(
                SonarToolConfig(url=url, sonar_token=sonar_token, sonar_project_name=sonar_project_name)
            )

            response = tool.execute("api/authentication/validate", "")
            if not response.get('valid', False):
                return False, "Validation error"

            if not sonar_project_name:
                return True, "" 
            
            page = 1
            page_size = 100

            while True:

                response = tool.execute("api/projects/search", f'{{"p": {page}, "ps": {page_size}}}')
                projects = response.get("components", [])

                if any(project.get('name', "") == sonar_project_name for project in projects):
                    return True, ""

                total_projects = response.get("paging", {}).get("total", 0)
                if page * page_size >= total_projects:
                    return False, "Project not found"

                page += 1

        except RequestException as e:
            return False, str(e)

