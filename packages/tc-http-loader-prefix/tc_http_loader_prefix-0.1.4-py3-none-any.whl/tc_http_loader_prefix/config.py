# coding: utf-8

def register_config():
    from thumbor.config import Config
    Config.define('TC_HTTP_LOADER_PREFIX', None, 'Define a prefix path for HTTP loader', 'tc_http_loader_prefix')
