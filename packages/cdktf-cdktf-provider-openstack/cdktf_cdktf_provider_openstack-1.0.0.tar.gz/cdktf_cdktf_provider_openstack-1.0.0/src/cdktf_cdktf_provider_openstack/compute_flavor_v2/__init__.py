r'''
# `openstack_compute_flavor_v2`

Refer to the Terraform Registry for docs: [`openstack_compute_flavor_v2`](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2).
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


class ComputeFlavorV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.computeFlavorV2.ComputeFlavorV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2 openstack_compute_flavor_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        disk: jsii.Number,
        name: builtins.str,
        ram: jsii.Number,
        vcpus: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        ephemeral: typing.Optional[jsii.Number] = None,
        extra_specs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        flavor_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_public: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        rx_tx_factor: typing.Optional[jsii.Number] = None,
        swap: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2 openstack_compute_flavor_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#disk ComputeFlavorV2#disk}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#name ComputeFlavorV2#name}.
        :param ram: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#ram ComputeFlavorV2#ram}.
        :param vcpus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#vcpus ComputeFlavorV2#vcpus}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#description ComputeFlavorV2#description}.
        :param ephemeral: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#ephemeral ComputeFlavorV2#ephemeral}.
        :param extra_specs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#extra_specs ComputeFlavorV2#extra_specs}.
        :param flavor_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#flavor_id ComputeFlavorV2#flavor_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#id ComputeFlavorV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_public: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#is_public ComputeFlavorV2#is_public}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#region ComputeFlavorV2#region}.
        :param rx_tx_factor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#rx_tx_factor ComputeFlavorV2#rx_tx_factor}.
        :param swap: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#swap ComputeFlavorV2#swap}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9921de49d16d0025ac86da5fc49d4eb6a2fe7111c4a8c19fd153ef9b072af760)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeFlavorV2Config(
            disk=disk,
            name=name,
            ram=ram,
            vcpus=vcpus,
            description=description,
            ephemeral=ephemeral,
            extra_specs=extra_specs,
            flavor_id=flavor_id,
            id=id,
            is_public=is_public,
            region=region,
            rx_tx_factor=rx_tx_factor,
            swap=swap,
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
        '''Generates CDKTF code for importing a ComputeFlavorV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeFlavorV2 to import.
        :param import_from_id: The id of the existing ComputeFlavorV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeFlavorV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__628f3d3c931b13dc46a78941fed1dfeaac941ef16b087c53fdc40ccf7f918b96)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEphemeral")
    def reset_ephemeral(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEphemeral", []))

    @jsii.member(jsii_name="resetExtraSpecs")
    def reset_extra_specs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtraSpecs", []))

    @jsii.member(jsii_name="resetFlavorId")
    def reset_flavor_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlavorId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsPublic")
    def reset_is_public(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsPublic", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRxTxFactor")
    def reset_rx_tx_factor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRxTxFactor", []))

    @jsii.member(jsii_name="resetSwap")
    def reset_swap(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSwap", []))

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
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="diskInput")
    def disk_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskInput"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralInput")
    def ephemeral_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ephemeralInput"))

    @builtins.property
    @jsii.member(jsii_name="extraSpecsInput")
    def extra_specs_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "extraSpecsInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorIdInput")
    def flavor_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isPublicInput")
    def is_public_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isPublicInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="ramInput")
    def ram_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ramInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="rxTxFactorInput")
    def rx_tx_factor_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rxTxFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="swapInput")
    def swap_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "swapInput"))

    @builtins.property
    @jsii.member(jsii_name="vcpusInput")
    def vcpus_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vcpusInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac9eb2538c43f1cfbf4878d2667f88de0d37400a6722cade92789ca0d464bcd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disk")
    def disk(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "disk"))

    @disk.setter
    def disk(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dd2e54089a74e0c8fd076ec91b9edbc384b60f40619165aa28b8b28024191eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ephemeral")
    def ephemeral(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ephemeral"))

    @ephemeral.setter
    def ephemeral(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c13b6e2002929cb2a744c6aa533c0e139cee39622901c9990183f97b8824ada7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ephemeral", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extraSpecs")
    def extra_specs(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "extraSpecs"))

    @extra_specs.setter
    def extra_specs(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89abd1a633a10119669b3456513dbd92881fb88f428fe7101eb8a1f3e4528987)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extraSpecs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flavorId")
    def flavor_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavorId"))

    @flavor_id.setter
    def flavor_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85eadb9183aaa04d39c5fb38db608dd5fefb381efbebcc41217a7f7fd5fd56a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavorId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9109b662c6f10931b30807b5b288fcf0ad09301864bfad667a4e482d323e8653)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isPublic")
    def is_public(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isPublic"))

    @is_public.setter
    def is_public(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0d73b8275bdf3780363fdb57c6c79e20ca7e7879296e68aec40ceafbf2a4a09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isPublic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00c9ccaa7501b8aa348726c6957953de946df5ad55d7d377e4f1055a650a6d66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ram")
    def ram(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ram"))

    @ram.setter
    def ram(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86633b41e80f0e06ea4633beccf52f1a9d27b1e75005e16069db4a0ac2f45b38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ram", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52bc6962de36b9364a08a23a668fa2a526b88deafeb53254ef357aec8291b63c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rxTxFactor")
    def rx_tx_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rxTxFactor"))

    @rx_tx_factor.setter
    def rx_tx_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1065c26ed592eaacd14a295f43172fef146a3304ed7e18835e52adbb08f7996d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rxTxFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="swap")
    def swap(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "swap"))

    @swap.setter
    def swap(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b73c2b000df6cdd342eddf59d00837ff497e834324f400617d60ebc2979268ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "swap", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vcpus")
    def vcpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vcpus"))

    @vcpus.setter
    def vcpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28c2bcfa6c8ce4e4dbe31f6fdef79d9fad44b0302dddbb746f934f69e7faf142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vcpus", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.computeFlavorV2.ComputeFlavorV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "disk": "disk",
        "name": "name",
        "ram": "ram",
        "vcpus": "vcpus",
        "description": "description",
        "ephemeral": "ephemeral",
        "extra_specs": "extraSpecs",
        "flavor_id": "flavorId",
        "id": "id",
        "is_public": "isPublic",
        "region": "region",
        "rx_tx_factor": "rxTxFactor",
        "swap": "swap",
    },
)
class ComputeFlavorV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        disk: jsii.Number,
        name: builtins.str,
        ram: jsii.Number,
        vcpus: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        ephemeral: typing.Optional[jsii.Number] = None,
        extra_specs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        flavor_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_public: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        rx_tx_factor: typing.Optional[jsii.Number] = None,
        swap: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#disk ComputeFlavorV2#disk}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#name ComputeFlavorV2#name}.
        :param ram: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#ram ComputeFlavorV2#ram}.
        :param vcpus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#vcpus ComputeFlavorV2#vcpus}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#description ComputeFlavorV2#description}.
        :param ephemeral: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#ephemeral ComputeFlavorV2#ephemeral}.
        :param extra_specs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#extra_specs ComputeFlavorV2#extra_specs}.
        :param flavor_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#flavor_id ComputeFlavorV2#flavor_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#id ComputeFlavorV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_public: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#is_public ComputeFlavorV2#is_public}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#region ComputeFlavorV2#region}.
        :param rx_tx_factor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#rx_tx_factor ComputeFlavorV2#rx_tx_factor}.
        :param swap: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#swap ComputeFlavorV2#swap}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e81da45da226efc7484a87d099ebd343ca4be915ac31b38ac2776d5e6c66566f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument disk", value=disk, expected_type=type_hints["disk"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ram", value=ram, expected_type=type_hints["ram"])
            check_type(argname="argument vcpus", value=vcpus, expected_type=type_hints["vcpus"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument ephemeral", value=ephemeral, expected_type=type_hints["ephemeral"])
            check_type(argname="argument extra_specs", value=extra_specs, expected_type=type_hints["extra_specs"])
            check_type(argname="argument flavor_id", value=flavor_id, expected_type=type_hints["flavor_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_public", value=is_public, expected_type=type_hints["is_public"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument rx_tx_factor", value=rx_tx_factor, expected_type=type_hints["rx_tx_factor"])
            check_type(argname="argument swap", value=swap, expected_type=type_hints["swap"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disk": disk,
            "name": name,
            "ram": ram,
            "vcpus": vcpus,
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
        if description is not None:
            self._values["description"] = description
        if ephemeral is not None:
            self._values["ephemeral"] = ephemeral
        if extra_specs is not None:
            self._values["extra_specs"] = extra_specs
        if flavor_id is not None:
            self._values["flavor_id"] = flavor_id
        if id is not None:
            self._values["id"] = id
        if is_public is not None:
            self._values["is_public"] = is_public
        if region is not None:
            self._values["region"] = region
        if rx_tx_factor is not None:
            self._values["rx_tx_factor"] = rx_tx_factor
        if swap is not None:
            self._values["swap"] = swap

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
    def disk(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#disk ComputeFlavorV2#disk}.'''
        result = self._values.get("disk")
        assert result is not None, "Required property 'disk' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#name ComputeFlavorV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ram(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#ram ComputeFlavorV2#ram}.'''
        result = self._values.get("ram")
        assert result is not None, "Required property 'ram' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def vcpus(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#vcpus ComputeFlavorV2#vcpus}.'''
        result = self._values.get("vcpus")
        assert result is not None, "Required property 'vcpus' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#description ComputeFlavorV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ephemeral(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#ephemeral ComputeFlavorV2#ephemeral}.'''
        result = self._values.get("ephemeral")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def extra_specs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#extra_specs ComputeFlavorV2#extra_specs}.'''
        result = self._values.get("extra_specs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def flavor_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#flavor_id ComputeFlavorV2#flavor_id}.'''
        result = self._values.get("flavor_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#id ComputeFlavorV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_public(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#is_public ComputeFlavorV2#is_public}.'''
        result = self._values.get("is_public")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#region ComputeFlavorV2#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rx_tx_factor(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#rx_tx_factor ComputeFlavorV2#rx_tx_factor}.'''
        result = self._values.get("rx_tx_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def swap(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_flavor_v2#swap ComputeFlavorV2#swap}.'''
        result = self._values.get("swap")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeFlavorV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ComputeFlavorV2",
    "ComputeFlavorV2Config",
]

publication.publish()

def _typecheckingstub__9921de49d16d0025ac86da5fc49d4eb6a2fe7111c4a8c19fd153ef9b072af760(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    disk: jsii.Number,
    name: builtins.str,
    ram: jsii.Number,
    vcpus: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    ephemeral: typing.Optional[jsii.Number] = None,
    extra_specs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    flavor_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_public: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    rx_tx_factor: typing.Optional[jsii.Number] = None,
    swap: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__628f3d3c931b13dc46a78941fed1dfeaac941ef16b087c53fdc40ccf7f918b96(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac9eb2538c43f1cfbf4878d2667f88de0d37400a6722cade92789ca0d464bcd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd2e54089a74e0c8fd076ec91b9edbc384b60f40619165aa28b8b28024191eb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13b6e2002929cb2a744c6aa533c0e139cee39622901c9990183f97b8824ada7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89abd1a633a10119669b3456513dbd92881fb88f428fe7101eb8a1f3e4528987(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85eadb9183aaa04d39c5fb38db608dd5fefb381efbebcc41217a7f7fd5fd56a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9109b662c6f10931b30807b5b288fcf0ad09301864bfad667a4e482d323e8653(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d73b8275bdf3780363fdb57c6c79e20ca7e7879296e68aec40ceafbf2a4a09(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c9ccaa7501b8aa348726c6957953de946df5ad55d7d377e4f1055a650a6d66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86633b41e80f0e06ea4633beccf52f1a9d27b1e75005e16069db4a0ac2f45b38(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52bc6962de36b9364a08a23a668fa2a526b88deafeb53254ef357aec8291b63c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1065c26ed592eaacd14a295f43172fef146a3304ed7e18835e52adbb08f7996d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b73c2b000df6cdd342eddf59d00837ff497e834324f400617d60ebc2979268ff(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c2bcfa6c8ce4e4dbe31f6fdef79d9fad44b0302dddbb746f934f69e7faf142(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e81da45da226efc7484a87d099ebd343ca4be915ac31b38ac2776d5e6c66566f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    disk: jsii.Number,
    name: builtins.str,
    ram: jsii.Number,
    vcpus: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    ephemeral: typing.Optional[jsii.Number] = None,
    extra_specs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    flavor_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_public: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    rx_tx_factor: typing.Optional[jsii.Number] = None,
    swap: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
