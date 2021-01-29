import yaml
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader).get('DEFAULT', 'DEFAULT')
    print(type(cfg['pOT1']))
    print(cfg['pOT1'])

