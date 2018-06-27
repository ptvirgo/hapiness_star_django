module Main exposing (..)

import Html exposing (program, programWithFlags)
import Model exposing (..)

import Model exposing (..)
import View exposing (viewModel)
import Control exposing (updateModel, Msg(..), saveStar, nullStarInput)

withJwt : String -> (Model, Cmd Msg)
withJwt jwt =
    (
    { star = Nothing
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
