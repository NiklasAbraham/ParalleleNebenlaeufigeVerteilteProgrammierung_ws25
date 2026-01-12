module Ticker exposing (..)

import Browser
import Html exposing (Html, div, text)
import Html.Attributes exposing (style)
import Time

type alias Model = Int

type Event = Tick

init : () -> ( Model, Cmd Event )
init _ = ( 0, Cmd.none )

update : Event -> Model -> ( Model, Cmd Event )
update event model = case event of
    Tick -> ( model + 1, Cmd.none )

view : Model -> Html Event
view model = div [ style "text-align" "center", style "margin-top" "100px", style "font-size" "10em" ] [
    text (String.fromInt model)
  ]

subscriptions : Model -> Sub Event
subscriptions _ = Time.every 1000 (always Tick)

main = Browser.element {
    init = init,
    update = update,
    view = view,
    subscriptions = subscriptions
  }

