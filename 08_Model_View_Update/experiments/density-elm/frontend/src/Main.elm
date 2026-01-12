module Main exposing (main)

import Browser
import Html exposing (Html, button, div, input, text)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput)
import Http
import Json.Decode as D
import Svg exposing (..)
import Svg.Attributes exposing (..)


-- MODEL


type alias Domain =
    { xMin : Float
    , xMax : Float
    , yMin : Float
    , yMax : Float
    }


type alias Contour =
    { level : Float
    , paths : List (List ( Float, Float ))
    }


type alias ApiResponse =
    { domain : Domain
    , points : List ( Float, Float )
    , contours : List Contour
    }


type alias Model =
    { bandwidth : Float
    , levels : Int
    , grid : Int
    , loading : Bool
    , error : Maybe String
    , data : Maybe ApiResponse
    }


init : () -> ( Model, Cmd Msg )
init _ =
    let
        m =
            { bandwidth = 2.0
            , levels = 15
            , grid = 200
            , loading = True
            , error = Nothing
            , data = Nothing
            }
    in
    ( m, fetchContours m )


-- UPDATE


type Msg
    = SetBandwidth String
    | SetLevels String
    | SetGrid String
    | GotContours (Result Http.Error ApiResponse)


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        SetBandwidth s ->
            let
                b =
                    s |> String.toFloat |> Maybe.withDefault model.bandwidth

                m2 =
                    { model | bandwidth = b, loading = True, error = Nothing }
            in
            ( m2, fetchContours m2 )

        SetLevels s ->
            let
                lv =
                    s |> String.toInt |> Maybe.withDefault model.levels

                m2 =
                    { model | levels = clampInt 3 40 lv, loading = True, error = Nothing }
            in
            ( m2, fetchContours m2 )

        SetGrid s ->
            let
                g =
                    s |> String.toInt |> Maybe.withDefault model.grid

                m2 =
                    { model | grid = clampInt 80 400 g, loading = True, error = Nothing }
            in
            ( m2, fetchContours m2 )

        GotContours res ->
            case res of
                Ok payload ->
                    ( { model | loading = False, data = Just payload, error = Nothing }, Cmd.none )

                Err e ->
                    ( { model | loading = False, error = Just (httpErrorToString e) }, Cmd.none )


clampInt : Int -> Int -> Int -> Int
clampInt lo hi v =
    if v < lo then
        lo
    else if v > hi then
        hi
    else
        v


httpErrorToString : Http.Error -> String
httpErrorToString err =
    case err of
        Http.BadUrl u ->
            "Bad URL: " ++ u

        Http.Timeout ->
            "Request timeout"

        Http.NetworkError ->
            "Network error"

        Http.BadStatus n ->
            "Bad status: " ++ String.fromInt n

        Http.BadBody s ->
            "Bad body: " ++ s


-- HTTP


fetchContours : Model -> Cmd Msg
fetchContours model =
    let
        url =
            "/api/contours"
                ++ "?bandwidth=" ++ String.fromFloat model.bandwidth
                ++ "&levels=" ++ String.fromInt model.levels
                ++ "&grid=" ++ String.fromInt model.grid
    in
    Http.get
        { url = url
        , expect = Http.expectJson GotContours apiDecoder
        }


apiDecoder : D.Decoder ApiResponse
apiDecoder =
    D.map3 ApiResponse
        (D.field "domain" domainDecoder)
        (D.field "points" (D.list pointDecoder))
        (D.field "contours" (D.list contourDecoder))


domainDecoder : D.Decoder Domain
domainDecoder =
    D.map4 Domain
        (D.field "xMin" D.float)
        (D.field "xMax" D.float)
        (D.field "yMin" D.float)
        (D.field "yMax" D.float)


pointDecoder : D.Decoder ( Float, Float )
pointDecoder =
    D.map2 Tuple.pair
        (D.index 0 D.float)
        (D.index 1 D.float)


contourDecoder : D.Decoder Contour
contourDecoder =
    D.map2 Contour
        (D.field "level" D.float)
        (D.field "paths" (D.list (D.list pointDecoder)))


-- VIEW


main : Program () Model Msg
main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = \_ -> Sub.none
        , view = view
        }


