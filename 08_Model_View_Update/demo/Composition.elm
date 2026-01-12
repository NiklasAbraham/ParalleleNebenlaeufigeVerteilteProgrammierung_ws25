module Composition exposing (main)

import Browser
import Html exposing (Html, div)
import Html.Attributes exposing (style)
import Ticker
import Fetch

type alias Model = { ticker : Ticker.Model, fetch : Fetch.Model }

type Event = ForTicker Ticker.Event | ForFetch Fetch.Event

init : () -> ( Model, Cmd Event )
init _ = ( { ticker = Tuple.first (Ticker.init ()), fetch = Tuple.first (Fetch.init ()) }, Cmd.none )

update : Event -> Model -> ( Model, Cmd Event )
update event model =
    case event of
        ForTicker tickerMsg -> (
            { model | ticker = Tuple.first (Ticker.update tickerMsg model.ticker) },
            Cmd.map ForTicker (Tuple.second (Ticker.update tickerMsg model.ticker)))
        ForFetch fetchMsg -> (
            { model | fetch = Tuple.first (Fetch.update fetchMsg model.fetch) },
            Cmd.map ForFetch (Tuple.second (Fetch.update fetchMsg model.fetch)))

view : Model -> Html Event
view model = div [] [
    Html.map ForTicker (Ticker.view model.ticker),
    Html.map ForFetch (Fetch.view model.fetch)
  ]

subscriptions : Model -> Sub Event
subscriptions model = Sub.map ForTicker (Ticker.subscriptions model.ticker)

main = Browser.element {
    init = init,
    update = update,
    view = view,
    subscriptions = subscriptions
  }

