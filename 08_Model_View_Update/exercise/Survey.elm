module Survey exposing (main)

import Browser
import Html exposing (Html, div, button, h1, h2, text)
import Html.Attributes exposing (style)
import Html.Events exposing (onClick)

type alias Item = { question : String, answers : List String }

type State = Answering (List Item) | ThankYou

init : State
init = Answering [
    { question = "What is your favorite programming paradigm?",
      answers = [ "Functional", "Object-Oriented", "Procedural", "Logic" ] },
    { question = "How do you handle concurrency?",
      answers = [ "Threads", "Actors", "Channels", "STM" ] },
    { question = "What is your preferred language?",
      answers = [ "Haskell", "Elixir", "Go", "Elm" ] }
  ]

type Event = Answer

update : Event -> State -> State
update event state = Debug.todo "update"

view : State -> Html Event
view state = Debug.todo "view"

viewAnswer : String -> Html Event
viewAnswer answer = Debug.todo "view answer"

main = Browser.sandbox {
    init = init,
    update = update,
    view = view
  }



