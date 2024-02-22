'use client'
import Image from "next/image";
import styles from "./page.module.css";
import Link from 'next/link';

import { createRoom } from "./actions.js"

// TODO: no reason this shouldn't be a server side thingy
/*
on form submission we need to make a server call to create a session,
we then need to take this session id and route to the lobby page
(url : '/{session id})

the lobby page should establish a websocket connection to the server to
display the usernames of those who have joined the server
*/

// https://www.reddit.com/r/nextjs/comments/17gsis3/when_would_i_use_redirect_vs_routerpush_in_next_13/
// https://www.reddit.com/r/learnjavascript/comments/zhxkpc/event_deprecated/
// https://nextjs.org/docs/pages/building-your-application/data-fetching/forms-and-mutations
// https://socket.io/how-to/use-with-react

export default function Home() {

  function handleSubmit(event) {
    console.log("validate stuff here bro");
  } 

  return (
    <>
    <h1>Tom's Movie Decider App</h1> 
    <form onSubmit={ handleSubmit } action={ createRoom }>
      <input type="text" placeholder="Enter your nickname" name="username"></input>
      <input type="submit" value="Create Session"></input>
    </form>
    </>
    
  );
}

/*

On creating rooms

I think i should have the endpoint return some additional token that is needed in order to control the lobby
things like starting the game, and in the future, configuring genre and streaming service preferences, should have to be submitted with a special token
so that randos can't hack it and stuff

*/