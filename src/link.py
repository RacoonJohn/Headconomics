
# Imports
from beet import Context
from stewbeet import *  # type: ignore
from stouputils.typing import JsonDict


# Main entry point (ran just before making finalyzing the build process (zip, headers, lang, ...))
def beet_default(ctx: Context):
	ns: str = Mem.ctx.project_id
	definitions: JsonDict = Mem.definitions

	# Add some commands when loading datapack
	write_load_file(f"""
function {ns}:load/msg


execute in overworld run forceload add 3000000 32000
execute in overworld unless entity 170328e0-1ea6-42ca-8ad3-7120326bb638 run summon minecraft:text_display 3000000 1000000 32000 {{UUID:[I;386083040,514212554,-1965854432,845919800],Tags:["bs.entity","bs.persistent","smithed.entity","smithed.strict"],view_range:0f,alignment:"center"}}


scoreboard objectives add {ns}.id dummy
scoreboard objectives add {ns}.data dummy
scoreboard objectives add {ns}.init_version dummy
scoreboard objectives add {ns}.my_time dummy

scoreboard objectives add {ns}.transfer_voucher trigger
scoreboard objectives add {ns}.wallet trigger

scoreboard objectives add {ns}.death deathCount

execute unless data storage {ns}:data uuids run function {ns}:head/reset_data

execute unless data storage {ns}:data config run function {ns}:config/reset


""")

	write_function(f"{ns}:load/msg",f"""
# Add a message when loading
execute if score #loaded {ns}.data matches 1 run return run say Headconomics reloaded
say Headconomics loaded
scoreboard objectives add {ns}.data dummy
scoreboard players set #loaded {ns}.data 1

""")



