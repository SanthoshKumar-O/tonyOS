from tony.configuration import ConfigurationManager

config = ConfigurationManager.load()

print(config)
print(config.application.name)
print(config.logging.level)
