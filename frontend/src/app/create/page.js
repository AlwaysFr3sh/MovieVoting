'use client'

import Image from "next/image";
import styles from "./styles.module.css";
import Link from 'next/link';
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function Home() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event) {
    // TODO: captcha or something here??
    // TODO: is this function unnecessary could html not just post the form data to the server without all this crap???
    // TODO: Validate data 
    event.preventDefault();
    setIsLoading(true);
    const formData = new FormData(event.currentTarget);

    const response = await fetch("http://127.0.0.1:8000/create_room", {
      method: "POST",
      cache: "no-cache",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();
    const gamepin = data.room_key;
    const username = formData.get("username");
    const sleep = milliseconds => new Promise(resolve => setTimeout(resolve, milliseconds));
    await sleep(5000);
    setIsLoading(false);
    //router.push(`/${ gamePin }?username=${ username }`);
    router.push(`/game?gamepin=${ gamepin }&username=${ username }`)
  } 

  return (
    <>
    <h1>Tom's Movie Decider App</h1> 
    <form onSubmit={ handleSubmit }>
      <input type="text" placeholder="Enter your nickname" name="username"></input>
      <button type="submit" disabled={ isLoading }>
        {isLoading ? "Loading..." : "Submit"}
      </button>
    </form>
    </>
    
  );
}

/*

<input type="submit" value="Create Session" disabled={ isLoading }></input>

On creating rooms

I think i should have the endpoint return some additional token that is needed in order to control the lobby
things like starting the game, and in the future, configuring genre and streaming service preferences, should have to be submitted with a special token
so that randos can't hack it and stuff

*/
