from __future__ import absolute_import, print_function, unicode_literals

import boto3


def clean_old_lambda_versions():
    session = boto3.Session(profile_name='staging')
    client = session.client('lambda', region_name='eu-west-1')
    functions = client.list_functions()['Functions']
    for function in functions:
        versions = client.list_versions_by_function(FunctionName=function['FunctionArn'])['Versions']
        available_versions_list = []
        for version in versions:
            available_versions_list.append(version['Version'])

        aliases_response = client.list_aliases(FunctionName=function['FunctionArn'])['Aliases']
        aliased_versions_list = []
        for alias in aliases_response:
            aliased_versions_list.append(alias['FunctionVersion'])
        untagged_versions = set(available_versions_list) - set(aliased_versions_list) - {'$LATEST'}

        print("Versions that are not aliased", untagged_versions)
        for version in untagged_versions:
            print("Deleting Untagged Versions")
            print(client.delete_function(FunctionName=function['FunctionArn'], Qualifier=version))



if __name__ == '__main__':
    clean_old_lambda_versions()
