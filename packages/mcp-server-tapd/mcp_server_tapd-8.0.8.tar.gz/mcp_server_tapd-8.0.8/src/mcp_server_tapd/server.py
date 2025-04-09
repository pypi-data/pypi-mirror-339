import os
import json
import requests
from mcp.server.fastmcp import FastMCP
from mcp_server_tapd.tapd import TAPDClient
from mcp_server_tapd.app_config import AppConfig

mcp = FastMCP("mcp-tapd")
client = TAPDClient()

@mcp.tool()
def get_stories(workspace_id: int, options: dict = None) -> str:
    """获取 TAPD 需求，如果没有 limit 参数，则需要同时调用 get_story_count 工具获取需求数量
    TAPD API 文档：https://open.tapd.cn/document/api-doc/API%E6%96%87%E6%A1%A3/api_reference/story/get_stories.html
    Args:
        workspace_id: 项目ID（必填）
        options: 可选参数字典，支持以下字段：
            - id: ID
            - name: 标题，支持模糊匹配，例如："%需求%"
            等等...
    Returns:  <str>  # 需求所有字段数据的 json 格式，返回需求链接给用户，链接要可点击，链接的格式。而且需要返回剩余的需求数量，让用户确定是否需要继续获取剩余的需求
    Note: 需求链接格式为 {tapd_base_url}/{workspace_id}/prong/stories/view/{story_id}
    Note: 如果没有给limit 参数，则需要提醒用户剩余的需求数量
    """
    story_condition = {
        "workspace_id": workspace_id,
    }
    
    if options:
        story_condition.update(options)
    
    ret = client.get_stories(story_condition)
    count_ret = client.get_story_count(story_condition)
    config = AppConfig()
    return {
        "base_url": f'{config.tapd_base_url}/',
        "data": json.dumps(ret, indent=2, ensure_ascii=False),
        "count": json.dumps(count_ret, indent=2, ensure_ascii=False)
    }

@mcp.tool()
def get_story_custom_fields(workspace_id: int) -> str:
    """获取 TAPD 需求自定义字段配置
    Args:
        workspace_id: 项目ID（必填）
    Returns:  <str>  # 需求所有自定义字段配置数据的 json 格式
    """
    ret = client.get_story_custom_fields(workspace_id)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_story_count(workspace_id: int, options: dict = None) -> str:
    """获取 TAPD 需求数量
    TAPD API 文档：https://open.tapd.cn/document/api-doc/API%E6%96%87%E6%A1%A3/api_reference/story/get_stories_count.html
    Args:
        workspace_id: 项目ID（必填）
        options: 可选参数字典，支持以下字段：
            - id: ID
            - name: 标题
            等等...
    Returns:  <str>  # 需求所有字段数据的 json 格式
    """
    new_story = {
        "workspace_id": workspace_id,
    }
    
    if options:
        new_story.update(options)
    
    ret = client.get_story_count(new_story)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def update_story(workspace_id: int, options: dict = None) -> str:
    """更新 TAPD 需求
    TAPD API 文档：https://open.tapd.cn/document/api-doc/API%E6%96%87%E6%A1%A3/api_reference/story/update_story.html
    Args:
        workspace_id: 项目ID（必填，格式如：59271484）
        options: 可选参数字典，支持以下字段：
            - id: 需求ID（必填，格式如：1159271484001002933）
            - name: 标题
            - description: 需求描述
            等等...
    Returns: <str>,  # 需求所有字段数据的 json 格式
    Note: 需求链接格式为 {tapd_base_url}/{workspace_id}/prong/stories/view/{story_id}
    """
    new_story = {
        "workspace_id": workspace_id,
    }
    
    if options:
        new_story.update(options)
    
    created_story = client.create_or_update_story(new_story)
    config = AppConfig()
    return {
        "base_url": f'{config.tapd_base_url}/',
        "data": json.dumps(created_story, indent=2, ensure_ascii=False)
    }

@mcp.tool()
def create_story(workspace_id: int, name: str, options: dict = None) -> dict:
    """创建 TAPD 需求
    TAPD API 文档：https://open.tapd.cn/document/api-doc/API%E6%96%87%E6%A1%A3/api_reference/story/add_story.html
    Args:
        workspace_id: 项目ID（必填）
        name: 需求标题（必填）
        options: 可选参数字典，支持以下字段：
            - priority_label: 优先级
            - description: 需求描述，用富文本格式
            等等...
    Returns:
        {
            "data": <str>,  # 需求所有字段数据的 json 格式
            "url": <str>  # 需求 url，返回给用户时，链接要可点击
        }
    """
    new_story = {
        "workspace_id": workspace_id,
        "name": name
    }
    
    if options:
        new_story.update(options)
    
    created_story = client.create_or_update_story(new_story)
    config = AppConfig()
    return {
        "url": f'{config.tapd_base_url}/{workspace_id}/prong/stories/view/{created_story["data"]["Story"]["id"]}', # 返回给用户时，链接要可点击
        "data": json.dumps(created_story, indent=2, ensure_ascii=False),
    }