view : Model -> Html Msg
view model =
    div [ style "font-family" "system-ui, sans-serif", style "padding" "16px" ]
        [ div [ style "max-width" "920px" ]
            [ div [ style "display" "flex", style "gap" "24px", style "align-items" "center", style "flex-wrap" "wrap" ]
                [ controlSliderFloat "Bandwidth" 0.2 8.0 0.1 model.bandwidth SetBandwidth
                , controlSliderInt "Levels" 3 40 model.levels SetLevels
                , controlSliderInt "Grid" 80 400 model.grid SetGrid
                , div [] [ text (if model.loading then "Loading…" else "") ]
                ]
            , div [ style "margin-top" "12px" ] [ viewStatus model ]
            , div [ style "margin-top" "16px" ] [ viewViz model ]
            ]
        ]


viewStatus : Model -> Html msg
viewStatus model =
    case model.error of
        Nothing ->
            text ""

        Just e ->
            div [ style "color" "#b00020" ] [ text e ]


controlSliderFloat :
    String -> Float -> Float -> Float -> Float -> (String -> Msg) -> Html Msg
controlSliderFloat labelTxt lo hi stepVal current toMsg =
    div [ style "min-width" "260px" ]
        [ div [ style "font-size" "12px", style "margin-bottom" "4px" ]
            [ text (labelTxt ++ ": " ++ String.fromFloat current) ]
        , input
            [ type_ "range"
            , min (String.fromFloat lo)
            , max (String.fromFloat hi)
            , step (String.fromFloat stepVal)
            , value (String.fromFloat current)
            , onInput toMsg
            ]
            []
        ]


controlSliderInt :
    String -> Int -> Int -> Int -> (String -> Msg) -> Html Msg
controlSliderInt labelTxt lo hi current toMsg =
    div [ style "min-width" "260px" ]
        [ div [ style "font-size" "12px", style "margin-bottom" "4px" ]
            [ text (labelTxt ++ ": " ++ String.fromInt current) ]
        , input
            [ type_ "range"
            , min (String.fromInt lo)
            , max (String.fromInt hi)
            , step "1"
            , value (String.fromInt current)
            , onInput toMsg
            ]
            []
        ]


viewViz : Model -> Html Msg
viewViz model =
    case model.data of
        Nothing ->
            div [] [ text "No data yet." ]

        Just payload ->
            let
                w = 860
                h = 520
                pad = 30

                sx x =
                    pad
                        + (x - payload.domain.xMin)
                        * (toFloat (w - 2 * pad))
                        / (payload.domain.xMax - payload.domain.xMin)

                sy y =
                    -- SVG y axis downward, so invert
                    pad
                        + (payload.domain.yMax - y)
                        * (toFloat (h - 2 * pad))
                        / (payload.domain.yMax - payload.domain.yMin)
            in
            Svg.svg
                [ width (String.fromInt w)
                , height (String.fromInt h)
                , viewBox ("0 0 " ++ String.fromInt w ++ " " ++ String.fromInt h)
                , style "border: 1px solid #ddd; background: #fff;"
                ]
                (List.concat
                    [ [ rect
                            [ x "0", y "0", width (String.fromInt w), height (String.fromInt h)
                            , fill "white"
                            ]
                            []
                      ]
                    , renderContours sx sy payload.contours
                    , renderPoints sx sy payload.points
                    ]
                )
                |> Html.fromSvg


renderPoints : (Float -> Float) -> (Float -> Float) -> List ( Float, Float ) -> List (Svg msg)
renderPoints sx sy pts =
    List.map
        (\( x0, y0 ) ->
            circle
                [ cx (String.fromFloat (sx x0))
                , cy (String.fromFloat (sy y0))
                , r "2.2"
                , fill "#111"
                , opacity "0.55"
                ]
                []
        )
        pts


renderContours : (Float -> Float) -> (Float -> Float) -> List Contour -> List (Svg msg)
renderContours sx sy contours =
    contours
        |> List.concatMap
            (\c ->
                c.paths
                    |> List.map
                        (\polyline ->
                            path
                                [ d (toPathD sx sy polyline)
                                , fill "none"
                                , stroke "#0b5"
                                , strokeWidth "1.2"
                                , opacity "0.85"
                                ]
                                []
                        )
            )


toPathD : (Float -> Float) -> (Float -> Float) -> List ( Float, Float ) -> String
toPathD sx sy pts =
    case pts of
        [] ->
            ""

        ( x0, y0 ) :: rest ->
            let
                start =
                    "M " ++ f (sx x0) ++ " " ++ f (sy y0)

                segs =
                    rest
                        |> List.map (\( x1, y1 ) -> " L " ++ f (sx x1) ++ " " ++ f (sy y1))
                        |> String.concat
            in
            start ++ segs


f : Float -> String
f x =
    -- compact float formatting
    String.fromFloat x
