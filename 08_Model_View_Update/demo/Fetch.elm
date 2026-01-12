module Fetch exposing (..)

import Browser
import Html exposing (Html, div, button, text)
import Html.Attributes exposing (style)
import Html.Events exposing (onClick)
import Http exposing (Expect, expectString, Error)

type Model = Initial | Started | Failed String | One Int | Both Int Int

type Event = PerformRequest | HandleResponse String | HandleError Error

init : () -> ( Model, Cmd Event )
init _ = ( Initial, Cmd.none )

expectEvent : Expect Event
expectEvent = expectString (\result -> case result of
    Ok str -> HandleResponse str
    Err err -> HandleError err
  )

request1 : Cmd Event
request1 = Http.get { url = "http://localhost:8001", expect = expectEvent }

request2 : Cmd Event
request2 = Http.get { url = "http://localhost:8002", expect = expectEvent }

update : Event -> Model -> ( Model, Cmd Event )
update event model = case event of
    PerformRequest ->
        ( Started, Cmd.batch [ request1, request2 ] )
    HandleResponse result -> case String.toInt result of
        Just n -> case model of
            One m -> ( Both m n, Cmd.none )
            _ -> ( One n, Cmd.none )
        Nothing -> ( Failed "Failed integer conversion", Cmd.none )
    HandleError error ->
        ( Failed (Debug.toString error) , Cmd.none )

view : Model -> Html Event
view model = div [ style "text-align" "center", style "margin-top" "100px" ] [
    button [ onClick PerformRequest ] [ text "Fetch and Add" ],
    div [] [ text (case model of
        Initial -> "Click to fetch"
        Started -> "Loading two..."
        Failed message -> "Failed " ++ message
        One _ -> "Loading one..."
        Both m n -> String.fromInt (m + n)
    ) ]
  ]

main = Browser.element {
    init = init,
    view = view,
    update = update,
    subscriptions = \_ -> Sub.none
  }

