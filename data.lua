-- Data stage: Defining the machine's existence
local idle_machine_item = {
    type = "item",
    name = "idle-machine",
    icon = "__idle-machine__/graphics/icons/idle-machine.png",
    icon_size = 64,
    subgroup = "production-machine",
    order = "a[idle-machine]",
    place_result = "idle-machine",
    stack_size = 10
}

local idle_machine_recipe = {
    type = "recipe",
    name = "idle-machine",
    enabled = true,
    ingredients = {
        {type = "item", name = "iron-plate", amount = 2}
    },
    results = {{type = "item", name = "idle-machine", amount = 1}}
}

-- Dummy recipe to keep the furnace "active"
local idle_dummy_recipe = {
    type = "recipe",
    name = "idle-dummy-recipe",
    icon = "__idle-machine__/graphics/icons/idle-machine.png",
    icon_size = 64,
    enabled = true,
    hidden = true,
    energy_required = 1,
    ingredients = {},
    results = {},
    category = "idle-machine-crafting"
}

local idle_machine_entity = {
    type = "furnace",
    name = "idle-machine",
    icon = "__idle-machine__/graphics/icons/idle-machine.png",
    flags = {"placeable-neutral", "placeable-player", "player-creation"},
    minable = {mining_time = 0.2, result = "idle-machine"},
    max_health = 150,
    corpse = "big-remnants",
    dying_explosion = "big-explosion",
    collision_box = {{-1.2, -1.2}, {1.2, 1.2}},
    selection_box = {{-1.5, -1.5}, {1.5, 1.5}},
    module_specification = { module_slots = 3 },
    allowed_effects = {"consumption", "speed", "productivity", "pollution"},
    crafting_categories = {"idle-machine-crafting"},
    crafting_speed = 1,
    source_inventory_size = 0,
    result_inventory_size = 20,
    energy_usage = "33kW", -- 33kW matches the 1 wood = 20 items balance at initial speed
    energy_source = {
        type = "electric",
        usage_priority = "secondary-input",
        emissions_per_minute = { pollution = 1 }
    },
    graphics_set = {
        animation = {
            layers = {
                {
                    filename = "__idle-machine__/graphics/entity/idle-machine.png",
                    priority = "high",
                    width = 214,
                    height = 190,
                    frame_count = 32,
                    line_length = 8,
                    shift = {0.34375, 0.03125},
                    scale = 0.5
                }
            }
        }
    }
}

data:extend({
    {
        type = "recipe-category",
        name = "idle-machine-crafting"
    },
    idle_machine_item,
    idle_machine_recipe,
    idle_dummy_recipe,
    idle_machine_entity
})
