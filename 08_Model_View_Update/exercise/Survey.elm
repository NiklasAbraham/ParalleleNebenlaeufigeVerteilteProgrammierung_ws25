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

type Event = Answer String

update : Event -> State -> State
update event state = 
    case state of
        -- if we're still answering questions
        Answering items ->
            case items of
                -- no questions left, so we're done
                [] -> ThankYou
                -- at least one question left
                -- `first` stands for the first element
                -- `rest` stands for the remaining elements
                first :: rest ->
                    -- if that was the last question, move to ThankYou
                    if List.isEmpty rest then
                        ThankYou
                    else
                        -- otherwise, move on to the next question
                        Answering rest
        -- already finished, stay in ThankYou no matter what
        ThankYou -> ThankYou

view : State -> Html Event
view state = 
    case state of
        -- if we're still answering questions, show the current question and answers
        Answering items ->
            case items of
                -- nothing to show, so thank the user
                [] -> 
                    div [ style "padding" "20px" ] [
                        h1 [] [ text "Thank you!" ]
                    ]
                -- show the current question and all answer buttons
                current :: _ ->
                    div [ style "padding" "20px", style "font-family" "sans-serif" ] [
                        h1 [] [ text "Survey" ], -- page title
                        h2 [] [ text current.question ], -- show the current question
                        div [] (List.map viewAnswer current.answers) -- show all possible answers
                    ]
        -- if already finished, show thank you message
        ThankYou ->
            div [ style "padding" "20px", style "font-family" "sans-serif" ] [
                h1 [] [ text "Thank you for completing the survey!" ]
            ]

viewAnswer : String -> Html Event
viewAnswer answer = 
    button [
        onClick (Answer answer),
        style "display" "block",
        style "width" "200px",
        style "padding" "10px",
        style "margin" "5px 0",
        style "font-size" "16px",
        style "cursor" "pointer"
    ] [ text answer ]

main = Browser.sandbox {
    init = init,
    update = update,
    view = view
  }



