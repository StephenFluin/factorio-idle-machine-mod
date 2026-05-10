---
name: factorio-modding
description: Expert guidance for developing Factorio mods, focusing on Factorio 2.0 standards, Lua API, and performance optimization. Use when building, debugging, or refactoring Factorio mods.
---

# Factorio Modding Skill

This skill provides expert guidance for developing Factorio mods. It is optimized for Factorio 2.0.

## Core Mandates

1. **Use `storage` for Persistence**: In Factorio 2.0, use the `storage` table instead of `global` for all data that must persist across save/load.
2. **Optimize Events**: Use event filters (`{filter = "name", name = "my-entity"}`) whenever possible to reduce the frequency of Lua calls.
3. **Respect the Data Lifecycle**: Prototypes must be defined in the `data` stage. Scripting logic belongs in the `control` stage. Never mix them.
4. **Localization**: Always use `locale/` files for user-facing text. Never hardcode strings in Lua.

## Workflows

### Creating a New Entity
1. Define the prototype in `data.lua` using a standard type (e.g., `furnace`, `assembling-machine`).
2. Add localization for the entity name and description in `locale/en/config.cfg`.
3. If specific logic is needed, register events in `control.lua`.

### Debugging Crashes
1. Identify if the crash is in the **Data Stage** (loading error) or **Control Stage** (runtime error).
2. Check `factorio-current.log` for the full stack trace.
3. Use `game.print()` or `log()` for runtime debugging.

## Reference Materials
- [Factorio API Docs](https://lua-api.factorio.com/latest/)
- [2.0 Porting Guide](https://github.com/tburrows13/factorio-2.0-mod-porting-guide)
