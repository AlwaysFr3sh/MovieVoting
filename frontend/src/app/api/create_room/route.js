import { NextResponse } from "next/server";
import { redirect } from "next/navigation";


async function doAThing() {
  const response = await fetch("http://127.0.0.1:8000/create_room", {
    method: "POST",
    cache: "no-cache",
    headers: {
      "Content-Type": "application/json",
    },
  });

  return response.json();
}

export async function GET(request) {

  const data = await doAThing(); 
  console.log(data);

  redirect(`/${data.room_key}?username=${"Tom"}`);
}