from hatchling.builders.hooks.plugin.interface import BuildHookInterface

class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        build_data['purelib'] = 'src'
        build_data['packages'] = ['src/async_task_worker']
