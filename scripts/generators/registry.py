CUSTOM_GENERATORS = {
    "dungeons": {
        "sandbox_gen": {
            "label": "Sandbox Dungeon Generator",
            "generators": {
                "room": {
                    "label": "Dungeon Room",
                    "function": "scripts.generators.dungeons.sandbox_gen.room.generate"
                },
                "corridor": {
                    "label": "Corridor Section",
                    "function": "scripts.generators.dungeons.sandbox_gen.corridor.generate"
                },
                "full_dungeon": {
                    "label": "Full Dungeon Layout",
                    "function": "scripts.generators.dungeons.sandbox_gen.full_dungeon.generate"
                }
            }
        }
    }
}
