module Ticker exposing (main)

import Browser exposing (element)
import Html exposing (Html, div, text)
import Html.Attributes exposing (style)
import Http exposing (Error)
import Json.Decode exposing (..)
import Svg exposing (svg, polyline)
import Svg.Attributes exposing (points, fill, stroke, strokeWidth, viewBox)
import Time exposing (every)

type alias State = {
    prices : List Float,
    status : Status
  }

type Status = Loading | Error String | Loaded Float

init : () -> ( State, Cmd Event )
init _ = ( { prices = [], status = Loading }, fetchPrice )

type Event = Tick | GotPrice (Result Http.Error Float)

update : Event -> State -> ( State, Cmd Event )
update event state = Debug.todo "update"

fetchPrice : Cmd Event
fetchPrice =
    Http.get {
        url = "https://api.coinbase.com/v2/prices/BTC-USD/spot",
        expect = Http.expectJson GotPrice priceDecoder
      }

priceDecoder : Json.Decode.Decoder Float
priceDecoder = Json.Decode.at ["data", "amount"] Json.Decode.string
    |> Json.Decode.andThen (\s -> case String.toFloat s of
        Just f -> Json.Decode.succeed f
        Nothing -> Json.Decode.fail "Invalid price")

subscriptions : State -> Sub Event
subscriptions _ = Time.every 2000 (\_ -> Tick)

view : State -> Html Event
view state = div [ style "padding" "20px", style "font-family" "sans-serif" ] [
    viewStatus state.status,
    viewGraph state.prices
  ]

viewStatus : Status -> Html Event
viewStatus status = case status of
    Loading -> div [ style "font-size" "36px", style "margin" "20px 0" ] [
        text "Loading..."
      ]
    Error msg -> div [ style "color" "red", style "margin" "20px 0" ] [
        text msg
      ]
    Loaded price -> div [ style "font-size" "36px", style "margin" "20px 0", style "font-weight" "bold" ] [
        text ("$" ++ String.fromFloat price)
      ]

viewGraph : List Float -> Html Event
viewGraph prices = if List.isEmpty prices
    then
        div [] []
    else
      let
          minPrice = List.minimum prices |> Maybe.withDefault 0
          maxPrice = List.maximum prices |> Maybe.withDefault 0
          range = maxPrice - minPrice
          scale = if range > 0 then 100 / range else 1
          pointsString = prices
              |> List.indexedMap (\i p ->
                  String.fromInt (i * 10) ++ "," ++ String.fromFloat (100 - (p - minPrice) * scale))
              |> String.join " "
      in svg [
          viewBox "0 0 300 120",
          style "width" "600px",
          style "height" "240px",
          style "border" "1px solid #ccc",
          style "margin-top" "20px"
        ] [
          polyline [
              points pointsString,
              fill "none",
              stroke "#3498db",
              strokeWidth "2"
            ] []
        ]

main : Program () State Event
main = Browser.element {
    init = init,
    update = update,
    view = view,
    subscriptions = subscriptions
  }

