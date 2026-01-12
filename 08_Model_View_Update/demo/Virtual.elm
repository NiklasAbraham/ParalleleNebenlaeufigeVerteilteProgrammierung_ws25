module Virtual exposing (main)

import Browser
import Html exposing (Html, button, div, li, text, ul)
import Html.Events exposing (onClick)


type alias Model = List String

init : Model
init = []

type Event = AddItem

update : Event -> Model -> Model
update event model = case event of
    AddItem -> List.reverse (model ++ [ "Item " ++ String.fromInt (List.length model + 1) ])


view : Model -> Html Event
view model = div [] [
    button [ onClick AddItem ] [ text "Add" ],
    ul [] (List.map (\item -> li [] [ text item ]) model)
  ]

main = Browser.sandbox { init = init, update = update, view = view }

