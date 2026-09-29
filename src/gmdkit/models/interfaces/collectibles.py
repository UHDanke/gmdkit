# Package Imports
from gmdkit.models.interfaces.base import (
    EffectObject, TriggerObject, Field, register_id
    )
from gmdkit.models.interfaces.animated import AnimatedObject


class CollectibleObject(TriggerObject):
    group_id: int = Field(51)
    sub_count: bool = Field(78)
    item_id: int = Field(80)
    pickup_item: bool = Field(381)
    toggle_trigger: bool = Field(382)
    points: int = Field(383)
    particle: int = Field(440)
    no_anim: bool = Field(463)
    
    
class SecretCoin(CollectibleObject):
    coin_id: int = Field(12)
    
    
class SmallCoin(AnimatedObject,CollectibleObject):
    pass


class UserCoin(AnimatedObject,EffectObject):
    pass


# CollectibleObject
register_id(1275, CollectibleObject)  # collectible.KEY
register_id(1329, CollectibleObject)  # collectible.USER_COIN
register_id(1587, CollectibleObject)  # Heart Collectable
register_id(1589, CollectibleObject)  # Potion Collectable
register_id(1598, CollectibleObject)  # Skull Collectable
register_id(1614, CollectibleObject)  # collectible.SMALL_COIN
register_id(3601, CollectibleObject)  # Clock Collectable
register_id(4401, CollectibleObject)  # Small Potion Pixel Collectable
register_id(4402, CollectibleObject)  # Medium Potion Pixel Collectable
register_id(4403, CollectibleObject)  # Large Potion Pixel Collectable
register_id(4404, CollectibleObject)  # Diagonal Key Pixel Collectable
register_id(4405, CollectibleObject)  # Round Key Pixel Collectable
register_id(4406, CollectibleObject)  # Flat Key Pixel Collectable
register_id(4407, CollectibleObject)  # Coin Pixel Collectable
register_id(4408, CollectibleObject)  # Small Coin Stack Pixel Collectable
register_id(4409, CollectibleObject)  # Large Coin Stack Pixel Collectable
register_id(4410, CollectibleObject)  # Candy Pixel Collectable
register_id(4411, CollectibleObject)  # Mushroom Pixel Collectable
register_id(4412, CollectibleObject)  # Bone Pixel Collectable
register_id(4413, CollectibleObject)  # Sphere Pixel Collectable
register_id(4414, CollectibleObject)  # Ingot Pixel Collectable
register_id(4415, CollectibleObject)  # Square Gem Pixel Collectable
register_id(4416, CollectibleObject)  # Hexagon Gem Pixel Collectable
register_id(4417, CollectibleObject)  # Octagon Gem Pixel Collectable
register_id(4418, CollectibleObject)  # Rectangle Gem Pixel Collectable
register_id(4419, CollectibleObject)  # Pointy Gem Pixel Collectable
register_id(4420, CollectibleObject)  # Diamond Pixel Collectable
register_id(4421, CollectibleObject)  # Fish Pixel Collectable
register_id(4422, CollectibleObject)  # Rocks Pixel Collectable
register_id(4423, CollectibleObject)  # Wood Pixel Collectable
register_id(4424, CollectibleObject)  # Egg Pixel Collectable
register_id(4425, CollectibleObject)  # Large Heart Pixel Collectable
register_id(4426, CollectibleObject)  # Small Heart Pixel Collectable
register_id(4427, CollectibleObject)  # Map Pixel Collectable
register_id(4428, CollectibleObject)  # Book Pixel Collectable
register_id(4429, CollectibleObject)  # Device Pixel Collectable
register_id(4430, CollectibleObject)  # Computer Pixel Collectable
register_id(4431, CollectibleObject)  # Large Skull Pixel Collectable
register_id(4432, CollectibleObject)  # Small Skull Pixel Collectable
register_id(4433, CollectibleObject)  # Speech Bubble Pixel Collectable
register_id(4434, CollectibleObject)  # Branch Pixel Collectable
register_id(4435, CollectibleObject)  # Shard Gem Pixel Collectable
register_id(4436, CollectibleObject)  # Eye Pixel Collectable
register_id(4437, CollectibleObject)  # Eyeball Pixel Collectable
register_id(4438, CollectibleObject)  # Up Arrow Pixel Collectable
register_id(4439, CollectibleObject)  # Down Arrow Pixel Collectable
register_id(4440, CollectibleObject)  # Lightning Pixel Collectable
register_id(4441, CollectibleObject)  # No Symbol Pixel Collectable
register_id(4442, CollectibleObject)  # Gear Pixel Collectable
register_id(4443, CollectibleObject)  # Plus Pixel Collectable
register_id(4444, CollectibleObject)  # Plus Symbols Pixel Collectable
register_id(4445, CollectibleObject)  # Pebbles Pixel Collectable
register_id(4446, CollectibleObject)  # Present Pixel Collectable
register_id(4447, CollectibleObject)  # Chest Pixel Collectable
register_id(4448, CollectibleObject)  # Bag Pixel Collectable
register_id(4449, CollectibleObject)  # Backpack Pixel Collectable
register_id(4450, CollectibleObject)  # Bundle Pixel Collectable
register_id(4451, CollectibleObject)  # Ring Pixel Collectable
register_id(4452, CollectibleObject)  # Patterned Ring Pixel Collectable
register_id(4453, CollectibleObject)  # Gem Ring Pixel Collectable
register_id(4454, CollectibleObject)  # Large Necklace Pixel Collectable
register_id(4455, CollectibleObject)  # Small Necklace Pixel Collectable
register_id(4456, CollectibleObject)  # Shoe Pixel Collectable
register_id(4457, CollectibleObject)  # Boot Pixel Collectable
register_id(4458, CollectibleObject)  # Pointy Boot Pixel Collectable
register_id(4459, CollectibleObject)  # Hat Pixel Collectable
register_id(4460, CollectibleObject)  # Pointy Hat Pixel Collectable
register_id(4461, CollectibleObject)  # Curly Hat Pixel Collectable
register_id(4462, CollectibleObject)  # Helmet 1 Pixel Collectable
register_id(4463, CollectibleObject)  # Helmet 2 Pixel Collectable
register_id(4464, CollectibleObject)  # Helmet 3 Pixel Collectable
register_id(4465, CollectibleObject)  # Mask 1 Pixel Collectable
register_id(4466, CollectibleObject)  # Mask 2 Pixel Collectable
register_id(4467, CollectibleObject)  # Mask 3 Pixel Collectable
register_id(4468, CollectibleObject)  # Round Mask Pixel Collectable
register_id(4469, CollectibleObject)  # Horned Round Mask Pixel Collectable
register_id(4470, CollectibleObject)  # Small Lab Coat Pixel Collectable
register_id(4471, CollectibleObject)  # Large Lab Coat Pixel Collectable
register_id(4472, CollectibleObject)  # Armor 1 Pixel Collectable
register_id(4473, CollectibleObject)  # Armor 2 Pixel Collectable
register_id(4474, CollectibleObject)  # Armor 3 Pixel Collectable
register_id(4475, CollectibleObject)  # Armor 4 Pixel Collectable
register_id(4476, CollectibleObject)  # Armor 5 Pixel Collectable
register_id(4477, CollectibleObject)  # Armor 6 Pixel Collectable
register_id(4478, CollectibleObject)  # Shield 1 Pixel Collectable
register_id(4479, CollectibleObject)  # Shield 2 Pixel Collectable
register_id(4480, CollectibleObject)  # Shield 3 Pixel Collectable
register_id(4481, CollectibleObject)  # Shield 4 Pixel Collectable
register_id(4482, CollectibleObject)  # Shield 5 Pixel Collectable
register_id(4483, CollectibleObject)  # Shield 6 Pixel Collectable
register_id(4484, CollectibleObject)  # Shield 7 Pixel Collectable
register_id(4485, CollectibleObject)  # Shield 8 Pixel Collectable
register_id(4486, CollectibleObject)  # Shield 9 Pixel Collectable
register_id(4487, CollectibleObject)  # Sword Pixel Collectable
register_id(4488, CollectibleObject)  # Bow Pixel Collectable
register_id(4489, CollectibleObject)  # Axe Pixel Collectable
register_id(4490, CollectibleObject)  # Spear Pixel Collectable
register_id(4491, CollectibleObject)  # Large Staff Pixel Collectable
register_id(4492, CollectibleObject)  # Shovel Pixel Collectable
register_id(4493, CollectibleObject)  # Pickaxe Pixel Collectable
register_id(4494, CollectibleObject)  # Hammer Pixel Collectable
register_id(4495, CollectibleObject)  # Hoe Pixel Collectable
register_id(4496, CollectibleObject)  # Small Staff Pixel Collectable
register_id(4497, CollectibleObject)  # Hook Pixel Collectable
register_id(4498, CollectibleObject)  # Exclamation Point Pixel Collectable
register_id(4499, CollectibleObject)  # Question Mark Pixel Collectable
register_id(4500, CollectibleObject)  # Plus Sign Pixel Collectable
register_id(4501, CollectibleObject)  # Minus Sign Pixel Collectable
register_id(4502, CollectibleObject)  # Equals Sign Pixel Collectable
register_id(4503, CollectibleObject)  # Times Sign Pixel Collectable
register_id(4504, CollectibleObject)  # Division Sign Pixel Collectable
register_id(4505, CollectibleObject)  # Numeral 0 Pixel Collectable
register_id(4506, CollectibleObject)  # Numeral 1 Pixel Collectable
register_id(4507, CollectibleObject)  # Numeral 2 Pixel Collectable
register_id(4508, CollectibleObject)  # Numeral 3 Pixel Collectable
register_id(4509, CollectibleObject)  # Numeral 4 Pixel Collectable
register_id(4510, CollectibleObject)  # Numeral 5 Pixel Collectable
register_id(4511, CollectibleObject)  # Numeral 6 Pixel Collectable
register_id(4512, CollectibleObject)  # Numeral 7 Pixel Collectable
register_id(4513, CollectibleObject)  # Numeral 8 Pixel Collectable
register_id(4514, CollectibleObject)  # Numeral 9 Pixel Collectable
register_id(4515, CollectibleObject)  # Animal Skull Pixel Collectable
register_id(4516, CollectibleObject)  # Cracked Skull Pixel Collectable
register_id(4517, CollectibleObject)  # Small Bone Pixel Collectable
register_id(4518, CollectibleObject)  # Large Key Pixel Collectable
register_id(4519, CollectibleObject)  # Keyhole Chest Pixel Collectable
register_id(4520, CollectibleObject)  # Bread Pixel Collectable
register_id(4521, CollectibleObject)  # Small Diamond Pixel Collectable
register_id(4522, CollectibleObject)  # Cloak Pixel Collectable
register_id(4523, CollectibleObject)  # Scroll Pixel Collectable
register_id(4524, CollectibleObject)  # Banner Pixel Collectable
register_id(4525, CollectibleObject)  # Bomb Pixel Collectable
register_id(4526, CollectibleObject)  # Metal Nugget Pixel Collectable
register_id(4527, CollectibleObject)  # Small Arrow Pixel Collectable
register_id(4528, CollectibleObject)  # Large Arrow Pixel Collectable
register_id(4529, CollectibleObject)  # Cheese Pixel Collectable
register_id(4530, CollectibleObject)  # Apple Pixel Collectable
register_id(4531, CollectibleObject)  # Carrot Pixel Collectable
register_id(4532, CollectibleObject)  # Steak Pixel Collectable
register_id(4533, CollectibleObject)  # Fire Pixel Collectable
register_id(4534, CollectibleObject)  # Wave Pixel Collectable
register_id(4535, CollectibleObject)  # Spike Pixel Collectable
register_id(4536, CollectibleObject)  # Cauldron Pixel Collectable
register_id(4537, CollectibleObject)  # Fishing Rod Pixel Collectable
register_id(4538, CollectibleObject)  # Pointy Bow Pixel Collectable
register_id(4539, CollectibleObject)  # Floppy Disk Pixel Collectable

# SecretCoin
register_id(142, SecretCoin)  # Secret Coin

# SmallCoin
register_id(1614, SmallCoin)  # Small Coin Collectable

# UserCoin
register_id(1329, UserCoin)  # User Coin
