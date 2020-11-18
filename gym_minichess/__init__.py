from gym.envs.registration import register

register(
    id='minichess-gardner-v0',
    entry_point='gym_minichess.envs:GardnerMiniChessEnv'
)

# more variants here # TODO

# register(
#     id='minichess-atomic-v0',
#     entry_point='gym_minichess.envs:AtomicMinichessEnv'
# )

# register(
#     id='minichess-dark-v0',
#     entry_point='gym_minichess.envs:DarkMinichessEnv'
# )

# register(
#     id='minichess-extinction-v0',
#     entry_point='gym_minichess.envs:ExtinctionMinichessEnv'
# )

# register(
#     id='minichess-monochromatic-v0',
#     entry_point='gym_minichess.envs:MonochromaticMinichessEnv'
# )

# register(
#     id='minichess-portal-v0',
#     entry_point='gym_minichess.envs:PortalMinichessEnv'
# )

# register(
#     id='minichess-progressive-v0',
#     entry_point='gym_minichess.envs:ProgressiveMinichessEnv'
# )

register(
    id='minichess-rifle-v0',
    entry_point='gym_minichess.envs:RifleMinichessEnv'
)
