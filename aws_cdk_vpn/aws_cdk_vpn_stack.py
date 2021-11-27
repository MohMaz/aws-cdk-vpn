from aws_cdk import (
    core as cdk
    # aws_sqs as sqs,
)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
import aws_cdk.aws_iam as iam
import aws_cdk.aws_ec2 as ec2


class AwsCdkVpnStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        vpc = ec2.Vpc(self, "VPN-VPC")
        ec2_role = iam.Role(self, "VPNInstanceRole",
                            assumed_by=iam.ServicePrincipal(
                                "ec2.amazonaws.com"),
                            )

        vpn_security_group = ec2.SecurityGroup(self, "VPNSecurityGroup",
                                               vpc=vpc,
                                               description="Allow ssh access to ec2 instances",
                                               allow_all_outbound=True,
                                               security_group_name="VPNSecurityGroup"
                                               )

        vpn_security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "allow ssh access from the world")

        vpn_security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(443), "allow https access from the world")

        instance = ec2.Instance(self, "VPNInstance",
                                vpc=vpc,
                                role=ec2_role,
                                instance_type=ec2.InstanceType.of(
                                    ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO),
                                security_group=vpn_security_group,
                                machine_image=ec2.MachineImage.latest_amazon_linux(),
                                key_name="vpn-server",
                                vpc_subnets=ec2.SubnetSelection(
                                    subnet_type=ec2.SubnetType.PUBLIC),
                                block_devices=[ec2.BlockDevice(
                                    device_name="/dev/sda1",
                                    volume=ec2.BlockDeviceVolume.ebs(20)
                                ), ec2.BlockDevice(
                                    device_name="/dev/sdm",
                                    volume=ec2.BlockDeviceVolume.ebs(30)
                                )
                                ]
                                )

        core.CfnOutput(self, "VPNServerPublicIP",
                       value=instance.instance_public_ip)
