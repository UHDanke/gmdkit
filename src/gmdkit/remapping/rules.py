# Package Imports
from gmdkit.mappings import obj_prop, obj_id
from gmdkit.remapping.base import ID_RULES as BASE_ID_HANDLER
from gmdkit.remapping.classes import IDRule, RuleHandler
from gmdkit.remapping.types import IDType
from gmdkit.remapping.utils import create_text_rule, create_label_rule

ALL_IDS = (
    IDType.GROUP_ID,  
    IDType.ITEM_ID,
    IDType.TIME_ID,
    IDType.COLLISION_ID,
    IDType.COLOR_ID,
    IDType.CONTROL_ID,
    IDType.LINK_ID,
    IDType.TRIGGER_CHANNEL,
    IDType.ENTER_CHANNEL,
    IDType.MATERIAL_ID,
    IDType.EFFECT_ID,
    IDType.GRADIENT_ID,
    IDType.FORCE_ID,
    IDType.KEYFRAME_ID,
    IDType.SFX_ID,
    IDType.SONG_ID,
    IDType.UNIQUE_SFX_ID,
    IDType.SFX_GROUP,
    IDType.SONG_CHANNEL,
    IDType.REMAP_BASE,
    IDType.REMAP_TARGET
    )

COPY_IDS = (
    IDType.LINK_ID,
    IDType.KEYFRAME_ID
    )

GROUP_IDS = (
    IDType.GROUP_ID,
    IDType.ITEM_ID,
    IDType.TIME_ID,
    IDType.COLLISION_ID
    )

REMAP_IDS = (
    *GROUP_IDS,
    IDType.CONTROL_ID,
    IDType.REMAP_BASE,
    IDType.REMAP_TARGET
    )

REMAP_COLOR_IDS = (
    *REMAP_IDS,
    IDType.COLOR_ID
    )

REGROUP_IDS = (
    *REMAP_IDS,
    IDType.FORCE_ID,
    IDType.GRADIENT_ID
    )

REGROUP_COLOR_IDS = (
    *REGROUP_IDS,
    IDType.COLOR_ID
    )

TEXT_NUM_RULE = create_text_rule(
    regex=r"^\d+$",
    id_type=IDType.ANY,
    id_min=1,
    id_max=9999
    )
    
TEXT_ID_RULE = create_text_rule(
    regex=r"\bID\s+(\d+)\b",
    id_type=IDType.GROUP_ID,
    id_min=1,
    id_max=9999
    )

TEXT_REMAP_RULE = create_text_rule(
    regex=r"^(\d+)\s+[A-Za-z]+",
    id_type=IDType.LABEL
    )

TEXT_ID_LABEL_RULE = create_label_rule(
    template="ID {}",
    id_type=IDType.LABEL
    )

TEXT_ID_HANDLER = RuleHandler(by_id={obj_id.TEXT:(TEXT_NUM_RULE,TEXT_ID_RULE,TEXT_REMAP_RULE)})

EDITOR_LAYERS_HANDLER = RuleHandler(base=(
    IDRule(obj_prop.EDITOR_L1, IDType.GENERIC, reference=True, default=0, id_min=-32768, id_max=32767),
    IDRule(obj_prop.EDITOR_L2, IDType.GENERIC, reference=True, default=lambda obj: 0 if obj.get(obj_prop.EDITOR_L1) else None, id_min=-32768, id_max=32767)
    ))

Z_LAYER_HANDLER = RuleHandler(base=(
    IDRule(obj_prop.Z_LAYER, IDType.GENERIC, reference=True, id_min=-5, id_max=11),
    ))

COPY_ID_HANDLER = BASE_ID_HANDLER.compile_rules(id_types=COPY_IDS)

REMAP_ID_HANDLER = BASE_ID_HANDLER.compile_rules(id_types=REMAP_IDS)

REMAP_COLOR_ID_HANDLER = BASE_ID_HANDLER.compile_rules(id_types=REMAP_COLOR_IDS)

REGROUP_ID_HANDLER = BASE_ID_HANDLER.compile_rules(id_types=REGROUP_IDS)

REGROUP_COLOR_ID_HANDLER = BASE_ID_HANDLER.compile_rules(id_types=REGROUP_COLOR_IDS)