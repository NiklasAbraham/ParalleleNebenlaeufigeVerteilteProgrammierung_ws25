module Sleep exposing (main)

import Browser
import Html exposing (Html, div, button, text)
import Html.Attributes exposing (style)
import Html.Events exposing (onClick)
import Process
import Task

type Model = Initial | Waiting | Final

type Event = Clicked | Waited

init : () -> ( Model, Cmd Event )
init _ = ( Initial, Cmd.none )

update : Event -> Model -> ( Model, Cmd Event )
update event model = case event of
    Clicked ->
        ( Waiting, Task.perform (\_ -> Waited) (Process.sleep 2000) )
    Waited ->
        ( Final, Cmd.none )

view : Model -> Html Event
view model = div [ style "text-align" "center", style "margin-top" "100px" ] [
    button [ onClick Clicked ] [ text "Start Delay" ],
    div [] [ text (case model of
        Initial -> "Click the button"
        Waiting -> "Waiting..."
        Final -> "Hello after 2 seconds!"
    ) ]
  ]

main = Browser.element {
    init = init,
    update = update,
    view = view,
    subscriptions = \_ -> Sub.none
  }
