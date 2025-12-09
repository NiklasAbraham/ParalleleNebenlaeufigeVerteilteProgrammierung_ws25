{-# LANGUAGE BlockArguments #-}
import Control.Concurrent
import Control.Concurrent.STM
import Control.Monad
-- import System.Exit

data Event = Reindeer | Elves

main :: IO ()
main = do
  waitingReindeer <- newTVarIO []
  waitingElves <- newTVarIO []

  forM_ [1..9] $ \i -> do
    forkIO do

      reindeer <- newEmptyTMVarIO
      forever do
        -- reindeer is on vacation
        putStrLn $ "Reindeer " ++ show i ++ " is on vacation"
        threadDelay 3000000
        -- reindeer returns from vacation
        putStrLn $ "Reindeer " ++ show i ++ " returns from vacation and arrives at Santa's door"
        atomically (modifyTVar waitingReindeer (reindeer :))
        atomically (takeTMVar reindeer)

        putStrLn $ "Reindeer " ++ show i ++ " did its Job for Santa, going back on vacation"

  forM_ [1..10] $ \i -> do
    forkIO do
      elf <- newEmptyTMVarIO
      forever do
        -- elf is working, because elves do not take vaction --> missing labour union!
        -- lesson: elves are not that smart, reindeer are!
        putStrLn $ "Elf " ++ show i ++ " is working"
        threadDelay 700000
        putStrLn $ "Elf " ++ show i ++ " has a problem and arrives at Santa's door"
        atomically (modifyTVar waitingElves (elf :))
        atomically (takeTMVar elf)
        putStrLn $ "Elf " ++ show i ++ " helped by Santa, going back to work"

  forever do
    putStrLn "Santa is sleeping"
    event <- atomically do
      reindeerList <- readTVar waitingReindeer
      elfList <- readTVar waitingElves
      
      if length reindeerList == 9 then do
        writeTVar waitingReindeer []
        mapM_ (`putTMVar` ()) reindeerList
        return Reindeer
      else if length elfList >= 3 then do
        -- let (elvesToHelp, remainingElves) = splitAt 3 elfList
        let reversed = reverse elfList
            elvesToHelp = take 3 reversed
            remainingElves = reverse (drop 3 reversed)
        writeTVar waitingElves remainingElves
        mapM_ (`putTMVar` ()) elvesToHelp
        return Elves
      else retry

    case event of
      Reindeer -> do
        putStrLn "Santa wakes up and helps the reindeer"
        threadDelay 2000000
        putStrLn "Santa finished helping reindeer, going back to sleep"
        -- exitSuccess
      Elves -> do
        putStrLn "Santa wakes up and helps the elves"
        threadDelay 1000000
        putStrLn "Santa finished helping elves, going back to sleep"

