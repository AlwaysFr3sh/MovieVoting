'use client'
// This whole file is such a mess lol
import { useSearchParams } from "next/navigation";
import { useState, useEffect } from "react"
import { socket } from "../socket"
import { EventFactory } from "./events"
import styles from './styles.module.css'

// TODO: only the lobby creator should see the 'start game' button
export default function Game({ params }) {
  const searchParams = useSearchParams();
  const userName = searchParams.get('username');
  const roomKey = params.sessionid;

  const [isConnected, setIsConnected] = useState(socket.connected);
  const [users, setUsers] = useState([]);
  const [showLobby, setShowLobby] = useState(true);

  const [movies, setMovies] = useState([]);
  const [index, setIndex] = useState(0);
  const [gameOver, setGameOver] = useState(false);
  const [decidedMovie, setDecidedMovie] = useState();

  const [error, setError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const onClick = (vote) => {
    if ( index < movies.length - 1 ) {
      socket.emit("register_vote", { "movie_id" : movies[index].id , "vote" : vote });
      setIndex(index + 1);
    } else {
      // TODO: figure out what to do in this scenario
      console.log("We out of movies bro!!");
    }
  }

  useEffect(() => {
    const events = new EventFactory();
    
    socket.on("connect", events.onConnect(setIsConnected));
    socket.on("disconnect", events.onDisconnect(setIsConnected));
    socket.on("update_lobby", events.onUpdateLobby(setUsers));
    //socket.on("start_game", events.onStartGame(setMovies, setShowLobby));
    socket.on("start_game", events.onStartGame(setMovies, setShowLobby, roomKey, userName))
    socket.on("pick_movie", events.onPickMovie(setGameOver, setDecidedMovie));
    socket.on("error", events.onError(setError, setErrorMessage));

    socket.emit("join_room", {"username": userName, "room_key": roomKey});

    return () => {
      socket.off("connect", events.onConnect(setIsConnected));
      socket.off("disconnect", events.onDisconnect(setIsConnected));
      socket.off("update_lobby", events.onUpdateLobby(setUsers));
      socket.off("start_game", events.onStartGame(setMovies, setShowLobby));
      socket.off("pick_movie", events.onPickMovie(setGameOver, setDecidedMovie));
      socket.off("error", events.onError(setError, setErrorMessage));
    };

  }, []); 

  if (error) {
    // TODO: This always throws because react double executes useEffect in dev mode
    //throw new Error(errorMessage);
    console.log("error");
  }

  if (!isConnected) {
    throw new Error("Failed to connect to server");
  }

  return (
    <>
      {showLobby ?  
        <Lobby users={ users } roomKey={ roomKey }/> : 
        <MovieCard title={ movies[index].title } year={ movies[index].year } gamepin={ roomKey } movieid={ "penis" } onClick={ onClick }/>
      }
      {gameOver ? <GameOver title={decidedMovie} year={"who knows"}/> : null}
    </>
    
  )
}

function Lobby({ users, roomKey }) {
  const onClick = () => socket.emit("start_game");

  return (
    <div className={ styles.lobby }>
      <h1>Session: {roomKey}</h1>
      <ul>
        {users.map((user) => <Participant userName={ user } />)}
      </ul>
      <div className={ styles.bottom }>
        <button onClick={ onClick }>Start Game</button>
      </div>
    </div>
  );
}

function Participant({ userName }) {
  return <li key={ userName }><p>{ userName }</p></li>
}

function MovieCard({ title, year, gamepin, movieid, onClick }) {
  return (
    <div>
      <p>{ title }</p>
      <p>{ year }</p>
      <img src={ `http://localhost:8000/posters/${movieid}?game_pin=${gamepin}` }/>
      <button onClick={ () => onClick(true) }>yes</button>
      <button onClick={ () => onClick(false) }>no</button>
    </div>
  );
}

function GameOver({title, year}) {
  return (
    <div>
      <p>{ title }</p>
      <p>{ year }</p>
    </div>
  );
}

/*
TODO:

CLIENT:
-------------------------------------------------
# Disable input & buttons while loading
-------------------------------------------------
# Figure out what to do when we run out of movies
- Either fetch another batch of movies, 
- End the game or,
- Re implement this page so that we only fetch one 
  movie at a time and just do this forever until there's a match
-------------------------------------------------
# Match condition
The match condition may be configurable in the future but for now 
it should be greater than 50% for groups and 100% for couples?
Something like that
-------------------------------------------------
# Load Images
Sign up for images with omdb and figure it out
-------------------------------------------------
# Only room creator should see "start game button"
-------------------------------------------------
*/
