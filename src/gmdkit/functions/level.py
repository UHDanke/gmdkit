# Package Imports
from gmdkit.models.level import Level
from gmdkit.utils.enums import (
    LevelDifficulty, LevelRating, DemonRating,
    EpicRating, FeatureRating,
    TimelyType
)

def get_difficulty_rating(level:Level) -> LevelDifficulty:
    """
    Gets the difficulty rating of a level.

    Parameters
    ----------
    level : Level
        The level to check.

    Returns
    -------
    LevelDifficulty
        An enum specifying the level's difficulty.

    """
    if level.rating == 0:
        return LevelDifficulty.NA

    match level.rating_sum:

        case LevelRating.NONE:
            return LevelDifficulty.NA

        case LevelRating.EASY:
            if level.is_auto:
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
            if level.is_demon:

                match level.demon_type:

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
    """
    Gets the feature rating of a level.

    Parameters
    ----------
    level : Level
        The level to check.

    Returns
    -------
    FeatureRating
        An enum specifying the level's feature rating.

    """
    match level.epic_rating:

        case EpicRating.EPIC:
            return FeatureRating.EPIC

        case EpicRating.LEGENDARY:
            return FeatureRating.LEGENDARY

        case EpicRating.MYTHIC:
            return FeatureRating.MYTHIC

        case _:
            if level.feature_score:
                return FeatureRating.FEATURED

            elif level.stars:
                return FeatureRating.RATED

            else:
                return FeatureRating.UNRATED


def get_timely_type(level:Level) -> TimelyType:
    """
    Gets the timely (daily, weekly, event) type of a level.

    Parameters
    ----------
    level : Level
        The level to check.

    Returns
    -------
    TimelyType
        An enum specifying the level's timely type.

    """
    tid = level.timely_id

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
