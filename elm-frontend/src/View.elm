module View exposing (viewModel)

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)

import Model exposing (..)
import Control exposing (..)

viewModel : Model -> Html Msg
viewModel model = div
    []
    [ viewStar model.star
    , viewError model.error
    ]

yellowStar : String
yellowStar = "/static/happiness_star/gold_star.svg"

greyStar : String
greyStar = "/static/happiness_star/grey_star.svg"

{-| Display the Star -}
viewStar : Star -> Html Msg
viewStar star = div
    [ id "StarDiv" ]
    [ table []
        [ tr []
            [ td [] []
            , td [] [ h1 [] [ text ("Stars for " ++ star.date) ] ]
            ]
        , ratingField Spirit star.spirit 
        , ratingField Exercise star.exercise 
        , ratingField Play star.play 
        , ratingField Work star.work
        , ratingField Friends star.friends
        , ratingField Adventure star.adventure
        ]
    ]

{-| Display interface to update a single Point -}

ratingField : Point -> Rating -> Html Msg
ratingField point rating =
    tr [ class "starRating" ]
        [ td [] [ text (toString point) ]
        , td [] 
            ( List.foldr
                (\x elems ->
                    text " " ::
                    img [ src ( if x > rating then greyStar else yellowStar)
                        , onClick (Update point x)
                        ]
                        [] ::
                    elems
                )
                []
                (List.range 1 5)
            )
        ]

viewError : Maybe String -> Html msg
viewError err = case err of
    Just message -> p [ class "error" ] [ text message ]
    Nothing -> text ""

-- Helpers
