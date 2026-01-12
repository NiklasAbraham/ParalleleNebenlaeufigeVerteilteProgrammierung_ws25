module Stroop exposing (main)

import Browser
import Html exposing (Html, div, button, h1, h2, text)
import Html.Attributes exposing (style)
import Html.Events exposing (onClick)
import Time
import Random

type Color = Red | Green | Blue | Yellow

type alias State = {
    word : Color,
    color : Color,
    score : Int,
    timeLeft : Float,
    gameStatus : GameStatus
  }

type GameStatus = Playing | GameOver

init : State
init = {
    word = Red,
    color = Red,
    score = 0,
    timeLeft = 30.0,
    gameStatus = Playing
  }

type Event = ColorClicked Color | Tick Time.Posix | NewWord Color Color

update : Event -> State -> ( State, Cmd Event )
update event state = 
    case event of
        ColorClicked clickedColor ->
            if state.gameStatus == Playing then
                if clickedColor == state.color then
                    ( { state | score = state.score + 1 }, Random.generate (\pair -> NewWord (Tuple.first pair) (Tuple.second pair)) (Random.pair randomColor randomColor) )
                else
                    ( { state | gameStatus = GameOver }, Cmd.none )
            else
                ( state, Cmd.none )
        Tick _ ->
            if state.gameStatus == Playing then
                let
                    newTime = state.timeLeft - 0.1
                in
                    if newTime <= 0 then
                        ( { state | timeLeft = 0, gameStatus = GameOver }, Cmd.none )
                    else
                        ( { state | timeLeft = newTime }, Cmd.none )
            else
                ( state, Cmd.none )
        NewWord newWord newColor ->
            ( { state | word = newWord, color = newColor }, Cmd.none )

randomColor : Random.Generator Color
randomColor = Random.uniform Red [ Green, Blue, Yellow ] -- fucked up syntax, but it works

subscriptions : State -> Sub Event
subscriptions state = 
    if state.gameStatus == Playing then
        Time.every 100 Tick
    else
        Sub.none

view : State -> Html Event
view state = 
    div [ style "padding" "20px", style "font-family" "sans-serif", style "text-align" "center" ] [
        h1 [] [ text "Stroop Effect Game" ],
        div [ style "font-size" "24px", style "margin" "20px 0" ] [
            text ("Score: " ++ String.fromInt state.score)
        ],
        div [ style "font-size" "18px", style "margin" "10px 0" ] [
            text ("Time: " ++ String.fromFloat (toFloat (round (state.timeLeft * 10)) / 10) ++ "s")
        ],
        if state.gameStatus == Playing then
            div [] [
                div [
                    style "font-size" "72px",
                    style "font-weight" "bold",
                    style "margin" "40px 0",
                    style "color" (colorToHex state.color)
                ] [
                    text (colorToString state.word)
                ],
                div [ style "margin" "40px 0" ] [
                    text "Click the COLOR of the word (not the word itself):"
                ],
                div [] [
                    colorButton Red,
                    colorButton Green,
                    colorButton Blue,
                    colorButton Yellow
                ]
            ]
        else
            div [] [
                h2 [] [ text "Game Over!" ],
                div [ style "font-size" "24px", style "margin" "20px 0" ] [
                    text ("Final Score: " ++ String.fromInt state.score)
                ],
                button [
                    onClick (ColorClicked Red),
                    style "padding" "10px 20px",
                    style "font-size" "16px",
                    style "margin-top" "20px",
                    style "cursor" "pointer"
                ] [ text "Play Again" ]
            ]
    ]

colorButton : Color -> Html Event
colorButton color = 
    button [
        onClick (ColorClicked color),
        style "background-color" (colorToHex color),
        style "color" "white",
        style "border" "none",
        style "padding" "15px 30px",
        style "margin" "10px",
        style "font-size" "18px",
        style "font-weight" "bold",
        style "cursor" "pointer",
        style "border-radius" "5px"
    ] [ text (colorToString color) ]

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
        init = \_ -> ( init, Random.generate (\pair -> NewWord (Tuple.first pair) (Tuple.second pair)) (Random.pair randomColor randomColor) ),
        update = update,
        view = view,
        subscriptions = subscriptions
      }

