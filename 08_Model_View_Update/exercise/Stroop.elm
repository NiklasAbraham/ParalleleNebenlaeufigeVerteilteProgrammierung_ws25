module Stroop exposing (main)

import Browser
import Html exposing (Html, div, button, h1, h2, text)
import Html.Attributes exposing (style)
import Html.Events exposing (onClick)
import Time

type Color = Red | Green | Blue | Yellow

type State = ()

init : State
init = ()

type Event = ()

update : Event -> State -> ( State, Cmd Event )
update event state = Debug.todo "update"

subscriptions : State -> Sub Event
subscriptions state = Debug.todo "subscriptions"

view : State -> Html Event
view state = Debug.todo "view"

colorButton : Color -> Html Event
colorButton color = Debug.todo "button"

colorToString : Color -> String
colorToString color = case color of
    Red -> "RED"
    Green -> "GREEN"
    Blue -> "BLUE"
    Yellow -> "YELLOW"

colorToHex : Color -> String
colorToHex color = case color of
    Red -> "#e74c3c"
    Green -> "#2ecc71"
    Blue -> "#3498db"
    Yellow -> "#f1c40f"

main : Program () State Event
main =
    Browser.element {
        init = \_ -> ( init, Cmd.none ),
        update = updateWithCmd,
        view = view,
        subscriptions = subscriptions
      }

