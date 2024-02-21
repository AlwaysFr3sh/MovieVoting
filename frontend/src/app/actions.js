'use server'

import { redirect } from "next/navigation";

async function getRoomKey() {
  const response = await fetch("http://127.0.0.1:8000/create_room", { 
    method: "POST",
    cache: "no-cache",
    headers: {
      "Content-Type": "application/json",
    },
  });

  return response.json();
}

export async function createRoom( formData ) {
  const data = await getRoomKey();
  const roomKey = data.room_key;
  const userName = formData.get("username");
  redirect(`/${ roomKey }?username=${ userName }`);
}