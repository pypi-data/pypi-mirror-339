import glob,os,json
from abstract_utilities import *
from pathlib import Path
from io import BytesIO
from abstract_utilities.path_utils import get_files
from .serverManager import *
def get_server_mgr(src_dir=None,domain=None,imgs_dir=None,fb_id=None,directory=None):
    server_mgr = serverManager(src_dir=src_dir,domain=domain,imgs_dir=imgs_dir,fb_id=fb_id,directory=directory)
    return server_mgr
def get_abs_path():
    return os.path.abspath(__file__)
def get_abs_dir():
    abs_path = get_abs_path()
    return os.path.dirname(abs_path)
def get_sections_dir():
    return 'collect_media/sections'
def get_src_dir():
    return get_server_mgr().src_dir
def get_base_dir():
    return os.path.dirname(get_src_dir())
def get_imgs_dir():
    return get_server_mgr().imgs_dir
def get_json_directory():
    server_mgr = get_server_mgr()
    return server_mgr.json_dir
def get_json_directories():
    return get_dir_paths(get_json_directory())
def get_dir_paths(directory):
    json_dirs = [os.path.join(directory,item) for item in os.listdir(directory)]
    json_dirs = [json_dir for json_dir in json_dirs if os.path.isdir(json_dir)]
    return json_dirs
def get_data(file_path):
    return safe_read_from_json(file_path)
def consolidate_media(file_path):
    data = safe_read_from_json(file_path)
    data = get_new_media(data)
    safe_dump_to_file(data,file_path)
    return data
def get_json_data(file_path):
    json_contents = safe_read_from_json(file_path)
    if not json_contents:
        return 
    return json_contents
def get_all_json_paths(directory):
    json_paths = glob.glob(os.path.join(directory, '**', '*.json'), recursive=True)
    return json_paths
def combine_media(media,media_2):
    for key,value in media.items():
        media[key] = check_value(value) or check_value(media_2.get(key))
    return media
def find_all_files_with_substring(substr, directory=None):
    base_dir = Path(directory) if directory else Path.cwd()
    return [path for path in base_dir.rglob('*') if os.path.isfile(str(path)) and substr in os.path.basename(str(path))]

def create_source_dirs():
    json_directories = get_json_directories()
    for json_directory in json_directories:
        basename = os.path.basename(json_directory)
        filename,ext = os.path.splitext(basename)
        source_dir = os.path.join(get_sections_dir(),filename)
        os.makedirs(source_dir,exist_ok=True)
        all_medias = get_all_medias(json_directory)
        all_keywords = get_all_keywords(json_directory)
        sources_json = os.path.join(source_dir,'sources.json')
        if not os.path.isfile(sources_json):
            safe_dump_to_file([],sources_json)
        sources_data =safe_read_from_json(sources_json)
        images_json = os.path.join(source_dir,'images.json')
        if not os.path.isfile(sources_json):
            safe_dump_to_file([],images_json)    
        images_data =safe_read_from_json(images_json)
        keywords_json = os.path.join(source_dir,'keywords.json')
        if not os.path.isfile(keywords_json):
            safe_dump_to_file([],keywords_json)
        images_data,sources_data = consolidate_medias(all_medias,images=images_data,others=sources_data)
        safe_dump_to_file(sources_data,sources_json)
        safe_dump_to_file(images_data,images_json)
