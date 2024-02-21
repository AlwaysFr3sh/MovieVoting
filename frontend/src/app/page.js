'use client'
import Image from "next/image";
import styles from "./page.module.css";
import Link from 'next/link';

import { useState } from 'react';
import { useRouter } from "next/navigation";

import { createRoom } from "./actions.js"

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
  const router = useRouter();
  const [userName, setUserName] = useState("");

  // TODO: is this better or "server action"
  // UPDATE: I am doing server action
  function handleSubmit(event) {
    console.log("validate stuff here bro");
  } 

  // TODO: dont need username hook i dont think, we are just passing it to the action directly from the formdata
  return (
    <>
    <h1>Tom's Movie Decider App</h1> 
    <form onSubmit={ handleSubmit } action={ createRoom }>
      <input type="text" placeholder="Enter your nickname" name="username" onChange={ (e) => setUserName(e.target.value) }></input>
      <input type="submit" value="Create Session"></input>
    </form>
    </>
    
  );
}
