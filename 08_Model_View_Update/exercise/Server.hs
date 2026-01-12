{-# LANGUAGE BlockArguments #-}
{-# LANGUAGE OverloadedStrings #-}
{-# LANGUAGE TypeApplications #-}

module Main where
import Control.Concurrent (MVar, newMVar, modifyMVar_, readMVar)
import Control.Exception (try, SomeException (SomeException))
import Control.Monad (forM_, forever)
import qualified Data.Text as T
import qualified Network.WebSockets as WS

type Client = WS.Connection

application :: MVar [Client] -> WS.ServerApp
application state pending = do
    connection <- WS.acceptRequest pending
    WS.withPingThread connection 30 (return ()) do
        modifyMVar_ state (\clients -> return (connection : clients))
        talk connection state

talk :: WS.Connection -> MVar [Client] -> IO ()
talk connection state = forever do
    message <- WS.receiveData @T.Text connection
    clients <- readMVar state
    forM_ clients (\client ->
        try @SomeException (WS.sendTextData client message))

main :: IO ()
main = do
    state <- newMVar []
    WS.runServer "127.0.0.1" 8080 (application state)

