'use client'
// This whole file is such a mess lol
import { useSearchParams } from 'next/navigation';
import { useState, useEffect } from 'react'
import { socket } from '../socket'

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

  const onClick = (vote) => {
    if ( index < movies.length - 1 ) {
      socket.emit("register_vote", { "title" : movies[index].title , "vote" : vote })
      setIndex(index + 1);
    } else {
      // TODO: figure out what to do in this scenario
      console.log("We out of movies bro!!");
    }
  }

  useEffect(() => {
    function onConnect() {
      setIsConnected(true);
      console.log("Connected");
    }

    function onDisconnect() {
      setIsConnected(false);
      console.log("Disconnected");
    }

    function onUpdateLobby(data) {
      setUsers(data.members);
    }
    
    function onStartGame(data) {
      fetch(`/api/movies?seed=${data.seed}`)
        .then(response => response.json())
        .then(movies => setMovies(movies))
        .then(() => setShowLobby(false));
    }

    function onStartGame2(data) {
      setMovies(data.movies);
      setShowLobby(false);
    }

    function onPickMovie(data) {
      setGameOver(true); // this var might be not very useful
      setDecidedMovie(data.title);
    }
    
    socket.on('connect', onConnect);
    socket.on('disconnect', onDisconnect);
    socket.on('update_lobby', onUpdateLobby);
    socket.on("start_game", onStartGame);
    socket.on("start_game2", onStartGame2);
    socket.on("pick_movie", onPickMovie);

    socket.connect();
    socket.emit("join_room", {"username": userName, "room_key": roomKey});

    return () => {
      socket.off('connect', onConnect);
      socket.off('disconnect', onDisconnect);
      socket.off('update_lobby', onUpdateLobby);
      socket.off("start_game", onStartGame);
      socket.off("start_game2", onStartGame2);
      socket.off("pick_movie", onPickMovie);
    };

  }, []); 

  return (
    <>
      {showLobby ?  
        <Lobby users={ users } roomKey={ roomKey }/> : 
        <MovieCard title={ movies[index].title } year={ movies[index].year } onClick={ onClick }/>
      }
      {gameOver ? <GameOver title={decidedMovie} year={"who knows"}/> : null}
    </>
    
  )
}

function Lobby({ users, roomKey }) {
  const onClick = () => socket.emit("start_game");

  return (
    <>
      <h1>Session: {roomKey}</h1>
      <ul>
        {users.map((user) => <Participant userName={ user } />)}
      </ul>
      <button onClick={ onClick }>Start Game</button>
    </>
  );
}

function Participant({ userName }) {
  return <li key={ userName }> { userName } </li>
}

function MovieCard({ title, year, onClick }) {
  return (
    <div>
      <p>{ title }</p>
      <p>{ year }</p>
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
# Server side create room page
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