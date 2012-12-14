# -*- coding: utf8 -*- 

import uuid
from ckan.logic import get_action

def getExtraProperty(package_info, key):
        for extra_entry in package_info['extras']:
            if extra_entry['key'] == key:
                return extra_entry['value'][1:-1]
        return None

def createExtraProperty(package_info, key, value):
    extra_property = {}
    extra_property['state'] = 'active'
    extra_property['value'] = '"' + str(value) + '"'
    extra_property['revision_timestamp'] = '2012-12-13T14:27:35.654886'
    extra_property['package_id'] = package_info['id']
    extra_property['key'] = key
    extra_property['revision_id'] = str(uuid.uuid4())
    extra_property['id'] = str(uuid.uuid4())

    package_info['extras'].append(extra_property)
    
def checkExtraProperty(package_info, key):
    for extra_data in package_info['extras']:
        if extra_data['key'] == key:
            return True

    return False

def updateExtraProperty(package_info, key, value):
    for extra_data in package_info['extras']:
        if extra_data['key'] == key:
            extra_data['value'] = '"' + str(value) + '"'
            extra_data['revision_id'] = str(uuid.uuid4())
            extra_data['revision_timestamp'] = '2012-12-13T14:27:35.654886'
            return 

    package_info['extras'].append(extra_property)

def deleteExtraProperty(package_info, key):
    for extra_data in package_info['extras']:
        if extra_data['key'] == key:
            package_info['extras'].remove(extra_data)

def updatePackage(context, package_info):
    updated_info = {}

    #set log message 
    updated_info['log_message'] = 'Updating ADAPTA extra information'

    #copy other required fields
    updated_info['id'] = package_info['id']
    updated_info['extras'] = []
    updated_info['extras'] = updated_info['extras'] + package_info['extras']
    updated_info['maintainer'] = package_info['maintainer']
    updated_info['name'] = package_info['name']
    updated_info['author'] = package_info['author']
    updated_info['author_email'] = package_info['author_email']
    updated_info['tag_string'] = ''
    updated_info['title'] = package_info['title']
    updated_info['maintainer_email'] = package_info['maintainer_email']
    updated_info['url'] = package_info['url']
    updated_info['version'] = package_info['version']
    updated_info['license_id'] = package_info['license_id']
    updated_info['notes'] = package_info['notes']

    updated_package = get_action('package_update')(context, updated_info)
