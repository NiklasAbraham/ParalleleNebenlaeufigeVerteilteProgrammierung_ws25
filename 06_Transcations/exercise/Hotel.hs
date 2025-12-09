{-# LANGUAGE DataKinds #-}
{-# LANGUAGE DeriveGeneric #-}
{-# LANGUAGE TypeOperators #-}
{-# LANGUAGE OverloadedStrings #-}
{-# LANGUAGE BlockArguments #-}

module Main where

import GHC.Generics
import Control.Concurrent.STM
import Control.Monad.IO.Class
import Servant
import Data.Aeson
import Network.Wai
import Network.Wai.Handler.Warp

data BookingRequest = BookingRequest
  { days :: [Int]
  } deriving (Generic, Show)

instance FromJSON BookingRequest

data BookingResponse = BookingResponse
  { success :: Bool
  , booked :: [Int]
  } deriving (Generic, Show)

instance ToJSON BookingResponse

type API = "book" :> ReqBody '[JSON] BookingRequest :> Post '[JSON] BookingResponse :<|> Raw

server :: TVar [Int] -> BookingRequest -> Handler BookingResponse
server daysRef request = liftIO do
  atomically do
    booked <- readTVar daysRef
    let requested = days request
    if any (`elem` booked) requested
      then do
        return (BookingResponse False booked)
      else do
        let newBooked = booked ++ requested
        writeTVar daysRef newBooked
        return (BookingResponse True newBooked)

main = do
  daysRef <- newTVarIO []
  run 8080 do
    serve (Proxy :: Proxy API) (server daysRef :<|> serveDirectoryWebApp "static")

