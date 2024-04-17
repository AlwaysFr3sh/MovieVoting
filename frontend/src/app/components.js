'use client'
import { useEffect } from "react";
import { socket } from "./socket";

export function SocketioConnection({ children }) {
  useEffect( () => {
    socket.connect();
  }, []);

  return children;
}