# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
#pylint: disable=line-too-long

from azure.cli.core.commands.parameters import \
    (location_type, enum_choice_list, get_resource_name_completion_list, CliArgumentType)
from azure.cli.core.commands import register_cli_argument
from azure.mgmt.iothub.models.iot_hub_client_enums import IotHubSku
from ._factory import iot_hub_service_factory
from .custom import iot_device_list


def get_device_id_completion_list(prefix, action, parsed_args, **kwargs):#pylint: disable=unused-argument
    client = iot_hub_service_factory(kwargs)
    return [d.device_id for d in iot_device_list(client, parsed_args.hub_name, top=100)] if parsed_args.hub_name else []

hub_name_type = CliArgumentType(completer=get_resource_name_completion_list('Microsoft.Devices/IotHubs'),
                                help='IoT Hub name.')

register_cli_argument('iot hub', 'hub_name', hub_name_type, options_list=('--name', '-n'))
for subgroup in ['consumer-group', 'policy']:
    register_cli_argument('iot hub {}'.format(subgroup), 'hub_name', options_list=('--hub-name',))

register_cli_argument('iot device', 'hub_name', hub_name_type)

register_cli_argument('iot', 'device_id', options_list=('--device-id', '-d'), help='Device Id.',
                      completer=get_device_id_completion_list)

# Arguments for 'iot hub consumer-group' group
register_cli_argument('iot hub consumer-group', 'consumer_group_name', options_list=('--name', '-n'),
                      help='Event hub consumer group name.')
register_cli_argument('iot hub consumer-group', 'event_hub_name', help='Target event hub name.')

# Arguments for 'iot hub policy' group
register_cli_argument('iot hub policy', 'policy_name', options_list=('--name', '-n'), help='Share access policy name.')

# Arguments for 'iot hub create'
register_cli_argument('iot hub create', 'hub_name', options_list=('--name', '-n'), completer=None)
register_cli_argument('iot hub create', 'location', location_type,
                      help='Location of your IoT Hub. Default is the location of target resource group.')
register_cli_argument('iot hub create', 'sku',
                      help='Pricing tier for Azure IoT Hub. Default value is F1, which is free. '
                           'Note that only one free IoT Hub instance is allowed in each subscription. '
                           'Exception will be thrown if free instances exceed one.',
                      **enum_choice_list(IotHubSku))
register_cli_argument('iot hub create', 'unit', help='Units in your IoT Hub.', type=int)

# Arguments for 'iot hub show-connection-string'
register_cli_argument('iot hub show-connection-string', 'policy_name', help='Shared access policy to use.')

# Arguments for 'iot device create'
register_cli_argument('iot device create', 'device_id', completer=None)
register_cli_argument('iot device create', 'x509', action='store_true', arg_group='X.509 Certificate',
                      help='Use X.509 certificate for device authentication.')
register_cli_argument('iot device create', 'primary_thumbprint', arg_group='X.509 Certificate',
                      help='Primary X.509 certificate thumbprint to authenticate device.')
register_cli_argument('iot device create', 'secondary_thumbprint', arg_group='X.509 Certificate',
                      help='Secondary X.509 certificate thumbprint to authenticate device.')
register_cli_argument('iot device create', 'valid_days', type=int, arg_group='X.509 Certificate',
                      help='Number of days the generated self-signed X.509 certificate should be valid for.'
                           'Default validity is 365 days.')
register_cli_argument('iot device create', 'output_dir', arg_group='X.509 Certificate',
                      help='Output directory for generated self-signed X.509 certificate. '
                           'Default is current working directory.')

# Arguments for 'iot device list'
register_cli_argument('iot device list', 'top', help='Maximum number of device identities to return.', type=int)

# Arguments for 'iot device delete'
register_cli_argument('iot device delete', 'etag',
                      help='ETag of the target device. It is used for the purpose of optimistic concurrency. '
                           'Delete operation will be performed only if the specified ETag matches the value maintained by the server, '
                           'indicating that the device identity has not been modified since it was retrieved. '
                           'Default value is set to wildcard character (*) to force an unconditional delete.')

# Arguments for 'iot device show-connection-string'
register_cli_argument('iot device show-connection-string', 'top',
                      help='Maximum number of connection strings to return.', type=int)
