﻿from azure.mgmt.resource.resources.operations.resource_groups_operations \
    import ResourceGroupsOperations
from azure.mgmt.resource.resources.operations.tags_operations import TagsOperations
from azure.mgmt.resource.resources.operations.deployments_operations import DeploymentsOperations
from azure.mgmt.resource.resources.operations.deployment_operations_operations \
    import DeploymentOperationsOperations
from azure.cli.commands._auto_command import build_operation, CommandDefinition
from azure.cli.commands import CommandTable, LongRunningOperation, patch_aliases
from azure.cli._locale import L

from ._params import PARAMETER_ALIASES, _resource_client_factory
from .custom import ConvenienceResourceGroupCommands, ConvenienceResourceCommands

command_table = CommandTable()

build_operation(
    'resource group', 'resource_groups', _resource_client_factory,
    [
        CommandDefinition(
            ResourceGroupsOperations.delete,
            LongRunningOperation(L('Deleting resource group'), L('Resource group deleted'))),
        CommandDefinition(ResourceGroupsOperations.get, 'ResourceGroup', 'show'),
        CommandDefinition(ResourceGroupsOperations.check_existence, 'Bool', 'exists'),
    ],
    command_table, patch_aliases(PARAMETER_ALIASES, {
        'resource_group_name': {'name': '--name -n'}
    }))

build_operation(
    'resource group', None, ConvenienceResourceGroupCommands,
    [
        CommandDefinition(ConvenienceResourceGroupCommands.list, '[ResourceGroup]'),
        CommandDefinition(ConvenienceResourceGroupCommands.create, 'ResourceGroup'),
        CommandDefinition(ConvenienceResourceGroupCommands.export_group_as_template,
                          None, "export")
    ],
    command_table, patch_aliases(PARAMETER_ALIASES, {
        'resource_group_name':{'name':'--name -n'},
        'include_comments':{'action':'store_true'},
        'include_parameter_default_value':{'action':'store_true'}
    }))

build_operation(
    'resource', None, ConvenienceResourceCommands,
    [
        CommandDefinition(ConvenienceResourceCommands.list, '[Resource]'),
        CommandDefinition(ConvenienceResourceCommands.show, 'Resource'),
        CommandDefinition(ConvenienceResourceCommands.deploy, 'Resource'),
    ],
    command_table, patch_aliases(PARAMETER_ALIASES, {
        'resource_name': {'name': '--name -n'},
        'mode': {
            'name': '--mode',
            'choices': ['Incremental', 'Complete'],
            'help': 'Incremental (only add resources to resource group) or '
                    'Complete (remove extra resources from resource group)',
            'default': 'Incremental'
        }
    }))

build_operation(
    'tag', 'tags', _resource_client_factory,
    [
        CommandDefinition(TagsOperations.list, '[Tag]'),
        CommandDefinition(TagsOperations.create_or_update, 'Tag', 'create'),
        CommandDefinition(TagsOperations.delete, None, 'delete'),
        CommandDefinition(TagsOperations.create_or_update_value, 'Tag', 'add-value'),
        CommandDefinition(TagsOperations.delete_value, None, 'remove-value'),
    ],
    command_table, patch_aliases(PARAMETER_ALIASES, {
        'tag_name': {'name': '--name -n'},
        'tag_value': {'name': '--value'}
    }))

build_operation(
    'resource group deployment', 'deployments', _resource_client_factory,
    [
        CommandDefinition(DeploymentsOperations.list, '[Deployment]'),
        CommandDefinition(DeploymentsOperations.get, 'Deployment', 'show'),
        CommandDefinition(DeploymentsOperations.validate, 'Object'),
        #CommandDefinition(DeploymentsOperations.delete, 'Object'),
        CommandDefinition(DeploymentsOperations.check_existence, 'Bool', 'exists'),
        #CommandDefinition(DeploymentsOperations.cancel, 'Object'),
        #CommandDefinition(DeploymentsOperations.create_or_update, 'Object', 'create'),
    ],
    command_table, patch_aliases(PARAMETER_ALIASES, {
        'deployment_name': {'name': '--name -n', 'required': True}
    }))

build_operation(
    'resource group deployment operation', 'deployment_operations', _resource_client_factory,
    [
        CommandDefinition(DeploymentOperationsOperations.list, '[DeploymentOperations]'),
        CommandDefinition(DeploymentOperationsOperations.get, 'DeploymentOperations', 'show')
    ],
    command_table, patch_aliases(PARAMETER_ALIASES, {
        'deployment_name': {'name': '--name -n', 'required': True}
    }))