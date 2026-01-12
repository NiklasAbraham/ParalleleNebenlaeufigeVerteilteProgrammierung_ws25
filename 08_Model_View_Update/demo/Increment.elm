module Increment exposing (main)

import Browser
import Html exposing (Html, div, button, text)
import Html.Attributes exposing (style)
import Html.Events exposing (onClick)

type alias Model = Int

type Event = Increment | Decrement

init : Model
init = 0

update : Event -> Model -> Model
update event model = case event of
    Increment -> model + 1
    Decrement -> model - 1

view : Model -> Html Event
view model = div [ style "text-align" "center", style "margin-top" "100px" ] [
    button [ onClick Increment ] [ text "+" ],
    button [ onClick Decrement ] [ text "-" ],
    div [] [ text (String.fromInt model) ]
  ]

main = Browser.sandbox {
    init = init,
    update = update,
    view = view
  }

