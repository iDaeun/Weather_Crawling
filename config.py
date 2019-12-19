import yaml

y_file = './resource/application-dev.yml'

with open(y_file, 'r') as yml:
    cfg = yaml.safe_load(yml)

class TargetConfig:
    WEATHER = cfg['URL']['WEATHER']