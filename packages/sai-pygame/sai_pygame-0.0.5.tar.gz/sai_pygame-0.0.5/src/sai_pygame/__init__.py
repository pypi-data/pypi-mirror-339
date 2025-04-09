from gymnasium import register

register(
    id="CoopPuzzle-v0",
    entry_point="sai_pygame.coop_puzzle:CoopPuzzleEnv",
)

register(
    id="Pong-v0",
    entry_point="sai_pygame.pong:PongEnv",
)

register(
    id="SpaceEvaders-v0",
    entry_point="sai_pygame.space_evaders:SpaceEvadersEnv",
)

register(
    id="SquidHunt-v0",
    entry_point="sai_pygame.squid_hunt:SquidHuntEnv",
)

register(
    id="MagnetMania-v0",
    entry_point="sai_pygame.magnet_mania:MagnetManiaEnv",
)
