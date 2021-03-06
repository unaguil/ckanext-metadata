# -*- coding: utf8 -*- 

from ckan.plugins import SingletonPlugin, IGenshiStreamFilter, implements, IConfigurer, IRoutes
from logging import getLogger
from pylons import request
from genshi.input import HTML
from genshi.filters.transform import Transformer
import os

log = getLogger(__name__)

class MetadataExtension(SingletonPlugin):
    
    implements(IConfigurer, inherit=True)
    implements(IGenshiStreamFilter, inherit=True)
    implements(IRoutes, inherit=True)
    
    def update_config(self, config):
        here = os.path.dirname(__file__)
        rootdir = os.path.dirname(os.path.dirname(here))
        our_public_dir = os.path.join(rootdir, 'ckanext', 
				'metadata', 'theme', 'public')
                                      
        template_dir = os.path.join(rootdir, 'ckanext',
				'metadata', 'theme', 'templates')
				
        # set resource and template overrides
        config['extra_public_paths'] = ','.join([our_public_dir,
                config.get('extra_public_paths', '')])
                
        config['extra_template_paths'] = ','.join([template_dir,
				config.get('extra_template_paths', '')])
    
    def filter(self, stream):
        routes = request.environ.get('pylons.routes_dict')
        log.info(routes)
        if routes.get('controller') in ('package', 'related',
			'ckanext.metadata.controller:MetadataController') :
               stream = stream | Transformer('//ul[@class="nav nav-pills"]').append(HTML(
                    
                    '''<li class>
                        <a class href="/dataset/metadata/%s">
                            <img src="/icons/rdf_flyer.24" height="16px" width="16px" alt="None" class="inline-icon ">
                             Metadata
                        </a>
                    </li>''' % routes.get('id')
                    
                ))
                
        if routes.get('controller') in ('admin', 'ckanext.metadata.controller:AdminController'):
			 stream = stream | Transformer('//ul[@class="nav nav-pills"]').append(HTML(
                    
                    '''<li class>
                        <a class href="/ckan-admin/metadata-tasks">
                            <img src="/icons/rdf_flyer.24" height="16px" width="16px" alt="None" class="inline-icon ">
                            Metadata Tasks Status
                        </a>
                    </li>'''
                    
                ))

        return stream
       
    def before_map(self, map):
        map.connect('/dataset/metadata/{id}',
            controller='ckanext.metadata.controller:MetadataController',
            action='show_metadata')
            
        map.connect('/dataset/metadata/{id}/void.rdf',
            controller='ckanext.metadata.controller:MetadataController',
            action='get_void_desc')

        map.connect('/ckan-admin/metadata-tasks',
            controller='ckanext.metadata.controller:AdminController',
            action='metadata_tasks')

        map.connect('api_update_properties', '/api/2/update/package/properties',
            controller='ckanext.metadata.controller:ApiController',
            action='update_properties')
        
        map.connect('api_update_vocab_count', '/api/2/update/update_vocab_count',
            controller='ckanext.metadata.controller:ApiController',
            action='update_vocabulary_count')

        map.connect('api_get_metadata_timestamp', '/api/2/get/get_metadata_timestamp',
            controller='ckanext.metadata.controller:ApiController',
            action='get_metadata_timestamp')

        map.connect('api_get_metadata_properties', '/api/2/get/get_metadata_properties',
            controller='ckanext.metadata.controller:ApiController',
            action='get_metadata_properties')

        return map
        
