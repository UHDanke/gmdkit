# Package Imports
from gmdkit.mappings import lvl_prop
from gmdkit.models.level import Level
from gmdkit.serialization.enums import (
    LevelDifficulty, LevelRating, DemonRating, 
    EpicRating, FeatureRating,
    TimelyType
)

def get_difficulty_rating(level:Level) -> LevelDifficulty:
    if level.get(lvl_prop.RATING,0) == 0:
        return LevelDifficulty.NA
    
    match level.get(lvl_prop.RATING_SUM, 0):
        
        case LevelRating.NONE:
            return LevelDifficulty.NA
        
        case LevelRating.EASY:
            if level.get(lvl_prop.IS_AUTO,False):
                return LevelDifficulty.AUTO
            else:
                return LevelDifficulty.EASY
            
        case LevelRating.NORMAL:
            return LevelDifficulty.NORMAL
        
        case LevelRating.HARD:
            return LevelDifficulty.HARD
        
        case LevelRating.HARDER:
            return LevelDifficulty.HARDER
        
        case LevelRating.INSANE:
            if level.get(lvl_prop.IS_DEMON,False):
                
                match level.get(lvl_prop.DEMON_TYPE,0):
                    
                    case DemonRating.EASY:
                        return LevelDifficulty.EASY_DEMON
                    
                    case DemonRating.MEDIUM:
                        return LevelDifficulty.MEDIUM_DEMON
                    
                    case DemonRating.HARD:
                        return LevelDifficulty.HARD_DEMON
                    
                    case DemonRating.INSANE:
                        return LevelDifficulty.INSANE_DEMON
                    
                    case DemonRating.EXTREME:
                        return LevelDifficulty.EXTREME_DEMON
                    
                    case _:
                        return LevelDifficulty.HARD_DEMON
            else:
                return LevelDifficulty.INSANE
            
        case _:
            return LevelDifficulty.NA


def get_feature_rating(level:Level) -> FeatureRating:
    match level.get(lvl_prop.EPIC_RATING, 0):
        
        case EpicRating.EPIC:
            return FeatureRating.EPIC
        
        case EpicRating.LEGENDARY:
            return FeatureRating.LEGENDARY
        
        case EpicRating.MYTHIC:
            return FeatureRating.MYTHIC
        
        case _:
            if level.get(lvl_prop.FEATURE_SCORE,0):
                return FeatureRating.FEATURED
        
            elif level.get(lvl_prop.STARS,0):
                return FeatureRating.RATED
            
            else:
                return FeatureRating.UNRATED


def get_timely_type(level:Level) -> TimelyType:
    tid = level.get(lvl_prop.TIMELY_ID)
    
    if tid is None:
        return TimelyType.NONE
    elif (0<tid<=10000):
        return TimelyType.DAILY
    elif (10000<tid<=20000):
        return TimelyType.WEEKLY
    elif (20000<tid<=30000):
        return TimelyType.EVENT
    else:
        return TimelyType.NONE
