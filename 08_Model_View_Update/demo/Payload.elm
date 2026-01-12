module Payload exposing (main)
import Browser
import Html exposing (Html, div, button, input, text)
import Html.Attributes exposing (style, value)
import Html.Events exposing (onClick, onInput)

type alias Model = { counter : Int, amount : String }

type Event = IncrementCounter | ChangeAmount String

init : Model
init = { counter = 0, amount = "" }

update : Event -> Model -> Model 
update event model = case event of
    IncrementCounter ->
        case String.toInt model.amount of
            Just amount -> { model | counter = model.counter + amount }
            Nothing -> { model | counter = model.counter + 1 }
    ChangeAmount str ->
        { model | amount = str }

view : Model -> Html Event
view model = div [ style "text-align" "center", style "margin-top" "100px" ] [
    input [value model.amount, onInput ChangeAmount] [],
    button [onClick IncrementCounter] [ text "+" ],
    div [] [text (String.fromInt model.counter)]
  ]

main = Browser.sandbox {
    init = init,
    update = update,
    view = view
  }

