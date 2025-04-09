from .nile_river_simulation import create_nile_river_env
from .omo_river_simulation import create_omo_river_env
from .susquehanna_river_simulation import create_susquehanna_river_env
from gymnasium.envs.registration import register

__all__=['create_nile_river_env', 'create_omo_river_env', 'create_susquehanna_river_env']


register(
    id='nile-v0',
    entry_point='morl4water.examples.nile_river_simulation:create_nile_river_env',
)

register(
    id='omo-v0',
    entry_point='morl4water.examples.omo_river_simulation:create_omo_river_env',
)


register(
    id='susquehanna-v0',
    entry_point='morl4water.examples.susquehanna_river_simulation:create_susquehanna_river_env',
)