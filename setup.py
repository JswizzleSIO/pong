import cx_Freeze

executables = [cx_Freeze.Executable("PongLegacy.py")]

cx_Freeze.setup(
    name="Pong Legacy",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["Minecraft.ttf", "coin.png", "heart.png", "beep.wav", "bump.wav", "bwubwub.wav", "music.wav"]}},
    executables = executables
    )
