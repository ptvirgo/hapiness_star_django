module Control exposing (..)

import GraphQL.Request.Builder exposing (..)
import GraphQL.Request.Builder.Arg as Arg
import GraphQL.Request.Builder.Variable as Var
import GraphQL.Client.Http as GraphQLClient
import Task exposing (Task)

import Model exposing (..)

type Msg = Update Point Rating | NewStar Star | GotError String

updateModel : Msg -> Model -> (Model, Cmd Msg)
updateModel msg model = case msg of
    (Update pt x) -> updatePoint pt x model
    (NewStar star) -> ({ model | star = Just star, error = Nothing }, Cmd.none )
    (GotError err) -> ({ model | error = Just err }, Cmd.none )

updatePoint : Point -> Rating -> Model -> (Model, Cmd Msg)
updatePoint pt x model = (model, saveStarInput model.jwt pt x |> saveStar)

type alias StarInput =
    { token : String
    , spirit : Maybe Int
    , exercise : Maybe Int
    , play : Maybe Int
    , work : Maybe Int
    , friends : Maybe Int
    , adventure : Maybe Int
    }

nullStarInput : String -> StarInput
nullStarInput jwt =
    { token = jwt
    , spirit = Nothing
    , exercise = Nothing
    , play = Nothing
    , work = Nothing
    , friends = Nothing
    , adventure = Nothing
    }

saveStarGQL : Document Mutation Star StarInput
saveStarGQL =
    let
        -- arguments parsed from a provided record
        jwt = Var.required "token" .token Var.string
        spirit = Var.required "spirit" .spirit (Var.nullable Var.int)
        exercise = Var.required "exercise" .exercise (Var.nullable Var.int)
        play = Var.required "play" .play (Var.nullable Var.int)
        work = Var.required "work" .work (Var.nullable Var.int)
        friends = Var.required "friends" .friends (Var.nullable Var.int)
        adventure = Var.required "adventure" .adventure (Var.nullable Var.int)

        -- this decodes the response
        star =
            object Star
                |> with (field "spirit" [] int)
                |> with (field "exercise" [] int)
                |> with (field "play" [] int)
                |> with (field "work" [] int)
                |> with (field "friends" [] int)
                |> with (field "adventure" [] int)
                |> with (field "date" [] string)

        mutationRoot =
            extract
                (field "saveStar"
                    [ ( "token", Arg.variable jwt )
                    , ( "spirit", Arg.variable spirit )
                    , ( "exercise", Arg.variable exercise )
                    , ( "play", Arg.variable play )
                    , ( "work", Arg.variable work )
                    , ( "friends", Arg.variable friends )
                    , ( "adventure", Arg.variable adventure )
                    ]
                    star
                )
    in
        mutationDocument mutationRoot

saveStarInput : String -> Point -> Rating -> StarInput
saveStarInput token pt x =
    let nsi = nullStarInput token in case pt of
    Spirit -> { nsi | spirit = Just x }
    Exercise -> { nsi | exercise = Just x }
    Play -> { nsi | play = Just x }
    Work -> { nsi | work = Just x }
    Friends -> { nsi | friends = Just x }
    Adventure-> { nsi | adventure = Just x }

recieveStar : Result GraphQLClient.Error Star -> Msg
recieveStar res = case res of
    Err (GraphQLClient.HttpError err)-> GotError (toString err)
    Err (GraphQLClient.GraphQLError err)-> GotError (toString err)
    Ok star -> NewStar star

saveStar : StarInput -> Cmd Msg
saveStar input = saveStarGQL
    |> request input
    |> GraphQLClient.sendMutation "/graphql/?"
    |> Task.attempt recieveStar
