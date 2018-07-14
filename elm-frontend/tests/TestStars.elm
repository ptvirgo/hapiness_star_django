module TestStars exposing (..)

import Expect exposing (Expectation)
import Fuzz exposing (Fuzzer, intRange, list, string)
import Test exposing (..)
import Random.Pcg as Random
import Shrink

import Model exposing (..)
import View exposing (..)
import Control exposing (..)

tag : Fuzzer Tag
tag = string

randomDateString : Random.Generator String
randomDateString =
    let stringify =
        (\year month day -> toString year ++ "-" ++ toString month ++ "-" ++ toString day)
    in
        ( Random.map3 stringify
            (Random.int 2015 2030)
            (Random.int 1 12)
            (Random.int 1 28)
        )

randomStar : Fuzzer Star
randomStar = Fuzz.custom
    ( Random.map Star (Random.int 1 5)
    |> Random.andMap (Random.int 1 5)
    |> Random.andMap (Random.int 1 5)
    |> Random.andMap (Random.int 1 5)
    |> Random.andMap (Random.int 1 5)
    |> Random.andMap (Random.int 1 5)
    |> Random.andMap (randomDateString)
    )
    (\star -> Shrink.map Star (Shrink.int star.spirit)
        |> Shrink.andMap (Shrink.int star.exercise)
        |> Shrink.andMap (Shrink.int star.play)
        |> Shrink.andMap (Shrink.int star.work)
        |> Shrink.andMap (Shrink.int star.friends)
        |> Shrink.andMap (Shrink.int star.adventure)
        |> Shrink.andMap (Shrink.string star.date)
    )

suite : Test
suite = describe "Stars Front-End"
    [ testUpdates ]


testUpdates : Test
testUpdates = describe "Update Messages"
    []
