"use server"
import {redirect} from 'next/navigation'

export async function joinRoom( formData ) {
  const roomKey = formData.get("room");
  const userName = formData.get("username");
  redirect(`/${ roomKey }?username=${ userName }`);
}