r'''
# `openstack_containerinfra_cluster_v1`

Refer to the Terraform Registry for docs: [`openstack_containerinfra_cluster_v1`](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class ContainerinfraClusterV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.containerinfraClusterV1.ContainerinfraClusterV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1 openstack_containerinfra_cluster_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_template_id: builtins.str,
        create_timeout: typing.Optional[jsii.Number] = None,
        discovery_url: typing.Optional[builtins.str] = None,
        docker_volume_size: typing.Optional[jsii.Number] = None,
        fixed_network: typing.Optional[builtins.str] = None,
        fixed_subnet: typing.Optional[builtins.str] = None,
        flavor: typing.Optional[builtins.str] = None,
        floating_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        keypair: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        master_count: typing.Optional[jsii.Number] = None,
        master_flavor: typing.Optional[builtins.str] = None,
        master_lb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        merge_labels: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        node_count: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ContainerinfraClusterV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1 openstack_containerinfra_cluster_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_template_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#cluster_template_id ContainerinfraClusterV1#cluster_template_id}.
        :param create_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#create_timeout ContainerinfraClusterV1#create_timeout}.
        :param discovery_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#discovery_url ContainerinfraClusterV1#discovery_url}.
        :param docker_volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#docker_volume_size ContainerinfraClusterV1#docker_volume_size}.
        :param fixed_network: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#fixed_network ContainerinfraClusterV1#fixed_network}.
        :param fixed_subnet: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#fixed_subnet ContainerinfraClusterV1#fixed_subnet}.
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#flavor ContainerinfraClusterV1#flavor}.
        :param floating_ip_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#floating_ip_enabled ContainerinfraClusterV1#floating_ip_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#id ContainerinfraClusterV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param keypair: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#keypair ContainerinfraClusterV1#keypair}.
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#labels ContainerinfraClusterV1#labels}.
        :param master_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#master_count ContainerinfraClusterV1#master_count}.
        :param master_flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#master_flavor ContainerinfraClusterV1#master_flavor}.
        :param master_lb_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#master_lb_enabled ContainerinfraClusterV1#master_lb_enabled}.
        :param merge_labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#merge_labels ContainerinfraClusterV1#merge_labels}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#name ContainerinfraClusterV1#name}.
        :param node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#node_count ContainerinfraClusterV1#node_count}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#region ContainerinfraClusterV1#region}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#timeouts ContainerinfraClusterV1#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43cf740669c0daabbdebd8091b3e7e2ee330d83f8f88686e026906c9d3c962c9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ContainerinfraClusterV1Config(
            cluster_template_id=cluster_template_id,
            create_timeout=create_timeout,
            discovery_url=discovery_url,
            docker_volume_size=docker_volume_size,
            fixed_network=fixed_network,
            fixed_subnet=fixed_subnet,
            flavor=flavor,
            floating_ip_enabled=floating_ip_enabled,
            id=id,
            keypair=keypair,
            labels=labels,
            master_count=master_count,
            master_flavor=master_flavor,
            master_lb_enabled=master_lb_enabled,
            merge_labels=merge_labels,
            name=name,
            node_count=node_count,
            region=region,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a ContainerinfraClusterV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ContainerinfraClusterV1 to import.
        :param import_from_id: The id of the existing ContainerinfraClusterV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ContainerinfraClusterV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26a43b1630bb4d3600693953cd56952942e05fd2ec525cec63884778b06438a9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#create ContainerinfraClusterV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#delete ContainerinfraClusterV1#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#update ContainerinfraClusterV1#update}.
        '''
        value = ContainerinfraClusterV1Timeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCreateTimeout")
    def reset_create_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateTimeout", []))

    @jsii.member(jsii_name="resetDiscoveryUrl")
    def reset_discovery_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiscoveryUrl", []))

    @jsii.member(jsii_name="resetDockerVolumeSize")
    def reset_docker_volume_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerVolumeSize", []))

    @jsii.member(jsii_name="resetFixedNetwork")
    def reset_fixed_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedNetwork", []))

    @jsii.member(jsii_name="resetFixedSubnet")
    def reset_fixed_subnet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedSubnet", []))

    @jsii.member(jsii_name="resetFlavor")
    def reset_flavor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlavor", []))

    @jsii.member(jsii_name="resetFloatingIpEnabled")
    def reset_floating_ip_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFloatingIpEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKeypair")
    def reset_keypair(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeypair", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMasterCount")
    def reset_master_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasterCount", []))

    @jsii.member(jsii_name="resetMasterFlavor")
    def reset_master_flavor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasterFlavor", []))

    @jsii.member(jsii_name="resetMasterLbEnabled")
    def reset_master_lb_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasterLbEnabled", []))

    @jsii.member(jsii_name="resetMergeLabels")
    def reset_merge_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergeLabels", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNodeCount")
    def reset_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeCount", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="apiAddress")
    def api_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiAddress"))

    @builtins.property
    @jsii.member(jsii_name="coeVersion")
    def coe_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "coeVersion"))

    @builtins.property
    @jsii.member(jsii_name="containerVersion")
    def container_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerVersion"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="kubeconfig")
    def kubeconfig(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "kubeconfig"))

    @builtins.property
    @jsii.member(jsii_name="masterAddresses")
    def master_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "masterAddresses"))

    @builtins.property
    @jsii.member(jsii_name="nodeAddresses")
    def node_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "nodeAddresses"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stackId"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ContainerinfraClusterV1TimeoutsOutputReference":
        return typing.cast("ContainerinfraClusterV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userId"))

    @builtins.property
    @jsii.member(jsii_name="clusterTemplateIdInput")
    def cluster_template_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterTemplateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="createTimeoutInput")
    def create_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "createTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="discoveryUrlInput")
    def discovery_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "discoveryUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerVolumeSizeInput")
    def docker_volume_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dockerVolumeSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedNetworkInput")
    def fixed_network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fixedNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedSubnetInput")
    def fixed_subnet_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fixedSubnetInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorInput")
    def flavor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorInput"))

    @builtins.property
    @jsii.member(jsii_name="floatingIpEnabledInput")
    def floating_ip_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "floatingIpEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keypairInput")
    def keypair_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keypairInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="masterCountInput")
    def master_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "masterCountInput"))

    @builtins.property
    @jsii.member(jsii_name="masterFlavorInput")
    def master_flavor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "masterFlavorInput"))

    @builtins.property
    @jsii.member(jsii_name="masterLbEnabledInput")
    def master_lb_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "masterLbEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="mergeLabelsInput")
    def merge_labels_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mergeLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeCountInput")
    def node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerinfraClusterV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerinfraClusterV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterTemplateId")
    def cluster_template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterTemplateId"))

    @cluster_template_id.setter
    def cluster_template_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d533bd5eb3fdd9c025c70d3cdc027b03f1b7731ac7bfb66c402122f0161f0c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterTemplateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createTimeout")
    def create_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "createTimeout"))

    @create_timeout.setter
    def create_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fbfdafaeac64faff17cd1b1fca78ff3f385a4d9319775fe08c1123a14d58d7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="discoveryUrl")
    def discovery_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "discoveryUrl"))

    @discovery_url.setter
    def discovery_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3dd2fdbe8608e59465e3f6976b946016bd8fd0b4f8e0eedceba3b64657b348b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "discoveryUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dockerVolumeSize")
    def docker_volume_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dockerVolumeSize"))

    @docker_volume_size.setter
    def docker_volume_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f331501a688ec4584dcc823b2c503e19612fbb11adcb9bfbfaeb816d77420e1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerVolumeSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fixedNetwork")
    def fixed_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fixedNetwork"))

    @fixed_network.setter
    def fixed_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fe69e441d310a83c9bb6bfccbafb6fe228ac1551bae86e90f1fb503cb149f77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fixedSubnet")
    def fixed_subnet(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fixedSubnet"))

    @fixed_subnet.setter
    def fixed_subnet(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f816823be0b7c018c89fa2009711f773f25fd8f6fa44650f019e97b4d6831a77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedSubnet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flavor")
    def flavor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavor"))

    @flavor.setter
    def flavor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__250885d105c645bda45137e8ad5912db1bf74e1eb61ac4d40da5f0de728a56cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="floatingIpEnabled")
    def floating_ip_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "floatingIpEnabled"))

    @floating_ip_enabled.setter
    def floating_ip_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b931cf5455f16c163cc86a75a07e0695157b9041f4293e0edb003706c5925c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "floatingIpEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cc30acb5c2220c70f9177bce9e4d360f32578a24de941c913de337d27030050)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keypair")
    def keypair(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keypair"))

    @keypair.setter
    def keypair(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28c7e1e7e9e8e7a4996056224d5dd3b3ce9e089a2fa6c605505e4781cc33d62a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keypair", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f7365ef55e8d8596f36ad4749a78b4907d016184f070345e1f6bc3b45c40bd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="masterCount")
    def master_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "masterCount"))

    @master_count.setter
    def master_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a59790860a6478f16738b42a92e8c2ce002cf7019d9722309378638adf13c80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="masterFlavor")
    def master_flavor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "masterFlavor"))

    @master_flavor.setter
    def master_flavor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d11f118666accb196644f3777194cf6d6c4dcc4408a2a1e1a3bbffb9b0bc4378)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterFlavor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="masterLbEnabled")
    def master_lb_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "masterLbEnabled"))

    @master_lb_enabled.setter
    def master_lb_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8acc8b169e0dc8126a721600d3b498808b664ae255a2b4b419f805f431092fcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterLbEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mergeLabels")
    def merge_labels(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mergeLabels"))

    @merge_labels.setter
    def merge_labels(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49069434019f9b4e0455ecc14cdc8fddbcdbe05ed813ae067865e1d9082c9a10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mergeLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e494c394faba8adc0646b5e3ccbe2e8c602f847eb329c469675a3db6e167c292)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b58a9f5a4ece780c660252969a1d2a67905917e105103deb2a87eb89425e1c59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a51c04c57098fde3ea0652d9885ea969b1d63e271906109359398d359d1f0616)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.containerinfraClusterV1.ContainerinfraClusterV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cluster_template_id": "clusterTemplateId",
        "create_timeout": "createTimeout",
        "discovery_url": "discoveryUrl",
        "docker_volume_size": "dockerVolumeSize",
        "fixed_network": "fixedNetwork",
        "fixed_subnet": "fixedSubnet",
        "flavor": "flavor",
        "floating_ip_enabled": "floatingIpEnabled",
        "id": "id",
        "keypair": "keypair",
        "labels": "labels",
        "master_count": "masterCount",
        "master_flavor": "masterFlavor",
        "master_lb_enabled": "masterLbEnabled",
        "merge_labels": "mergeLabels",
        "name": "name",
        "node_count": "nodeCount",
        "region": "region",
        "timeouts": "timeouts",
    },
)
class ContainerinfraClusterV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cluster_template_id: builtins.str,
        create_timeout: typing.Optional[jsii.Number] = None,
        discovery_url: typing.Optional[builtins.str] = None,
        docker_volume_size: typing.Optional[jsii.Number] = None,
        fixed_network: typing.Optional[builtins.str] = None,
        fixed_subnet: typing.Optional[builtins.str] = None,
        flavor: typing.Optional[builtins.str] = None,
        floating_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        keypair: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        master_count: typing.Optional[jsii.Number] = None,
        master_flavor: typing.Optional[builtins.str] = None,
        master_lb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        merge_labels: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        node_count: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ContainerinfraClusterV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_template_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#cluster_template_id ContainerinfraClusterV1#cluster_template_id}.
        :param create_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#create_timeout ContainerinfraClusterV1#create_timeout}.
        :param discovery_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#discovery_url ContainerinfraClusterV1#discovery_url}.
        :param docker_volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#docker_volume_size ContainerinfraClusterV1#docker_volume_size}.
        :param fixed_network: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#fixed_network ContainerinfraClusterV1#fixed_network}.
        :param fixed_subnet: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#fixed_subnet ContainerinfraClusterV1#fixed_subnet}.
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#flavor ContainerinfraClusterV1#flavor}.
        :param floating_ip_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#floating_ip_enabled ContainerinfraClusterV1#floating_ip_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#id ContainerinfraClusterV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param keypair: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#keypair ContainerinfraClusterV1#keypair}.
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#labels ContainerinfraClusterV1#labels}.
        :param master_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#master_count ContainerinfraClusterV1#master_count}.
        :param master_flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#master_flavor ContainerinfraClusterV1#master_flavor}.
        :param master_lb_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#master_lb_enabled ContainerinfraClusterV1#master_lb_enabled}.
        :param merge_labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#merge_labels ContainerinfraClusterV1#merge_labels}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#name ContainerinfraClusterV1#name}.
        :param node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#node_count ContainerinfraClusterV1#node_count}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#region ContainerinfraClusterV1#region}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#timeouts ContainerinfraClusterV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ContainerinfraClusterV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eef2bdcb88c96292e93a694b48f173dd41585c2ea6c2be954951fe6c3c8864b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster_template_id", value=cluster_template_id, expected_type=type_hints["cluster_template_id"])
            check_type(argname="argument create_timeout", value=create_timeout, expected_type=type_hints["create_timeout"])
            check_type(argname="argument discovery_url", value=discovery_url, expected_type=type_hints["discovery_url"])
            check_type(argname="argument docker_volume_size", value=docker_volume_size, expected_type=type_hints["docker_volume_size"])
            check_type(argname="argument fixed_network", value=fixed_network, expected_type=type_hints["fixed_network"])
            check_type(argname="argument fixed_subnet", value=fixed_subnet, expected_type=type_hints["fixed_subnet"])
            check_type(argname="argument flavor", value=flavor, expected_type=type_hints["flavor"])
            check_type(argname="argument floating_ip_enabled", value=floating_ip_enabled, expected_type=type_hints["floating_ip_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument keypair", value=keypair, expected_type=type_hints["keypair"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument master_count", value=master_count, expected_type=type_hints["master_count"])
            check_type(argname="argument master_flavor", value=master_flavor, expected_type=type_hints["master_flavor"])
            check_type(argname="argument master_lb_enabled", value=master_lb_enabled, expected_type=type_hints["master_lb_enabled"])
            check_type(argname="argument merge_labels", value=merge_labels, expected_type=type_hints["merge_labels"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_template_id": cluster_template_id,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if create_timeout is not None:
            self._values["create_timeout"] = create_timeout
        if discovery_url is not None:
            self._values["discovery_url"] = discovery_url
        if docker_volume_size is not None:
            self._values["docker_volume_size"] = docker_volume_size
        if fixed_network is not None:
            self._values["fixed_network"] = fixed_network
        if fixed_subnet is not None:
            self._values["fixed_subnet"] = fixed_subnet
        if flavor is not None:
            self._values["flavor"] = flavor
        if floating_ip_enabled is not None:
            self._values["floating_ip_enabled"] = floating_ip_enabled
        if id is not None:
            self._values["id"] = id
        if keypair is not None:
            self._values["keypair"] = keypair
        if labels is not None:
            self._values["labels"] = labels
        if master_count is not None:
            self._values["master_count"] = master_count
        if master_flavor is not None:
            self._values["master_flavor"] = master_flavor
        if master_lb_enabled is not None:
            self._values["master_lb_enabled"] = master_lb_enabled
        if merge_labels is not None:
            self._values["merge_labels"] = merge_labels
        if name is not None:
            self._values["name"] = name
        if node_count is not None:
            self._values["node_count"] = node_count
        if region is not None:
            self._values["region"] = region
        if timeouts is not None:
            self._values["timeouts"] = timeouts

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def cluster_template_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#cluster_template_id ContainerinfraClusterV1#cluster_template_id}.'''
        result = self._values.get("cluster_template_id")
        assert result is not None, "Required property 'cluster_template_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def create_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#create_timeout ContainerinfraClusterV1#create_timeout}.'''
        result = self._values.get("create_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def discovery_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#discovery_url ContainerinfraClusterV1#discovery_url}.'''
        result = self._values.get("discovery_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_volume_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#docker_volume_size ContainerinfraClusterV1#docker_volume_size}.'''
        result = self._values.get("docker_volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fixed_network(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#fixed_network ContainerinfraClusterV1#fixed_network}.'''
        result = self._values.get("fixed_network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fixed_subnet(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#fixed_subnet ContainerinfraClusterV1#fixed_subnet}.'''
        result = self._values.get("fixed_subnet")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flavor(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#flavor ContainerinfraClusterV1#flavor}.'''
        result = self._values.get("flavor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def floating_ip_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#floating_ip_enabled ContainerinfraClusterV1#floating_ip_enabled}.'''
        result = self._values.get("floating_ip_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#id ContainerinfraClusterV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keypair(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#keypair ContainerinfraClusterV1#keypair}.'''
        result = self._values.get("keypair")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#labels ContainerinfraClusterV1#labels}.'''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def master_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#master_count ContainerinfraClusterV1#master_count}.'''
        result = self._values.get("master_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def master_flavor(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#master_flavor ContainerinfraClusterV1#master_flavor}.'''
        result = self._values.get("master_flavor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_lb_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#master_lb_enabled ContainerinfraClusterV1#master_lb_enabled}.'''
        result = self._values.get("master_lb_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def merge_labels(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#merge_labels ContainerinfraClusterV1#merge_labels}.'''
        result = self._values.get("merge_labels")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#name ContainerinfraClusterV1#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#node_count ContainerinfraClusterV1#node_count}.'''
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#region ContainerinfraClusterV1#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ContainerinfraClusterV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#timeouts ContainerinfraClusterV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ContainerinfraClusterV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerinfraClusterV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.containerinfraClusterV1.ContainerinfraClusterV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ContainerinfraClusterV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#create ContainerinfraClusterV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#delete ContainerinfraClusterV1#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#update ContainerinfraClusterV1#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5798282fdc063c628fc3231d01a2cc77d7efe1c1eeae55b0fc6bd6f68d1aca7f)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#create ContainerinfraClusterV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#delete ContainerinfraClusterV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_cluster_v1#update ContainerinfraClusterV1#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerinfraClusterV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerinfraClusterV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.containerinfraClusterV1.ContainerinfraClusterV1TimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58582f8a7760f1b728807bdebd642aa9eabe54d6a98258f4f8a7647f8ed6f789)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b32f27cb3dd0cca1bd75506bc2b4bfecdd2ae2a2a81218a026571ae7625ca7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e68afb6fd0dd3a7b6da4471ba6ac8c1e9cd8e5bd57dd67123bf643e43f51cf45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95ae5758369ec8c596fe135781d9c0d0fc59bc756faf9e2468d40ba6a2347971)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerinfraClusterV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerinfraClusterV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerinfraClusterV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6321fec5aa6cd62729ca48281af5bf248747018f6d1484043c967948c7b5364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ContainerinfraClusterV1",
    "ContainerinfraClusterV1Config",
    "ContainerinfraClusterV1Timeouts",
    "ContainerinfraClusterV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__43cf740669c0daabbdebd8091b3e7e2ee330d83f8f88686e026906c9d3c962c9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_template_id: builtins.str,
    create_timeout: typing.Optional[jsii.Number] = None,
    discovery_url: typing.Optional[builtins.str] = None,
    docker_volume_size: typing.Optional[jsii.Number] = None,
    fixed_network: typing.Optional[builtins.str] = None,
    fixed_subnet: typing.Optional[builtins.str] = None,
    flavor: typing.Optional[builtins.str] = None,
    floating_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    keypair: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    master_count: typing.Optional[jsii.Number] = None,
    master_flavor: typing.Optional[builtins.str] = None,
    master_lb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    merge_labels: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    node_count: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ContainerinfraClusterV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a43b1630bb4d3600693953cd56952942e05fd2ec525cec63884778b06438a9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d533bd5eb3fdd9c025c70d3cdc027b03f1b7731ac7bfb66c402122f0161f0c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fbfdafaeac64faff17cd1b1fca78ff3f385a4d9319775fe08c1123a14d58d7f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3dd2fdbe8608e59465e3f6976b946016bd8fd0b4f8e0eedceba3b64657b348b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f331501a688ec4584dcc823b2c503e19612fbb11adcb9bfbfaeb816d77420e1d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fe69e441d310a83c9bb6bfccbafb6fe228ac1551bae86e90f1fb503cb149f77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f816823be0b7c018c89fa2009711f773f25fd8f6fa44650f019e97b4d6831a77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__250885d105c645bda45137e8ad5912db1bf74e1eb61ac4d40da5f0de728a56cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b931cf5455f16c163cc86a75a07e0695157b9041f4293e0edb003706c5925c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cc30acb5c2220c70f9177bce9e4d360f32578a24de941c913de337d27030050(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c7e1e7e9e8e7a4996056224d5dd3b3ce9e089a2fa6c605505e4781cc33d62a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7365ef55e8d8596f36ad4749a78b4907d016184f070345e1f6bc3b45c40bd9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a59790860a6478f16738b42a92e8c2ce002cf7019d9722309378638adf13c80(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d11f118666accb196644f3777194cf6d6c4dcc4408a2a1e1a3bbffb9b0bc4378(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8acc8b169e0dc8126a721600d3b498808b664ae255a2b4b419f805f431092fcf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49069434019f9b4e0455ecc14cdc8fddbcdbe05ed813ae067865e1d9082c9a10(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e494c394faba8adc0646b5e3ccbe2e8c602f847eb329c469675a3db6e167c292(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58a9f5a4ece780c660252969a1d2a67905917e105103deb2a87eb89425e1c59(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a51c04c57098fde3ea0652d9885ea969b1d63e271906109359398d359d1f0616(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eef2bdcb88c96292e93a694b48f173dd41585c2ea6c2be954951fe6c3c8864b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_template_id: builtins.str,
    create_timeout: typing.Optional[jsii.Number] = None,
    discovery_url: typing.Optional[builtins.str] = None,
    docker_volume_size: typing.Optional[jsii.Number] = None,
    fixed_network: typing.Optional[builtins.str] = None,
    fixed_subnet: typing.Optional[builtins.str] = None,
    flavor: typing.Optional[builtins.str] = None,
    floating_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    keypair: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    master_count: typing.Optional[jsii.Number] = None,
    master_flavor: typing.Optional[builtins.str] = None,
    master_lb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    merge_labels: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    node_count: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ContainerinfraClusterV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5798282fdc063c628fc3231d01a2cc77d7efe1c1eeae55b0fc6bd6f68d1aca7f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58582f8a7760f1b728807bdebd642aa9eabe54d6a98258f4f8a7647f8ed6f789(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b32f27cb3dd0cca1bd75506bc2b4bfecdd2ae2a2a81218a026571ae7625ca7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e68afb6fd0dd3a7b6da4471ba6ac8c1e9cd8e5bd57dd67123bf643e43f51cf45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ae5758369ec8c596fe135781d9c0d0fc59bc756faf9e2468d40ba6a2347971(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6321fec5aa6cd62729ca48281af5bf248747018f6d1484043c967948c7b5364(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerinfraClusterV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
