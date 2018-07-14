module Model exposing (..)

{-| Tags |-}
type alias Tag = String

{-| Rating is a value, 1-5, associated with the area (Spirit, Exercise, etc)
tracked by the Star -}
type alias Rating = Int

{-| Point represents an area of life (Spirit, Exercise, etc) -}
type Point  = Spirit | Exercise | Play | Work | Friends | Adventure

-- Model

{-| Star assoctiates rating names and values -}
type alias Star =
    { spirit : Rating
    , exercise : Rating
    , play : Rating
    , work : Rating
    , friends : Rating
    , adventure : Rating
    , date : String
    }

type alias Model =
        { star : Maybe Star
        , jwt : String
        , error : Maybe String
        }
