r'''
# `openstack_containerinfra_clustertemplate_v1`

Refer to the Terraform Registry for docs: [`openstack_containerinfra_clustertemplate_v1`](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1).
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


class ContainerinfraClustertemplateV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.containerinfraClustertemplateV1.ContainerinfraClustertemplateV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1 openstack_containerinfra_clustertemplate_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        coe: builtins.str,
        image: builtins.str,
        name: builtins.str,
        apiserver_port: typing.Optional[jsii.Number] = None,
        cluster_distro: typing.Optional[builtins.str] = None,
        dns_nameserver: typing.Optional[builtins.str] = None,
        docker_storage_driver: typing.Optional[builtins.str] = None,
        docker_volume_size: typing.Optional[jsii.Number] = None,
        external_network_id: typing.Optional[builtins.str] = None,
        fixed_network: typing.Optional[builtins.str] = None,
        fixed_subnet: typing.Optional[builtins.str] = None,
        flavor: typing.Optional[builtins.str] = None,
        floating_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hidden: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_proxy: typing.Optional[builtins.str] = None,
        https_proxy: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        insecure_registry: typing.Optional[builtins.str] = None,
        keypair_id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        master_flavor: typing.Optional[builtins.str] = None,
        master_lb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network_driver: typing.Optional[builtins.str] = None,
        no_proxy: typing.Optional[builtins.str] = None,
        public: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        registry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        server_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ContainerinfraClustertemplateV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        volume_driver: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1 openstack_containerinfra_clustertemplate_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param coe: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#coe ContainerinfraClustertemplateV1#coe}.
        :param image: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#image ContainerinfraClustertemplateV1#image}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#name ContainerinfraClustertemplateV1#name}.
        :param apiserver_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#apiserver_port ContainerinfraClustertemplateV1#apiserver_port}.
        :param cluster_distro: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#cluster_distro ContainerinfraClustertemplateV1#cluster_distro}.
        :param dns_nameserver: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#dns_nameserver ContainerinfraClustertemplateV1#dns_nameserver}.
        :param docker_storage_driver: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#docker_storage_driver ContainerinfraClustertemplateV1#docker_storage_driver}.
        :param docker_volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#docker_volume_size ContainerinfraClustertemplateV1#docker_volume_size}.
        :param external_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#external_network_id ContainerinfraClustertemplateV1#external_network_id}.
        :param fixed_network: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#fixed_network ContainerinfraClustertemplateV1#fixed_network}.
        :param fixed_subnet: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#fixed_subnet ContainerinfraClustertemplateV1#fixed_subnet}.
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#flavor ContainerinfraClustertemplateV1#flavor}.
        :param floating_ip_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#floating_ip_enabled ContainerinfraClustertemplateV1#floating_ip_enabled}.
        :param hidden: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#hidden ContainerinfraClustertemplateV1#hidden}.
        :param http_proxy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#http_proxy ContainerinfraClustertemplateV1#http_proxy}.
        :param https_proxy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#https_proxy ContainerinfraClustertemplateV1#https_proxy}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#id ContainerinfraClustertemplateV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param insecure_registry: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#insecure_registry ContainerinfraClustertemplateV1#insecure_registry}.
        :param keypair_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#keypair_id ContainerinfraClustertemplateV1#keypair_id}.
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#labels ContainerinfraClustertemplateV1#labels}.
        :param master_flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#master_flavor ContainerinfraClustertemplateV1#master_flavor}.
        :param master_lb_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#master_lb_enabled ContainerinfraClustertemplateV1#master_lb_enabled}.
        :param network_driver: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#network_driver ContainerinfraClustertemplateV1#network_driver}.
        :param no_proxy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#no_proxy ContainerinfraClustertemplateV1#no_proxy}.
        :param public: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#public ContainerinfraClustertemplateV1#public}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#region ContainerinfraClustertemplateV1#region}.
        :param registry_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#registry_enabled ContainerinfraClustertemplateV1#registry_enabled}.
        :param server_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#server_type ContainerinfraClustertemplateV1#server_type}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#timeouts ContainerinfraClustertemplateV1#timeouts}
        :param tls_disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#tls_disabled ContainerinfraClustertemplateV1#tls_disabled}.
        :param volume_driver: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#volume_driver ContainerinfraClustertemplateV1#volume_driver}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3097cfbc4b0a5814aa9128fcdc8f084c577dc09b01ccbb3d3e6132a969effa3b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ContainerinfraClustertemplateV1Config(
            coe=coe,
            image=image,
            name=name,
            apiserver_port=apiserver_port,
            cluster_distro=cluster_distro,
            dns_nameserver=dns_nameserver,
            docker_storage_driver=docker_storage_driver,
            docker_volume_size=docker_volume_size,
            external_network_id=external_network_id,
            fixed_network=fixed_network,
            fixed_subnet=fixed_subnet,
            flavor=flavor,
            floating_ip_enabled=floating_ip_enabled,
            hidden=hidden,
            http_proxy=http_proxy,
            https_proxy=https_proxy,
            id=id,
            insecure_registry=insecure_registry,
            keypair_id=keypair_id,
            labels=labels,
            master_flavor=master_flavor,
            master_lb_enabled=master_lb_enabled,
            network_driver=network_driver,
            no_proxy=no_proxy,
            public=public,
            region=region,
            registry_enabled=registry_enabled,
            server_type=server_type,
            timeouts=timeouts,
            tls_disabled=tls_disabled,
            volume_driver=volume_driver,
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
        '''Generates CDKTF code for importing a ContainerinfraClustertemplateV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ContainerinfraClustertemplateV1 to import.
        :param import_from_id: The id of the existing ContainerinfraClustertemplateV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ContainerinfraClustertemplateV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6ff90e6366e83f4039ab7c58e5be204edd05b70258d5f5587605b930b9f54d1)
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
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#create ContainerinfraClustertemplateV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#delete ContainerinfraClustertemplateV1#delete}.
        '''
        value = ContainerinfraClustertemplateV1Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetApiserverPort")
    def reset_apiserver_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiserverPort", []))

    @jsii.member(jsii_name="resetClusterDistro")
    def reset_cluster_distro(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterDistro", []))

    @jsii.member(jsii_name="resetDnsNameserver")
    def reset_dns_nameserver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsNameserver", []))

    @jsii.member(jsii_name="resetDockerStorageDriver")
    def reset_docker_storage_driver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerStorageDriver", []))

    @jsii.member(jsii_name="resetDockerVolumeSize")
    def reset_docker_volume_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerVolumeSize", []))

    @jsii.member(jsii_name="resetExternalNetworkId")
    def reset_external_network_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalNetworkId", []))

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

    @jsii.member(jsii_name="resetHidden")
    def reset_hidden(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHidden", []))

    @jsii.member(jsii_name="resetHttpProxy")
    def reset_http_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpProxy", []))

    @jsii.member(jsii_name="resetHttpsProxy")
    def reset_https_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsProxy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInsecureRegistry")
    def reset_insecure_registry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecureRegistry", []))

    @jsii.member(jsii_name="resetKeypairId")
    def reset_keypair_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeypairId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMasterFlavor")
    def reset_master_flavor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasterFlavor", []))

    @jsii.member(jsii_name="resetMasterLbEnabled")
    def reset_master_lb_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasterLbEnabled", []))

    @jsii.member(jsii_name="resetNetworkDriver")
    def reset_network_driver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkDriver", []))

    @jsii.member(jsii_name="resetNoProxy")
    def reset_no_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoProxy", []))

    @jsii.member(jsii_name="resetPublic")
    def reset_public(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublic", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRegistryEnabled")
    def reset_registry_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistryEnabled", []))

    @jsii.member(jsii_name="resetServerType")
    def reset_server_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerType", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTlsDisabled")
    def reset_tls_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsDisabled", []))

    @jsii.member(jsii_name="resetVolumeDriver")
    def reset_volume_driver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeDriver", []))

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
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ContainerinfraClustertemplateV1TimeoutsOutputReference":
        return typing.cast("ContainerinfraClustertemplateV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userId"))

    @builtins.property
    @jsii.member(jsii_name="apiserverPortInput")
    def apiserver_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "apiserverPortInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterDistroInput")
    def cluster_distro_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterDistroInput"))

    @builtins.property
    @jsii.member(jsii_name="coeInput")
    def coe_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "coeInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsNameserverInput")
    def dns_nameserver_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsNameserverInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerStorageDriverInput")
    def docker_storage_driver_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dockerStorageDriverInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerVolumeSizeInput")
    def docker_volume_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dockerVolumeSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="externalNetworkIdInput")
    def external_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalNetworkIdInput"))

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
    @jsii.member(jsii_name="hiddenInput")
    def hidden_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hiddenInput"))

    @builtins.property
    @jsii.member(jsii_name="httpProxyInput")
    def http_proxy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsProxyInput")
    def https_proxy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpsProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureRegistryInput")
    def insecure_registry_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "insecureRegistryInput"))

    @builtins.property
    @jsii.member(jsii_name="keypairIdInput")
    def keypair_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keypairIdInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkDriverInput")
    def network_driver_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkDriverInput"))

    @builtins.property
    @jsii.member(jsii_name="noProxyInput")
    def no_proxy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "noProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="publicInput")
    def public_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="registryEnabledInput")
    def registry_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "registryEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="serverTypeInput")
    def server_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerinfraClustertemplateV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerinfraClustertemplateV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsDisabledInput")
    def tls_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeDriverInput")
    def volume_driver_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeDriverInput"))

    @builtins.property
    @jsii.member(jsii_name="apiserverPort")
    def apiserver_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "apiserverPort"))

    @apiserver_port.setter
    def apiserver_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c192a296748ef2d7580fae5a0eb0905c2951e59c398ffa98a55531191e4af57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiserverPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterDistro")
    def cluster_distro(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterDistro"))

    @cluster_distro.setter
    def cluster_distro(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e701193901661b013cde5a25aec2c6da2d20d9894b55a0d93955d5e7b7a33e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterDistro", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="coe")
    def coe(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "coe"))

    @coe.setter
    def coe(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3643fa5f50349d23cc9608bc8f4db9b8d76d25904932c674b0413b3c2541efdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coe", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsNameserver")
    def dns_nameserver(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsNameserver"))

    @dns_nameserver.setter
    def dns_nameserver(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e853dd9fe3708114c656be6ba81fdd836ae9f1b36f40b81f1b6f1b35d85f487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsNameserver", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dockerStorageDriver")
    def docker_storage_driver(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dockerStorageDriver"))

    @docker_storage_driver.setter
    def docker_storage_driver(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af063c48f8cd4e0717757cbeb21c00f2ca4c406ff73787f966dd0ff0035decda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerStorageDriver", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dockerVolumeSize")
    def docker_volume_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dockerVolumeSize"))

    @docker_volume_size.setter
    def docker_volume_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7eb7c0c8fc0ff60e3b37f84f44899b917ce03418dfb44df49525f89f0551df1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerVolumeSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalNetworkId")
    def external_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalNetworkId"))

    @external_network_id.setter
    def external_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c42c9f62c4bb425d27862d79d650bf03092c56bdcc01bad5bab2e2d6c8b44007)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fixedNetwork")
    def fixed_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fixedNetwork"))

    @fixed_network.setter
    def fixed_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a2a5e5cad957b578764ebef6f1f7e1148f21ddf3ec01aa5a07dcf290271d85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fixedSubnet")
    def fixed_subnet(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fixedSubnet"))

    @fixed_subnet.setter
    def fixed_subnet(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f3435434456fea0add55355e444e48801711ceb322faa42f8af6d53225ebf25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedSubnet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flavor")
    def flavor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavor"))

    @flavor.setter
    def flavor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__020dc77c998c18f0cb10c8f89dcb41f4012e7e78fbdc0be486e6da2314a1059d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d345b400f420c66ff0d9fc036cb7f2a931f4e2b39f9a9e8335731969ab9e741)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "floatingIpEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hidden")
    def hidden(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hidden"))

    @hidden.setter
    def hidden(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9143df8dfaf615345f50d712f3830b44d67e2f2e869f0f3c8712533169522a76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hidden", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpProxy")
    def http_proxy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpProxy"))

    @http_proxy.setter
    def http_proxy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c81dd48d20e77a18aee0f8de3bb77920f21003aa90bbac825ebbe080dff6823)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpProxy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsProxy")
    def https_proxy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsProxy"))

    @https_proxy.setter
    def https_proxy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0501f3d503e8b2e8d1095a305bfa6476c38eb26e6751cca5013d9240f7b9e07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsProxy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0953ec827b95b6845c9c1a4b312af53a2716fdc824675d23eef511b4031b7d19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b15006ad742ebb8089d21deb50989b212a6fac1a9f4859aa61e913d51cd424fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="insecureRegistry")
    def insecure_registry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "insecureRegistry"))

    @insecure_registry.setter
    def insecure_registry(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40749a42c0fdfd42eae783b63053ad01c6e00b1b807c206bfbedd64a4813aacb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecureRegistry", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keypairId")
    def keypair_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keypairId"))

    @keypair_id.setter
    def keypair_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__562c4247b693178d23514842fc5432004be51921963a50b1a9276e5563803ec0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keypairId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59a4fbc54a04c450d0587ba6b56cdcefcb787a04ee4840d244bad84133343479)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="masterFlavor")
    def master_flavor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "masterFlavor"))

    @master_flavor.setter
    def master_flavor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a07a0ca5318616db60be26fe97bb57dd3c4043a67f6587294458fe895699f378)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c14ae37f2bbfd8c29b9791e9252f235ea32db50a9e7d6c7709fccbb48005fb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterLbEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd2bdc6eec22bf3e19d98f0cf6c56d2f866b77c8ded5d1d2d0be05b251575c17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkDriver")
    def network_driver(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkDriver"))

    @network_driver.setter
    def network_driver(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15260fa7137e9efc7ed09c0c2dc7b1231dbc7b6978b019a2b0616d1be1d7c2f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkDriver", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noProxy")
    def no_proxy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "noProxy"))

    @no_proxy.setter
    def no_proxy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6376c227930df8332c69015111ecd30241d2b7644c598802e9724fed60afe0ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noProxy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="public")
    def public(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "public"))

    @public.setter
    def public(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eca78711a572dd854ea711066ab3f9e3c89e7651d2ffaa519b815d5eba73053)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "public", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbd297040284f000d65928dbc0d3db4f60a6016e23832257a8ef70e0f26fab9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registryEnabled")
    def registry_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "registryEnabled"))

    @registry_enabled.setter
    def registry_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9caf7acf74f004f95f2eaa0db54143559ef40a802e0b570d5f4acbbbafffe23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverType")
    def server_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverType"))

    @server_type.setter
    def server_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6858be0a6b2bd85710d62e0512b7e20e407163ee6f6bad6ea7e6f8014119b487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsDisabled")
    def tls_disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tlsDisabled"))

    @tls_disabled.setter
    def tls_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a78a361c590316bb96feb5cdb6105f3c0d10a2010524fda5fbf74f5c8a752706)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeDriver")
    def volume_driver(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeDriver"))

    @volume_driver.setter
    def volume_driver(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__437a5b7de1ff8e4336df25e0f9a5914f2bbf0e8a3530eddda819fc43cc7ece46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeDriver", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.containerinfraClustertemplateV1.ContainerinfraClustertemplateV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "coe": "coe",
        "image": "image",
        "name": "name",
        "apiserver_port": "apiserverPort",
        "cluster_distro": "clusterDistro",
        "dns_nameserver": "dnsNameserver",
        "docker_storage_driver": "dockerStorageDriver",
        "docker_volume_size": "dockerVolumeSize",
        "external_network_id": "externalNetworkId",
        "fixed_network": "fixedNetwork",
        "fixed_subnet": "fixedSubnet",
        "flavor": "flavor",
        "floating_ip_enabled": "floatingIpEnabled",
        "hidden": "hidden",
        "http_proxy": "httpProxy",
        "https_proxy": "httpsProxy",
        "id": "id",
        "insecure_registry": "insecureRegistry",
        "keypair_id": "keypairId",
        "labels": "labels",
        "master_flavor": "masterFlavor",
        "master_lb_enabled": "masterLbEnabled",
        "network_driver": "networkDriver",
        "no_proxy": "noProxy",
        "public": "public",
        "region": "region",
        "registry_enabled": "registryEnabled",
        "server_type": "serverType",
        "timeouts": "timeouts",
        "tls_disabled": "tlsDisabled",
        "volume_driver": "volumeDriver",
    },
)
class ContainerinfraClustertemplateV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        coe: builtins.str,
        image: builtins.str,
        name: builtins.str,
        apiserver_port: typing.Optional[jsii.Number] = None,
        cluster_distro: typing.Optional[builtins.str] = None,
        dns_nameserver: typing.Optional[builtins.str] = None,
        docker_storage_driver: typing.Optional[builtins.str] = None,
        docker_volume_size: typing.Optional[jsii.Number] = None,
        external_network_id: typing.Optional[builtins.str] = None,
        fixed_network: typing.Optional[builtins.str] = None,
        fixed_subnet: typing.Optional[builtins.str] = None,
        flavor: typing.Optional[builtins.str] = None,
        floating_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hidden: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_proxy: typing.Optional[builtins.str] = None,
        https_proxy: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        insecure_registry: typing.Optional[builtins.str] = None,
        keypair_id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        master_flavor: typing.Optional[builtins.str] = None,
        master_lb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network_driver: typing.Optional[builtins.str] = None,
        no_proxy: typing.Optional[builtins.str] = None,
        public: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        registry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        server_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ContainerinfraClustertemplateV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        volume_driver: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param coe: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#coe ContainerinfraClustertemplateV1#coe}.
        :param image: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#image ContainerinfraClustertemplateV1#image}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#name ContainerinfraClustertemplateV1#name}.
        :param apiserver_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#apiserver_port ContainerinfraClustertemplateV1#apiserver_port}.
        :param cluster_distro: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#cluster_distro ContainerinfraClustertemplateV1#cluster_distro}.
        :param dns_nameserver: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#dns_nameserver ContainerinfraClustertemplateV1#dns_nameserver}.
        :param docker_storage_driver: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#docker_storage_driver ContainerinfraClustertemplateV1#docker_storage_driver}.
        :param docker_volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#docker_volume_size ContainerinfraClustertemplateV1#docker_volume_size}.
        :param external_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#external_network_id ContainerinfraClustertemplateV1#external_network_id}.
        :param fixed_network: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#fixed_network ContainerinfraClustertemplateV1#fixed_network}.
        :param fixed_subnet: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#fixed_subnet ContainerinfraClustertemplateV1#fixed_subnet}.
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#flavor ContainerinfraClustertemplateV1#flavor}.
        :param floating_ip_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#floating_ip_enabled ContainerinfraClustertemplateV1#floating_ip_enabled}.
        :param hidden: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#hidden ContainerinfraClustertemplateV1#hidden}.
        :param http_proxy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#http_proxy ContainerinfraClustertemplateV1#http_proxy}.
        :param https_proxy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#https_proxy ContainerinfraClustertemplateV1#https_proxy}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#id ContainerinfraClustertemplateV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param insecure_registry: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#insecure_registry ContainerinfraClustertemplateV1#insecure_registry}.
        :param keypair_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#keypair_id ContainerinfraClustertemplateV1#keypair_id}.
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#labels ContainerinfraClustertemplateV1#labels}.
        :param master_flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#master_flavor ContainerinfraClustertemplateV1#master_flavor}.
        :param master_lb_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#master_lb_enabled ContainerinfraClustertemplateV1#master_lb_enabled}.
        :param network_driver: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#network_driver ContainerinfraClustertemplateV1#network_driver}.
        :param no_proxy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#no_proxy ContainerinfraClustertemplateV1#no_proxy}.
        :param public: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#public ContainerinfraClustertemplateV1#public}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#region ContainerinfraClustertemplateV1#region}.
        :param registry_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#registry_enabled ContainerinfraClustertemplateV1#registry_enabled}.
        :param server_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#server_type ContainerinfraClustertemplateV1#server_type}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#timeouts ContainerinfraClustertemplateV1#timeouts}
        :param tls_disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#tls_disabled ContainerinfraClustertemplateV1#tls_disabled}.
        :param volume_driver: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#volume_driver ContainerinfraClustertemplateV1#volume_driver}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ContainerinfraClustertemplateV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82c4d0ab18af1668ba6f2bdb76d9788b42e3eb30dae74332d8eb4fbc5a01e997)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument coe", value=coe, expected_type=type_hints["coe"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument apiserver_port", value=apiserver_port, expected_type=type_hints["apiserver_port"])
            check_type(argname="argument cluster_distro", value=cluster_distro, expected_type=type_hints["cluster_distro"])
            check_type(argname="argument dns_nameserver", value=dns_nameserver, expected_type=type_hints["dns_nameserver"])
            check_type(argname="argument docker_storage_driver", value=docker_storage_driver, expected_type=type_hints["docker_storage_driver"])
            check_type(argname="argument docker_volume_size", value=docker_volume_size, expected_type=type_hints["docker_volume_size"])
            check_type(argname="argument external_network_id", value=external_network_id, expected_type=type_hints["external_network_id"])
            check_type(argname="argument fixed_network", value=fixed_network, expected_type=type_hints["fixed_network"])
            check_type(argname="argument fixed_subnet", value=fixed_subnet, expected_type=type_hints["fixed_subnet"])
            check_type(argname="argument flavor", value=flavor, expected_type=type_hints["flavor"])
            check_type(argname="argument floating_ip_enabled", value=floating_ip_enabled, expected_type=type_hints["floating_ip_enabled"])
            check_type(argname="argument hidden", value=hidden, expected_type=type_hints["hidden"])
            check_type(argname="argument http_proxy", value=http_proxy, expected_type=type_hints["http_proxy"])
            check_type(argname="argument https_proxy", value=https_proxy, expected_type=type_hints["https_proxy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument insecure_registry", value=insecure_registry, expected_type=type_hints["insecure_registry"])
            check_type(argname="argument keypair_id", value=keypair_id, expected_type=type_hints["keypair_id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument master_flavor", value=master_flavor, expected_type=type_hints["master_flavor"])
            check_type(argname="argument master_lb_enabled", value=master_lb_enabled, expected_type=type_hints["master_lb_enabled"])
            check_type(argname="argument network_driver", value=network_driver, expected_type=type_hints["network_driver"])
            check_type(argname="argument no_proxy", value=no_proxy, expected_type=type_hints["no_proxy"])
            check_type(argname="argument public", value=public, expected_type=type_hints["public"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument registry_enabled", value=registry_enabled, expected_type=type_hints["registry_enabled"])
            check_type(argname="argument server_type", value=server_type, expected_type=type_hints["server_type"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument tls_disabled", value=tls_disabled, expected_type=type_hints["tls_disabled"])
            check_type(argname="argument volume_driver", value=volume_driver, expected_type=type_hints["volume_driver"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "coe": coe,
            "image": image,
            "name": name,
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
        if apiserver_port is not None:
            self._values["apiserver_port"] = apiserver_port
        if cluster_distro is not None:
            self._values["cluster_distro"] = cluster_distro
        if dns_nameserver is not None:
            self._values["dns_nameserver"] = dns_nameserver
        if docker_storage_driver is not None:
            self._values["docker_storage_driver"] = docker_storage_driver
        if docker_volume_size is not None:
            self._values["docker_volume_size"] = docker_volume_size
        if external_network_id is not None:
            self._values["external_network_id"] = external_network_id
        if fixed_network is not None:
            self._values["fixed_network"] = fixed_network
        if fixed_subnet is not None:
            self._values["fixed_subnet"] = fixed_subnet
        if flavor is not None:
            self._values["flavor"] = flavor
        if floating_ip_enabled is not None:
            self._values["floating_ip_enabled"] = floating_ip_enabled
        if hidden is not None:
            self._values["hidden"] = hidden
        if http_proxy is not None:
            self._values["http_proxy"] = http_proxy
        if https_proxy is not None:
            self._values["https_proxy"] = https_proxy
        if id is not None:
            self._values["id"] = id
        if insecure_registry is not None:
            self._values["insecure_registry"] = insecure_registry
        if keypair_id is not None:
            self._values["keypair_id"] = keypair_id
        if labels is not None:
            self._values["labels"] = labels
        if master_flavor is not None:
            self._values["master_flavor"] = master_flavor
        if master_lb_enabled is not None:
            self._values["master_lb_enabled"] = master_lb_enabled
        if network_driver is not None:
            self._values["network_driver"] = network_driver
        if no_proxy is not None:
            self._values["no_proxy"] = no_proxy
        if public is not None:
            self._values["public"] = public
        if region is not None:
            self._values["region"] = region
        if registry_enabled is not None:
            self._values["registry_enabled"] = registry_enabled
        if server_type is not None:
            self._values["server_type"] = server_type
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if tls_disabled is not None:
            self._values["tls_disabled"] = tls_disabled
        if volume_driver is not None:
            self._values["volume_driver"] = volume_driver

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
    def coe(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#coe ContainerinfraClustertemplateV1#coe}.'''
        result = self._values.get("coe")
        assert result is not None, "Required property 'coe' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#image ContainerinfraClustertemplateV1#image}.'''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#name ContainerinfraClustertemplateV1#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def apiserver_port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#apiserver_port ContainerinfraClustertemplateV1#apiserver_port}.'''
        result = self._values.get("apiserver_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cluster_distro(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#cluster_distro ContainerinfraClustertemplateV1#cluster_distro}.'''
        result = self._values.get("cluster_distro")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_nameserver(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#dns_nameserver ContainerinfraClustertemplateV1#dns_nameserver}.'''
        result = self._values.get("dns_nameserver")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_storage_driver(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#docker_storage_driver ContainerinfraClustertemplateV1#docker_storage_driver}.'''
        result = self._values.get("docker_storage_driver")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_volume_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#docker_volume_size ContainerinfraClustertemplateV1#docker_volume_size}.'''
        result = self._values.get("docker_volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def external_network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#external_network_id ContainerinfraClustertemplateV1#external_network_id}.'''
        result = self._values.get("external_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fixed_network(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#fixed_network ContainerinfraClustertemplateV1#fixed_network}.'''
        result = self._values.get("fixed_network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fixed_subnet(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#fixed_subnet ContainerinfraClustertemplateV1#fixed_subnet}.'''
        result = self._values.get("fixed_subnet")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flavor(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#flavor ContainerinfraClustertemplateV1#flavor}.'''
        result = self._values.get("flavor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def floating_ip_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#floating_ip_enabled ContainerinfraClustertemplateV1#floating_ip_enabled}.'''
        result = self._values.get("floating_ip_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hidden(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#hidden ContainerinfraClustertemplateV1#hidden}.'''
        result = self._values.get("hidden")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def http_proxy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#http_proxy ContainerinfraClustertemplateV1#http_proxy}.'''
        result = self._values.get("http_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_proxy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#https_proxy ContainerinfraClustertemplateV1#https_proxy}.'''
        result = self._values.get("https_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#id ContainerinfraClustertemplateV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insecure_registry(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#insecure_registry ContainerinfraClustertemplateV1#insecure_registry}.'''
        result = self._values.get("insecure_registry")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keypair_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#keypair_id ContainerinfraClustertemplateV1#keypair_id}.'''
        result = self._values.get("keypair_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#labels ContainerinfraClustertemplateV1#labels}.'''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def master_flavor(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#master_flavor ContainerinfraClustertemplateV1#master_flavor}.'''
        result = self._values.get("master_flavor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_lb_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#master_lb_enabled ContainerinfraClustertemplateV1#master_lb_enabled}.'''
        result = self._values.get("master_lb_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def network_driver(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#network_driver ContainerinfraClustertemplateV1#network_driver}.'''
        result = self._values.get("network_driver")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_proxy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#no_proxy ContainerinfraClustertemplateV1#no_proxy}.'''
        result = self._values.get("no_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#public ContainerinfraClustertemplateV1#public}.'''
        result = self._values.get("public")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#region ContainerinfraClustertemplateV1#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registry_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#registry_enabled ContainerinfraClustertemplateV1#registry_enabled}.'''
        result = self._values.get("registry_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def server_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#server_type ContainerinfraClustertemplateV1#server_type}.'''
        result = self._values.get("server_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ContainerinfraClustertemplateV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#timeouts ContainerinfraClustertemplateV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ContainerinfraClustertemplateV1Timeouts"], result)

    @builtins.property
    def tls_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#tls_disabled ContainerinfraClustertemplateV1#tls_disabled}.'''
        result = self._values.get("tls_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def volume_driver(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#volume_driver ContainerinfraClustertemplateV1#volume_driver}.'''
        result = self._values.get("volume_driver")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerinfraClustertemplateV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.containerinfraClustertemplateV1.ContainerinfraClustertemplateV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class ContainerinfraClustertemplateV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#create ContainerinfraClustertemplateV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#delete ContainerinfraClustertemplateV1#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5de3a8adad6df380fcfa9ec414b8b12cd293ba0c3852bbd995590980401a4c55)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#create ContainerinfraClustertemplateV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/containerinfra_clustertemplate_v1#delete ContainerinfraClustertemplateV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerinfraClustertemplateV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerinfraClustertemplateV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.containerinfraClustertemplateV1.ContainerinfraClustertemplateV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04d1a6bec10a8e13a286254a8cc86111d4ad8e4ca94e9b28c3b140dbb1fa063d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8782487ce856921a91f7bf2b03895e790f6b703c59e557ddc410d2c6b6651de3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbc08a851a5595face1e467520f68ae85fd41027cd410e92e006a321e2bca477)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerinfraClustertemplateV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerinfraClustertemplateV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerinfraClustertemplateV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c2a7260929aa09995a8587787fcbcd8c6a6f0f11121b85d6c0b2f1c99ccae20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ContainerinfraClustertemplateV1",
    "ContainerinfraClustertemplateV1Config",
    "ContainerinfraClustertemplateV1Timeouts",
    "ContainerinfraClustertemplateV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3097cfbc4b0a5814aa9128fcdc8f084c577dc09b01ccbb3d3e6132a969effa3b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    coe: builtins.str,
    image: builtins.str,
    name: builtins.str,
    apiserver_port: typing.Optional[jsii.Number] = None,
    cluster_distro: typing.Optional[builtins.str] = None,
    dns_nameserver: typing.Optional[builtins.str] = None,
    docker_storage_driver: typing.Optional[builtins.str] = None,
    docker_volume_size: typing.Optional[jsii.Number] = None,
    external_network_id: typing.Optional[builtins.str] = None,
    fixed_network: typing.Optional[builtins.str] = None,
    fixed_subnet: typing.Optional[builtins.str] = None,
    flavor: typing.Optional[builtins.str] = None,
    floating_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hidden: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    http_proxy: typing.Optional[builtins.str] = None,
    https_proxy: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    insecure_registry: typing.Optional[builtins.str] = None,
    keypair_id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    master_flavor: typing.Optional[builtins.str] = None,
    master_lb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    network_driver: typing.Optional[builtins.str] = None,
    no_proxy: typing.Optional[builtins.str] = None,
    public: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    registry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    server_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ContainerinfraClustertemplateV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    volume_driver: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__b6ff90e6366e83f4039ab7c58e5be204edd05b70258d5f5587605b930b9f54d1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c192a296748ef2d7580fae5a0eb0905c2951e59c398ffa98a55531191e4af57(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e701193901661b013cde5a25aec2c6da2d20d9894b55a0d93955d5e7b7a33e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3643fa5f50349d23cc9608bc8f4db9b8d76d25904932c674b0413b3c2541efdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e853dd9fe3708114c656be6ba81fdd836ae9f1b36f40b81f1b6f1b35d85f487(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af063c48f8cd4e0717757cbeb21c00f2ca4c406ff73787f966dd0ff0035decda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7eb7c0c8fc0ff60e3b37f84f44899b917ce03418dfb44df49525f89f0551df1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c42c9f62c4bb425d27862d79d650bf03092c56bdcc01bad5bab2e2d6c8b44007(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a2a5e5cad957b578764ebef6f1f7e1148f21ddf3ec01aa5a07dcf290271d85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f3435434456fea0add55355e444e48801711ceb322faa42f8af6d53225ebf25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020dc77c998c18f0cb10c8f89dcb41f4012e7e78fbdc0be486e6da2314a1059d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d345b400f420c66ff0d9fc036cb7f2a931f4e2b39f9a9e8335731969ab9e741(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9143df8dfaf615345f50d712f3830b44d67e2f2e869f0f3c8712533169522a76(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c81dd48d20e77a18aee0f8de3bb77920f21003aa90bbac825ebbe080dff6823(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0501f3d503e8b2e8d1095a305bfa6476c38eb26e6751cca5013d9240f7b9e07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0953ec827b95b6845c9c1a4b312af53a2716fdc824675d23eef511b4031b7d19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b15006ad742ebb8089d21deb50989b212a6fac1a9f4859aa61e913d51cd424fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40749a42c0fdfd42eae783b63053ad01c6e00b1b807c206bfbedd64a4813aacb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__562c4247b693178d23514842fc5432004be51921963a50b1a9276e5563803ec0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a4fbc54a04c450d0587ba6b56cdcefcb787a04ee4840d244bad84133343479(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a07a0ca5318616db60be26fe97bb57dd3c4043a67f6587294458fe895699f378(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c14ae37f2bbfd8c29b9791e9252f235ea32db50a9e7d6c7709fccbb48005fb7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd2bdc6eec22bf3e19d98f0cf6c56d2f866b77c8ded5d1d2d0be05b251575c17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15260fa7137e9efc7ed09c0c2dc7b1231dbc7b6978b019a2b0616d1be1d7c2f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6376c227930df8332c69015111ecd30241d2b7644c598802e9724fed60afe0ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eca78711a572dd854ea711066ab3f9e3c89e7651d2ffaa519b815d5eba73053(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbd297040284f000d65928dbc0d3db4f60a6016e23832257a8ef70e0f26fab9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9caf7acf74f004f95f2eaa0db54143559ef40a802e0b570d5f4acbbbafffe23(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6858be0a6b2bd85710d62e0512b7e20e407163ee6f6bad6ea7e6f8014119b487(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a78a361c590316bb96feb5cdb6105f3c0d10a2010524fda5fbf74f5c8a752706(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__437a5b7de1ff8e4336df25e0f9a5914f2bbf0e8a3530eddda819fc43cc7ece46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82c4d0ab18af1668ba6f2bdb76d9788b42e3eb30dae74332d8eb4fbc5a01e997(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    coe: builtins.str,
    image: builtins.str,
    name: builtins.str,
    apiserver_port: typing.Optional[jsii.Number] = None,
    cluster_distro: typing.Optional[builtins.str] = None,
    dns_nameserver: typing.Optional[builtins.str] = None,
    docker_storage_driver: typing.Optional[builtins.str] = None,
    docker_volume_size: typing.Optional[jsii.Number] = None,
    external_network_id: typing.Optional[builtins.str] = None,
    fixed_network: typing.Optional[builtins.str] = None,
    fixed_subnet: typing.Optional[builtins.str] = None,
    flavor: typing.Optional[builtins.str] = None,
    floating_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hidden: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    http_proxy: typing.Optional[builtins.str] = None,
    https_proxy: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    insecure_registry: typing.Optional[builtins.str] = None,
    keypair_id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    master_flavor: typing.Optional[builtins.str] = None,
    master_lb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    network_driver: typing.Optional[builtins.str] = None,
    no_proxy: typing.Optional[builtins.str] = None,
    public: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    registry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    server_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ContainerinfraClustertemplateV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    volume_driver: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de3a8adad6df380fcfa9ec414b8b12cd293ba0c3852bbd995590980401a4c55(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04d1a6bec10a8e13a286254a8cc86111d4ad8e4ca94e9b28c3b140dbb1fa063d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8782487ce856921a91f7bf2b03895e790f6b703c59e557ddc410d2c6b6651de3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc08a851a5595face1e467520f68ae85fd41027cd410e92e006a321e2bca477(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2a7260929aa09995a8587787fcbcd8c6a6f0f11121b85d6c0b2f1c99ccae20(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerinfraClustertemplateV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
