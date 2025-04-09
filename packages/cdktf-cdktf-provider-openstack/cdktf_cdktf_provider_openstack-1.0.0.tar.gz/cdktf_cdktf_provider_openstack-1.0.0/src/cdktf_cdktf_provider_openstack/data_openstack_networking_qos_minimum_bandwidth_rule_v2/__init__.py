r'''
# `data_openstack_networking_qos_minimum_bandwidth_rule_v2`

Refer to the Terraform Registry for docs: [`data_openstack_networking_qos_minimum_bandwidth_rule_v2`](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_qos_minimum_bandwidth_rule_v2).
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


class DataOpenstackNetworkingQosMinimumBandwidthRuleV2(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.dataOpenstackNetworkingQosMinimumBandwidthRuleV2.DataOpenstackNetworkingQosMinimumBandwidthRuleV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_qos_minimum_bandwidth_rule_v2 openstack_networking_qos_minimum_bandwidth_rule_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        qos_policy_id: builtins.str,
        direction: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        min_kbps: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_qos_minimum_bandwidth_rule_v2 openstack_networking_qos_minimum_bandwidth_rule_v2} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param qos_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_qos_minimum_bandwidth_rule_v2#qos_policy_id DataOpenstackNetworkingQosMinimumBandwidthRuleV2#qos_policy_id}.
        :param direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_qos_minimum_bandwidth_rule_v2#direction DataOpenstackNetworkingQosMinimumBandwidthRuleV2#direction}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_qos_minimum_bandwidth_rule_v2#id DataOpenstackNetworkingQosMinimumBandwidthRuleV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param min_kbps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_qos_minimum_bandwidth_rule_v2#min_kbps DataOpenstackNetworkingQosMinimumBandwidthRuleV2#min_kbps}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_qos_minimum_bandwidth_rule_v2#region DataOpenstackNetworkingQosMinimumBandwidthRuleV2#region}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__380c276c72cd9e83f0d738971dd302b851c29189425a9823f7d2e7aea048ff49)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOpenstackNetworkingQosMinimumBandwidthRuleV2Config(
            qos_policy_id=qos_policy_id,
            direction=direction,
            id=id,
            min_kbps=min_kbps,
            region=region,
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
        '''Generates CDKTF code for importing a DataOpenstackNetworkingQosMinimumBandwidthRuleV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpenstackNetworkingQosMinimumBandwidthRuleV2 to import.
        :param import_from_id: The id of the existing DataOpenstackNetworkingQosMinimumBandwidthRuleV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_qos_minimum_bandwidth_rule_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpenstackNetworkingQosMinimumBandwidthRuleV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__568c4e2356ab830e1ded21b155ded7009925ab5f814ec46fa42c63017bbd6c10)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetDirection")
    def reset_direction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirection", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMinKbps")
    def reset_min_kbps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinKbps", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    @jsii.member(jsii_name="directionInput")
    def direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="minKbpsInput")
    def min_kbps_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minKbpsInput"))

    @builtins.property
    @jsii.member(jsii_name="qosPolicyIdInput")
    def qos_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "qosPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "direction"))

    @direction.setter
    def direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87afd90bdd23050381fce60f4b765ffec3c2f86ba7b301c5a7eeda16a8e9f102)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "direction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b1e54ba05ba56d8eb712c79a441e88bac1498b2c384b9ea278c415ba5fe31c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minKbps")
    def min_kbps(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minKbps"))

    @min_kbps.setter
    def min_kbps(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b64b30e5875037a61c045e8cfaf0fb07f5116ba0f5d311ffeaee0eb6debfdc19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minKbps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="qosPolicyId")
    def qos_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "qosPolicyId"))

    @qos_policy_id.setter
    def qos_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7672a2aaed08a1abb1a77b8e1161ac53ad663a295f823fca3b787243d70e0b6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qosPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__416888a55b154a15139c6c93602d588bee8da87543efb82161fe7ac955d54215)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.dataOpenstackNetworkingQosMinimumBandwidthRuleV2.DataOpenstackNetworkingQosMinimumBandwidthRuleV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "qos_policy_id": "qosPolicyId",
        "direction": "direction",
        "id": "id",
        "min_kbps": "minKbps",
        "region": "region",
    },
)
class DataOpenstackNetworkingQosMinimumBandwidthRuleV2Config(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        qos_policy_id: builtins.str,
        direction: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        min_kbps: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param qos_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_qos_minimum_bandwidth_rule_v2#qos_policy_id DataOpenstackNetworkingQosMinimumBandwidthRuleV2#qos_policy_id}.
        :param direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_qos_minimum_bandwidth_rule_v2#direction DataOpenstackNetworkingQosMinimumBandwidthRuleV2#direction}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_qos_minimum_bandwidth_rule_v2#id DataOpenstackNetworkingQosMinimumBandwidthRuleV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param min_kbps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_qos_minimum_bandwidth_rule_v2#min_kbps DataOpenstackNetworkingQosMinimumBandwidthRuleV2#min_kbps}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_qos_minimum_bandwidth_rule_v2#region DataOpenstackNetworkingQosMinimumBandwidthRuleV2#region}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb922d6ac7147d9baaf60933d80eb1568bb03c1521967308a86715b4f5ebea36)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument qos_policy_id", value=qos_policy_id, expected_type=type_hints["qos_policy_id"])
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument min_kbps", value=min_kbps, expected_type=type_hints["min_kbps"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if min_kbps is not None:
            self._values["min_kbps"] = min_kbps
        if region is not None:
            self._values["region"] = region

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
    def qos_policy_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_qos_minimum_bandwidth_rule_v2#qos_policy_id DataOpenstackNetworkingQosMinimumBandwidthRuleV2#qos_policy_id}.'''
        result = self._values.get("qos_policy_id")
        assert result is not None, "Required property 'qos_policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def direction(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_qos_minimum_bandwidth_rule_v2#direction DataOpenstackNetworkingQosMinimumBandwidthRuleV2#direction}.'''
        result = self._values.get("direction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_qos_minimum_bandwidth_rule_v2#id DataOpenstackNetworkingQosMinimumBandwidthRuleV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_kbps(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_qos_minimum_bandwidth_rule_v2#min_kbps DataOpenstackNetworkingQosMinimumBandwidthRuleV2#min_kbps}.'''
        result = self._values.get("min_kbps")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/data-sources/networking_qos_minimum_bandwidth_rule_v2#region DataOpenstackNetworkingQosMinimumBandwidthRuleV2#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpenstackNetworkingQosMinimumBandwidthRuleV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataOpenstackNetworkingQosMinimumBandwidthRuleV2",
    "DataOpenstackNetworkingQosMinimumBandwidthRuleV2Config",
]

publication.publish()

def _typecheckingstub__380c276c72cd9e83f0d738971dd302b851c29189425a9823f7d2e7aea048ff49(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    qos_policy_id: builtins.str,
    direction: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    min_kbps: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__568c4e2356ab830e1ded21b155ded7009925ab5f814ec46fa42c63017bbd6c10(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87afd90bdd23050381fce60f4b765ffec3c2f86ba7b301c5a7eeda16a8e9f102(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b1e54ba05ba56d8eb712c79a441e88bac1498b2c384b9ea278c415ba5fe31c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b64b30e5875037a61c045e8cfaf0fb07f5116ba0f5d311ffeaee0eb6debfdc19(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7672a2aaed08a1abb1a77b8e1161ac53ad663a295f823fca3b787243d70e0b6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__416888a55b154a15139c6c93602d588bee8da87543efb82161fe7ac955d54215(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb922d6ac7147d9baaf60933d80eb1568bb03c1521967308a86715b4f5ebea36(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    qos_policy_id: builtins.str,
    direction: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    min_kbps: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
