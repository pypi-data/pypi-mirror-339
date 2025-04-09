r'''
# `openstack_compute_instance_v2`

Refer to the Terraform Registry for docs: [`openstack_compute_instance_v2`](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2).
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


class ComputeInstanceV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.computeInstanceV2.ComputeInstanceV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2 openstack_compute_instance_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        access_ip_v4: typing.Optional[builtins.str] = None,
        access_ip_v6: typing.Optional[builtins.str] = None,
        admin_pass: typing.Optional[builtins.str] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        availability_zone_hints: typing.Optional[builtins.str] = None,
        block_device: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceV2BlockDevice", typing.Dict[builtins.str, typing.Any]]]]] = None,
        config_drive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        flavor_id: typing.Optional[builtins.str] = None,
        flavor_name: typing.Optional[builtins.str] = None,
        force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        image_id: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        key_pair: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceV2Network", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network_mode: typing.Optional[builtins.str] = None,
        personality: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceV2Personality", typing.Dict[builtins.str, typing.Any]]]]] = None,
        power_state: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        scheduler_hints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceV2SchedulerHints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        stop_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeInstanceV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_data: typing.Optional[builtins.str] = None,
        vendor_options: typing.Optional[typing.Union["ComputeInstanceV2VendorOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2 openstack_compute_instance_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#name ComputeInstanceV2#name}.
        :param access_ip_v4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#access_ip_v4 ComputeInstanceV2#access_ip_v4}.
        :param access_ip_v6: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#access_ip_v6 ComputeInstanceV2#access_ip_v6}.
        :param admin_pass: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#admin_pass ComputeInstanceV2#admin_pass}.
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#availability_zone ComputeInstanceV2#availability_zone}.
        :param availability_zone_hints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#availability_zone_hints ComputeInstanceV2#availability_zone_hints}.
        :param block_device: block_device block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#block_device ComputeInstanceV2#block_device}
        :param config_drive: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#config_drive ComputeInstanceV2#config_drive}.
        :param flavor_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#flavor_id ComputeInstanceV2#flavor_id}.
        :param flavor_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#flavor_name ComputeInstanceV2#flavor_name}.
        :param force_delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#force_delete ComputeInstanceV2#force_delete}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#id ComputeInstanceV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#image_id ComputeInstanceV2#image_id}.
        :param image_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#image_name ComputeInstanceV2#image_name}.
        :param key_pair: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#key_pair ComputeInstanceV2#key_pair}.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#metadata ComputeInstanceV2#metadata}.
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#network ComputeInstanceV2#network}
        :param network_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#network_mode ComputeInstanceV2#network_mode}.
        :param personality: personality block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#personality ComputeInstanceV2#personality}
        :param power_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#power_state ComputeInstanceV2#power_state}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#region ComputeInstanceV2#region}.
        :param scheduler_hints: scheduler_hints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#scheduler_hints ComputeInstanceV2#scheduler_hints}
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#security_groups ComputeInstanceV2#security_groups}.
        :param stop_before_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#stop_before_destroy ComputeInstanceV2#stop_before_destroy}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#tags ComputeInstanceV2#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#timeouts ComputeInstanceV2#timeouts}
        :param user_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#user_data ComputeInstanceV2#user_data}.
        :param vendor_options: vendor_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#vendor_options ComputeInstanceV2#vendor_options}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33ceeaee9ef417ea4eb8d40e7c00e600e821ba14e8817d7a0b61ea2504f0e029)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeInstanceV2Config(
            name=name,
            access_ip_v4=access_ip_v4,
            access_ip_v6=access_ip_v6,
            admin_pass=admin_pass,
            availability_zone=availability_zone,
            availability_zone_hints=availability_zone_hints,
            block_device=block_device,
            config_drive=config_drive,
            flavor_id=flavor_id,
            flavor_name=flavor_name,
            force_delete=force_delete,
            id=id,
            image_id=image_id,
            image_name=image_name,
            key_pair=key_pair,
            metadata=metadata,
            network=network,
            network_mode=network_mode,
            personality=personality,
            power_state=power_state,
            region=region,
            scheduler_hints=scheduler_hints,
            security_groups=security_groups,
            stop_before_destroy=stop_before_destroy,
            tags=tags,
            timeouts=timeouts,
            user_data=user_data,
            vendor_options=vendor_options,
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
        '''Generates CDKTF code for importing a ComputeInstanceV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeInstanceV2 to import.
        :param import_from_id: The id of the existing ComputeInstanceV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeInstanceV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97970c806bb731f68a80770d7088d89c2258528dba2c12148fe881221a2e96dc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBlockDevice")
    def put_block_device(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceV2BlockDevice", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b374d1f7689451a966210b4e8851c75acc8357e8d476ef097f1ce28b88aea65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBlockDevice", [value]))

    @jsii.member(jsii_name="putNetwork")
    def put_network(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceV2Network", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a49658fbc4f8ce205fdff8a7205f6dbac40492f084d715ee994ee74278be47c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetwork", [value]))

    @jsii.member(jsii_name="putPersonality")
    def put_personality(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceV2Personality", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82b76e489135f6c266745c9c15c9b94eadaa9b79a4273128da1d66ffcbaeb90b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPersonality", [value]))

    @jsii.member(jsii_name="putSchedulerHints")
    def put_scheduler_hints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceV2SchedulerHints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc284645b75def46d323be21aced349a4f096181bec881000a7a4c76cc5547af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchedulerHints", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#create ComputeInstanceV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#delete ComputeInstanceV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#update ComputeInstanceV2#update}.
        '''
        value = ComputeInstanceV2Timeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVendorOptions")
    def put_vendor_options(
        self,
        *,
        detach_ports_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ignore_resize_confirmation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param detach_ports_before_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#detach_ports_before_destroy ComputeInstanceV2#detach_ports_before_destroy}.
        :param ignore_resize_confirmation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#ignore_resize_confirmation ComputeInstanceV2#ignore_resize_confirmation}.
        '''
        value = ComputeInstanceV2VendorOptions(
            detach_ports_before_destroy=detach_ports_before_destroy,
            ignore_resize_confirmation=ignore_resize_confirmation,
        )

        return typing.cast(None, jsii.invoke(self, "putVendorOptions", [value]))

    @jsii.member(jsii_name="resetAccessIpV4")
    def reset_access_ip_v4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessIpV4", []))

    @jsii.member(jsii_name="resetAccessIpV6")
    def reset_access_ip_v6(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessIpV6", []))

    @jsii.member(jsii_name="resetAdminPass")
    def reset_admin_pass(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminPass", []))

    @jsii.member(jsii_name="resetAvailabilityZone")
    def reset_availability_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityZone", []))

    @jsii.member(jsii_name="resetAvailabilityZoneHints")
    def reset_availability_zone_hints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityZoneHints", []))

    @jsii.member(jsii_name="resetBlockDevice")
    def reset_block_device(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockDevice", []))

    @jsii.member(jsii_name="resetConfigDrive")
    def reset_config_drive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigDrive", []))

    @jsii.member(jsii_name="resetFlavorId")
    def reset_flavor_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlavorId", []))

    @jsii.member(jsii_name="resetFlavorName")
    def reset_flavor_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlavorName", []))

    @jsii.member(jsii_name="resetForceDelete")
    def reset_force_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceDelete", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImageId")
    def reset_image_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageId", []))

    @jsii.member(jsii_name="resetImageName")
    def reset_image_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageName", []))

    @jsii.member(jsii_name="resetKeyPair")
    def reset_key_pair(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyPair", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetNetworkMode")
    def reset_network_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkMode", []))

    @jsii.member(jsii_name="resetPersonality")
    def reset_personality(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPersonality", []))

    @jsii.member(jsii_name="resetPowerState")
    def reset_power_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPowerState", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSchedulerHints")
    def reset_scheduler_hints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedulerHints", []))

    @jsii.member(jsii_name="resetSecurityGroups")
    def reset_security_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroups", []))

    @jsii.member(jsii_name="resetStopBeforeDestroy")
    def reset_stop_before_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStopBeforeDestroy", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUserData")
    def reset_user_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserData", []))

    @jsii.member(jsii_name="resetVendorOptions")
    def reset_vendor_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVendorOptions", []))

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
    @jsii.member(jsii_name="allMetadata")
    def all_metadata(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "allMetadata"))

    @builtins.property
    @jsii.member(jsii_name="allTags")
    def all_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allTags"))

    @builtins.property
    @jsii.member(jsii_name="blockDevice")
    def block_device(self) -> "ComputeInstanceV2BlockDeviceList":
        return typing.cast("ComputeInstanceV2BlockDeviceList", jsii.get(self, "blockDevice"))

    @builtins.property
    @jsii.member(jsii_name="created")
    def created(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "created"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> "ComputeInstanceV2NetworkList":
        return typing.cast("ComputeInstanceV2NetworkList", jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="personality")
    def personality(self) -> "ComputeInstanceV2PersonalityList":
        return typing.cast("ComputeInstanceV2PersonalityList", jsii.get(self, "personality"))

    @builtins.property
    @jsii.member(jsii_name="schedulerHints")
    def scheduler_hints(self) -> "ComputeInstanceV2SchedulerHintsList":
        return typing.cast("ComputeInstanceV2SchedulerHintsList", jsii.get(self, "schedulerHints"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeInstanceV2TimeoutsOutputReference":
        return typing.cast("ComputeInstanceV2TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updated")
    def updated(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updated"))

    @builtins.property
    @jsii.member(jsii_name="vendorOptions")
    def vendor_options(self) -> "ComputeInstanceV2VendorOptionsOutputReference":
        return typing.cast("ComputeInstanceV2VendorOptionsOutputReference", jsii.get(self, "vendorOptions"))

    @builtins.property
    @jsii.member(jsii_name="accessIpV4Input")
    def access_ip_v4_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessIpV4Input"))

    @builtins.property
    @jsii.member(jsii_name="accessIpV6Input")
    def access_ip_v6_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessIpV6Input"))

    @builtins.property
    @jsii.member(jsii_name="adminPassInput")
    def admin_pass_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminPassInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneHintsInput")
    def availability_zone_hints_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneHintsInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneInput")
    def availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="blockDeviceInput")
    def block_device_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2BlockDevice"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2BlockDevice"]]], jsii.get(self, "blockDeviceInput"))

    @builtins.property
    @jsii.member(jsii_name="configDriveInput")
    def config_drive_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "configDriveInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorIdInput")
    def flavor_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorNameInput")
    def flavor_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorNameInput"))

    @builtins.property
    @jsii.member(jsii_name="forceDeleteInput")
    def force_delete_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageIdInput")
    def image_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageIdInput"))

    @builtins.property
    @jsii.member(jsii_name="imageNameInput")
    def image_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyPairInput")
    def key_pair_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyPairInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2Network"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2Network"]]], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="networkModeInput")
    def network_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkModeInput"))

    @builtins.property
    @jsii.member(jsii_name="personalityInput")
    def personality_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2Personality"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2Personality"]]], jsii.get(self, "personalityInput"))

    @builtins.property
    @jsii.member(jsii_name="powerStateInput")
    def power_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "powerStateInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulerHintsInput")
    def scheduler_hints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2SchedulerHints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2SchedulerHints"]]], jsii.get(self, "schedulerHintsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsInput")
    def security_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="stopBeforeDestroyInput")
    def stop_before_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "stopBeforeDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeInstanceV2Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeInstanceV2Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userDataInput")
    def user_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userDataInput"))

    @builtins.property
    @jsii.member(jsii_name="vendorOptionsInput")
    def vendor_options_input(self) -> typing.Optional["ComputeInstanceV2VendorOptions"]:
        return typing.cast(typing.Optional["ComputeInstanceV2VendorOptions"], jsii.get(self, "vendorOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="accessIpV4")
    def access_ip_v4(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessIpV4"))

    @access_ip_v4.setter
    def access_ip_v4(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc89392c4699e668b2c5ef7a36b93a315f1fcc9cbe143918e5742eb7c59cf7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessIpV4", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accessIpV6")
    def access_ip_v6(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessIpV6"))

    @access_ip_v6.setter
    def access_ip_v6(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f68aaf094d69b1998d0a2621a6a6c4eb28209b7aff55161df99df027bc4a97b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessIpV6", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="adminPass")
    def admin_pass(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminPass"))

    @admin_pass.setter
    def admin_pass(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14c9f10c502b78e2d9fe0e5c444d47a9e7bee023151b75066620363ea1a031da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminPass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb20502aa95a09d36b1726e276560a75a0789c76a4f5135274f73ee190d7aeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneHints")
    def availability_zone_hints(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZoneHints"))

    @availability_zone_hints.setter
    def availability_zone_hints(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bb0aa58664eab75dddec0ef4cbaf8a7fa4cea83805b04e723cfcf196e5daff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZoneHints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="configDrive")
    def config_drive(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "configDrive"))

    @config_drive.setter
    def config_drive(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45edc6b6785692d60d18c98a78445ea59892b48aa8f2ceb35a34b4b87c17e1e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configDrive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flavorId")
    def flavor_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavorId"))

    @flavor_id.setter
    def flavor_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdebca954fc5e56777e0ba43b1624a1ef96ede71577f4d1dd94284e8c1ce1f6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavorId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flavorName")
    def flavor_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavorName"))

    @flavor_name.setter
    def flavor_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a7ac0836d80a7b182ec6c822cb4586fcc8c433b6e557ae786ff2cdabe6a4874)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavorName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceDelete")
    def force_delete(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceDelete"))

    @force_delete.setter
    def force_delete(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a321e1b5fb02ec8bae1ef20252b36625bc73efdeca09b585a051e90db8f2406d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cdb45546b3dc61afe614c4d60df4edaa3a7a7e6cf44a63eab02dcc5ca95ce91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageId"))

    @image_id.setter
    def image_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfb679b995620846b49df94e8a800f53ac50b897d0bc0e654fd3435048f32f5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6f1679bff59109fe390df9b4f7380b73a1cfede57124db5005a85a3f961ecde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyPair")
    def key_pair(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyPair"))

    @key_pair.setter
    def key_pair(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16af4f6aa8caab60c7f0bd123e3057a41fdea38b633f6a28de08dd6e41d2a6c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyPair", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db79207baf6a984a11bb68113d24fd056c28cce7e7f475498eaeff9042421258)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3cdebb8b769f3fa7a983440b92f23b65a71f5191986c825202d6811fd33930c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkMode")
    def network_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkMode"))

    @network_mode.setter
    def network_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57d179bed10a53962995fab1bfec496261e9d12cf35c1f73064cc6cb2f4bf3bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="powerState")
    def power_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "powerState"))

    @power_state.setter
    def power_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29d7714a28591046058ab330c3dc98234b7045c34f9a990ad5eeb7a855a75dc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "powerState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a90abcdd072a4985d9b690f28e87b4d424ade14d8b2bc5852d23a577438c9ed9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e8436c1391ad45258faebcb31510242fb746e85a5e09ae248c297aa532f3793)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stopBeforeDestroy")
    def stop_before_destroy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "stopBeforeDestroy"))

    @stop_before_destroy.setter
    def stop_before_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__539d36fd1732ca904460fcbf8f072398d930f1ed654aff2a9d1517add91479fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stopBeforeDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__130d4093d35e2a1e3d1f2b182d3f12b0e3238b973e464f47316f8607a47f047b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userData")
    def user_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userData"))

    @user_data.setter
    def user_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25ac877cb37d79a19749ad83d5ee320a28c46abb82ad5701c0826ffccb3d453)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userData", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.computeInstanceV2.ComputeInstanceV2BlockDevice",
    jsii_struct_bases=[],
    name_mapping={
        "source_type": "sourceType",
        "boot_index": "bootIndex",
        "delete_on_termination": "deleteOnTermination",
        "destination_type": "destinationType",
        "device_type": "deviceType",
        "disk_bus": "diskBus",
        "guest_format": "guestFormat",
        "multiattach": "multiattach",
        "uuid": "uuid",
        "volume_size": "volumeSize",
        "volume_type": "volumeType",
    },
)
class ComputeInstanceV2BlockDevice:
    def __init__(
        self,
        *,
        source_type: builtins.str,
        boot_index: typing.Optional[jsii.Number] = None,
        delete_on_termination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        destination_type: typing.Optional[builtins.str] = None,
        device_type: typing.Optional[builtins.str] = None,
        disk_bus: typing.Optional[builtins.str] = None,
        guest_format: typing.Optional[builtins.str] = None,
        multiattach: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        uuid: typing.Optional[builtins.str] = None,
        volume_size: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#source_type ComputeInstanceV2#source_type}.
        :param boot_index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#boot_index ComputeInstanceV2#boot_index}.
        :param delete_on_termination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#delete_on_termination ComputeInstanceV2#delete_on_termination}.
        :param destination_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#destination_type ComputeInstanceV2#destination_type}.
        :param device_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#device_type ComputeInstanceV2#device_type}.
        :param disk_bus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#disk_bus ComputeInstanceV2#disk_bus}.
        :param guest_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#guest_format ComputeInstanceV2#guest_format}.
        :param multiattach: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#multiattach ComputeInstanceV2#multiattach}.
        :param uuid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#uuid ComputeInstanceV2#uuid}.
        :param volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#volume_size ComputeInstanceV2#volume_size}.
        :param volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#volume_type ComputeInstanceV2#volume_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c9918966b50342e763a197f8bdc88ad845e0cac4943969a174e36a139c78c8f)
            check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
            check_type(argname="argument boot_index", value=boot_index, expected_type=type_hints["boot_index"])
            check_type(argname="argument delete_on_termination", value=delete_on_termination, expected_type=type_hints["delete_on_termination"])
            check_type(argname="argument destination_type", value=destination_type, expected_type=type_hints["destination_type"])
            check_type(argname="argument device_type", value=device_type, expected_type=type_hints["device_type"])
            check_type(argname="argument disk_bus", value=disk_bus, expected_type=type_hints["disk_bus"])
            check_type(argname="argument guest_format", value=guest_format, expected_type=type_hints["guest_format"])
            check_type(argname="argument multiattach", value=multiattach, expected_type=type_hints["multiattach"])
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
            check_type(argname="argument volume_size", value=volume_size, expected_type=type_hints["volume_size"])
            check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_type": source_type,
        }
        if boot_index is not None:
            self._values["boot_index"] = boot_index
        if delete_on_termination is not None:
            self._values["delete_on_termination"] = delete_on_termination
        if destination_type is not None:
            self._values["destination_type"] = destination_type
        if device_type is not None:
            self._values["device_type"] = device_type
        if disk_bus is not None:
            self._values["disk_bus"] = disk_bus
        if guest_format is not None:
            self._values["guest_format"] = guest_format
        if multiattach is not None:
            self._values["multiattach"] = multiattach
        if uuid is not None:
            self._values["uuid"] = uuid
        if volume_size is not None:
            self._values["volume_size"] = volume_size
        if volume_type is not None:
            self._values["volume_type"] = volume_type

    @builtins.property
    def source_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#source_type ComputeInstanceV2#source_type}.'''
        result = self._values.get("source_type")
        assert result is not None, "Required property 'source_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def boot_index(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#boot_index ComputeInstanceV2#boot_index}.'''
        result = self._values.get("boot_index")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def delete_on_termination(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#delete_on_termination ComputeInstanceV2#delete_on_termination}.'''
        result = self._values.get("delete_on_termination")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def destination_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#destination_type ComputeInstanceV2#destination_type}.'''
        result = self._values.get("destination_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#device_type ComputeInstanceV2#device_type}.'''
        result = self._values.get("device_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_bus(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#disk_bus ComputeInstanceV2#disk_bus}.'''
        result = self._values.get("disk_bus")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def guest_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#guest_format ComputeInstanceV2#guest_format}.'''
        result = self._values.get("guest_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multiattach(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#multiattach ComputeInstanceV2#multiattach}.'''
        result = self._values.get("multiattach")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def uuid(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#uuid ComputeInstanceV2#uuid}.'''
        result = self._values.get("uuid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volume_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#volume_size ComputeInstanceV2#volume_size}.'''
        result = self._values.get("volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#volume_type ComputeInstanceV2#volume_type}.'''
        result = self._values.get("volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceV2BlockDevice(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceV2BlockDeviceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.computeInstanceV2.ComputeInstanceV2BlockDeviceList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0241998806057f6d5807eafb60ea248f2952431a49db05c3194a3b2a72adc696)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeInstanceV2BlockDeviceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f351e517e4750b1e77d57ada00ba0426039df409266fb1b9682324156aefbfe6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceV2BlockDeviceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__638b179d592589d80b94553a9b92a5a826ad0d257a459ff8bdbe6442a30d81d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23c8d5d0188c0107fc874427f76493c9cc8254f2a63502ddf3ae5666496e40be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab84fb086cf606fd8b6035677879ea57c500bd4ccc3c190d8c09cea9b26ffc53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2BlockDevice]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2BlockDevice]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2BlockDevice]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad77400e15bc9c0c0fe4a4e7cfe3f150ac3f2beb90aa271eb309a885df1e7506)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceV2BlockDeviceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.computeInstanceV2.ComputeInstanceV2BlockDeviceOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e068caa78e10ff734e735a5e0ecefa9c7076997f3441f553e12f26a2d2e81e7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBootIndex")
    def reset_boot_index(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootIndex", []))

    @jsii.member(jsii_name="resetDeleteOnTermination")
    def reset_delete_on_termination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteOnTermination", []))

    @jsii.member(jsii_name="resetDestinationType")
    def reset_destination_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationType", []))

    @jsii.member(jsii_name="resetDeviceType")
    def reset_device_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceType", []))

    @jsii.member(jsii_name="resetDiskBus")
    def reset_disk_bus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskBus", []))

    @jsii.member(jsii_name="resetGuestFormat")
    def reset_guest_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuestFormat", []))

    @jsii.member(jsii_name="resetMultiattach")
    def reset_multiattach(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiattach", []))

    @jsii.member(jsii_name="resetUuid")
    def reset_uuid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUuid", []))

    @jsii.member(jsii_name="resetVolumeSize")
    def reset_volume_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeSize", []))

    @jsii.member(jsii_name="resetVolumeType")
    def reset_volume_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeType", []))

    @builtins.property
    @jsii.member(jsii_name="bootIndexInput")
    def boot_index_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootIndexInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteOnTerminationInput")
    def delete_on_termination_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteOnTerminationInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationTypeInput")
    def destination_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceTypeInput")
    def device_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="diskBusInput")
    def disk_bus_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskBusInput"))

    @builtins.property
    @jsii.member(jsii_name="guestFormatInput")
    def guest_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "guestFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="multiattachInput")
    def multiattach_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "multiattachInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceTypeInput")
    def source_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="uuidInput")
    def uuid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uuidInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeSizeInput")
    def volume_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "volumeSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeTypeInput")
    def volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="bootIndex")
    def boot_index(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootIndex"))

    @boot_index.setter
    def boot_index(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62d472eb5a71fe9efeb2e7ad3f2e592cb50d4fbe97d2aa0a99054362f617cc6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootIndex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteOnTermination")
    def delete_on_termination(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteOnTermination"))

    @delete_on_termination.setter
    def delete_on_termination(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a779d7a878c13d1047c3cf0c154d12c8caf839b21732fc9d56adc71a7fabaef4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteOnTermination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationType")
    def destination_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationType"))

    @destination_type.setter
    def destination_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0b7618476ebed4f53a1a695054496297d74bcc4888528900a64f1e87c15100c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceType")
    def device_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceType"))

    @device_type.setter
    def device_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ac0bc95a0253af1165fbf1d845b8ed8fac21f36b5e5fdb48d1a5e99f78e2835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskBus")
    def disk_bus(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskBus"))

    @disk_bus.setter
    def disk_bus(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa9ae286a92340a71bab93acf0bcf6707bb62b297002fa70944bb789e1c96065)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskBus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="guestFormat")
    def guest_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "guestFormat"))

    @guest_format.setter
    def guest_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cd3d03a0cb6c310f9b3b68f95724357b9bc6c3d5c6813812380de49014438f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guestFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multiattach")
    def multiattach(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "multiattach"))

    @multiattach.setter
    def multiattach(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21596f0aee7ef91dc9b04392c54a8e510a191d28de51dc4ec7ee2e6f42b35832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiattach", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceType")
    def source_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceType"))

    @source_type.setter
    def source_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b206df2c17da310e4f0ed26d0c2866e754208d2ae296542c6945ffe599650e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

    @uuid.setter
    def uuid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__923f46b957a835f0dd1b071e96a1cd6ed0ee93d9a2166189f93d2ac10a8099c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uuid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeSize")
    def volume_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "volumeSize"))

    @volume_size.setter
    def volume_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b15f04bf834a386c766e67dcb968b2cc8f0718928cb45ad42eed1f1391bfa55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeType")
    def volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeType"))

    @volume_type.setter
    def volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ced0b223d5293c3a2a7bd44bc696f12c56a3e1b717795b128ca70a674161df4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2BlockDevice]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2BlockDevice]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2BlockDevice]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__699795e0f1680f1e362cfcdf8244223c028f567db096885ad947763c06b807d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.computeInstanceV2.ComputeInstanceV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "access_ip_v4": "accessIpV4",
        "access_ip_v6": "accessIpV6",
        "admin_pass": "adminPass",
        "availability_zone": "availabilityZone",
        "availability_zone_hints": "availabilityZoneHints",
        "block_device": "blockDevice",
        "config_drive": "configDrive",
        "flavor_id": "flavorId",
        "flavor_name": "flavorName",
        "force_delete": "forceDelete",
        "id": "id",
        "image_id": "imageId",
        "image_name": "imageName",
        "key_pair": "keyPair",
        "metadata": "metadata",
        "network": "network",
        "network_mode": "networkMode",
        "personality": "personality",
        "power_state": "powerState",
        "region": "region",
        "scheduler_hints": "schedulerHints",
        "security_groups": "securityGroups",
        "stop_before_destroy": "stopBeforeDestroy",
        "tags": "tags",
        "timeouts": "timeouts",
        "user_data": "userData",
        "vendor_options": "vendorOptions",
    },
)
class ComputeInstanceV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        access_ip_v4: typing.Optional[builtins.str] = None,
        access_ip_v6: typing.Optional[builtins.str] = None,
        admin_pass: typing.Optional[builtins.str] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        availability_zone_hints: typing.Optional[builtins.str] = None,
        block_device: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2BlockDevice, typing.Dict[builtins.str, typing.Any]]]]] = None,
        config_drive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        flavor_id: typing.Optional[builtins.str] = None,
        flavor_name: typing.Optional[builtins.str] = None,
        force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        image_id: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        key_pair: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceV2Network", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network_mode: typing.Optional[builtins.str] = None,
        personality: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceV2Personality", typing.Dict[builtins.str, typing.Any]]]]] = None,
        power_state: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        scheduler_hints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceV2SchedulerHints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        stop_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeInstanceV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_data: typing.Optional[builtins.str] = None,
        vendor_options: typing.Optional[typing.Union["ComputeInstanceV2VendorOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#name ComputeInstanceV2#name}.
        :param access_ip_v4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#access_ip_v4 ComputeInstanceV2#access_ip_v4}.
        :param access_ip_v6: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#access_ip_v6 ComputeInstanceV2#access_ip_v6}.
        :param admin_pass: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#admin_pass ComputeInstanceV2#admin_pass}.
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#availability_zone ComputeInstanceV2#availability_zone}.
        :param availability_zone_hints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#availability_zone_hints ComputeInstanceV2#availability_zone_hints}.
        :param block_device: block_device block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#block_device ComputeInstanceV2#block_device}
        :param config_drive: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#config_drive ComputeInstanceV2#config_drive}.
        :param flavor_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#flavor_id ComputeInstanceV2#flavor_id}.
        :param flavor_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#flavor_name ComputeInstanceV2#flavor_name}.
        :param force_delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#force_delete ComputeInstanceV2#force_delete}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#id ComputeInstanceV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#image_id ComputeInstanceV2#image_id}.
        :param image_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#image_name ComputeInstanceV2#image_name}.
        :param key_pair: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#key_pair ComputeInstanceV2#key_pair}.
        :param metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#metadata ComputeInstanceV2#metadata}.
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#network ComputeInstanceV2#network}
        :param network_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#network_mode ComputeInstanceV2#network_mode}.
        :param personality: personality block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#personality ComputeInstanceV2#personality}
        :param power_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#power_state ComputeInstanceV2#power_state}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#region ComputeInstanceV2#region}.
        :param scheduler_hints: scheduler_hints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#scheduler_hints ComputeInstanceV2#scheduler_hints}
        :param security_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#security_groups ComputeInstanceV2#security_groups}.
        :param stop_before_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#stop_before_destroy ComputeInstanceV2#stop_before_destroy}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#tags ComputeInstanceV2#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#timeouts ComputeInstanceV2#timeouts}
        :param user_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#user_data ComputeInstanceV2#user_data}.
        :param vendor_options: vendor_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#vendor_options ComputeInstanceV2#vendor_options}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ComputeInstanceV2Timeouts(**timeouts)
        if isinstance(vendor_options, dict):
            vendor_options = ComputeInstanceV2VendorOptions(**vendor_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d9817657721f4148f25436509b89684eeef05f95300bae7806e6e87384dafa8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument access_ip_v4", value=access_ip_v4, expected_type=type_hints["access_ip_v4"])
            check_type(argname="argument access_ip_v6", value=access_ip_v6, expected_type=type_hints["access_ip_v6"])
            check_type(argname="argument admin_pass", value=admin_pass, expected_type=type_hints["admin_pass"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument availability_zone_hints", value=availability_zone_hints, expected_type=type_hints["availability_zone_hints"])
            check_type(argname="argument block_device", value=block_device, expected_type=type_hints["block_device"])
            check_type(argname="argument config_drive", value=config_drive, expected_type=type_hints["config_drive"])
            check_type(argname="argument flavor_id", value=flavor_id, expected_type=type_hints["flavor_id"])
            check_type(argname="argument flavor_name", value=flavor_name, expected_type=type_hints["flavor_name"])
            check_type(argname="argument force_delete", value=force_delete, expected_type=type_hints["force_delete"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument key_pair", value=key_pair, expected_type=type_hints["key_pair"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument network_mode", value=network_mode, expected_type=type_hints["network_mode"])
            check_type(argname="argument personality", value=personality, expected_type=type_hints["personality"])
            check_type(argname="argument power_state", value=power_state, expected_type=type_hints["power_state"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument scheduler_hints", value=scheduler_hints, expected_type=type_hints["scheduler_hints"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument stop_before_destroy", value=stop_before_destroy, expected_type=type_hints["stop_before_destroy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
            check_type(argname="argument vendor_options", value=vendor_options, expected_type=type_hints["vendor_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if access_ip_v4 is not None:
            self._values["access_ip_v4"] = access_ip_v4
        if access_ip_v6 is not None:
            self._values["access_ip_v6"] = access_ip_v6
        if admin_pass is not None:
            self._values["admin_pass"] = admin_pass
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if availability_zone_hints is not None:
            self._values["availability_zone_hints"] = availability_zone_hints
        if block_device is not None:
            self._values["block_device"] = block_device
        if config_drive is not None:
            self._values["config_drive"] = config_drive
        if flavor_id is not None:
            self._values["flavor_id"] = flavor_id
        if flavor_name is not None:
            self._values["flavor_name"] = flavor_name
        if force_delete is not None:
            self._values["force_delete"] = force_delete
        if id is not None:
            self._values["id"] = id
        if image_id is not None:
            self._values["image_id"] = image_id
        if image_name is not None:
            self._values["image_name"] = image_name
        if key_pair is not None:
            self._values["key_pair"] = key_pair
        if metadata is not None:
            self._values["metadata"] = metadata
        if network is not None:
            self._values["network"] = network
        if network_mode is not None:
            self._values["network_mode"] = network_mode
        if personality is not None:
            self._values["personality"] = personality
        if power_state is not None:
            self._values["power_state"] = power_state
        if region is not None:
            self._values["region"] = region
        if scheduler_hints is not None:
            self._values["scheduler_hints"] = scheduler_hints
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if stop_before_destroy is not None:
            self._values["stop_before_destroy"] = stop_before_destroy
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if user_data is not None:
            self._values["user_data"] = user_data
        if vendor_options is not None:
            self._values["vendor_options"] = vendor_options

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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#name ComputeInstanceV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_ip_v4(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#access_ip_v4 ComputeInstanceV2#access_ip_v4}.'''
        result = self._values.get("access_ip_v4")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def access_ip_v6(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#access_ip_v6 ComputeInstanceV2#access_ip_v6}.'''
        result = self._values.get("access_ip_v6")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def admin_pass(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#admin_pass ComputeInstanceV2#admin_pass}.'''
        result = self._values.get("admin_pass")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#availability_zone ComputeInstanceV2#availability_zone}.'''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def availability_zone_hints(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#availability_zone_hints ComputeInstanceV2#availability_zone_hints}.'''
        result = self._values.get("availability_zone_hints")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def block_device(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2BlockDevice]]]:
        '''block_device block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#block_device ComputeInstanceV2#block_device}
        '''
        result = self._values.get("block_device")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2BlockDevice]]], result)

    @builtins.property
    def config_drive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#config_drive ComputeInstanceV2#config_drive}.'''
        result = self._values.get("config_drive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def flavor_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#flavor_id ComputeInstanceV2#flavor_id}.'''
        result = self._values.get("flavor_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flavor_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#flavor_name ComputeInstanceV2#flavor_name}.'''
        result = self._values.get("flavor_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#force_delete ComputeInstanceV2#force_delete}.'''
        result = self._values.get("force_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#id ComputeInstanceV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#image_id ComputeInstanceV2#image_id}.'''
        result = self._values.get("image_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#image_name ComputeInstanceV2#image_name}.'''
        result = self._values.get("image_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_pair(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#key_pair ComputeInstanceV2#key_pair}.'''
        result = self._values.get("key_pair")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#metadata ComputeInstanceV2#metadata}.'''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def network(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2Network"]]]:
        '''network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#network ComputeInstanceV2#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2Network"]]], result)

    @builtins.property
    def network_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#network_mode ComputeInstanceV2#network_mode}.'''
        result = self._values.get("network_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def personality(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2Personality"]]]:
        '''personality block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#personality ComputeInstanceV2#personality}
        '''
        result = self._values.get("personality")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2Personality"]]], result)

    @builtins.property
    def power_state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#power_state ComputeInstanceV2#power_state}.'''
        result = self._values.get("power_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#region ComputeInstanceV2#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheduler_hints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2SchedulerHints"]]]:
        '''scheduler_hints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#scheduler_hints ComputeInstanceV2#scheduler_hints}
        '''
        result = self._values.get("scheduler_hints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceV2SchedulerHints"]]], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#security_groups ComputeInstanceV2#security_groups}.'''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def stop_before_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#stop_before_destroy ComputeInstanceV2#stop_before_destroy}.'''
        result = self._values.get("stop_before_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#tags ComputeInstanceV2#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeInstanceV2Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#timeouts ComputeInstanceV2#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeInstanceV2Timeouts"], result)

    @builtins.property
    def user_data(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#user_data ComputeInstanceV2#user_data}.'''
        result = self._values.get("user_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vendor_options(self) -> typing.Optional["ComputeInstanceV2VendorOptions"]:
        '''vendor_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#vendor_options ComputeInstanceV2#vendor_options}
        '''
        result = self._values.get("vendor_options")
        return typing.cast(typing.Optional["ComputeInstanceV2VendorOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.computeInstanceV2.ComputeInstanceV2Network",
    jsii_struct_bases=[],
    name_mapping={
        "access_network": "accessNetwork",
        "fixed_ip_v4": "fixedIpV4",
        "fixed_ip_v6": "fixedIpV6",
        "name": "name",
        "port": "port",
        "uuid": "uuid",
    },
)
class ComputeInstanceV2Network:
    def __init__(
        self,
        *,
        access_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fixed_ip_v4: typing.Optional[builtins.str] = None,
        fixed_ip_v6: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
        uuid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_network: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#access_network ComputeInstanceV2#access_network}.
        :param fixed_ip_v4: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#fixed_ip_v4 ComputeInstanceV2#fixed_ip_v4}.
        :param fixed_ip_v6: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#fixed_ip_v6 ComputeInstanceV2#fixed_ip_v6}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#name ComputeInstanceV2#name}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#port ComputeInstanceV2#port}.
        :param uuid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#uuid ComputeInstanceV2#uuid}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e5e47606bce1590efb8fa658cc0b4b0ba65b767ef700dbf503d931f5eb58377)
            check_type(argname="argument access_network", value=access_network, expected_type=type_hints["access_network"])
            check_type(argname="argument fixed_ip_v4", value=fixed_ip_v4, expected_type=type_hints["fixed_ip_v4"])
            check_type(argname="argument fixed_ip_v6", value=fixed_ip_v6, expected_type=type_hints["fixed_ip_v6"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_network is not None:
            self._values["access_network"] = access_network
        if fixed_ip_v4 is not None:
            self._values["fixed_ip_v4"] = fixed_ip_v4
        if fixed_ip_v6 is not None:
            self._values["fixed_ip_v6"] = fixed_ip_v6
        if name is not None:
            self._values["name"] = name
        if port is not None:
            self._values["port"] = port
        if uuid is not None:
            self._values["uuid"] = uuid

    @builtins.property
    def access_network(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#access_network ComputeInstanceV2#access_network}.'''
        result = self._values.get("access_network")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fixed_ip_v4(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#fixed_ip_v4 ComputeInstanceV2#fixed_ip_v4}.'''
        result = self._values.get("fixed_ip_v4")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fixed_ip_v6(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#fixed_ip_v6 ComputeInstanceV2#fixed_ip_v6}.'''
        result = self._values.get("fixed_ip_v6")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#name ComputeInstanceV2#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#port ComputeInstanceV2#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uuid(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#uuid ComputeInstanceV2#uuid}.'''
        result = self._values.get("uuid")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceV2Network(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceV2NetworkList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.computeInstanceV2.ComputeInstanceV2NetworkList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d791ccaf1d3b6065ccf4b7f7d9b98cf34c37a179c5ea3201b84c22ad5de52df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeInstanceV2NetworkOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9d7f8a7e642db222ef5e6579e8efa3a75a0a637f98c0dc13caf477c08045839)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceV2NetworkOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1168633862656768070d4e77ba4ac193d11bf44017731155a460c9020878f7c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de783f7ccaae66ec6e5783028110358d8a44b8f2dc0f38b2d04ca35d8f908fd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d1606f32a423d195a719d58beb947de8295db49ddf5916516a10d024d49da12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2Network]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2Network]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2Network]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3961feb9803228adce3e2f2340a691227bef67cdbd865bf0f57d2b5c6da5f9ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceV2NetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.computeInstanceV2.ComputeInstanceV2NetworkOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__660c0d1ac4e17069bc434f49c064fe803bbc4788c81d35f4795551f3a9cdf946)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccessNetwork")
    def reset_access_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessNetwork", []))

    @jsii.member(jsii_name="resetFixedIpV4")
    def reset_fixed_ip_v4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedIpV4", []))

    @jsii.member(jsii_name="resetFixedIpV6")
    def reset_fixed_ip_v6(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedIpV6", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetUuid")
    def reset_uuid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUuid", []))

    @builtins.property
    @jsii.member(jsii_name="mac")
    def mac(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mac"))

    @builtins.property
    @jsii.member(jsii_name="accessNetworkInput")
    def access_network_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "accessNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedIpV4Input")
    def fixed_ip_v4_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fixedIpV4Input"))

    @builtins.property
    @jsii.member(jsii_name="fixedIpV6Input")
    def fixed_ip_v6_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fixedIpV6Input"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="uuidInput")
    def uuid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uuidInput"))

    @builtins.property
    @jsii.member(jsii_name="accessNetwork")
    def access_network(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "accessNetwork"))

    @access_network.setter
    def access_network(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1abb4665af3c877464fbe67a32d3b0274b4f819349c18708fb15e707ac036368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fixedIpV4")
    def fixed_ip_v4(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fixedIpV4"))

    @fixed_ip_v4.setter
    def fixed_ip_v4(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20007150075f376069707626ae5dae3bb17a296170110e70cc83e00bdb048951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedIpV4", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fixedIpV6")
    def fixed_ip_v6(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fixedIpV6"))

    @fixed_ip_v6.setter
    def fixed_ip_v6(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__459d23a8eb930155bcd05ab11afc09d01638bd7aee4d05d633b271db10c0a335)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedIpV6", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c18ba6ced25d296046c298da0eeb8372e04feece9ddb26c16421b52117ddcede)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__045f90ad276f05f6ba7df22b1ec63a6075cf5fd35820c6c64d30af53ec523a91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

    @uuid.setter
    def uuid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c1577ad1b30f9fdbac7d05984b6c49c397c5ab00187acba729d2ff74240696c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uuid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2Network]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2Network]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2Network]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62ed5d106ec232097b1ddddcc684023aac13e8be40a09056be0304ab98e7d23b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.computeInstanceV2.ComputeInstanceV2Personality",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "file": "file"},
)
class ComputeInstanceV2Personality:
    def __init__(self, *, content: builtins.str, file: builtins.str) -> None:
        '''
        :param content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#content ComputeInstanceV2#content}.
        :param file: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#file ComputeInstanceV2#file}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f094e19f77cf387f11cff3cf896514cbb549d2fa97b481837f01f880f5644e)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "file": file,
        }

    @builtins.property
    def content(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#content ComputeInstanceV2#content}.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def file(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#file ComputeInstanceV2#file}.'''
        result = self._values.get("file")
        assert result is not None, "Required property 'file' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceV2Personality(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceV2PersonalityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.computeInstanceV2.ComputeInstanceV2PersonalityList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2c00cc421b10b02dbd5df769a16f69407e8159abf84c9af75849ce79e9c32b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeInstanceV2PersonalityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64daee034231408bbe220a4ef135ca9623a0b2596e36f4ad0a988d900596c0e5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceV2PersonalityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c417857575573791a2e72aa619034057acbf81e4d9d15f4c94e5d85cdd40207)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__063d854e12d3c130aa34d0d8e1b4882847a1a8bba34d52ceaa8304d23db2d2e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ec696a11ac269f7b16a5cb7b360cc40cc7e4308e68b67bc6c7ff5e3d58536c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2Personality]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2Personality]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2Personality]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21b9d4b420c34bd37d4545cce3f592c27d5603c819b0a2caa132af4abb497e8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceV2PersonalityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.computeInstanceV2.ComputeInstanceV2PersonalityOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e21f51df212460c2e7968e3c21145b86349c095528e370f7bcc29dad9720e1f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96f308575d8879485abdc69704aea01e659d42ad5d70069c797561dd84f0199)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "file"))

    @file.setter
    def file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f8be982bca3d7f1039a43bce66bfcb8bf720806a628e7d675311fbd1857774e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "file", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2Personality]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2Personality]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2Personality]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbfafdb195ea739e11214f327d5981a294c46294732f2c925c16084e65f70ecf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.computeInstanceV2.ComputeInstanceV2SchedulerHints",
    jsii_struct_bases=[],
    name_mapping={
        "additional_properties": "additionalProperties",
        "build_near_host_ip": "buildNearHostIp",
        "different_cell": "differentCell",
        "different_host": "differentHost",
        "group": "group",
        "query": "query",
        "same_host": "sameHost",
        "target_cell": "targetCell",
    },
)
class ComputeInstanceV2SchedulerHints:
    def __init__(
        self,
        *,
        additional_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        build_near_host_ip: typing.Optional[builtins.str] = None,
        different_cell: typing.Optional[typing.Sequence[builtins.str]] = None,
        different_host: typing.Optional[typing.Sequence[builtins.str]] = None,
        group: typing.Optional[builtins.str] = None,
        query: typing.Optional[typing.Sequence[builtins.str]] = None,
        same_host: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_cell: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param additional_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#additional_properties ComputeInstanceV2#additional_properties}.
        :param build_near_host_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#build_near_host_ip ComputeInstanceV2#build_near_host_ip}.
        :param different_cell: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#different_cell ComputeInstanceV2#different_cell}.
        :param different_host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#different_host ComputeInstanceV2#different_host}.
        :param group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#group ComputeInstanceV2#group}.
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#query ComputeInstanceV2#query}.
        :param same_host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#same_host ComputeInstanceV2#same_host}.
        :param target_cell: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#target_cell ComputeInstanceV2#target_cell}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa17e6b8e7f975e148dcb83cd6758786830429c9abc45c5c78a8b00be2875602)
            check_type(argname="argument additional_properties", value=additional_properties, expected_type=type_hints["additional_properties"])
            check_type(argname="argument build_near_host_ip", value=build_near_host_ip, expected_type=type_hints["build_near_host_ip"])
            check_type(argname="argument different_cell", value=different_cell, expected_type=type_hints["different_cell"])
            check_type(argname="argument different_host", value=different_host, expected_type=type_hints["different_host"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument same_host", value=same_host, expected_type=type_hints["same_host"])
            check_type(argname="argument target_cell", value=target_cell, expected_type=type_hints["target_cell"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_properties is not None:
            self._values["additional_properties"] = additional_properties
        if build_near_host_ip is not None:
            self._values["build_near_host_ip"] = build_near_host_ip
        if different_cell is not None:
            self._values["different_cell"] = different_cell
        if different_host is not None:
            self._values["different_host"] = different_host
        if group is not None:
            self._values["group"] = group
        if query is not None:
            self._values["query"] = query
        if same_host is not None:
            self._values["same_host"] = same_host
        if target_cell is not None:
            self._values["target_cell"] = target_cell

    @builtins.property
    def additional_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#additional_properties ComputeInstanceV2#additional_properties}.'''
        result = self._values.get("additional_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def build_near_host_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#build_near_host_ip ComputeInstanceV2#build_near_host_ip}.'''
        result = self._values.get("build_near_host_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def different_cell(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#different_cell ComputeInstanceV2#different_cell}.'''
        result = self._values.get("different_cell")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def different_host(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#different_host ComputeInstanceV2#different_host}.'''
        result = self._values.get("different_host")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def group(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#group ComputeInstanceV2#group}.'''
        result = self._values.get("group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#query ComputeInstanceV2#query}.'''
        result = self._values.get("query")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def same_host(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#same_host ComputeInstanceV2#same_host}.'''
        result = self._values.get("same_host")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target_cell(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#target_cell ComputeInstanceV2#target_cell}.'''
        result = self._values.get("target_cell")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceV2SchedulerHints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceV2SchedulerHintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.computeInstanceV2.ComputeInstanceV2SchedulerHintsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__093d94dd34f9c6ad94b33bc6cf34d96fdf527a1d8cf66ecc6c32909b91ab479c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceV2SchedulerHintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aedd0898e1f0d54c07c89e2a02940701adbe2d02febb2bd8fcb5f7af7ea5057b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceV2SchedulerHintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579673d8eafaad2d27ac7620e2b8178baf6597543f753b0072636a19854ce6e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9c8be9ff0b32ceeea1c79ee17a6c484adf56915ab5ef8de5e8982759bde0317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8267472cbec93334dc80b28c309b46a276c9f4d717cc7f4ef73d36187f63cf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2SchedulerHints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2SchedulerHints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2SchedulerHints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19196e21e6fffba9ffcf749c475dd564eee7e5043d500a7f90d38ce6ba75b49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceV2SchedulerHintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.computeInstanceV2.ComputeInstanceV2SchedulerHintsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1edb002c45c353f29998811893392de4bd0861c597e74cca9bedead2411397cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAdditionalProperties")
    def reset_additional_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalProperties", []))

    @jsii.member(jsii_name="resetBuildNearHostIp")
    def reset_build_near_host_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildNearHostIp", []))

    @jsii.member(jsii_name="resetDifferentCell")
    def reset_different_cell(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDifferentCell", []))

    @jsii.member(jsii_name="resetDifferentHost")
    def reset_different_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDifferentHost", []))

    @jsii.member(jsii_name="resetGroup")
    def reset_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroup", []))

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

    @jsii.member(jsii_name="resetSameHost")
    def reset_same_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSameHost", []))

    @jsii.member(jsii_name="resetTargetCell")
    def reset_target_cell(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetCell", []))

    @builtins.property
    @jsii.member(jsii_name="additionalPropertiesInput")
    def additional_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "additionalPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="buildNearHostIpInput")
    def build_near_host_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildNearHostIpInput"))

    @builtins.property
    @jsii.member(jsii_name="differentCellInput")
    def different_cell_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "differentCellInput"))

    @builtins.property
    @jsii.member(jsii_name="differentHostInput")
    def different_host_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "differentHostInput"))

    @builtins.property
    @jsii.member(jsii_name="groupInput")
    def group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="sameHostInput")
    def same_host_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sameHostInput"))

    @builtins.property
    @jsii.member(jsii_name="targetCellInput")
    def target_cell_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetCellInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalProperties")
    def additional_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "additionalProperties"))

    @additional_properties.setter
    def additional_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7480b5e0319dee856f4f643fd3fdf8bc24a0feafb80f531c4599831ba2229f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="buildNearHostIp")
    def build_near_host_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildNearHostIp"))

    @build_near_host_ip.setter
    def build_near_host_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6796ab1b725ef8f5c5669c442ae9ac052a3a3f072adfb83fae49559d1b745a90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildNearHostIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="differentCell")
    def different_cell(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "differentCell"))

    @different_cell.setter
    def different_cell(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aefe3780c0461f2e29b59fac8a0b94f727e57323d1177d803bb253a692a13d88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "differentCell", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="differentHost")
    def different_host(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "differentHost"))

    @different_host.setter
    def different_host(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f8dde31b83956d1e3b2c24560e6a53d62b50598c0d341946c21e7bb896448db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "differentHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "group"))

    @group.setter
    def group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e3b556528a02f2bf6f83b3d5bcf2a9d3e5a847cf036817c8694417b3e9706d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "query"))

    @query.setter
    def query(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__554d9cbeec64b40b7a348e0bc29babe717df4926cf0e83568d2d12f8d840980b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sameHost")
    def same_host(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sameHost"))

    @same_host.setter
    def same_host(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d51944754a1376f045ae12178f0acf3d54175f8d872615320d192b17bd8dba32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sameHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetCell")
    def target_cell(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetCell"))

    @target_cell.setter
    def target_cell(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6db2a351841c86740dfcc6a714c59795136e4d78789b51433c0f15101b24806)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetCell", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2SchedulerHints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2SchedulerHints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2SchedulerHints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50dd934574d514e61cf00e3558c70d6b909a1d2fa0707434da156661c041895b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.computeInstanceV2.ComputeInstanceV2Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeInstanceV2Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#create ComputeInstanceV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#delete ComputeInstanceV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#update ComputeInstanceV2#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9fbd4b210d1fe2e6faad9d42ae2c5d1f32a502b8dee06d303d844c4149678b8)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#create ComputeInstanceV2#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#delete ComputeInstanceV2#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#update ComputeInstanceV2#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceV2Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceV2TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.computeInstanceV2.ComputeInstanceV2TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c47b4f81d5825b846faeee6b37dfa04102dc5700bd51e54dcd36fa82431d33d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b32d19bdf3529ed6e8ecdd2421e6ca87064a86db2bb41c94a30092c1ba501a37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56b6cb5a0616dbf141a13d94e33d63c2f11ff889c7cff8a8623c1e6a4c47e7d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d85d9036f099bf9c19aede4a11b66ab2015b5a7113601d0d04342c3fc165dc82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0aceaa87e8fda5bbbec75bd88905c49d85e75618a6bf5537396055ee87bf505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-openstack.computeInstanceV2.ComputeInstanceV2VendorOptions",
    jsii_struct_bases=[],
    name_mapping={
        "detach_ports_before_destroy": "detachPortsBeforeDestroy",
        "ignore_resize_confirmation": "ignoreResizeConfirmation",
    },
)
class ComputeInstanceV2VendorOptions:
    def __init__(
        self,
        *,
        detach_ports_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ignore_resize_confirmation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param detach_ports_before_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#detach_ports_before_destroy ComputeInstanceV2#detach_ports_before_destroy}.
        :param ignore_resize_confirmation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#ignore_resize_confirmation ComputeInstanceV2#ignore_resize_confirmation}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60d9c2a451a0e14cf7eabe7112865211160bd89bd972b628a853822546aa499d)
            check_type(argname="argument detach_ports_before_destroy", value=detach_ports_before_destroy, expected_type=type_hints["detach_ports_before_destroy"])
            check_type(argname="argument ignore_resize_confirmation", value=ignore_resize_confirmation, expected_type=type_hints["ignore_resize_confirmation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if detach_ports_before_destroy is not None:
            self._values["detach_ports_before_destroy"] = detach_ports_before_destroy
        if ignore_resize_confirmation is not None:
            self._values["ignore_resize_confirmation"] = ignore_resize_confirmation

    @builtins.property
    def detach_ports_before_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#detach_ports_before_destroy ComputeInstanceV2#detach_ports_before_destroy}.'''
        result = self._values.get("detach_ports_before_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ignore_resize_confirmation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/terraform-provider-openstack/openstack/3.0.0/docs/resources/compute_instance_v2#ignore_resize_confirmation ComputeInstanceV2#ignore_resize_confirmation}.'''
        result = self._values.get("ignore_resize_confirmation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceV2VendorOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceV2VendorOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-openstack.computeInstanceV2.ComputeInstanceV2VendorOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e37e961d14b616f3adcca1250114cc626a83dc9922e34ff3cd38165babec1941)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDetachPortsBeforeDestroy")
    def reset_detach_ports_before_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDetachPortsBeforeDestroy", []))

    @jsii.member(jsii_name="resetIgnoreResizeConfirmation")
    def reset_ignore_resize_confirmation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreResizeConfirmation", []))

    @builtins.property
    @jsii.member(jsii_name="detachPortsBeforeDestroyInput")
    def detach_ports_before_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "detachPortsBeforeDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreResizeConfirmationInput")
    def ignore_resize_confirmation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreResizeConfirmationInput"))

    @builtins.property
    @jsii.member(jsii_name="detachPortsBeforeDestroy")
    def detach_ports_before_destroy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "detachPortsBeforeDestroy"))

    @detach_ports_before_destroy.setter
    def detach_ports_before_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__686b9a37c1773e312cd66ca7613472ae0a3201effe37532656ecf842dea601c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detachPortsBeforeDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreResizeConfirmation")
    def ignore_resize_confirmation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreResizeConfirmation"))

    @ignore_resize_confirmation.setter
    def ignore_resize_confirmation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ce55acb1927cc2486c59e073545d3042bfedc00ff11f17178e95db4801c0f71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreResizeConfirmation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeInstanceV2VendorOptions]:
        return typing.cast(typing.Optional[ComputeInstanceV2VendorOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceV2VendorOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cde2c3e1dc370e7b4a26d48ebb7607aabd84a9c792937b5c1f2032c144b25b5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeInstanceV2",
    "ComputeInstanceV2BlockDevice",
    "ComputeInstanceV2BlockDeviceList",
    "ComputeInstanceV2BlockDeviceOutputReference",
    "ComputeInstanceV2Config",
    "ComputeInstanceV2Network",
    "ComputeInstanceV2NetworkList",
    "ComputeInstanceV2NetworkOutputReference",
    "ComputeInstanceV2Personality",
    "ComputeInstanceV2PersonalityList",
    "ComputeInstanceV2PersonalityOutputReference",
    "ComputeInstanceV2SchedulerHints",
    "ComputeInstanceV2SchedulerHintsList",
    "ComputeInstanceV2SchedulerHintsOutputReference",
    "ComputeInstanceV2Timeouts",
    "ComputeInstanceV2TimeoutsOutputReference",
    "ComputeInstanceV2VendorOptions",
    "ComputeInstanceV2VendorOptionsOutputReference",
]

publication.publish()

def _typecheckingstub__33ceeaee9ef417ea4eb8d40e7c00e600e821ba14e8817d7a0b61ea2504f0e029(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    access_ip_v4: typing.Optional[builtins.str] = None,
    access_ip_v6: typing.Optional[builtins.str] = None,
    admin_pass: typing.Optional[builtins.str] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    availability_zone_hints: typing.Optional[builtins.str] = None,
    block_device: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2BlockDevice, typing.Dict[builtins.str, typing.Any]]]]] = None,
    config_drive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    flavor_id: typing.Optional[builtins.str] = None,
    flavor_name: typing.Optional[builtins.str] = None,
    force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    image_id: typing.Optional[builtins.str] = None,
    image_name: typing.Optional[builtins.str] = None,
    key_pair: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2Network, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network_mode: typing.Optional[builtins.str] = None,
    personality: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2Personality, typing.Dict[builtins.str, typing.Any]]]]] = None,
    power_state: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    scheduler_hints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2SchedulerHints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    stop_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeInstanceV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_data: typing.Optional[builtins.str] = None,
    vendor_options: typing.Optional[typing.Union[ComputeInstanceV2VendorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__97970c806bb731f68a80770d7088d89c2258528dba2c12148fe881221a2e96dc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b374d1f7689451a966210b4e8851c75acc8357e8d476ef097f1ce28b88aea65(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2BlockDevice, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a49658fbc4f8ce205fdff8a7205f6dbac40492f084d715ee994ee74278be47c5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2Network, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b76e489135f6c266745c9c15c9b94eadaa9b79a4273128da1d66ffcbaeb90b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2Personality, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc284645b75def46d323be21aced349a4f096181bec881000a7a4c76cc5547af(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2SchedulerHints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc89392c4699e668b2c5ef7a36b93a315f1fcc9cbe143918e5742eb7c59cf7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f68aaf094d69b1998d0a2621a6a6c4eb28209b7aff55161df99df027bc4a97b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14c9f10c502b78e2d9fe0e5c444d47a9e7bee023151b75066620363ea1a031da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb20502aa95a09d36b1726e276560a75a0789c76a4f5135274f73ee190d7aeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb0aa58664eab75dddec0ef4cbaf8a7fa4cea83805b04e723cfcf196e5daff5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45edc6b6785692d60d18c98a78445ea59892b48aa8f2ceb35a34b4b87c17e1e4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdebca954fc5e56777e0ba43b1624a1ef96ede71577f4d1dd94284e8c1ce1f6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7ac0836d80a7b182ec6c822cb4586fcc8c433b6e557ae786ff2cdabe6a4874(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a321e1b5fb02ec8bae1ef20252b36625bc73efdeca09b585a051e90db8f2406d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cdb45546b3dc61afe614c4d60df4edaa3a7a7e6cf44a63eab02dcc5ca95ce91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb679b995620846b49df94e8a800f53ac50b897d0bc0e654fd3435048f32f5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f1679bff59109fe390df9b4f7380b73a1cfede57124db5005a85a3f961ecde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16af4f6aa8caab60c7f0bd123e3057a41fdea38b633f6a28de08dd6e41d2a6c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db79207baf6a984a11bb68113d24fd056c28cce7e7f475498eaeff9042421258(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3cdebb8b769f3fa7a983440b92f23b65a71f5191986c825202d6811fd33930c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57d179bed10a53962995fab1bfec496261e9d12cf35c1f73064cc6cb2f4bf3bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29d7714a28591046058ab330c3dc98234b7045c34f9a990ad5eeb7a855a75dc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90abcdd072a4985d9b690f28e87b4d424ade14d8b2bc5852d23a577438c9ed9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e8436c1391ad45258faebcb31510242fb746e85a5e09ae248c297aa532f3793(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__539d36fd1732ca904460fcbf8f072398d930f1ed654aff2a9d1517add91479fd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__130d4093d35e2a1e3d1f2b182d3f12b0e3238b973e464f47316f8607a47f047b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25ac877cb37d79a19749ad83d5ee320a28c46abb82ad5701c0826ffccb3d453(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c9918966b50342e763a197f8bdc88ad845e0cac4943969a174e36a139c78c8f(
    *,
    source_type: builtins.str,
    boot_index: typing.Optional[jsii.Number] = None,
    delete_on_termination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    destination_type: typing.Optional[builtins.str] = None,
    device_type: typing.Optional[builtins.str] = None,
    disk_bus: typing.Optional[builtins.str] = None,
    guest_format: typing.Optional[builtins.str] = None,
    multiattach: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    uuid: typing.Optional[builtins.str] = None,
    volume_size: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0241998806057f6d5807eafb60ea248f2952431a49db05c3194a3b2a72adc696(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f351e517e4750b1e77d57ada00ba0426039df409266fb1b9682324156aefbfe6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__638b179d592589d80b94553a9b92a5a826ad0d257a459ff8bdbe6442a30d81d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23c8d5d0188c0107fc874427f76493c9cc8254f2a63502ddf3ae5666496e40be(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab84fb086cf606fd8b6035677879ea57c500bd4ccc3c190d8c09cea9b26ffc53(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad77400e15bc9c0c0fe4a4e7cfe3f150ac3f2beb90aa271eb309a885df1e7506(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2BlockDevice]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e068caa78e10ff734e735a5e0ecefa9c7076997f3441f553e12f26a2d2e81e7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d472eb5a71fe9efeb2e7ad3f2e592cb50d4fbe97d2aa0a99054362f617cc6e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a779d7a878c13d1047c3cf0c154d12c8caf839b21732fc9d56adc71a7fabaef4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b7618476ebed4f53a1a695054496297d74bcc4888528900a64f1e87c15100c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac0bc95a0253af1165fbf1d845b8ed8fac21f36b5e5fdb48d1a5e99f78e2835(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa9ae286a92340a71bab93acf0bcf6707bb62b297002fa70944bb789e1c96065(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd3d03a0cb6c310f9b3b68f95724357b9bc6c3d5c6813812380de49014438f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21596f0aee7ef91dc9b04392c54a8e510a191d28de51dc4ec7ee2e6f42b35832(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b206df2c17da310e4f0ed26d0c2866e754208d2ae296542c6945ffe599650e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__923f46b957a835f0dd1b071e96a1cd6ed0ee93d9a2166189f93d2ac10a8099c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b15f04bf834a386c766e67dcb968b2cc8f0718928cb45ad42eed1f1391bfa55(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ced0b223d5293c3a2a7bd44bc696f12c56a3e1b717795b128ca70a674161df4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__699795e0f1680f1e362cfcdf8244223c028f567db096885ad947763c06b807d9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2BlockDevice]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d9817657721f4148f25436509b89684eeef05f95300bae7806e6e87384dafa8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    access_ip_v4: typing.Optional[builtins.str] = None,
    access_ip_v6: typing.Optional[builtins.str] = None,
    admin_pass: typing.Optional[builtins.str] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    availability_zone_hints: typing.Optional[builtins.str] = None,
    block_device: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2BlockDevice, typing.Dict[builtins.str, typing.Any]]]]] = None,
    config_drive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    flavor_id: typing.Optional[builtins.str] = None,
    flavor_name: typing.Optional[builtins.str] = None,
    force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    image_id: typing.Optional[builtins.str] = None,
    image_name: typing.Optional[builtins.str] = None,
    key_pair: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    network: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2Network, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network_mode: typing.Optional[builtins.str] = None,
    personality: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2Personality, typing.Dict[builtins.str, typing.Any]]]]] = None,
    power_state: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    scheduler_hints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceV2SchedulerHints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    stop_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeInstanceV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_data: typing.Optional[builtins.str] = None,
    vendor_options: typing.Optional[typing.Union[ComputeInstanceV2VendorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e5e47606bce1590efb8fa658cc0b4b0ba65b767ef700dbf503d931f5eb58377(
    *,
    access_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fixed_ip_v4: typing.Optional[builtins.str] = None,
    fixed_ip_v6: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    port: typing.Optional[builtins.str] = None,
    uuid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d791ccaf1d3b6065ccf4b7f7d9b98cf34c37a179c5ea3201b84c22ad5de52df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d7f8a7e642db222ef5e6579e8efa3a75a0a637f98c0dc13caf477c08045839(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1168633862656768070d4e77ba4ac193d11bf44017731155a460c9020878f7c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de783f7ccaae66ec6e5783028110358d8a44b8f2dc0f38b2d04ca35d8f908fd9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d1606f32a423d195a719d58beb947de8295db49ddf5916516a10d024d49da12(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3961feb9803228adce3e2f2340a691227bef67cdbd865bf0f57d2b5c6da5f9ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2Network]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__660c0d1ac4e17069bc434f49c064fe803bbc4788c81d35f4795551f3a9cdf946(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1abb4665af3c877464fbe67a32d3b0274b4f819349c18708fb15e707ac036368(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20007150075f376069707626ae5dae3bb17a296170110e70cc83e00bdb048951(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__459d23a8eb930155bcd05ab11afc09d01638bd7aee4d05d633b271db10c0a335(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c18ba6ced25d296046c298da0eeb8372e04feece9ddb26c16421b52117ddcede(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__045f90ad276f05f6ba7df22b1ec63a6075cf5fd35820c6c64d30af53ec523a91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c1577ad1b30f9fdbac7d05984b6c49c397c5ab00187acba729d2ff74240696c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62ed5d106ec232097b1ddddcc684023aac13e8be40a09056be0304ab98e7d23b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2Network]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f094e19f77cf387f11cff3cf896514cbb549d2fa97b481837f01f880f5644e(
    *,
    content: builtins.str,
    file: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c00cc421b10b02dbd5df769a16f69407e8159abf84c9af75849ce79e9c32b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64daee034231408bbe220a4ef135ca9623a0b2596e36f4ad0a988d900596c0e5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c417857575573791a2e72aa619034057acbf81e4d9d15f4c94e5d85cdd40207(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063d854e12d3c130aa34d0d8e1b4882847a1a8bba34d52ceaa8304d23db2d2e3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ec696a11ac269f7b16a5cb7b360cc40cc7e4308e68b67bc6c7ff5e3d58536c5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21b9d4b420c34bd37d4545cce3f592c27d5603c819b0a2caa132af4abb497e8e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2Personality]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e21f51df212460c2e7968e3c21145b86349c095528e370f7bcc29dad9720e1f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96f308575d8879485abdc69704aea01e659d42ad5d70069c797561dd84f0199(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f8be982bca3d7f1039a43bce66bfcb8bf720806a628e7d675311fbd1857774e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbfafdb195ea739e11214f327d5981a294c46294732f2c925c16084e65f70ecf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2Personality]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa17e6b8e7f975e148dcb83cd6758786830429c9abc45c5c78a8b00be2875602(
    *,
    additional_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    build_near_host_ip: typing.Optional[builtins.str] = None,
    different_cell: typing.Optional[typing.Sequence[builtins.str]] = None,
    different_host: typing.Optional[typing.Sequence[builtins.str]] = None,
    group: typing.Optional[builtins.str] = None,
    query: typing.Optional[typing.Sequence[builtins.str]] = None,
    same_host: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_cell: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__093d94dd34f9c6ad94b33bc6cf34d96fdf527a1d8cf66ecc6c32909b91ab479c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aedd0898e1f0d54c07c89e2a02940701adbe2d02febb2bd8fcb5f7af7ea5057b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579673d8eafaad2d27ac7620e2b8178baf6597543f753b0072636a19854ce6e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c8be9ff0b32ceeea1c79ee17a6c484adf56915ab5ef8de5e8982759bde0317(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8267472cbec93334dc80b28c309b46a276c9f4d717cc7f4ef73d36187f63cf0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19196e21e6fffba9ffcf749c475dd564eee7e5043d500a7f90d38ce6ba75b49(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceV2SchedulerHints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1edb002c45c353f29998811893392de4bd0861c597e74cca9bedead2411397cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7480b5e0319dee856f4f643fd3fdf8bc24a0feafb80f531c4599831ba2229f1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6796ab1b725ef8f5c5669c442ae9ac052a3a3f072adfb83fae49559d1b745a90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aefe3780c0461f2e29b59fac8a0b94f727e57323d1177d803bb253a692a13d88(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f8dde31b83956d1e3b2c24560e6a53d62b50598c0d341946c21e7bb896448db(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e3b556528a02f2bf6f83b3d5bcf2a9d3e5a847cf036817c8694417b3e9706d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__554d9cbeec64b40b7a348e0bc29babe717df4926cf0e83568d2d12f8d840980b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d51944754a1376f045ae12178f0acf3d54175f8d872615320d192b17bd8dba32(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6db2a351841c86740dfcc6a714c59795136e4d78789b51433c0f15101b24806(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50dd934574d514e61cf00e3558c70d6b909a1d2fa0707434da156661c041895b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2SchedulerHints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fbd4b210d1fe2e6faad9d42ae2c5d1f32a502b8dee06d303d844c4149678b8(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c47b4f81d5825b846faeee6b37dfa04102dc5700bd51e54dcd36fa82431d33d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b32d19bdf3529ed6e8ecdd2421e6ca87064a86db2bb41c94a30092c1ba501a37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56b6cb5a0616dbf141a13d94e33d63c2f11ff889c7cff8a8623c1e6a4c47e7d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85d9036f099bf9c19aede4a11b66ab2015b5a7113601d0d04342c3fc165dc82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0aceaa87e8fda5bbbec75bd88905c49d85e75618a6bf5537396055ee87bf505(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceV2Timeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d9c2a451a0e14cf7eabe7112865211160bd89bd972b628a853822546aa499d(
    *,
    detach_ports_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ignore_resize_confirmation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37e961d14b616f3adcca1250114cc626a83dc9922e34ff3cd38165babec1941(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686b9a37c1773e312cd66ca7613472ae0a3201effe37532656ecf842dea601c7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ce55acb1927cc2486c59e073545d3042bfedc00ff11f17178e95db4801c0f71(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde2c3e1dc370e7b4a26d48ebb7607aabd84a9c792937b5c1f2032c144b25b5a(
    value: typing.Optional[ComputeInstanceV2VendorOptions],
) -> None:
    """Type checking stubs"""
    pass
