'use client'
import { joinRoom } from "./actions.js";

export default function Join() {
  function handleSubmit(event) {
    console.log("validate stuff here bro");
  }
  return (
    <>
    <form onSubmit={ handleSubmit } action={ joinRoom }>
      <input type="text" placeholder="Enter your game pin" name="room"></input>
      <input type="text" placeholder="Enter your nickname" name="username"></input>
      <input type="submit" value="Join"></input>
    </form>
    </>
  );
}