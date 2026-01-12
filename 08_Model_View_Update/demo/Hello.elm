module Hello exposing (..)


myTuple : (Int, String)
myTuple = (1, "hi")

myList : List Int
myList = [1, 2, 3]

safeHead : Maybe Int
safeHead = List.head myList

parseNumber : Maybe Int
parseNumber = String.toInt "123"


type OutOfRange = TooSmall | TooLarge

validate : Int -> Result OutOfRange Int
validate n =
    if n < 0
        then Err TooSmall
        else if n > 100
            then Err TooLarge
            else Ok n


type alias Person = { name : String, age : Int }

alice : Person
alice = { name = "Alice", age = 30 }

getName : { r | name : String } -> String
getName person = person.name

birthday : { r | age : Int } -> { r | age : Int }
birthday person = { person | age = person.age + 1 }