@mcp.tool()
def get_bug(workspace_id: int, options: dict = None) -> str:
    """获取 TAPD 缺陷
    TAPD API 文档：https://open.tapd.cn/document/api-doc/API%E6%96%87%E6%A1%A3/api_reference/bug/get_bugs.html
    Args:
        workspace_id: 项目ID（必填）
        options: 可选参数字典，支持以下字段：
            - id: ID
            - title: 标题
            等等...
    Returns:  <str>  # 缺陷所有字段数据的 json 格式
    """
    bug_condition = {
        "workspace_id": workspace_id,
    }
    
    if options:
        bug_condition.update(options)
    
    ret = client.get_bug(bug_condition)
    count_ret = client.get_bug_count(bug_condition)
    config = AppConfig()
    return {
        "base_url": {config.tapd_base_url}, # 返回给用户时，链接要可点击
        "data": json.dumps(ret, indent=2, ensure_ascii=False),
        "count": json.dumps(count_ret, indent=2, ensure_ascii=False)
    }

@mcp.tool()
def get_bug_custom_fields(workspace_id: int) -> str:
    """获取 TAPD 缺陷自定义字段配置
    Args:
        workspace_id: 项目ID（必填）
    Returns:  <str>  # 需求所有自定义字段配置数据的 json 格式
    """
    
    ret = client.get_bug_custom_fields(workspace_id)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_bug_count(workspace_id: int, options: dict = None) -> str:
    """获取 TAPD 缺陷
    TAPD API 文档：https://open.tapd.cn/document/api-doc/API%E6%96%87%E6%A1%A3/api_reference/bug/get_bugs_count.html
    Args:
        workspace_id: 项目ID（必填）
        options: 可选参数字典，支持以下字段：
            - id: ID
            - name: 标题
            等等...
    Returns:  <str>  # 需求所有字段数据的 json 格式
    """
    new_bug = {
        "workspace_id": workspace_id,
    }
    
    if options:
        new_bug.update(options)
    
    ret = client.get_bug_count(new_bug)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def update_bug(workspace_id: int, options: dict = None) -> str:
    """更新 TAPD 缺陷
    TAPD API 文档：https://open.tapd.cn/document/api-doc/API%E6%96%87%E6%A1%A3/api_reference/bug/update_bug.html
    Args:
        workspace_id: 项目ID（必填）
        options: 可选参数字典，支持以下字段：
            - id: 缺陷ID（必填）
            - title: 标题
            - description: 描述
            等等...
    Returns: <str>  # 缺陷所有字段数据的 json 格式
    """
    new_bug = {
        "workspace_id": workspace_id,
    }
    
    if options:
        new_bug.update(options)
    
    created_bug = client.create_or_update_bug(new_bug)
    config = AppConfig()
    return {
        "base_url": {config.tapd_base_url}, # 返回给用户时，链接要可点击
        "data": json.dumps(created_bug, indent=2, ensure_ascii=False)
    }

@mcp.tool()
def create_bug(workspace_id: int, title: str, options: dict = None) -> dict:
    """创建 TAPD 缺陷
    TAPD API 文档：https://open.tapd.cn/document/api-doc/API%E6%96%87%E6%A1%A3/api_reference/bug/add_bug.html
    Args:
        workspace_id: 项目ID（必填）
        title: 缺陷标题（必填）
        options: 可选参数字典，支持以下字段：
            - priority_label: 优先级
            - description: 描述
            等等...
    Returns:
        {
            "data": <str>,  # 所有字段数据的 json 格式
            "url": <str>  #  url，返回给用户时，链接要可点击
        }
    """
    new_bug = {
        "workspace_id": workspace_id,
        "title": title
    }
    
    if options:
        new_bug.update(options)
    
    ret = client.create_or_update_bug(new_bug)
    config = AppConfig()
    return {
        "url": f'{config.tapd_base_url}/{workspace_id}/bugtrace/bugs/view/{ret["data"]["Bug"]["id"]}', # 返回给用户时，链接要可点击
        "data": json.dumps(ret, indent=2, ensure_ascii=False),
    }


