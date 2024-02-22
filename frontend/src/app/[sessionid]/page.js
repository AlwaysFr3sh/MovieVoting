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

  const onClick = (vote) => {
    //socket.emit("register_vote", { title : { title }, vote : { vote } })
    if ( index < movies.length - 1 ) {
      setIndex(index + 1);
    } else {
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
      console.log(data.members);
    }
    
    function onStartGame(data) {
      // get the movie data and do the game
      //alert(data.seed);
      //const movies = getMovies(data.seed); 
      //fetch(`/api/movies?seed=${data.seed}`).then(response => response.json()).then(json => alert(json[0].title));
      //alert(movies);
      //setMovies(movies);
      //fetch(`/api/movies?seed=${data.seed}`).then(response => response.json()).then(movies => setMovies(movies));//alert(json[0].title));
      fetch(`/api/movies?seed=${data.seed}`)
        .then(response => response.json())
        .then(movies => setMovies(movies))
        .then(() => setShowLobby(false));
        //.then(movies => alert(movies));
      //setShowLobby(false);
    }
    
    socket.on('connect', onConnect);
    socket.on('disconnect', onDisconnect);
    socket.on('update_lobby', onUpdateLobby);
    socket.on("start_game", onStartGame);

    socket.connect();
    socket.emit("join_room", {"username": userName, "room_key": roomKey});

    return () => {
      socket.off('connect', onConnect);
      socket.off('disconnect', onDisconnect);
      socket.off('update_lobby', onUpdateLobby);
      socket.off("start_game", onStartGame);
    };

  }, []); 


  // replace null with game once ready?
  /*return (
    <>
      <h1>Session: {roomKey}</h1> 
      {showLobby ? <Lobby users={ users }/> : null}
    </>
  );*/
  return (
    <>
      <h1>Session: {roomKey}</h1>
      <Lobby users={ users }/>
      <h1>Movies</h1> 
      {showLobby ? null : <MovieCard title={ movies[index].title } year={ movies[index].year } onClick={ onClick }/>}
      <h1>Movies Debug</h1>
      <MoviesDebug movies={ movies }/>
    </>
    
  )
}

function Lobby({ users }) {
  const onClick = () => socket.emit("start_game");

  return (
    <>
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

// Debug list movies get rid of this when everything works
function MoviesDebug({ movies }) {
  return (
    <ul>
      {movies.map((movie) => <MovieCardDebug title={ movie.title } year={ movie.year }/>)}
    </ul>
  );
}

function MovieCardDebug({ title, year }) {
  return (
    <p> Title: { title } Year: { year } </p>
  );
}