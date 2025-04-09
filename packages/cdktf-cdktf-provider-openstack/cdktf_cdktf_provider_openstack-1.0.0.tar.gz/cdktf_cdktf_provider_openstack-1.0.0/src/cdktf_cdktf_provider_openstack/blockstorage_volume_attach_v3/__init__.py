r'''
# `openstack_blockstorage_volume_attach_v3`

Refer to the Terraform Registry for docs: [`openstack_blockstorage_volume_attach_v3`](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3).
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


class BlockstorageVolumeAttachV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.blockstorageVolumeAttachV3.BlockstorageVolumeAttachV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3 openstack_blockstorage_volume_attach_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        host_name: builtins.str,
        volume_id: builtins.str,
        attach_mode: typing.Optional[builtins.str] = None,
        device: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        initiator: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[builtins.str] = None,
        multipath: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        os_type: typing.Optional[builtins.str] = None,
        platform: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BlockstorageVolumeAttachV3Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        wwnn: typing.Optional[builtins.str] = None,
        wwpn: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3 openstack_blockstorage_volume_attach_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#host_name BlockstorageVolumeAttachV3#host_name}.
        :param volume_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#volume_id BlockstorageVolumeAttachV3#volume_id}.
        :param attach_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#attach_mode BlockstorageVolumeAttachV3#attach_mode}.
        :param device: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#device BlockstorageVolumeAttachV3#device}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#id BlockstorageVolumeAttachV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initiator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#initiator BlockstorageVolumeAttachV3#initiator}.
        :param ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#ip_address BlockstorageVolumeAttachV3#ip_address}.
        :param multipath: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#multipath BlockstorageVolumeAttachV3#multipath}.
        :param os_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#os_type BlockstorageVolumeAttachV3#os_type}.
        :param platform: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#platform BlockstorageVolumeAttachV3#platform}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#region BlockstorageVolumeAttachV3#region}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#timeouts BlockstorageVolumeAttachV3#timeouts}
        :param wwnn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#wwnn BlockstorageVolumeAttachV3#wwnn}.
        :param wwpn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#wwpn BlockstorageVolumeAttachV3#wwpn}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1416730fc0ce85bf49d181a6d66bd7821aa1c134aebe2c05d09d917eeb1f3699)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BlockstorageVolumeAttachV3Config(
            host_name=host_name,
            volume_id=volume_id,
            attach_mode=attach_mode,
            device=device,
            id=id,
            initiator=initiator,
            ip_address=ip_address,
            multipath=multipath,
            os_type=os_type,
            platform=platform,
            region=region,
            timeouts=timeouts,
            wwnn=wwnn,
            wwpn=wwpn,
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
        '''Generates CDKTF code for importing a BlockstorageVolumeAttachV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BlockstorageVolumeAttachV3 to import.
        :param import_from_id: The id of the existing BlockstorageVolumeAttachV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BlockstorageVolumeAttachV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c7ab708ee77e851f5177b0dd89522367cfa43c32faa3c4fcf532294d14c7d9e)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#create BlockstorageVolumeAttachV3#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#delete BlockstorageVolumeAttachV3#delete}.
        '''
        value = BlockstorageVolumeAttachV3Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAttachMode")
    def reset_attach_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttachMode", []))

    @jsii.member(jsii_name="resetDevice")
    def reset_device(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDevice", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInitiator")
    def reset_initiator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitiator", []))

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @jsii.member(jsii_name="resetMultipath")
    def reset_multipath(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultipath", []))

    @jsii.member(jsii_name="resetOsType")
    def reset_os_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsType", []))

    @jsii.member(jsii_name="resetPlatform")
    def reset_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatform", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWwnn")
    def reset_wwnn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWwnn", []))

    @jsii.member(jsii_name="resetWwpn")
    def reset_wwpn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWwpn", []))

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
    @jsii.member(jsii_name="data")
    def data(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "data"))

    @builtins.property
    @jsii.member(jsii_name="driverVolumeType")
    def driver_volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "driverVolumeType"))

    @builtins.property
    @jsii.member(jsii_name="mountPointBase")
    def mount_point_base(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountPointBase"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BlockstorageVolumeAttachV3TimeoutsOutputReference":
        return typing.cast("BlockstorageVolumeAttachV3TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="attachModeInput")
    def attach_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attachModeInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceInput")
    def device_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="initiatorInput")
    def initiator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "initiatorInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="multipathInput")
    def multipath_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "multipathInput"))

    @builtins.property
    @jsii.member(jsii_name="osTypeInput")
    def os_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="platformInput")
    def platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platformInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BlockstorageVolumeAttachV3Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BlockstorageVolumeAttachV3Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeIdInput")
    def volume_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="wwnnInput")
    def wwnn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "wwnnInput"))

    @builtins.property
    @jsii.member(jsii_name="wwpnInput")
    def wwpn_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "wwpnInput"))

    @builtins.property
    @jsii.member(jsii_name="attachMode")
    def attach_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attachMode"))

    @attach_mode.setter
    def attach_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39bbd56f39a3dbf91f84c138948319600fa8361a91a61d816ffec2729b2d2bc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attachMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="device")
    def device(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "device"))

    @device.setter
    def device(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23649e15908121ae557f44f1ca7162f1d072caa134eb38c0e17097cb342fc137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "device", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84ecd33c1d65aae75b0d2cf09fdba6d466e3a5557e8255ca7f6348377902a506)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26441310c1a16dfef78314a6599db68a0b285bd1bfbfe553103267b901f3b430)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initiator")
    def initiator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "initiator"))

    @initiator.setter
    def initiator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f4c63288339f33640aed029b1191402a0345f9d23972887bcf6a7d81decdf35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initiator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5103366617765d9a0528da17314f1f2198ed2eb081fb7044a433a6044264c1a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multipath")
    def multipath(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "multipath"))

    @multipath.setter
    def multipath(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c03e20edcdda8e713ac75e00e64550a5934a496a383fe58bec3b619abda9a386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multipath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osType"))

    @os_type.setter
    def os_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6245699ba17e789df7babb762d1f93fa8b6f03833900edaeedeaa11ad57dbd2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platform"))

    @platform.setter
    def platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e0584a2639c14a66a4fb069a6236c369bd25f904bf2ad598ef8e2133c37626c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03dcb9c15702f9932ba68eaffbe9d84fd06ae81d77508292663ea347016e12d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeId")
    def volume_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeId"))

    @volume_id.setter
    def volume_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdcfd3e7441866b16d1df510d6a66ebf59120ab16e47c80a7701d31060203416)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wwnn")
    def wwnn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "wwnn"))

    @wwnn.setter
    def wwnn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d8b80ed3fff5d9f854089adb64d657463a67393423d588703c8a70a839e8500)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wwnn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wwpn")
    def wwpn(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "wwpn"))

    @wwpn.setter
    def wwpn(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__915b348547cd9964ea68bb81407f2c0c8d57a355c7ae0991144bebe6d0cd0f0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wwpn", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.blockstorageVolumeAttachV3.BlockstorageVolumeAttachV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "host_name": "hostName",
        "volume_id": "volumeId",
        "attach_mode": "attachMode",
        "device": "device",
        "id": "id",
        "initiator": "initiator",
        "ip_address": "ipAddress",
        "multipath": "multipath",
        "os_type": "osType",
        "platform": "platform",
        "region": "region",
        "timeouts": "timeouts",
        "wwnn": "wwnn",
        "wwpn": "wwpn",
    },
)
class BlockstorageVolumeAttachV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        host_name: builtins.str,
        volume_id: builtins.str,
        attach_mode: typing.Optional[builtins.str] = None,
        device: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        initiator: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[builtins.str] = None,
        multipath: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        os_type: typing.Optional[builtins.str] = None,
        platform: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BlockstorageVolumeAttachV3Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        wwnn: typing.Optional[builtins.str] = None,
        wwpn: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#host_name BlockstorageVolumeAttachV3#host_name}.
        :param volume_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#volume_id BlockstorageVolumeAttachV3#volume_id}.
        :param attach_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#attach_mode BlockstorageVolumeAttachV3#attach_mode}.
        :param device: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#device BlockstorageVolumeAttachV3#device}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#id BlockstorageVolumeAttachV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initiator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#initiator BlockstorageVolumeAttachV3#initiator}.
        :param ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#ip_address BlockstorageVolumeAttachV3#ip_address}.
        :param multipath: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#multipath BlockstorageVolumeAttachV3#multipath}.
        :param os_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#os_type BlockstorageVolumeAttachV3#os_type}.
        :param platform: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#platform BlockstorageVolumeAttachV3#platform}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#region BlockstorageVolumeAttachV3#region}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#timeouts BlockstorageVolumeAttachV3#timeouts}
        :param wwnn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#wwnn BlockstorageVolumeAttachV3#wwnn}.
        :param wwpn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#wwpn BlockstorageVolumeAttachV3#wwpn}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = BlockstorageVolumeAttachV3Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__957e70654308ec342c434f670186c93833047016d125d5bf6fcc4fb2c9a8b690)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument volume_id", value=volume_id, expected_type=type_hints["volume_id"])
            check_type(argname="argument attach_mode", value=attach_mode, expected_type=type_hints["attach_mode"])
            check_type(argname="argument device", value=device, expected_type=type_hints["device"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument initiator", value=initiator, expected_type=type_hints["initiator"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument multipath", value=multipath, expected_type=type_hints["multipath"])
            check_type(argname="argument os_type", value=os_type, expected_type=type_hints["os_type"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument wwnn", value=wwnn, expected_type=type_hints["wwnn"])
            check_type(argname="argument wwpn", value=wwpn, expected_type=type_hints["wwpn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_name": host_name,
            "volume_id": volume_id,
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
        if attach_mode is not None:
            self._values["attach_mode"] = attach_mode
        if device is not None:
            self._values["device"] = device
        if id is not None:
            self._values["id"] = id
        if initiator is not None:
            self._values["initiator"] = initiator
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if multipath is not None:
            self._values["multipath"] = multipath
        if os_type is not None:
            self._values["os_type"] = os_type
        if platform is not None:
            self._values["platform"] = platform
        if region is not None:
            self._values["region"] = region
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if wwnn is not None:
            self._values["wwnn"] = wwnn
        if wwpn is not None:
            self._values["wwpn"] = wwpn

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
    def host_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#host_name BlockstorageVolumeAttachV3#host_name}.'''
        result = self._values.get("host_name")
        assert result is not None, "Required property 'host_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def volume_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#volume_id BlockstorageVolumeAttachV3#volume_id}.'''
        result = self._values.get("volume_id")
        assert result is not None, "Required property 'volume_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attach_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#attach_mode BlockstorageVolumeAttachV3#attach_mode}.'''
        result = self._values.get("attach_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#device BlockstorageVolumeAttachV3#device}.'''
        result = self._values.get("device")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#id BlockstorageVolumeAttachV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initiator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#initiator BlockstorageVolumeAttachV3#initiator}.'''
        result = self._values.get("initiator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#ip_address BlockstorageVolumeAttachV3#ip_address}.'''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multipath(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#multipath BlockstorageVolumeAttachV3#multipath}.'''
        result = self._values.get("multipath")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def os_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#os_type BlockstorageVolumeAttachV3#os_type}.'''
        result = self._values.get("os_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#platform BlockstorageVolumeAttachV3#platform}.'''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#region BlockstorageVolumeAttachV3#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BlockstorageVolumeAttachV3Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#timeouts BlockstorageVolumeAttachV3#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BlockstorageVolumeAttachV3Timeouts"], result)

    @builtins.property
    def wwnn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#wwnn BlockstorageVolumeAttachV3#wwnn}.'''
        result = self._values.get("wwnn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wwpn(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#wwpn BlockstorageVolumeAttachV3#wwpn}.'''
        result = self._values.get("wwpn")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BlockstorageVolumeAttachV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.blockstorageVolumeAttachV3.BlockstorageVolumeAttachV3Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class BlockstorageVolumeAttachV3Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#create BlockstorageVolumeAttachV3#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#delete BlockstorageVolumeAttachV3#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bfa2c6e2136a2c652256981a5b52a2c794b31f6b31ea984f4ab032f3689a2ea)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#create BlockstorageVolumeAttachV3#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/blockstorage_volume_attach_v3#delete BlockstorageVolumeAttachV3#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BlockstorageVolumeAttachV3Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BlockstorageVolumeAttachV3TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.blockstorageVolumeAttachV3.BlockstorageVolumeAttachV3TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59179e297a44216d0581439ebd4c210174c156e903dbfe237135cdc1a20cd0e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce2d3eff384e92640e420cf2f8a158d91aa96ea4f757f38d2e5c0f87132810f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b00f0fa452fb20e6ac7d915563d059a745118ca5e5b424a1f80c860e7c30fb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BlockstorageVolumeAttachV3Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BlockstorageVolumeAttachV3Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BlockstorageVolumeAttachV3Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__633d160d8910b35b94e85787962d07c817f24d0b3373033bb7a46138d23c4c49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BlockstorageVolumeAttachV3",
    "BlockstorageVolumeAttachV3Config",
    "BlockstorageVolumeAttachV3Timeouts",
    "BlockstorageVolumeAttachV3TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__1416730fc0ce85bf49d181a6d66bd7821aa1c134aebe2c05d09d917eeb1f3699(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    host_name: builtins.str,
    volume_id: builtins.str,
    attach_mode: typing.Optional[builtins.str] = None,
    device: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    initiator: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[builtins.str] = None,
    multipath: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    os_type: typing.Optional[builtins.str] = None,
    platform: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BlockstorageVolumeAttachV3Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    wwnn: typing.Optional[builtins.str] = None,
    wwpn: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__4c7ab708ee77e851f5177b0dd89522367cfa43c32faa3c4fcf532294d14c7d9e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39bbd56f39a3dbf91f84c138948319600fa8361a91a61d816ffec2729b2d2bc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23649e15908121ae557f44f1ca7162f1d072caa134eb38c0e17097cb342fc137(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ecd33c1d65aae75b0d2cf09fdba6d466e3a5557e8255ca7f6348377902a506(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26441310c1a16dfef78314a6599db68a0b285bd1bfbfe553103267b901f3b430(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f4c63288339f33640aed029b1191402a0345f9d23972887bcf6a7d81decdf35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5103366617765d9a0528da17314f1f2198ed2eb081fb7044a433a6044264c1a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c03e20edcdda8e713ac75e00e64550a5934a496a383fe58bec3b619abda9a386(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6245699ba17e789df7babb762d1f93fa8b6f03833900edaeedeaa11ad57dbd2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0584a2639c14a66a4fb069a6236c369bd25f904bf2ad598ef8e2133c37626c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03dcb9c15702f9932ba68eaffbe9d84fd06ae81d77508292663ea347016e12d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdcfd3e7441866b16d1df510d6a66ebf59120ab16e47c80a7701d31060203416(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d8b80ed3fff5d9f854089adb64d657463a67393423d588703c8a70a839e8500(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__915b348547cd9964ea68bb81407f2c0c8d57a355c7ae0991144bebe6d0cd0f0a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__957e70654308ec342c434f670186c93833047016d125d5bf6fcc4fb2c9a8b690(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    host_name: builtins.str,
    volume_id: builtins.str,
    attach_mode: typing.Optional[builtins.str] = None,
    device: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    initiator: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[builtins.str] = None,
    multipath: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    os_type: typing.Optional[builtins.str] = None,
    platform: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BlockstorageVolumeAttachV3Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    wwnn: typing.Optional[builtins.str] = None,
    wwpn: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bfa2c6e2136a2c652256981a5b52a2c794b31f6b31ea984f4ab032f3689a2ea(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59179e297a44216d0581439ebd4c210174c156e903dbfe237135cdc1a20cd0e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce2d3eff384e92640e420cf2f8a158d91aa96ea4f757f38d2e5c0f87132810f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b00f0fa452fb20e6ac7d915563d059a745118ca5e5b424a1f80c860e7c30fb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__633d160d8910b35b94e85787962d07c817f24d0b3373033bb7a46138d23c4c49(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BlockstorageVolumeAttachV3Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
