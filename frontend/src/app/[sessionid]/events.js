export class EventFactory {

  onConnect(setIsConnected) {
    return function() {
      console.log("connected");
      setIsConnected(true);
    }
  }

  onDisconnect(setIsConnected) {
    return function() {
      console.log("disconnected");
      setIsConnected(false);
    }
  }

  onUpdateLobby(setUsers) {
    return function(data) {
      setUsers(data.members);
      console.log(data.members);
    }
  }

  /*onStartGame(setMovies, setShowLobby) {
    return function(data) {
      fetch(`/api/movies?seed=${data.seed}`)
        .then(response => response.json())
        .then(movies => setMovies(movies))
        .then(() => setShowLobby(false));
    } 
  }*/

  // TODO: this one needs some work
  onStartGame(setMovies, setShowLobby, gamepin, username) {
    return function() {
      fetch(`/api/movies/${gamepin}?username=${username}`)
        .then(response => response.json())
        .then(movies => setMovies(movies))
        .then(() => setShowLobby(false));
    }
  }

  onPickMovie(setGameOver, setDecidedMovie) {
    return function(data) {
      setGameOver(true);
      setDecidedMovie(data.title);
    }
  }

  onError(setError, setErrorMessage) {
    return function(error) {
      setErrorMessage(error.message);
      setError(true);
    }
  }
}