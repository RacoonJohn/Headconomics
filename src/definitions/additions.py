
# Imports
from beet import Context
from stewbeet import *  # type: ignore

ns: str = Mem.ctx.project_id

# Main entry point
def main():


  config_dialog = {
  "type": "minecraft:multi_action",
  "title": {
    "text": "✎ Config"
  },
  "inputs": [
    {
      "type": "minecraft:number_range",
      "key": "delay",
      "label": {
        "text": "⌚ Collection delay"
      },
      "label_format": "%1$s: %2$shours",
      "start": 1,
      "end": 100,
      "step": 1,
      "initial": 50
    },
    {
      "type": "minecraft:number_range",
      "key": "goal",
      "label": {
        "text": "⚐ Collection goal"
      },
      "label_format": "%1$s: %2$s",
      "start": 2,
      "end": 100,
      "step": 1,
      "initial": 50
    }
  ],
  "after_action": "close",
  "pause": False,
  "columns": 8,
  "actions": [
    {
      "label": {
        "text": "Save"
      },
      "action": {
        "type": "minecraft:dynamic/run_command",
        "template": f"/function {ns}:config/save {{goal:$(goal),delay:$(delay)}}"
      }
    }
  ]
}

  write_function_tag(f'{ns}:config', [f"{ns}:config/dialog"])

  write_advancement(f'{ns}:transfer_voucher',{
  "criteria": {
    "loot": {
      "trigger": "minecraft:using_item",
      "conditions": {
        "item": {
          "predicates": {
            "minecraft:custom_data": {
              f"{ns}":{
                "item":"transfer_voucher"
              }
            }
          }
        }
      }
    }
  },
  "rewards": {
    "function": f"{ns}:head/use_transfer_voucher"
  }
})

  Mem.ctx.data[ns].slot_sources["transfer_voucher"] = SlotSource({
  "type": "minecraft:filtered",
  "slot_source": {
    "type": "minecraft:group",
    "terms": [
      {
        "type": "minecraft:slot_range",
        "slots": "container.*"
      },
      {
        "type": "minecraft:slot_range",
        "slots": "weapon.offhand"
      }
    ]
  },
  "item_filter": {
    "predicates": {
      "minecraft:custom_data": {
        f"{ns}":{
          "item":"transfer_voucher"
        }
      }
    }
  }
})

  write_function(f'{ns}:config/dialog',f'''
data modify storage {ns}: dialog set value {config_dialog}

data modify storage {ns}: dialog.inputs[{{key:"goal"}}].initial set from storage {ns}:data config.goal
data modify storage {ns}: dialog.inputs[{{key:"delay"}}].initial set from storage {ns}:data config.delay

function {ns}:head/dialog/show with storage {ns}:
''')
	
  write_function(f'{ns}:config/save',f'''
$data modify storage {ns}:data config set value {{delay:$(delay),goal:$(goal)}}
''')
	

  write_function(f'{ns}:config/reset',f'''
data modify storage {ns}:data config set value {{delay:10,goal:10}}
''')

  write_function(f'{ns}:head/reset_data',f'''

scoreboard players add #init_version {ns}.data 1

scoreboard players set #count {ns}.id 0
data modify storage {ns}:data uuids set value [0]

''')

  write_tick_file(f'''

execute store result score #gametime {ns}.data run time query gametime
execute as @a run function {ns}:player/tick
''')

  write_function(f'{ns}:player/tick',f'''

execute unless score @s {ns}.init_version = #init_version {ns}.data run function {ns}:player/init

scoreboard players enable @s {ns}.wallet
execute if score @s {ns}.wallet matches 1.. run function {ns}:head/dialog

execute if predicate {{type:"entity_properties",entity:"this",predicate:{{movement:{{speed:{{min:0.1}}}}}}}} run tag @s remove {ns}.in_wallet

scoreboard players enable @s[tag={ns}.in_wallet,scores={{{ns}.my_time=1..}}] {ns}.transfer_voucher
scoreboard players reset @s[tag=!{ns}.in_wallet] {ns}.transfer_voucher
execute if score @s {ns}.transfer_voucher matches 1.. run function {ns}:head/get_transfer_voucher

execute if score @s {ns}.my_time matches 0 run function {ns}:player/reset_wallet

execute if items entity @s {ns}:transfer_voucher * run function {ns}:head/delete_date

scoreboard players add @s {ns}.my_time 1
execute if predicate {{type:"int_value_check",value:{{type:"score",score:"{ns}.my_time",target:"this"}},test:{{min:{{type:"mul",inputs:[72000,{{type:"storage",storage:"{ns}:data",path:"config.delay"}}]}}}}}} run function {ns}:delay/end

execute if score @s {ns}.death matches 1.. run function {ns}:player/death
''')

  write_function(f'{ns}:player/death',f'''

scoreboard players reset @s {ns}.death

execute store result storage {ns}: macro.id int 1 run scoreboard players get @s {ns}.id
function {ns}:head/get_uuid with storage {ns}: macro
data modify storage {ns}: macro set from storage {ns}: uuid
execute store result storage {ns}: macro.id int 1 run scoreboard players get @s {ns}.id
data modify storage {ns}: macro.text set from storage {ns}: macro.text.text
data modify storage {ns}: macro.owner set from storage {ns}: uuid.str
data modify storage {ns}: macro.owner_4int set from storage {ns}: uuid.4int
data modify storage {ns}: macro.owner_str set from storage {ns}: uuid.str
execute store result storage {ns}: macro.date int 1 run time query gametime
data modify storage {ns}: macro.date set compute default integer {{type:"add",inputs:[1200,{{type:"storage",storage:"{ns}:",path:"macro.date"}}]}}

data modify storage {ns}: macro.x set from entity @s LastDeathLocation.pos[0]
data modify storage {ns}: macro.y set from entity @s LastDeathLocation.pos[1]
data modify storage {ns}: macro.z set from entity @s LastDeathLocation.pos[2]

function {ns}:head/get_transfer_voucher/drop with storage {ns}: macro

''')

  write_function(f'{ns}:player/reset_wallet',f'''

data modify storage {ns}: temp set from storage {ns}:data uuids
function {ns}:player/reset_wallet/recurse with storage {ns}: temp[-1]

execute store result storage {ns}: macro.id int 1 run scoreboard players get @s {ns}.id
function {ns}:head/32 with storage {ns}: macro

''')

  write_function(f'{ns}:player/reset_wallet/recurse',f'''
$scoreboard players reset @s {ns}.head_count.$(int)

data remove storage {ns}: temp[-1]
execute if data storage {ns}: temp[-1] run function {ns}:player/reset_wallet/recurse with storage {ns}: temp[-1]
''')

  write_function(f'{ns}:player/init',f'''

execute store result storage {ns}: macro.id int 1 run scoreboard players add #count {ns}.id 1
scoreboard players operation @s {ns}.id = #count {ns}.id

execute store result storage {ns}: macro.id int 1 run scoreboard players get @s {ns}.id
function {ns}:head/32 with storage {ns}: macro

scoreboard players operation @s {ns}.init_version = #init_version {ns}.data

function {ns}:head/new with storage {ns}: macro

''')

  write_function(f'{ns}:delay/end',f'''

execute store result score #unique {ns}.data run function {ns}:head/get_unique

scoreboard players set @s {ns}.my_time -1200

attribute @s max_health modifier remove {ns}:sanction
tellraw @s {{text:"The delay to collect heads ended!\nAll previous sanctions are removed",color:"red"}}

execute unless predicate {{type:"int_value_check",value:{{type:"score",score:"{ns}.data",target:{{type:"fixed",name:"#unique"}}}},test:{{min:{{type:"storage",storage:"{ns}:data",path:"config.goal"}}}}}} run return run function {ns}:delay/fail

tellraw @s {{text:"Congratulation, you succeeded to acheive the goal!",color:"gold"}}

''')

  write_function(f'{ns}:delay/fail',f'''
tellraw @s {{text:"You failed to acheive the goal!",color:"dark_red"}}

attribute @s max_health modifier add {ns}:sanction -0.5 add_multiplied_total

''')

  write_function(f'{ns}:head/delete_date',f'''
execute if items entity @s weapon.offhand *[custom_data~{{{ns}:{{item:"transfer_voucher"}}}}] store result score #delete_date {ns}.data run data get entity @s equipment.offhand.components."minecraft:custom_data".{ns}.delete_date
execute if items entity @s weapon.offhand *[custom_data~{{{ns}:{{item:"transfer_voucher"}}}}] if score #delete_date {ns}.data < #gametime {ns}.data run item replace entity @s weapon.offhand with air
''')

  for slot in range(0,26):
    write_function(f'{ns}:head/delete_date',f'''
execute if items entity @s container.{slot} *[custom_data~{{{ns}:{{item:"transfer_voucher"}}}}] store result score #delete_date {ns}.data run data get entity @s Inventory[{{Slot:{slot}b}}].components."minecraft:custom_data".{ns}.delete_date
execute if items entity @s container.{slot} *[custom_data~{{{ns}:{{item:"transfer_voucher"}}}}] if score #delete_date {ns}.data < #gametime {ns}.data run item replace entity @s container.{slot} with air
''')

  write_function(f'{ns}:head/get_transfer_voucher',f'''
execute store result storage {ns}: macro.id int 1 run scoreboard players get @s {ns}.transfer_voucher
function {ns}:head/get_uuid with storage {ns}: macro
data modify storage {ns}: macro set from storage {ns}: uuid
data modify storage {ns}: macro.text set from storage {ns}: macro.text.text
execute store result storage {ns}: macro.id int 1 run scoreboard players get @s {ns}.id
function {ns}:head/get_uuid with storage {ns}: macro
data modify storage {ns}: macro.owner set from storage {ns}: uuid.str
data modify storage {ns}: macro.owner_4int set from storage {ns}: uuid.4int
data modify storage {ns}: macro.owner_str set from storage {ns}: uuid.str
execute store result storage {ns}: macro.date int 1 run time query gametime
data modify storage {ns}: macro.date set compute default integer {{type:"add",inputs:[1200,{{type:"storage",storage:"{ns}:",path:"macro.date"}}]}}
function {ns}:head/get_transfer_voucher/give with storage {ns}: macro
  
scoreboard players set @s {ns}.transfer_voucher 0
''')

  write_function(f'{ns}:head/get_transfer_voucher/give',f'''

$execute unless score @s {ns}.head_count.$(int) matches 1.. run return fail

$item modify entity @s {ns}:transfer_voucher {{type:"set_custom_data",tag:{{{ns}:{{delete_date:$(date)}}}}}}
$give @s flow_banner_pattern[max_stack_size=99,item_model="player_head",item_name={{text:"Transfer Voucher"}},rarity="uncommon",lore=[[{{translate:"hc.pre_head_available_1min",color:"gray",italic:false}},"$(text)",{{text:"s head (available 1min)"}}]],profile={{id:$(owner_4int)}},custom_data={{{ns}:{{item:"transfer_voucher",owner:"$(owner)",owner_str:"$(owner_str)",id:$(id),str:"$(str)",delete_date:$(date)}}}},!provides_banner_patterns,!banner_patterns,use_effects={{can_sprint:true}},consumable={{consume_seconds:1000000,sound:{{sound_id:"",range:0}}}}]
''')


  write_function(f'{ns}:head/get_transfer_voucher/drop',f'''

$summon item $(x) $(y) $(z) {{Item:{{id:"flow_banner_pattern",count:1,components:{{max_stack_size:99,item_model:"player_head",item_name:{{text:"Transfer Voucher"}},rarity:"uncommon",lore:[[{{translate:"hc.pre_head_available_1min",color:"gray",italic:false}},"$(text)",{{text:"s head (available 1min)"}}]],profile:{{id:$(owner_4int)}},custom_data:{{{ns}:{{item:"transfer_voucher",owner:"$(owner)",owner_str:"$(owner_str)",id:$(id),str:"$(str)",delete_date:$(date)}}}},"!provides_banner_patterns":{{}},"!banner_patterns":{{}},use_effects:{{can_sprint:true}},consumable:{{consume_seconds:1000000,sound:{{sound_id:"",range:0}}}}}}}}}}
''')

  write_function(f'{ns}:head/use_transfer_voucher',f'''

advancement revoke @s only {ns}:transfer_voucher

execute if score @s {ns}.my_time matches ..0 run return run tellraw @s {{text:"You cannot accept transfer vouchers for the moment",color:"red"}}

execute if items entity @s weapon.mainhand *[custom_data~{{{ns}:{{item:"transfer_voucher"}}}}] run data modify storage {ns}: item set from entity @s SelectedItem
execute unless items entity @s weapon.mainhand *[custom_data~{{{ns}:{{item:"transfer_voucher"}}}}] if items entity @s weapon.offhand *[custom_data~{{{ns}:{{item:"transfer_voucher"}}}}] run data modify storage {ns}: item set from entity @s equipment.offhand

data modify storage {ns}: macro set from storage {ns}: item.components."minecraft:custom_data".{ns}
data modify storage {ns}: macro.count set from storage {ns}: item.count

execute store result storage {ns}: count int 1 run function {ns}:head/get with storage {ns}: macro
data modify storage {ns}: macro.count set compute default integer {{type:"min",inputs:[{{type:"storage",storage:"{ns}:",path:"count"}},{{type:"storage",storage:"{ns}:",path:"macro.count"}}]}}

tag @s add {ns}.deductor
execute unless predicate {{type:"int_value_check",test:0,value:{{type:"storage",storage:"{ns}:",path:"macro.count"}}}} run function {ns}:head/deduct with storage {ns}: macro
tag @s remove {ns}.deductor

execute if items entity @s weapon.mainhand *[custom_data~{{{ns}:{{item:"transfer_voucher"}}}}] run return run item replace entity @s weapon.mainhand with air
item replace entity @s weapon.offhand with air

''')

  write_function(f'{ns}:head/new',f'''

$scoreboard objectives add {ns}.head_count.$(id) dummy

function gu:convert with entity @s
$data modify storage {ns}:data uuids append value {{4int:[],str:"",int:$(id),text:""}} 
data modify storage {ns}:data uuids[-1].4int set from entity @s UUID
data modify storage {ns}:data uuids[-1].str set from storage gu:main out
function hc:head/get_name
data modify storage {ns}:data uuids[-1].text set from storage {ns}: name
''')

  write_function(f'{ns}:head/get',f'''
$return run scoreboard players get $(owner) {ns}.head_count.$(id)
''')

  write_function(f'{ns}:head/32',f'''
$scoreboard players set @s {ns}.head_count.$(id) 32
''')
  
  write_function(f'{ns}:head/get_unique',f'''

scoreboard players set #temp {ns}.data 0
	
data modify storage {ns}: temp set from storage {ns}:data uuids
function {ns}:head/get_unique/recurse with storage {ns}: temp[-1]

return run scoreboard players get #temp {ns}.data
''')

  write_function(f'{ns}:head/get_unique/recurse',f'''
$execute if score @s {ns}.head_count.$(int) matches 1.. run scoreboard players add #temp {ns}.data 1

data remove storage {ns}: temp[-1]
execute if data storage {ns}: temp[-1] run function {ns}:head/get_unique/recurse with storage {ns}: temp[-1]
''')

  write_function(f'{ns}:head/get_uuid',f'''
$data modify storage {ns}: uuid set from storage {ns}:data uuids[$(id)]
''')

  write_function(f'{ns}:head/get_name',f'''
data modify storage {ns}: name set value {{selector:""}}
data modify storage {ns}: name.selector set from storage gu:main out
data modify entity 170328e0-1ea6-42ca-8ad3-7120326bb638 text set from storage {ns}: name
data modify storage {ns}: name set from entity 170328e0-1ea6-42ca-8ad3-7120326bb638 text
''')

  write_function(f'{ns}:head/deduct',f'''

$execute as $(owner) if entity @s[tag={ns}.deductor] run return run tellraw @s {{text:"You cannot deduct heads from yourself!",color:"red"}}

$tellraw @s [{{text:"You received ",color:"gray"}},"$(count) ",{{selector:"$(str)"}},{{text:"s heads from "}},{{selector:"$(owner_str)"}}]
$scoreboard players add @s {ns}.head_count.$(id) $(count)
$scoreboard players remove $(owner) {ns}.head_count.$(id) $(count)

''')

  dialog = {
  "type": "minecraft:multi_action",
  "title": [{"text": "Wallet","bold":True}],
  "body": {"type":"plain_message","contents":["",{"text":"/"},"","\n","",{"text":" hours left"}]},
  "inputs": [],
  "after_action": "none",
  "pause": False,
  "columns": 8,
  "actions": []
}
             
                 
  action = f'''{{
			"width":40,
      "label": [{{
        "player": {{
          "id": $(4int)
        }}
      }}," ",""],
      "tooltip": $(text),
      "action": {{
        "type": "minecraft:run_command",
        "command": "trigger {ns}.transfer_voucher set $(int)"
      }}
    }}'''.replace("\n","")

  write_function(f'{ns}:head/dialog',f'''

scoreboard players reset @s {ns}.wallet
tag @s add {ns}.in_wallet

data modify storage {ns}: dialog set value {dialog}

execute store result storage {ns}: macro.count int 1 run function {ns}:head/get_unique
data modify storage {ns}: dialog.body.contents[0] set string storage {ns}: macro.count
data modify storage {ns}: dialog.body.contents[2] set string storage {ns}:data config.goal

data modify storage {ns}: dialog.body.contents[4] set compute default integer {{type:"div",right:72000,left:{{type:"sub",left:{{type:"mul",inputs:[72000,{{type:"storage",storage:"{ns}:data",path:"config.delay"}}]}},right:{{type:"score",score:"{ns}.my_time",target:"this"}}}}}}
execute if predicate {{type:"int_value_check",test:0,value:{{type:"storage",storage:"{ns}:",path:"dialog.body.contents[4]"}}}} run data modify storage {ns}: dialog.body.contents[5] set value {{text:" minutes left"}}
execute if predicate {{type:"int_value_check",test:0,value:{{type:"storage",storage:"{ns}:",path:"dialog.body.contents[4]"}}}} run data modify storage {ns}: dialog.body.contents[4] set compute default integer {{type:"sub",left:{{type:"mul",inputs:[60,{{type:"storage",storage:"{ns}:data",path:"config.delay"}}]}},right:{{type:"div",right:1200,left:{{type:"score",score:"{ns}.my_time",target:"this"}}}}}}
data modify storage {ns}: dialog.body.contents[4] set string storage {ns}: dialog.body.contents[4]


data modify storage {ns}: temp set from storage {ns}:data uuids
function {ns}:head/dialog/recurse with storage {ns}: temp[-1]

function {ns}:head/dialog/show with storage {ns}:
''')

  write_function(f'{ns}:head/dialog/recurse',f'''

$execute unless score @s {ns}.head_count.$(int) matches 1.. run return run function {ns}:head/dialog/recurse_end

$data modify entity 170328e0-1ea6-42ca-8ad3-7120326bb638 text set value {{score:{{name:"$(str)",objective:"{ns}.head_count.$(int)"}}}}
$data modify storage {ns}: dialog.actions append value {action}
data modify storage {ns}: dialog.actions[-1].label[-1] set from entity 170328e0-1ea6-42ca-8ad3-7120326bb638 text

function {ns}:head/dialog/recurse_end

''')

  write_function(f'{ns}:head/dialog/recurse_end',f'''

data remove storage {ns}: temp[-1]
execute if data storage {ns}: temp[-1] run function {ns}:head/dialog/recurse with storage {ns}: temp[-1]
''')

  write_function(f'{ns}:head/dialog/show',f'''
$dialog show @s $(dialog)
''')


  pass

