from asyncio.log import logger
import json
import os
from typing import Any
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.cvm.v20170312 import cvm_client, models as cvm_models
from tencentcloud.vpc.v20170312 import vpc_client, models as vpc_models
from mcp_server_cvm.run_instances import run_instances as run_instances_impl

# 从环境变量中读取 SecretId 和 SecretKey
secret_id = os.getenv("TENCENTCLOUD_SECRET_ID")
secret_key = os.getenv("TENCENTCLOUD_SECRET_KEY")
default_region = os.getenv("TENCENTCLOUD_REGION")

server = Server("cvm")

def get_cvm_client(region: str) -> cvm_client.CvmClient:
    """
    创建并返回 CVM 客户端
    """
    cred = credential.Credential(secret_id, secret_key)
    if not region:
        region = default_region or "ap-guangzhou"

    http_profile = HttpProfile()
    http_profile.endpoint = "cvm.tencentcloudapi.com"

    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile

    return cvm_client.CvmClient(cred, region, client_profile)

def get_vpc_client(region: str) -> vpc_client.VpcClient:
    """
    创建并返回 VPC 客户端
    """
    cred = credential.Credential(secret_id, secret_key)
    if not region:
        region = default_region or "ap-guangzhou"

    http_profile = HttpProfile()
    http_profile.endpoint = "vpc.tencentcloudapi.com"

    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile

    return vpc_client.VpcClient(cred, region, client_profile)

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="DescribeRegions",
            description="查询腾讯云CVM支持的地域列表",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="DescribeZones",
            description="查询腾讯云CVM支持的可用区列表",
            inputSchema={
                "type": "object",
                "properties": {
                    "Region": {
                        "type": "string",
                        "description": "地域，如 ap-guangzhou",
                    }
                },
                "required": ["Region"],
            },
        ),
        types.Tool(
            name="DescribeInstances",
            description="查询腾讯云CVM实例列表",
            inputSchema={
                "type": "object",
                "properties": {
                    "Region": {
                        "type": "string",
                        "description": "地域，如 ap-guangzhou",
                    },
                    "Offset": {
                        "type": "integer",
                        "description": "偏移量，默认为0",
                    },
                    "Limit": {
                        "type": "integer",
                        "description": "返回数量，默认为20，最大值为100",
                    },
                    "InstanceIds": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "按照一个或者多个实例ID查询，每次请求的实例的上限为100",
                    }
                },
                "required": ["Region"],
            },
        ),
        types.Tool(
            name="DescribeImages",
            description="查询腾讯云CVM镜像列表",
            inputSchema={
                "type": "object",
                "properties": {
                    "Region": {
                        "type": "string",
                        "description": "地域，如 ap-guangzhou",
                    },
                    "ImageIds": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "镜像ID列表",
                    }
                },
                "required": ["Region"],
            },
        ),
        types.Tool(
            name="DescribeInstanceTypeConfigs",
            description="查询实例机型配置列表",
            inputSchema={
                "type": "object",
                "properties": {
                    "Region": {
                        "type": "string",
                        "description": "地域，如 ap-guangzhou",
                    },
                    "Zone": {
                        "type": "string",
                        "description": "可用区，如 ap-guangzhou-1",
                    },
                    "InstanceFamily": {
                        "type": "string",
                        "description": "实例机型系列，如 S5、SA2等",
                    }
                },
                "required": ["Region"],
            },
        ),
        types.Tool(
            name="RebootInstances",
            description="重启实例",
            inputSchema={
                "type": "object",
                "properties": {
                    "Region": {
                        "type": "string",
                        "description": "地域，如 ap-guangzhou",
                    },
                    "InstanceIds": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "一个或多个待操作的实例ID",
                    },
                    "StopType": {
                        "type": "string",
                        "description": "关机类型。SOFT：表示软关机，HARD：表示硬关机，SOFT_FIRST：表示优先软关机，失败再硬关机",
                        "enum": ["SOFT", "HARD", "SOFT_FIRST"],
                        "default": "SOFT"
                    }
                },
                "required": ["Region", "InstanceIds"],
            },
        ),
        types.Tool(
            name="StartInstances",
            description="启动实例",
            inputSchema={
                "type": "object",
                "properties": {
                    "Region": {
                        "type": "string",
                        "description": "地域，如 ap-guangzhou",
                    },
                    "InstanceIds": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "一个或多个待操作的实例ID",
                    }
                },
                "required": ["Region", "InstanceIds"],
            },
        ),
        types.Tool(
            name="StopInstances",
            description="关闭实例",
            inputSchema={
                "type": "object",
                "properties": {
                    "Region": {
                        "type": "string",
                        "description": "地域，如 ap-guangzhou",
                    },
                    "InstanceIds": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "一个或多个待操作的实例ID",
                    },
                    "StopType": {
                        "type": "string",
                        "description": "关机类型。SOFT：表示软关机，HARD：表示硬关机，SOFT_FIRST：表示优先软关机，失败再硬关机",
                        "enum": ["SOFT", "HARD", "SOFT_FIRST"],
                        "default": "SOFT"
                    },
                    "StoppedMode": {
                        "type": "string",
                        "description": "关机模式，仅对POSTPAID_BY_HOUR类型实例生效",
                        "enum": ["KEEP_CHARGING", "STOP_CHARGING"],
                        "default": "KEEP_CHARGING"
                    }
                },
                "required": ["Region", "InstanceIds"],
            },
        ),
        types.Tool(
            name="TerminateInstances",
            description="退还实例",
            inputSchema={
                "type": "object",
                "properties": {
                    "Region": {
                        "type": "string",
                        "description": "地域，如 ap-guangzhou",
                    },
                    "InstanceIds": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "一个或多个待操作的实例ID",
                    }
                },
                "required": ["Region", "InstanceIds"],
            },
        ),
        types.Tool(
            name="ResetInstancesPassword",
            description="重置实例密码",
            inputSchema={
                "type": "object",
                "properties": {
                    "Region": {
                        "type": "string",
                        "description": "地域，如 ap-guangzhou",
                    },
                    "InstanceIds": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "一个或多个待操作的实例ID",
                    },
                    "Password": {
                        "type": "string",
                        "description": "实例新密码",
                    },
                    "ForceStop": {
                        "type": "boolean",
                        "description": "是否强制关机执行",
                        "default": False
                    }
                },
                "required": ["Region", "InstanceIds", "Password"],
            },
        ),
        types.Tool(
            name="RunInstances",
            description="创建实例",
            inputSchema={
                "type": "object",
                "properties": {
                    "Region": {
                        "type": "string",
                        "description": "地域，如 ap-guangzhou",
                    },
                    "Zone": {
                        "type": "string",
                        "description": "可用区，如 ap-guangzhou-1",
                    },
                    "InstanceType": {
                        "type": "string",
                        "description": "实例机型，如 S5.MEDIUM4",
                    },
                    "ImageId": {
                        "type": "string",
                        "description": "镜像ID",
                    },
                    "VpcId": {
                        "type": "string",
                        "description": "私有网络ID",
                    },
                    "SubnetId": {
                        "type": "string",
                        "description": "子网ID",
                    },
                    "InstanceName": {
                        "type": "string",
                        "description": "实例名称",
                    },
                    "SecurityGroupIds": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "安全组ID列表",
                    },
                    "InstanceChargeType": {
                        "type": "string",
                        "description": "实例计费类型",
                        "enum": ["PREPAID", "POSTPAID_BY_HOUR"],
                        "default": "POSTPAID_BY_HOUR"
                    },
                    "Password": {
                        "type": "string",
                        "description": "实例密码",
                    }
                },
                "required": ["Region", "Zone", "InstanceType", "ImageId", "VpcId", "SubnetId"],
            },
        ),
        types.Tool(
            name="DescribeSecurityGroups",
            description="查询安全组列表",
            inputSchema={
                "type": "object",
                "properties": {
                    "Region": {
                        "type": "string",
                        "description": "地域，如 ap-guangzhou",
                    },
                    "SecurityGroupIds": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "安全组ID列表",
                    }
                },
                "required": ["Region"],
            },
        ),
        types.Tool(
            name="DescribeVpcs",
            description="查询VPC列表",
            inputSchema={
                "type": "object",
                "properties": {
                    "Region": {
                        "type": "string",
                        "description": "地域，如 ap-guangzhou",
                    },
                    "VpcIds": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "VPC实例ID数组",
                    }
                },
                "required": ["Region"],
            },
        ),
        types.Tool(
            name="DescribeSubnets",
            description="查询子网列表",
            inputSchema={
                "type": "object",
                "properties": {
                    "Region": {
                        "type": "string",
                        "description": "地域，如 ap-guangzhou",
                    },
                    "VpcId": {
                        "type": "string",
                        "description": "VPC实例ID",
                    },
                    "SubnetIds": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "子网实例ID列表",
                    }
                },
                "required": ["Region"],
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """处理工具调用请求"""
    try:
        if name == "DescribeRegions":
            result = describe_regions()
            return [types.TextContent(type="text", text=str(result))]
        
        elif name == "DescribeZones":
            region = arguments.get("Region", default_region)
            result = describe_zones(region)
            return [types.TextContent(type="text", text=str(result))]
        
        elif name == "DescribeInstances":
            region = arguments.get("Region", default_region)
            offset = arguments.get("Offset", 0)
            limit = arguments.get("Limit", 20)
            instance_ids = arguments.get("InstanceIds", [])
            result = describe_instances(region, offset, limit, instance_ids)
            return [types.TextContent(type="text", text=str(result))]
        
        elif name == "DescribeImages":
            region = arguments.get("Region", default_region)
            image_ids = arguments.get("ImageIds", [])
            result = describe_images(region, image_ids)
            return [types.TextContent(type="text", text=str(result))]
        
        elif name == "DescribeInstanceTypeConfigs":
            region = arguments.get("Region", default_region)
            zone = arguments.get("Zone")
            instance_family = arguments.get("InstanceFamily")
            result = describe_instance_type_configs(region, zone, instance_family)
            return [types.TextContent(type="text", text=str(result))]
        
        elif name == "RebootInstances":
            region = arguments.get("Region", default_region)
            instance_ids = arguments.get("InstanceIds")
            stop_type = arguments.get("StopType", "SOFT")
            result = reboot_instances(region, instance_ids, stop_type)
            return [types.TextContent(type="text", text=str(result))]
        
        elif name == "StartInstances":
            region = arguments.get("Region", default_region)
            instance_ids = arguments.get("InstanceIds")
            result = start_instances(region, instance_ids)
            return [types.TextContent(type="text", text=str(result))]
        
        elif name == "StopInstances":
            region = arguments.get("Region", default_region)
            instance_ids = arguments.get("InstanceIds")
            stop_type = arguments.get("StopType", "SOFT")
            stopped_mode = arguments.get("StoppedMode", "KEEP_CHARGING")
            result = stop_instances(region, instance_ids, stop_type, stopped_mode)
            return [types.TextContent(type="text", text=str(result))]
        
        elif name == "TerminateInstances":
            region = arguments.get("Region", default_region)
            instance_ids = arguments.get("InstanceIds")
            result = terminate_instances(region, instance_ids)
            return [types.TextContent(type="text", text=str(result))]
        
        elif name == "ResetInstancesPassword":
            region = arguments.get("Region", default_region)
            instance_ids = arguments.get("InstanceIds")
            password = arguments.get("Password")
            force_stop = arguments.get("ForceStop", False)
            result = reset_instances_password(region, instance_ids, password, force_stop)
            return [types.TextContent(type="text", text=str(result))]
        
        elif name == "RunInstances":
            region = arguments.get("Region", default_region)
            result = run_instances(region, arguments)
            return [types.TextContent(type="text", text=str(result))]
        
        elif name == "DescribeSecurityGroups":
            region = arguments.get("Region", default_region)
            security_group_ids = arguments.get("SecurityGroupIds")
            result = describe_security_groups(region, security_group_ids)
            return [types.TextContent(type="text", text=str(result))]
        
        elif name == "DescribeVpcs":
            region = arguments.get("Region", default_region)
            vpc_ids = arguments.get("VpcIds")
            result = describe_vpcs(region, vpc_ids)
            return [types.TextContent(type="text", text=str(result))]
        
        elif name == "DescribeSubnets":
            region = arguments.get("Region", default_region)
            vpc_id = arguments.get("VpcId")
            subnet_ids = arguments.get("SubnetIds")
            result = describe_subnets(region, vpc_id, subnet_ids)
            return [types.TextContent(type="text", text=str(result))]
        
        else:
            raise ValueError(f"未知的工具: {name}")
    except Exception as e:
        return [types.TextContent(type="text", text=f"错误: {str(e)}")]

def describe_regions() -> str:
    """查询地域列表"""
    client = get_cvm_client("ap-guangzhou")  # 使用默认地域
    req = cvm_models.DescribeRegionsRequest()
    resp = client.DescribeRegions(req)
    return resp.to_json_string()

def describe_zones(region: str) -> str:
    """查询可用区列表"""
    client = get_cvm_client(region)
    req = cvm_models.DescribeZonesRequest()
    resp = client.DescribeZones(req)
    return resp.to_json_string()

def describe_instances(region: str, offset: int, limit: int, instance_ids: list[str]) -> str:
    """查询实例列表"""
    client = get_cvm_client(region)
    req = cvm_models.DescribeInstancesRequest()
    
    params = {
        "Offset": offset,
        "Limit": limit
    }
    if instance_ids:
        params["InstanceIds"] = instance_ids
        
    req.from_json_string(json.dumps(params))
    resp = client.DescribeInstances(req)
    return resp.to_json_string()

def describe_images(region: str, image_ids: list[str]) -> str:
    """查询镜像列表"""
    client = get_cvm_client(region)
    req = cvm_models.DescribeImagesRequest()
    
    params = {}
    if image_ids:
        params["ImageIds"] = image_ids
        
    req.from_json_string(json.dumps(params))
    resp = client.DescribeImages(req)
    return resp.to_json_string()

def describe_instance_type_configs(region: str, zone: str = None, instance_family: str = None) -> str:
    """查询实例机型配置"""
    client = get_cvm_client(region)
    req = cvm_models.DescribeInstanceTypeConfigsRequest()
    
    params = {}
    if zone:
        params["Filters"] = [{
            "Name": "zone",
            "Values": [zone]
        }]
    if instance_family:
        if "Filters" not in params:
            params["Filters"] = []
        params["Filters"].append({
            "Name": "instance-family",
            "Values": [instance_family]
        })
        
    if params:
        req.from_json_string(json.dumps(params))
    resp = client.DescribeInstanceTypeConfigs(req)
    return resp.to_json_string()

def reboot_instances(region: str, instance_ids: list[str], stop_type: str) -> str:
    """重启实例"""
    client = get_cvm_client(region)
    req = cvm_models.RebootInstancesRequest()
    
    params = {
        "InstanceIds": instance_ids,
        "StopType": stop_type
    }
    req.from_json_string(json.dumps(params))
    resp = client.RebootInstances(req)
    return resp.to_json_string()

def start_instances(region: str, instance_ids: list[str]) -> str:
    """启动实例"""
    client = get_cvm_client(region)
    req = cvm_models.StartInstancesRequest()
    
    params = {
        "InstanceIds": instance_ids
    }
    req.from_json_string(json.dumps(params))
    resp = client.StartInstances(req)
    return resp.to_json_string()

def stop_instances(region: str, instance_ids: list[str], stop_type: str, stopped_mode: str) -> str:
    """关闭实例"""
    client = get_cvm_client(region)
    req = cvm_models.StopInstancesRequest()
    
    params = {
        "InstanceIds": instance_ids,
        "StopType": stop_type,
        "StoppedMode": stopped_mode
    }
    req.from_json_string(json.dumps(params))
    resp = client.StopInstances(req)
    return resp.to_json_string()

def terminate_instances(region: str, instance_ids: list[str]) -> str:
    """销毁实例"""
    client = get_cvm_client(region)
    req = cvm_models.TerminateInstancesRequest()
    
    params = {
        "InstanceIds": instance_ids
    }
    req.from_json_string(json.dumps(params))
    resp = client.TerminateInstances(req)
    return resp.to_json_string()

def reset_instances_password(region: str, instance_ids: list[str], password: str, force_stop: bool) -> str:
    """重置实例密码"""
    client = get_cvm_client(region)
    req = cvm_models.ResetInstancesPasswordRequest()
    
    params = {
        "InstanceIds": instance_ids,
        "Password": password,
        "ForceStop": force_stop
    }
    req.from_json_string(json.dumps(params))
    resp = client.ResetInstancesPassword(req)
    return resp.to_json_string()

def run_instances(region: str, params: dict) -> str:
    """
    创建实例
    """
    try:
        return run_instances_impl(
            region=region,
            zone=params.get("Zone"),
            instance_type=params.get("InstanceType"),
            image_id=params.get("ImageId"),
            vpc_id=params.get("VpcId"),
            subnet_id=params.get("SubnetId"),
            security_group_ids=params.get("SecurityGroupIds"),
            password=params.get("Password"),
            instance_name=params.get("InstanceName"),
            instance_charge_type=params.get("InstanceChargeType"),
            instance_count=params.get("InstanceCount"),
            dry_run=params.get("DryRun", False)
        )
    except Exception as e:
        logger.error(f"创建实例失败: {str(e)}")
        raise e

def describe_security_groups(region: str, security_group_ids: list[str] = None) -> str:
    """查询安全组列表"""
    client = get_vpc_client(region)
    req = vpc_models.DescribeSecurityGroupsRequest()
    
    params = {}
    if security_group_ids:
        params["SecurityGroupIds"] = security_group_ids
        
    if params:
        req.from_json_string(json.dumps(params))
    resp = client.DescribeSecurityGroups(req)
    return resp.to_json_string()

def describe_vpcs(region: str, vpc_ids: list[str] = None) -> str:
    """查询VPC列表"""
    client = get_vpc_client(region)
    req = vpc_models.DescribeVpcsRequest()
    
    params = {}
    if vpc_ids:
        params["VpcIds"] = vpc_ids
        
    if params:
        req.from_json_string(json.dumps(params))
    resp = client.DescribeVpcs(req)
    return resp.to_json_string()

def describe_subnets(region: str, vpc_id: str = None, subnet_ids: list[str] = None) -> str:
    """查询子网列表"""
    client = get_vpc_client(region)
    req = vpc_models.DescribeSubnetsRequest()
    
    params = {}
    if vpc_id:
        params["Filters"] = [{
            "Name": "vpc-id",
            "Values": [vpc_id]
        }]
    if subnet_ids:
        params["SubnetIds"] = subnet_ids
        
    if params:
        req.from_json_string(json.dumps(params))
    resp = client.DescribeSubnets(req)
    return resp.to_json_string()

async def serve():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="cvm",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
