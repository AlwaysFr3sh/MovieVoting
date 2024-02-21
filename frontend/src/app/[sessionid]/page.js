'use client'
import { useSearchParams } from 'next/navigation';
import { useState, useEffect } from 'react'
import { socket } from '../socket'

// TODO: only the lobby creator should see the 'start game' button
export default function Game({params}) {
  const searchParams = useSearchParams();
  const userName = searchParams.get('username');
  const roomKey = params.sessionid;
  const [isConnected, setIsConnected] = useState(socket.connected);
  const [users, setUsers] = useState([]);
  const [movies, setMovies] = useState([]);
  const [showLobby, setShowLobby] = useState(true);
  const [showGame, setShowGame] = useState(false);

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
      setShowLobby(false);
      setShowGame(true);
      // get the movie data and do the game
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


  return (
    <>
      <h1>Session: {roomKey}</h1>
      <Lobby users={users}/>
    </>
  );
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

// TODO: think of good name
function Thingo({ movies, index }) {
  var movie = movies[index];

  return (
    <MovieCard title={ movie.year } year={ movie.year }/>
  );
}

function MovieCard({ title, year }) {
  return (
    <div>
      <p>{ title }</p>
      <p>{ year }</p>
      <button>yes</button>
      <button>no</button>
    </div>
  );
}