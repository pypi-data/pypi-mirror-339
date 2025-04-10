#!/usr/bin/env python3

import os
import os.path
import sys
import json
import click
import base64
import boto3
import boto3.session
import botocore
import rich
import networkx as nx

from pathlib import Path
from rich.tree import Tree


EMPTY_SECRET = {'KEY': 'VALUE'}


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    try:
        session = boto3.session.Session()
        region = session.region_name
        if not region:
            click.echo('You need a default region or simply to have an aws cli login')
            exit(1)
        c = boto3.client('secretsmanager', region_name=region)
        ctx.obj['client'] = c
        c.list_secrets()
    except botocore.exceptions.NoCredentialsError:
        click.echo('You need to be logged in with aws-cli and have list secrets permission to use the tool')
        exit(1)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            raise Exception('Secret not found on aws secret manager')
    except Exception as e:
        raise Exception(e)


@cli.command()
@click.pass_context
@click.option('--find', '-f', help='String to match', default=None)
@click.option('--dir-only', '-d', is_flag=True, help='Only output structure', default=False)
def list(ctx, find, dir_only):
    """List secrets"""
    client = ctx.obj['client']

    G = nx.DiGraph()
    G.add_node('/')

    count = 0
    paginator = client.get_paginator('list_secrets')
    response = paginator.paginate()
    for page in response:
        for s in page['SecretList']:
            if find and not (find in s['Name']):
                continue

            count += 1
            parent, curPath = '/', ''
            for n in s['Name'].split('/'):
                curPath += f'/{n}'
                if n not in G.nodes:
                    G.add_node(curPath)
                G.add_edge(parent, curPath)
                parent = curPath

            G.nodes[parent]['name'] = f"/{s['Name']}"
            G.nodes[parent]['description'] = s.get('Description', 'N/A')

    def add_node(node, tree):
        successors = G.successors(node)
        for s in successors:
            is_leaf = sum(1 for _ in G.successors(s)) == 0
            if is_leaf:
                leaf = G.nodes[s]['name']
                tree.add(leaf)
            else:
                clean_s = s.split('/')[-1]
                branch = tree.add(clean_s)
                add_node(s, branch)

    tree = Tree('.')
    add_node('/', tree)

    click.echo(f'Secrets count: {count}')
    rich.print(tree)


@cli.command()
@click.pass_context
@click.option('--secret', '-s', help='Secret name', required=True)
@click.option('--description', '-d', help='Secret description', required=True)
def create(ctx, secret, description):
    """Create secret"""
    client = ctx.obj['client']
    content = click.edit(str(EMPTY_SECRET))
    name = secret.strip('/')
    if content:
        client.create_secret(
            Name=name,
            SecretString=content,
            Description=description
        )


@cli.command()
@click.pass_context
@click.option('--secret', '-s', help='Secret name', required=True)
@click.option('--description', '-d', help='Secret description')
def edit(ctx, secret, description):
    """Edit secret online"""
    client = ctx.obj['client']
    try:
        name = secret.strip('/')
        r = client.describe_secret(SecretId=name)
        valueExists = 'VersionIdsToStages' in r
        if valueExists:
            r = client.get_secret_value(SecretId=name)
            content = r['SecretString']
        else:
            content = json.dumps(EMPTY_SECRET, indent=4)
    except botocore.exceptions.ClientError:
        click.secho(f'Secret {secret} not found', fg='red')
        exit(1)

    try:
        j = json.loads(content)
        content = click.edit(json.dumps(j, indent=4))
    except ValueError:
        content = click.edit(content)

    if content:
        client.put_secret_value(
            SecretId=name,
            SecretString=content
        )


@cli.command()
@click.pass_context
@click.option('--secret', '-s', help='Secret name', required=True)
def view(ctx, secret):
    """View secret"""
    client = ctx.obj['client']
    try:
        name = secret.strip("/")
        r = client.get_secret_value(SecretId=name)
        content = r['SecretString']
    except botocore.exceptions.ClientError:
        click.secho(f'Secret {secret} not found', fg='red')
        exit(1)

    try:
        j = json.loads(content)
        click.echo(json.dumps(j, indent=4))
    except ValueError:
        click.echo(content)


@cli.command()
@click.pass_context
@click.option('--secret', '-s', help='Secret name', required=True)
def env(ctx, secret):
    """Expose secret as enviromental variables"""
    client = ctx.obj['client']
    try:
        name = secret.strip('/')
        r = client.get_secret_value(SecretId=name)
        content = r['SecretString']
    except botocore.exceptions.ClientError:
        click.secho(f'Secret {secret} not found', fg='red')
        exit(1)

    try:
        j = json.loads(content)
        for k, v in j.items():
            click.echo(f'export {k}={v}')
    except ValueError:
        click.echo('Secret is not in json format, or there is a parsing error!')


@cli.command()
@click.pass_context
@click.option('--secret', '-s', help='Secret name', required=True)
@click.option('--key', '-k', help='Secret key', required=True)
@click.option('--decode', '-d', is_flag=True, help='Base64 decode', default=False)
def get(ctx, secret, key, decode):
    """Get specific value from the password"""
    client = ctx.obj['client']
    try:
        name = secret.strip('/')
        r = client.get_secret_value(SecretId=name)
        content = r['SecretString']
    except botocore.exceptions.ClientError:
        click.secho(f'Secret {secret} not found', fg='red')
        exit(1)

    try:
        j = json.loads(content)
        if key in j:
            if decode:
                decoded = base64.b64decode(j[key])
                click.echo(decoded)
            else:
                click.echo(j[key])
        else:
            click.echo(f'Key [{key}] not found on secret [{secret}]')
    except ValueError:
        click.echo('Secret is not in json format, or there is a parsing error!')


@cli.command()
@click.pass_context
@click.option('--secret', '-s', help='Secret name', required=True)
@click.option('--key', '-k', help='Secret key', required=True)
@click.option('--value', '-v', help='Secret value', required=True)
def set(ctx, secret, key, value):
    """Set specific value from the password"""
    client = ctx.obj['client']
    try:
        name = secret.strip('/')
        r = client.get_secret_value(SecretId=name)
        content = r['SecretString']
    except botocore.exceptions.ClientError:
        click.secho(f'Secret {secret} not found', fg='red')
        exit(1)

    try:
        j = json.loads(content)
        j[key] = value
        client.put_secret_value(
            SecretId=name,
            SecretString=json.dumps(j)
        )
    except ValueError:
        click.echo('Secret is not in json format, or there is a parsing error!')


if __name__ == '__main__':
    cli()