@mcp.tool()
def create_comments(workspace_id: int, options: dict = None) -> dict:
    """添加评论
    TAPD API 文档：https://open.tapd.cn/document/api-doc/API%E6%96%87%E6%A1%A3/api_reference/comment/add_comment.html
    Args:
        workspace_id: 项目ID（必填）
        options: 可选参数字典，支持以下字段：
            - entry_id: 评论所依附的业务对象实体id（必填，格式如：1159271484001002933）
            - entry_type: 评论类型（取值： bug、 bug_remark （流转缺陷时候的评论）、 stories、 tasks 。）（必填）
            - author: 评论人（必填）
            - description: 内容（必填）
            - root_id: 根评论ID
            - reply_id: 需求评论回复的ID
    Returns: <str>  # 新建评论的数据
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    if options:
        data.update(options)
    
    created_story = client.create_comments(data)
    return json.dumps(created_story, indent=2, ensure_ascii=False)

@mcp.tool()
def get_workflows_all_transitions(workspace_id: int, options: dict = None) -> dict:
    """获取项目下的工作流流转细则，例如要流转到"实现中"，则需要调用这个工具查看当前状态能流转到的状态
    Args:
        workspace_id: 项目ID（必填）
        options:
            - system: 系统名。取 bug （缺陷的）或者 story（需求的）（必填）
            - workitem_type_id: 需求类别ID（必填）
    Returns: <str>  状态流转细则
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    if options:
        data.update(options)
    
    ret = client.get_workflows_all_transitions(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_workflows_status_map(workspace_id: int, options: dict = None) -> dict:
    """获取工作流状态中英文名对应关系，例如想要获取所有"实现中"的需求/缺陷等，可以调用这个接口先获取状态的英文名，再根据这个英文名作为 status 字段的值去查询
    Args:
        workspace_id: 项目ID（必填）
        options:
            - system: 系统名。取 bug （缺陷的）或者 story（需求的）（必填）
            - workitem_type_id: 需求类别ID（必填）
    Returns: <str>  状态流转细则
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    if options:
        data.update(options)
    
    ret = client.get_workflows_status_map(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_workitem_types(workspace_id: int, options: dict = None) -> dict:
    """获取符合查询条件的所有需求类别（分页显示，默认一页30条）
    TAPD API 文档：https://open.tapd.cn/document/api-doc/API%E6%96%87%E6%A1%A3/api_reference/story/get_workitem_types.html
    Args:
        workspace_id: 项目ID（必填）
        options:
            - id: id，支持多ID查询
            - name: 需求类别名称
            等等...
    Returns: <str>  项目下所有需求类别字段数据
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    if options:
        data.update(options)
    
    ret = client.get_workitem_types(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_workflows_last_steps(workspace_id: int, options: dict = None) -> dict:
    """获取工作流结束状态，一次只能获取一个项目的工作流结束状态
    Args:
        workspace_id: 项目ID（必填）
        options:
            - system: 系统名。取 bug （缺陷的）或者 story（需求的）（必填）
            - workitem_type_id: 需求类别id（不传则取项目下所有工作流的结束状态）
            - type: 节点类型，仅并行工作流需区分。status 状态，step 并行工作流节点。默认只返回结束状态。若需要同时返回结束状态和结束节点，支持数组type[]=status&type[]=step
    Returns: <str> 工作流结束状态
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    if options:
        data.update(options)
    
    ret = client.get_workflows_last_steps(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_stories_custom_fields_settings(workspace_id: int) -> dict:
    """获取需求自定义字段配置，一次只能获取一个项目的配置
    Args:
        workspace_id: 项目ID（必填）
    Returns: <str> 需求自定义字段配置
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    ret = client.get_stories_custom_fields_settings(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_stories_fields_lable(workspace_id: int) -> dict:
    """获取需求所有字段的中英文
    Args:
        workspace_id: 项目ID（必填）
    Returns: <str> 
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    ret = client.get_stories_fields_lable(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_stories_fields_info(workspace_id: int) -> dict:
    """获取需求所有字段及候选值，返回符合查询条件的所有需求字段及候选值。 部分字段为静态候选值，建议参考下方 "可选值说明"部分。其余动态字段（如：status(状态)/iteration_id(迭代)/categories(需求分类)），需要通过该接口获取对应的候选值（中英文映射）
    Args:
        workspace_id: 项目ID（必填）
    Returns: <str> 
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    ret = client.get_stories_fields_info(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_workspace_info(workspace_id: int) -> dict:
    """根据项目ID（workspace_id）获取项目信息，包含项目ID,项目名称,状态,创建时间,创建人等信息
    Args:
        workspace_id: 项目ID（必填）
    Returns: <str> 
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    ret = client.get_workspace_info(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_iterations(workspace_id: int, options: dict = None) -> dict:
    """根据项目ID（workspace_id）获取符合查询条件的所有迭代，例如可以通过名称获取迭代 id，然后作为iteration_id字段的值获取到迭代下的需求或缺陷
    Args:
        workspace_id: 项目ID（必填）
        options:
            - id: ID
            - name: 标题
            - startdate: 开始时间
            - enddate: 结束时间
            ...
    Returns: <str> 
    """
    data = {
        "workspace_id": workspace_id,
    }
    if options:
        data.update(options)
    ret = client.get_iterations(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

def main():
    mcp.run()

if __name__ == "__main__":
    mcp.run()