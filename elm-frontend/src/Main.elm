module Main exposing (..)

import Html exposing (program, programWithFlags)
import Model exposing (..)

import Model exposing (..)
import View exposing (viewModel)
import Control exposing (updateModel, Msg(..), saveStar, nullStarInput)

withJwt : String -> (Model, Cmd Msg)
withJwt jwt =
    (
    { star =
        { spirit = 3
        , exercise = 3
        , play = 3
        , work = 3
        , friends = 3
        , adventure = 3
        , date = "2001-1-1"
        }
    , jwt = jwt
    , error = Nothing
    }
    , saveStar (nullStarInput jwt)
    )

main = programWithFlags
    { init = withJwt
    , view = viewModel
    , update = updateModel
    , subscriptions = (\_ -> Sub.none)
    }
