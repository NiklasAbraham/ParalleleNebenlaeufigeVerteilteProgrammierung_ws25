port module Chat exposing (main)

import Browser
import Html exposing (Html, div, input, button, ul, li, text)
import Html.Attributes exposing (style, value)
import Html.Events exposing (onClick, onInput)

port sendMessage : String -> Cmd msg

port messageReceiver : (String -> msg) -> Sub msg

type alias State = {
    draft : String,
    messages : List String
  }

init : () -> ( State, Cmd Event )
init _ = ( { draft = "", messages = [] }, Cmd.none )

type Event = Changed String | Send | Recv String

update : Event -> State -> ( State, Cmd Event )
update event state = Debug.todo "update"

subscriptions : State -> Sub Event
subscriptions _ = messageReceiver Recv

view : State -> Html Event
view state = Debug.todo "view"

main : Program () State Event
main = Browser.element {
    init = init,
    update = update,
    view = view,
    subscriptions = subscriptions
  }

