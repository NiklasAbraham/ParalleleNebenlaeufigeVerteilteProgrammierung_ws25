# Exercise 08: Model View Update

## Survey Form

Create a simple survey application. The survey should present an item, which is
a question and a list of answers. When the user clicks any answer, it advances
to the next item. When there are no more items we thank the user.

Model the types of the state and the events appropriately.

Use file `Survey.elm` as a starting point.

Optional Challenge: add a button to go back.

## Stroop Effect

Implement the classic "click the colour not the word" game. Firstly, perform an
online search to find some version and play it. Use your own choice of colors
and features, but it should be possible to play at least one round against a
timer.

Use file `Stroop.elm` as a starting point.

## Cryptocurrency Ticker

Build a ticker that fetches the current Bitcoin price from the Coinbase API
every few seconds and displays it along with a graph of recent prices. Use the
Coinbase API endpoint: https://api.coinbase.com/v2/prices/BTC-USD/spot

Use file `Ticker.elm` as a starting point.

Optional Challenge: Add an input field to allow users to switch between
different cryptocurrencies (BTC, ETH, ADA, etc.).

## Chat Client

Finally, make a chat client that connects to a WebSocket server and allows users
to send and receive messages. The client should display all messages in a list,
with outgoing messages shown normally and incoming messages prefixed with "> ".

We yse ports to communicate with the WebSocket connection, which is already
handled by file `index.html`. The chat server in `Server.hs` broadcasts all
messages to all connected clients.

Start the server with:

```
runghc Server.hs
```

Build the client with:

```
elm make Chat.elm --output=chat.js
```

Then open `index.html` in your browser.

```
firefox ./index.html
```

Use file `Chat.elm` as a starting point.

