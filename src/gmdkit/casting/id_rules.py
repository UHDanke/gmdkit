# Package Imports
from gmdkit.mappings import obj_id, obj_prop, color_prop
from gmdkit.defaults.color_default import COLOR_1_DEFAULT, COLOR_2_DEFAULT


ID_RULES = {
    obj_id.trigger.COLOR: [
            {'type': 'color_id', 'property_id': obj_prop.trigger.color.CHANNEL, 'min': 1, 'max': 999, 'remappable': False, 'iterable': False},
            {'type': 'color_id', 'property_id': obj_prop.trigger.color.COPY_ID, 'min': 1, 'max': 999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.shader.GRAY_SCALE: [
            {'type': 'color_id', 'property_id': obj_prop.trigger.shader.GRAY_SCALE_TINT_CHANNEL, 'min': 1, 'max': 999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.shader.LENS_CIRCLE: [
            {'type': 'color_id', 'property_id': obj_prop.trigger.shader.LENS_CIRCLE_TINT_CHANNEL, 'min': 1, 'max': 999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.shader.LENS_CIRCLE_CENTER_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.shader.RADIAL_BLUR: [
            {'type': 'color_id', 'property_id': obj_prop.trigger.shader.RADIAL_BLUR_REF_CHANNEL, 'min': 1, 'max': 999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.shader.RADIAL_BLUR_CENTER_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.shader.MOTION_BLUR: [
            {'type': 'color_id', 'property_id': obj_prop.trigger.shader.MOTION_BLUR_REF_CHANNEL, 'min': 1, 'max': 999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.shader.MOTION_BLUR_CENTER_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    'any': [
            {'type': 'color_id', 'property_id': obj_prop.COLOR_1, 'default': lambda x: COLOR_1_DEFAULT.get(x,0), 'min': 1, 'max': 999, 'remappable': False, 'iterable': False},
            {'type': 'color_id', 'property_id': obj_prop.COLOR_2, 'default': lambda x: COLOR_2_DEFAULT.get(x,0), 'min': 1, 'max': 999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.GROUPS, 'replace': lambda x, kvm: x.remap(kvm), 'min': 1, 'max': 9999, 'remappable': False, 'iterable': True},
            {'type': 'group_id', 'property_id': obj_prop.PARENT_GROUPS, 'replace': lambda x, kvm: x.remap(kvm), 'min': 1, 'max': 9999, 'remappable': False, 'iterable': True},
            {'type': 'link_id', 'property_id': obj_prop.LINKED_GROUP, 'min': 1, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'type': 'trigger_channel', 'property_id': obj_prop.trigger.CHANNEL, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'type': 'enter_channel', 'property_id': obj_prop.ENTER_CHANNEL, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': False, 'iterable': False},
            {'type': 'material_id', 'property_id': obj_prop.MATERIAL, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': False, 'iterable': False},
            {'type': 'control_id', 'property_id': obj_prop.trigger.CONTROL_ID, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.PULSE: [
            {'type': 'color_id', 'property_id': obj_prop.trigger.pulse.COPY_ID, 'min': 1, 'max': 999, 'remappable': False, 'iterable': False},
            {'type': 'color_id', 'property_id': obj_prop.trigger.pulse.TARGET_ID, 'condition': lambda x: x.get(obj_prop.trigger.pulse.TARGET_TYPE,0) == 0, 'min': 1, 'max': 999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.pulse.TARGET_ID, 'condition': lambda x: x.get(obj_prop.trigger.pulse.TARGET_TYPE,0) == 1, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.area.TINT: [
            {'type': 'color_id', 'property_id': obj_prop.trigger.effect.TINT_CHANNEL, 'min': 1, 'max': 999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.effect.CENTER_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.effect.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'effect_id', 'property_id': obj_prop.trigger.effect.EFFECT_ID, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.enter.TINT: [
            {'type': 'color_id', 'property_id': obj_prop.trigger.effect.TINT_CHANNEL, 'min': 1, 'max': 999, 'remappable': False, 'iterable': False},
            {'type': 'effect_id', 'property_id': obj_prop.trigger.effect.EFFECT_ID, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'type': 'enter_channel', 'property_id': obj_prop.trigger.effect.ENTER_CHANNEL, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    obj_id.LEVEL_START: [
            {'type': 'color_id', 'property_id': obj_prop.level.COLORS, 'function': lambda x: x.unique_values(lambda i: i.channels), 'replace': lambda x, kvm: x.apply(lambda i: i.remap(kvm)), 'min': 1, 'max': 999, 'remappable': False, 'iterable': True},
            {'type': 'group_id', 'property_id': obj_prop.level.PLAYER_SPAWN, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.MOVE: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.move.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.move.TARGET_POS, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.move.TARGET_CENTER_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.ALPHA: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.alpha.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.TOGGLE: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.toggle.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.TOGGLE_BLOCK: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.toggle_block.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.orb.TOGGLE: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.toggle_block.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.ON_DEATH: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.on_death.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.SPAWN: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.spawn.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'remap_base', 'property_id': obj_prop.trigger.spawn.REMAPS, 'function': lambda x: x.keys(), 'replace': lambda x, kvm: x.apply(lambda i: i.remap(key_map=kvm)), 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': True},
            {'type': 'remap_target', 'property_id': obj_prop.trigger.spawn.REMAPS, 'condition': lambda x: x.get(obj_prop.trigger.spawn.RESET_REMAP,0) == 1, 'function': lambda x: x.values(), 'replace': lambda x, kvm: x.apply(lambda i: i.remap(value_map=kvm)), 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': True},
            {'type': 'remap_target', 'property_id': obj_prop.trigger.spawn.REMAPS, 'condition': lambda x: x.get(obj_prop.trigger.spawn.RESET_REMAP,0) == 0, 'function': lambda x: x.values(), 'replace': lambda x, kvm: x.apply(lambda i: i.remap(value_map=kvm)), 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': True}
        ],
    obj_id.trigger.TELEPORT: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.teleport.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.SONG: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.song.GROUP_ID_1, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.song.GROUP_ID_2, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'song_id', 'property_id': obj_prop.trigger.song.SONG_ID, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False},
            {'type': 'song_channel', 'property_id': obj_prop.trigger.song.CHANNEL, 'default': 0, 'min': 0, 'max': 4, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.SONG_EDIT: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.song.GROUP_ID_1, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.song.GROUP_ID_2, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.SFX: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.sfx.GROUP_ID_1, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.sfx.GROUP_ID_2, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'sfx_id', 'property_id': obj_prop.trigger.sfx.SFX_ID, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False},
            {'type': 'unique_sfx_id', 'property_id': obj_prop.trigger.sfx.UNIQUE_ID, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False},
            {'type': 'sfx_group', 'property_id': obj_prop.trigger.sfx.GROUP_ID, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.SFX_EDIT: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.sfx.GROUP_ID_1, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.sfx.GROUP_ID_2, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.sfx.GROUP, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.ROTATE: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.rotate.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.rotate.ROTATE_TARGET, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.rotate.AIM_TARGET, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.rotate.MIN_X_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.rotate.MIN_Y_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.rotate.MAX_X_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.rotate.MAX_Y_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.FOLLOW: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.follow.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.follow.FOLLOW_TARGET, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.ANIMATE: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.animate.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.TOUCH: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.touch.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.COUNT: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.count.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.count.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.INSTANT_COUNT: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.instant_count.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.instant_count.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.FOLLOW_PLAYER_Y: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.follow_player_y.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.COLLISION: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collision.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'collision_id', 'property_id': obj_prop.trigger.collision.BLOCK_A, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'collision_id', 'property_id': obj_prop.trigger.collision.BLOCK_B, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.RANDOM: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.random.TRUE_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.random.FALSE_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.END_WALL: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.end_wall.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.CAMERA_EDGE: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.camera_edge.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.CHECKPOINT: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.checkpoint.SPAWN_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.checkpoint.TARGET_POS, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.checkpoint.RESPAWN_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.SCALE: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.scale.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.scale.CENTER_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.ADV_FOLLOW: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.adv_follow.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.adv_follow.FOLLOW_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.adv_follow.MAX_RANGE_REF, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.adv_follow.START_SPEED_REF, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.adv_follow.START_DIR_REF, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.KEYFRAME: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.keyframe.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.keyframe.SPAWN_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'keyframe_id', 'property_id': obj_prop.trigger.keyframe.KEY_ID, 'default': 0, 'min': 0, 'max': 2147483647, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.ANIMATE_KEYFRAME: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.animate_keyframe.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.animate_keyframe.PARENT_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.animate_keyframe.ANIMATION_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.END: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.end.SPAWN_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.end.TARGET_POS, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.EVENT: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.event.SPAWN_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'material_id', 'property_id': obj_prop.trigger.event.EXTRA_ID_1, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.SPAWN_PARTICLE: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.spawn_particle.PARTICLE_GROUP, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.spawn_particle.POSITION_GROUP, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.INSTANT_COLLISION: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.instant_collision.TRUE_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.instant_collision.FALSE_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'collision_id', 'property_id': obj_prop.trigger.instant_collision.BLOCK_A, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'collision_id', 'property_id': obj_prop.trigger.instant_collision.BLOCK_B, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.UI: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.ui.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.ui.UI_TARGET, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.TIME: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.time.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'time_id', 'property_id': obj_prop.trigger.time.ITEM_ID, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.TIME_EVENT: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.time_event.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'time_id', 'property_id': obj_prop.trigger.time_event.ITEM_ID, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.RESET: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.reset.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.OBJECT_CONTROL: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.object_control.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.LINK_VISIBLE: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.link_visible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.ITEM_COMPARE: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.item_compare.TRUE_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.item_compare.FALSE_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.item_compare.ITEM_ID_1, 'condition': lambda x: x.get(obj_prop.trigger.item_compare.ITEM_TYPE_1,0) in (0,1), 'default': 0, 'min': 0, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'time_id', 'property_id': obj_prop.trigger.item_compare.ITEM_ID_1, 'condition': lambda x: x.get(obj_prop.trigger.item_compare.ITEM_TYPE_1,0) == 2, 'default': 0, 'min': 0, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.item_compare.ITEM_ID_2, 'condition': lambda x: x.get(obj_prop.trigger.item_compare.ITEM_TYPE_2,0) in (0,1), 'default': 0, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'time_id', 'property_id': obj_prop.trigger.item_compare.ITEM_ID_2, 'condition': lambda x: x.get(obj_prop.trigger.item_compare.ITEM_TYPE_2,0) == 2, 'default': 0, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.STATE_BLOCK: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.state_block.STATE_ON, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.state_block.STATE_OFF, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.STATIC_CAMERA: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.static_camera.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.GRADIENT: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.gradient.U, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.gradient.D, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.gradient.L, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.gradient.R, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'gradient_id', 'property_id': obj_prop.trigger.gradient.GRADIENT_ID, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.shader.SHOCKWAVE: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.shader.SHOCKWAVE_CENTER_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.shader.SHOCKLINE: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.shader.SHOCKLINE_CENTER_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.shader.BULGE: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.shader.BULGE_CENTER_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.shader.PINCH: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.shader.PINCH_CENTER_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.STOP: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.stop.TARGET_ID, 'condition': lambda x: x.get(obj_prop.trigger.stop.USE_CONTROL_ID,0)== 0, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'control_id', 'property_id': obj_prop.trigger.stop.TARGET_ID, 'condition': lambda x: x.get(obj_prop.trigger.stop.USE_CONTROL_ID,0) == 1, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.SEQUENCE: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.sequence.SEQUENCE, 'function': lambda x: x.keys(), 'replace': lambda x, kvm: x.apply(lambda i: i.remap(key_map=kvm)), 'min': 1, 'max': 9999, 'remappable': False, 'iterable': True}
        ],
    obj_id.trigger.ADV_RANDOM: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.adv_random.TARGETS, 'function': lambda x: x.keys(), 'replace': lambda x, kvm: x.apply(lambda i: i.remap(key_map=kvm)), 'min': 1, 'max': 9999, 'remappable': False, 'iterable': True}
        ],
    obj_id.trigger.EDIT_ADV_FOLLOW: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.edit_adv_follow.TARGET_ID, 'condition': lambda x: x.get(obj_prop.trigger.edit_adv_follow.USE_CONTROL_ID,0) == 0, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.edit_adv_follow.SPEED_REF, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.edit_adv_follow.DIR_REF, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'control_id', 'property_id': obj_prop.trigger.edit_adv_follow.TARGET_ID, 'condition': lambda x: x.get(obj_prop.trigger.edit_adv_follow.USE_CONTROL_ID,0) == 1, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.RETARGET_ADV_FOLLOW: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.edit_adv_follow.TARGET_ID, 'condition': lambda x: x.get(obj_prop.trigger.edit_adv_follow.USE_CONTROL_ID,0) == 0, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.edit_adv_follow.FOLLOW_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'control_id', 'property_id': obj_prop.trigger.edit_adv_follow.TARGET_ID, 'condition': lambda x: x.get(obj_prop.trigger.edit_adv_follow.USE_CONTROL_ID,0) == 1, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.collectible.USER_COIN: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.collectible.KEY: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    1587: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    1589: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    1598: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.collectible.SMALL_COIN: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    3601: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4401: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4402: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4403: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4404: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4405: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4406: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4407: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4408: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4409: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4410: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4411: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4412: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4413: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4414: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4415: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4416: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4417: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4418: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4419: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4420: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4421: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4422: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4423: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4424: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4425: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4426: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4427: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4428: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4429: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4430: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4431: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4432: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4433: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4434: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4435: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4436: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4437: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4438: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4439: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4440: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4441: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4442: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4443: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4444: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4445: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4446: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4447: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4448: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4449: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4450: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4451: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4452: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4453: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4454: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4455: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4456: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4457: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4458: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4459: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4460: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4461: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4462: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4463: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4464: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4465: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4466: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4467: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4468: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4469: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4470: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4471: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4472: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4473: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4474: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4475: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4476: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4477: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4478: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4479: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4480: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4481: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4482: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4483: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4484: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4485: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4486: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4487: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4488: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4538: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4489: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4490: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4491: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4492: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4493: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4494: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4495: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4496: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4497: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4537: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4498: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4499: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4500: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4501: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4502: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4503: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4504: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4505: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4506: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4507: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4508: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4509: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4510: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4511: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4512: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4513: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4514: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4515: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4516: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4517: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4518: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4519: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4520: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4521: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4522: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4523: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4524: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4525: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4526: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4527: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4528: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4529: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4530: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4531: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4532: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4533: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4534: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4535: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4536: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4539: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.GROUP_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.collectible.PARTICLE   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.collectible.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.area.MOVE: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.effect.CENTER_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.effect.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'effect_id', 'property_id': obj_prop.trigger.effect.EFFECT_ID, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.area.SCALE: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.effect.CENTER_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.effect.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'effect_id', 'property_id': obj_prop.trigger.effect.EFFECT_ID, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.area.ROTATE: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.effect.CENTER_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.effect.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'effect_id', 'property_id': obj_prop.trigger.effect.EFFECT_ID, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.area.FADE: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.effect.CENTER_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': obj_prop.trigger.effect.TARGET_ID, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'effect_id', 'property_id': obj_prop.trigger.effect.EFFECT_ID, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.area.MOVE_EDIT: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.effect.TARGET_ID, 'condition': lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 0, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.area.SCALE_EDIT: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.effect.TARGET_ID, 'condition': lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 1, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.area.ROTATE_EDIT: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.effect.TARGET_ID, 'condition': lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 2, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.area.FADE_EDIT: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.effect.TARGET_ID, 'condition': lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 3, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.area.TINT_EDIT: [
            {'type': 'group_id', 'property_id': obj_prop.trigger.effect.TARGET_ID, 'condition': lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 4, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.ITEM_EDIT: [
            {'type': 'item_id', 'property_id': obj_prop.trigger.item_edit.TARGET_ITEM_ID, 'condition': lambda x: x.get(obj_prop.trigger.item_edit.ITEM_TYPE_3,0) in (0,1), 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'time_id', 'property_id': obj_prop.trigger.item_edit.TARGET_ITEM_ID, 'condition': lambda x: x.get(obj_prop.trigger.item_edit.ITEM_TYPE_3,0) == 2, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.item_edit.ITEM_ID_1, 'condition': lambda x: x.get(obj_prop.trigger.item_edit.ITEM_TYPE_1,0) in (0,1), 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'time_id', 'property_id': obj_prop.trigger.item_edit.ITEM_ID_1, 'condition': lambda x: x.get(obj_prop.trigger.item_edit.ITEM_TYPE_1,0) == 2, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'item_id', 'property_id': obj_prop.trigger.item_edit.ITEM_ID_2, 'condition': lambda x: x.get(obj_prop.trigger.item_edit.ITEM_TYPE_2,0) in (0,1), 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'time_id', 'property_id': obj_prop.trigger.item_edit.ITEM_ID_2, 'condition': lambda x: x.get(obj_prop.trigger.item_edit.ITEM_TYPE_2,0) == 2, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.ITEM_LABEL: [
            {'type': 'item_id', 'property_id': obj_prop.item_label.ITEM_ID, 'condition': lambda x: x.get(obj_prop.item_label.TIME_COUNTER,0) == 0, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'time_id', 'property_id': obj_prop.item_label.ITEM_ID, 'condition': lambda x: x.get(obj_prop.item_label.TIME_COUNTER,0) == 1, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.PICKUP: [
            {'type': 'item_id', 'property_id': obj_prop.trigger.pickup.ITEM_ID, 'default': 0, 'min': 0, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.TIME_CONTROL: [
            {'type': 'time_id', 'property_id': obj_prop.trigger.time_control.ITEM_ID, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.ITEM_PERSIST: [
            {'type': 'item_id', 'property_id': obj_prop.trigger.item_persist.ITEM_ID, 'condition': lambda x: x.get(obj_prop.trigger.item_persist.TIMER,0) == 0, 'default': 0, 'min': 0, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'time_id', 'property_id': obj_prop.trigger.item_persist.ITEM_ID, 'condition': lambda x: x.get(obj_prop.trigger.item_persist.TIMER,0) == 1, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.COLLISION_BLOCK: [
            {'type': 'collision_id', 'property_id': obj_prop.trigger.collision_block.BLOCK_ID, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.ARROW: [
            {'type': 'trigger_channel', 'property_id': obj_prop.trigger.arrow.TARGET_CHANNEL, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.START_POS: [
            {'type': 'trigger_channel', 'property_id': obj_prop.start_pos.TARGET_CHANNEL, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.area.STOP: [
            {'type': 'effect_id', 'property_id': obj_prop.trigger.effect.TARGET_ID, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.enter.MOVE: [
            {'type': 'effect_id', 'property_id': obj_prop.trigger.effect.EFFECT_ID, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'type': 'enter_channel', 'property_id': obj_prop.trigger.effect.ENTER_CHANNEL, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.enter.SCALE: [
            {'type': 'effect_id', 'property_id': obj_prop.trigger.effect.EFFECT_ID, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'type': 'enter_channel', 'property_id': obj_prop.trigger.effect.ENTER_CHANNEL, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.enter.ROTATE: [
            {'type': 'effect_id', 'property_id': obj_prop.trigger.effect.EFFECT_ID, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'type': 'enter_channel', 'property_id': obj_prop.trigger.effect.ENTER_CHANNEL, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.enter.FADE: [
            {'type': 'effect_id', 'property_id': obj_prop.trigger.effect.EFFECT_ID, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'type': 'enter_channel', 'property_id': obj_prop.trigger.effect.ENTER_CHANNEL, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.enter.STOP: [
            {'type': 'effect_id', 'property_id': obj_prop.trigger.effect.EFFECT_ID, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'type': 'enter_channel', 'property_id': obj_prop.trigger.effect.ENTER_CHANNEL, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.area.EDIT_MOVE: [
            {'type': 'effect_id', 'property_id': obj_prop.trigger.effect.TARGET_ID, 'condition': lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 1, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.area.EDIT_SCALE: [
            {'type': 'effect_id', 'property_id': obj_prop.trigger.effect.TARGET_ID, 'condition': lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 1, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.area.EDIT_ROTATE: [
            {'type': 'effect_id', 'property_id': obj_prop.trigger.effect.TARGET_ID, 'condition': lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 1, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.area.EDIT_FADE: [
            {'type': 'effect_id', 'property_id': obj_prop.trigger.effect.TARGET_ID, 'condition': lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 1, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.area.EDIT_TINT: [
            {'type': 'effect_id', 'property_id': obj_prop.trigger.effect.TARGET_ID, 'condition': lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 1, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    22: [
            {'type': 'enter_channel', 'property_id': obj_prop.trigger.enter_preset.ENTER_CHANNEL, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    24: [
            {'type': 'enter_channel', 'property_id': obj_prop.trigger.enter_preset.ENTER_CHANNEL, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    23: [
            {'type': 'enter_channel', 'property_id': obj_prop.trigger.enter_preset.ENTER_CHANNEL, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    25: [
            {'type': 'enter_channel', 'property_id': obj_prop.trigger.enter_preset.ENTER_CHANNEL, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    26: [
            {'type': 'enter_channel', 'property_id': obj_prop.trigger.enter_preset.ENTER_CHANNEL, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    27: [
            {'type': 'enter_channel', 'property_id': obj_prop.trigger.enter_preset.ENTER_CHANNEL, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    28: [
            {'type': 'enter_channel', 'property_id': obj_prop.trigger.enter_preset.ENTER_CHANNEL, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    55: [
            {'type': 'enter_channel', 'property_id': obj_prop.trigger.enter_preset.ENTER_CHANNEL, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    56: [
            {'type': 'enter_channel', 'property_id': obj_prop.trigger.enter_preset.ENTER_CHANNEL, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    57: [
            {'type': 'enter_channel', 'property_id': obj_prop.trigger.enter_preset.ENTER_CHANNEL, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    58: [
            {'type': 'enter_channel', 'property_id': obj_prop.trigger.enter_preset.ENTER_CHANNEL, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    59: [
            {'type': 'enter_channel', 'property_id': obj_prop.trigger.enter_preset.ENTER_CHANNEL, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    1915: [
            {'type': 'enter_channel', 'property_id': obj_prop.trigger.enter_preset.ENTER_CHANNEL, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.EDIT_SFX: [
            {'type': 'unique_sfx_id', 'property_id': obj_prop.trigger.sfx.UNIQUE_ID, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False},
            {'type': 'sfx_group', 'property_id': obj_prop.trigger.sfx.GROUP_ID, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.EDIT_SONG: [
            {'type': 'song_channel', 'property_id': obj_prop.trigger.song.CHANNEL, 'default': 0, 'min': 0, 'max': 4, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.FORCE_BLOCK: [
            {'type': 'force_id', 'property_id': obj_prop.trigger.force_block.FORCE_ID, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.FORCE_CIRCLE: [
            {'type': 'force_id', 'property_id': obj_prop.trigger.force_block.FORCE_ID, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': False, 'iterable': False}
        ]
    }


def filter_rules(condition:callable, rule_list=ID_RULES):
    
    new_dict = {}
    
    for key, value in rule_list.items():
        
        new_list = []
        
        for item in value:
            
            if condition(item):
                
                new_list.append(item)
            
        if new_list != []:
            
            new_dict[key] = new_list
            
    return new_dict
