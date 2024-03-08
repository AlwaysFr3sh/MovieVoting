import { io } from 'socket.io-client';

const URL = 'http://localhost:8000/test';

export const socket = io(URL, {
  autoConnect: false
});