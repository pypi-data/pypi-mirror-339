# Tencent Cloud CVM MCP Server
Implementation of Tencent Cloud CVM (Cloud Virtual Machine) and VPC (Virtual Private Cloud) MCP server for managing Tencent Cloud instances and network resources.

## Features
- **Instance Management**: Full lifecycle management including creating, starting, stopping, restarting, and terminating instances
- **Instance Query**: Query instance lists and instance type configurations  
- **Image Management**: Query available image lists
- **Network Management**: Query network resources like VPCs, subnets, and security groups
- **Region Management**: Query available regions and availability zones

## API List
### Instance Management
#### DescribeInstances
Query instance list.

**Input Parameters**:
- `Region` (string): Region, e.g., ap-guangzhou
- `Offset` (integer, optional): Offset, default 0
- `Limit` (integer, optional): Number of results, default 20, max 100  
- `InstanceIds` (array[string], optional): Filter by instance ID(s)

#### RunInstances  
Create instance(s).

**Input Parameters**:
- `Region` (string): Region
- `Zone` (string): Availability zone
- `InstanceType` (string): Instance type  
- `ImageId` (string): Image ID
- `VpcId` (string): VPC ID
- `SubnetId` (string): Subnet ID
- `InstanceName` (string, optional): Instance name
- `SecurityGroupIds` (array[string], optional): Security group ID list
- `Password` (string, optional): Instance password
- `InstanceChargeType` (string, optional): Billing type: PREPAID or POSTPAID_BY_HOUR

#### StartInstances
Start instance(s).

**Input Parameters**:
- `Region` (string): Region  
- `InstanceIds` (array[string]): Instance ID list

#### StopInstances
Stop instance(s).

**Input Parameters**:
- `Region` (string): Region
- `InstanceIds` (array[string]): Instance ID list  
- `StopType` (string, optional): Shutdown type: SOFT/HARD/SOFT_FIRST
- `StoppedMode` (string, optional): Shutdown mode: KEEP_CHARGING/STOP_CHARGING

#### RebootInstances
Reboot instance(s).

**Input Parameters**:
- `Region` (string): Region
- `InstanceIds` (array[string]): Instance ID list
- `StopType` (string, optional): Shutdown type: SOFT/HARD/SOFT_FIRST

#### TerminateInstances
Terminate instance(s).

**Input Parameters**:
- `Region` (string): Region
- `InstanceIds` (array[string]): Instance ID list

#### ResetInstancesPassword
Reset instance password.

**Input Parameters**:
- `Region` (string): Region
- `InstanceIds` (array[string]): Instance ID list
- `Password` (string): New password
- `ForceStop` (boolean, optional): Whether to force shutdown

### Configuration Query
#### DescribeRegions
Query region list.

**Input Parameters**: None

#### DescribeZones
Query availability zone list.

**Input Parameters**:
- `Region` (string): Region

#### DescribeInstanceTypeConfigs
Query instance type configurations.

**Input Parameters**:
- `Region` (string): Region
- `Zone` (string, optional): Availability zone
- `InstanceFamily` (string, optional): Instance family

#### DescribeImages
Query image list.

**Input Parameters**:
- `Region` (string): Region
- `ImageIds` (array[string], optional): Image ID list

### Network Resources
#### DescribeVpcs
Query VPC list.

**Input Parameters**:
- `Region` (string): Region
- `VpcIds` (array[string], optional): VPC ID list

#### DescribeSubnets
Query subnet list.

**Input Parameters**:
- `Region` (string): Region
- `VpcId` (string, optional): VPC ID
- `SubnetIds` (array[string], optional): Subnet ID list

#### DescribeSecurityGroups
Query security group list.

**Input Parameters**:
- `Region` (string): Region
- `SecurityGroupIds` (array[string], optional): Security group ID list

## Configuration
### Set Tencent Cloud Credentials
1. Obtain SecretId and SecretKey from Tencent Cloud Console
2. Set default region (optional)

### Environment Variables
Configure the following environment variables:
- `TENCENTCLOUD_SECRET_ID`: Tencent Cloud SecretId
- `TENCENTCLOUD_SECRET_KEY`: Tencent Cloud SecretKey  
- `TENCENTCLOUD_REGION`: Default region (optional)

### Usage in Claude Desktop
Add the following configuration to claude_desktop_config.json:

```json
{
  "mcpServers": {
    "tencent-cvm": {
      "command": "uv",
      "args": [
        "run",
        "mcp-server-cvm"
      ],
      "env": {
        "TENCENTCLOUD_SECRET_ID": "YOUR_SECRET_ID_HERE",
        "TENCENTCLOUD_SECRET_KEY": "YOUR_SECRET_KEY_HERE",
        "TENCENTCLOUD_REGION": "YOUR_REGION_HERE"
      }
    }
  }
}
```

## Installation
```sh
pip install mcp-server-cvm
```

## License
MIT License. See LICENSE file for details.
