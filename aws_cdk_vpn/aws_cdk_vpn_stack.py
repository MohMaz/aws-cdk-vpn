from aws_cdk import CfnOutput, Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from constructs import Construct


class AwsCdkVpnStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        vpc = ec2.Vpc(self, "VPN-VPC")
        ec2_role = iam.Role(
            self,
            "VPNInstanceRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
        )

        vpn_security_group = ec2.SecurityGroup(
            self,
            "VPNSecurityGroup",
            vpc=vpc,
            description="Allow ssh access to ec2 instances",
            allow_all_outbound=True,
            security_group_name="VPNSecurityGroup",
        )

        any_ipv4 = ec2.Peer.any_ipv4()
        ssh_port = ec2.Port.tcp(22)
        https_port = ec2.Port.tcp(22)
        vpn_security_group.add_ingress_rule(
            any_ipv4, ssh_port, "allow ssh access from the world"
        )

        vpn_security_group.add_ingress_rule(
            any_ipv4, https_port, "allow https access from the world"
        )

        UBUNTU_SERVER_20_AMI = "ami-0bb84e7329f4fa1f7"
        instance = ec2.Instance(
            self,
            "VPNInstance",
            vpc=vpc,
            role=ec2_role,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO
            ),
            security_group=vpn_security_group,
            machine_image=ec2.MachineImage.generic_linux(
                {"ca-central-1": UBUNTU_SERVER_20_AMI}
            ),
            key_name="vpn-server",
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/sda1",
                    volume=ec2.BlockDeviceVolume.ebs(20),  # noqa: #501
                ),
                ec2.BlockDevice(
                    device_name="/dev/sdm",
                    volume=ec2.BlockDeviceVolume.ebs(30),  # noqa: #501
                ),
            ],
        )

        CfnOutput(self, "VPNServerPublicIP", value=instance.instance_public_ip)
