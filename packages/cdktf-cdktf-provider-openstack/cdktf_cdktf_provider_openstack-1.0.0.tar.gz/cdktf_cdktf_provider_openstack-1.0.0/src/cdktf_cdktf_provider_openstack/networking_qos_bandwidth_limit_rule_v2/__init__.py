r'''
# `openstack_networking_qos_bandwidth_limit_rule_v2`

Refer to the Terraform Registry for docs: [`openstack_networking_qos_bandwidth_limit_rule_v2`](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2).
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


class NetworkingQosBandwidthLimitRuleV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.networkingQosBandwidthLimitRuleV2.NetworkingQosBandwidthLimitRuleV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2 openstack_networking_qos_bandwidth_limit_rule_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        max_kbps: jsii.Number,
        qos_policy_id: builtins.str,
        direction: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        max_burst_kbps: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkingQosBandwidthLimitRuleV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2 openstack_networking_qos_bandwidth_limit_rule_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param max_kbps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#max_kbps NetworkingQosBandwidthLimitRuleV2#max_kbps}.
        :param qos_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#qos_policy_id NetworkingQosBandwidthLimitRuleV2#qos_policy_id}.
        :param direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#direction NetworkingQosBandwidthLimitRuleV2#direction}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#id NetworkingQosBandwidthLimitRuleV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_burst_kbps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#max_burst_kbps NetworkingQosBandwidthLimitRuleV2#max_burst_kbps}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#region NetworkingQosBandwidthLimitRuleV2#region}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#timeouts NetworkingQosBandwidthLimitRuleV2#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c7638c775edb264a78d15b8c52c96c01573ee5866ad07639f467937fb4968ef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkingQosBandwidthLimitRuleV2Config(
            max_kbps=max_kbps,
            qos_policy_id=qos_policy_id,
            direction=direction,
            id=id,
            max_burst_kbps=max_burst_kbps,
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
        '''Generates CDKTF code for importing a NetworkingQosBandwidthLimitRuleV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkingQosBandwidthLimitRuleV2 to import.
        :param import_from_id: The id of the existing NetworkingQosBandwidthLimitRuleV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkingQosBandwidthLimitRuleV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56a65628e3d9efb5dd9f5e6783e91a60f34bba4285662828602c89bca35b1309)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#create NetworkingQosBandwidthLimitRuleV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#delete NetworkingQosBandwidthLimitRuleV2#delete}.
        '''
        value = NetworkingQosBandwidthLimitRuleV2Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDirection")
    def reset_direction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirection", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaxBurstKbps")
    def reset_max_burst_kbps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxBurstKbps", []))

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
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetworkingQosBandwidthLimitRuleV2TimeoutsOutputReference":
        return typing.cast("NetworkingQosBandwidthLimitRuleV2TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="directionInput")
    def direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="maxBurstKbpsInput")
    def max_burst_kbps_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxBurstKbpsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxKbpsInput")
    def max_kbps_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxKbpsInput"))

    @builtins.property
    @jsii.member(jsii_name="qosPolicyIdInput")
    def qos_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "qosPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkingQosBandwidthLimitRuleV2Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkingQosBandwidthLimitRuleV2Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "direction"))

    @direction.setter
    def direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c519a75d2aa3fc8fa9e32b5724f66cea41309e8b1cf8f8be287c09bfaa34a02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "direction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb59e026f9f4a84cfb76f91e2d5fc6f764a3801c321f0bfef99777138a96ca21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxBurstKbps")
    def max_burst_kbps(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxBurstKbps"))

    @max_burst_kbps.setter
    def max_burst_kbps(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__787cc1b260ce38fc7f908481157b70cc4bfb202f1b642b343d3eae035e1485bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxBurstKbps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxKbps")
    def max_kbps(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxKbps"))

    @max_kbps.setter
    def max_kbps(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__212c3390c335869a72e5c40e229b5d7b4ecb793351d01d91396a565fd806b3c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxKbps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="qosPolicyId")
    def qos_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "qosPolicyId"))

    @qos_policy_id.setter
    def qos_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ea991809d4a04e20c8638d83f398423b4134da74aadcd4c6eb496efb1b1b665)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qosPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a74f45fbe8d1c7fd67752a766f5cfa794160d78d49b6c70a878803d0fb4595f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.networkingQosBandwidthLimitRuleV2.NetworkingQosBandwidthLimitRuleV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "max_kbps": "maxKbps",
        "qos_policy_id": "qosPolicyId",
        "direction": "direction",
        "id": "id",
        "max_burst_kbps": "maxBurstKbps",
        "region": "region",
        "timeouts": "timeouts",
    },
)
class NetworkingQosBandwidthLimitRuleV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        max_kbps: jsii.Number,
        qos_policy_id: builtins.str,
        direction: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        max_burst_kbps: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkingQosBandwidthLimitRuleV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param max_kbps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#max_kbps NetworkingQosBandwidthLimitRuleV2#max_kbps}.
        :param qos_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#qos_policy_id NetworkingQosBandwidthLimitRuleV2#qos_policy_id}.
        :param direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#direction NetworkingQosBandwidthLimitRuleV2#direction}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#id NetworkingQosBandwidthLimitRuleV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_burst_kbps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#max_burst_kbps NetworkingQosBandwidthLimitRuleV2#max_burst_kbps}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#region NetworkingQosBandwidthLimitRuleV2#region}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#timeouts NetworkingQosBandwidthLimitRuleV2#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = NetworkingQosBandwidthLimitRuleV2Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eef80923e80e748409d32f7be0945156ada29cdc0b50ee46575b3c39ab43de2c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument max_kbps", value=max_kbps, expected_type=type_hints["max_kbps"])
            check_type(argname="argument qos_policy_id", value=qos_policy_id, expected_type=type_hints["qos_policy_id"])
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument max_burst_kbps", value=max_burst_kbps, expected_type=type_hints["max_burst_kbps"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_kbps": max_kbps,
            "qos_policy_id": qos_policy_id,
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
        if direction is not None:
            self._values["direction"] = direction
        if id is not None:
            self._values["id"] = id
        if max_burst_kbps is not None:
            self._values["max_burst_kbps"] = max_burst_kbps
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
    def max_kbps(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#max_kbps NetworkingQosBandwidthLimitRuleV2#max_kbps}.'''
        result = self._values.get("max_kbps")
        assert result is not None, "Required property 'max_kbps' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def qos_policy_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#qos_policy_id NetworkingQosBandwidthLimitRuleV2#qos_policy_id}.'''
        result = self._values.get("qos_policy_id")
        assert result is not None, "Required property 'qos_policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def direction(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#direction NetworkingQosBandwidthLimitRuleV2#direction}.'''
        result = self._values.get("direction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#id NetworkingQosBandwidthLimitRuleV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_burst_kbps(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#max_burst_kbps NetworkingQosBandwidthLimitRuleV2#max_burst_kbps}.'''
        result = self._values.get("max_burst_kbps")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#region NetworkingQosBandwidthLimitRuleV2#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetworkingQosBandwidthLimitRuleV2Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#timeouts NetworkingQosBandwidthLimitRuleV2#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkingQosBandwidthLimitRuleV2Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkingQosBandwidthLimitRuleV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.networkingQosBandwidthLimitRuleV2.NetworkingQosBandwidthLimitRuleV2Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class NetworkingQosBandwidthLimitRuleV2Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#create NetworkingQosBandwidthLimitRuleV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#delete NetworkingQosBandwidthLimitRuleV2#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31825b8c755ff153a2aaef59d9d8ee5be6c665ed233b04f90d5ee3855523d71)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#create NetworkingQosBandwidthLimitRuleV2#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/networking_qos_bandwidth_limit_rule_v2#delete NetworkingQosBandwidthLimitRuleV2#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkingQosBandwidthLimitRuleV2Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkingQosBandwidthLimitRuleV2TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.networkingQosBandwidthLimitRuleV2.NetworkingQosBandwidthLimitRuleV2TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d74c1802015ef5d2d5cb91468b272a7797de4a1f891f91a900b3a5cdd010f70)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53c9e52bcdc10682e05b5a27d326b3af86d3f512092cb84339ac17027f20c20c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fcb467b0d36485dc0ceef8a36f965f560eafb67048b879fe0159145b878a84e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingQosBandwidthLimitRuleV2Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingQosBandwidthLimitRuleV2Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingQosBandwidthLimitRuleV2Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75cef49a2c63055b7fc83a45046bb5c75f4dc9d7af49b8d6d2bbbad3252a7676)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetworkingQosBandwidthLimitRuleV2",
    "NetworkingQosBandwidthLimitRuleV2Config",
    "NetworkingQosBandwidthLimitRuleV2Timeouts",
    "NetworkingQosBandwidthLimitRuleV2TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__5c7638c775edb264a78d15b8c52c96c01573ee5866ad07639f467937fb4968ef(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    max_kbps: jsii.Number,
    qos_policy_id: builtins.str,
    direction: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    max_burst_kbps: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkingQosBandwidthLimitRuleV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__56a65628e3d9efb5dd9f5e6783e91a60f34bba4285662828602c89bca35b1309(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c519a75d2aa3fc8fa9e32b5724f66cea41309e8b1cf8f8be287c09bfaa34a02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb59e026f9f4a84cfb76f91e2d5fc6f764a3801c321f0bfef99777138a96ca21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787cc1b260ce38fc7f908481157b70cc4bfb202f1b642b343d3eae035e1485bc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__212c3390c335869a72e5c40e229b5d7b4ecb793351d01d91396a565fd806b3c1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ea991809d4a04e20c8638d83f398423b4134da74aadcd4c6eb496efb1b1b665(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a74f45fbe8d1c7fd67752a766f5cfa794160d78d49b6c70a878803d0fb4595f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eef80923e80e748409d32f7be0945156ada29cdc0b50ee46575b3c39ab43de2c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_kbps: jsii.Number,
    qos_policy_id: builtins.str,
    direction: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    max_burst_kbps: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkingQosBandwidthLimitRuleV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31825b8c755ff153a2aaef59d9d8ee5be6c665ed233b04f90d5ee3855523d71(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d74c1802015ef5d2d5cb91468b272a7797de4a1f891f91a900b3a5cdd010f70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c9e52bcdc10682e05b5a27d326b3af86d3f512092cb84339ac17027f20c20c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fcb467b0d36485dc0ceef8a36f965f560eafb67048b879fe0159145b878a84e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75cef49a2c63055b7fc83a45046bb5c75f4dc9d7af49b8d6d2bbbad3252a7676(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkingQosBandwidthLimitRuleV2Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
