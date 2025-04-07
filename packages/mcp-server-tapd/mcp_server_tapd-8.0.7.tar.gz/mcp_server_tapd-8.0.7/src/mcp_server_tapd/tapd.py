import requests
import json
from typing import Dict, Any, Optional
from base64 import b64encode
from mcp_server_tapd.app_config import AppConfig

class TAPDClient:
    def __init__(self):
        """
        初始化 TAPD API 客户端
        使用配置文件中的常量进行初始化
        """
        config = AppConfig()
        self.base_url = config.api_base_url
        auth_str = f"{config.api_user}:{config.api_password}"
        self.headers = {
            "Authorization": f"Basic {b64encode(auth_str.encode()).decode()}",
            "Content-Type": "application/json"
        }

    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict:
        """
        发送 API 请求的通用方法
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            params=params,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def get_stories(self, params: Optional[Dict] = None) -> Dict:
        """
        获取需求
        """
        default_params = {
            "page": 1,
            "limit": 10
        }
        if params:
            default_params.update(params)
            
        return self._make_request("GET", "stories", params=default_params)

    def create_or_update_story(self, story_data: Dict[str, Any]) -> Dict:
        """
        创建/更新需求
        """
        return self._make_request("POST", "stories", data=story_data)

    def get_story_count(self, params: Optional[Dict] = None) -> Dict:
        """
        获取需求数量
        """
        return self._make_request("GET", "stories/count", params=params)

    def get_story_custom_fields(self, workspace_id: int) -> Dict:
        """
        获取需求自定义字段配置
        """
        return self._make_request("GET", f"stories/custom_fields_settings?workspace_id={workspace_id}")

    def get_bug(self, params: Optional[Dict] = None) -> Dict:
        """
        获取缺陷
        """
        default_params = {
            "page": 1,
            "limit": 10
        }
        if params:
            default_params.update(params)
            
        return self._make_request("GET", "bugs", params=default_params)

    def create_or_update_bug(self, data: Dict[str, Any]) -> Dict:
        """
        创建或更新缺陷
        """
        return self._make_request("POST", "bugs", data=data)

    def get_bug_count(self, params: Optional[Dict] = None) -> Dict:
        """
        获取缺陷数量
        """
        return self._make_request("GET", "bugs/count", params=params)

    def get_bug_custom_fields(self, workspace_id: int) -> Dict:
        """
        获取缺陷自定义字段配置
        """
        params = {"workspace_id": workspace_id}
        return self._make_request("GET", f"bugs/custom_fields_settings?workspace_id={workspace_id}", params=params)
    
    def create_comments(self, data: Dict[str, Any]) -> Dict:
        """
        新建评论
        """
        return self._make_request("POST", "comments", data=data)
    
    def get_workflows_all_transitions(self, data: Dict[str, Any]) -> Dict:
        """
        获取工作流流转细则
        """
        system = data['system']
        workspace_id = data['workspace_id']
        params = f"?workspace_id={workspace_id}&system={system}"
        if 'workitem_type_id' in data:
            workitem_type_id = data['workitem_type_id']
            params += f"&workitem_type_id={workitem_type_id}"
        return self._make_request("GET", f"workflows/all_transitions{params}")
    
    def get_workflows_status_map(self, data: Dict[str, Any]) -> Dict:
        """
        获取工作流状态中英文名对应关系
        """
        system = data['system']
        workspace_id = data['workspace_id']
        params = f"?workspace_id={workspace_id}&system={system}"
        if 'workitem_type_id' in data:
            workitem_type_id = data['workitem_type_id']
            params += f"&workitem_type_id={workitem_type_id}"
        return self._make_request("GET", f"workflows/status_map{params}")
    
    def get_workitem_types(self, data: Dict[str, Any]) -> Dict:
        """
        返回符合查询条件的所有需求类别（分页显示，默认一页30条）
        """
        workspace_id = data['workspace_id']
        return self._make_request("GET", f"workitem_types?workspace_id={workspace_id}", data=data)
   
    def get_workflows_last_steps(self, data: Dict[str, Any]) -> Dict:
        """
        获取工作流结束状态
        """
        system = data['system']
        workspace_id = data['workspace_id']
        params = f"?workspace_id={workspace_id}&system={system}"
        if 'workitem_type_id' in data:
            workitem_type_id = data['workitem_type_id']
            params += f"&workitem_type_id={workitem_type_id}"
        if 'type' in data:
            type = data['type']
            params += f"&type={type}"
        return self._make_request("GET", f"workflows/last_steps{params}", data=data)
    
    def get_stories_custom_fields_settings(self, data: Dict[str, Any]) -> Dict:
        """
        获取需求自定义字段配置
        """
        workspace_id = data['workspace_id']
        return self._make_request("GET", f"stories/custom_fields_settings?workspace_id={workspace_id}", data=data)
   
    def get_stories_fields_lable(self, data: Dict[str, Any]) -> Dict:
        """
        获取需求需求所有字段的中英文
        """
        workspace_id = data['workspace_id']
        return self._make_request("GET", f"stories/get_fields_lable?workspace_id={workspace_id}")
    
    def get_stories_fields_info(self, data: Dict[str, Any]) -> Dict:
        """
        获取需求所有字段及候选值，返回符合查询条件的所有需求字段及候选值
        """
        workspace_id = data['workspace_id']
        return self._make_request("GET", f"stories/get_fields_info?workspace_id={workspace_id}")
    
    def get_workspace_info(self, data: Dict[str, Any]) -> Dict:
        """
        根据项目ID（workspace_id）获取项目信息，包含项目ID,项目名称,状态,创建时间,创建人等信息
        """
        workspace_id = data['workspace_id']
        return self._make_request("GET", f"workspaces/get_workspace_info?workspace_id={workspace_id}", data=data)
    
    def get_iterations(self, data: Dict[str, Any]) -> Dict:
        """
        符合查询条件的所有迭代（分页显示，默认一页30条）
        """
        workspace_id = data['workspace_id']
        return self._make_request("GET", f"iterations?workspace_id={workspace_id}", data=data)
   