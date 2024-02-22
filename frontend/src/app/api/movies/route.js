import { NextResponse } from 'next/server';

export async function GET(request) {
  const seed = request.nextUrl.searchParams.get("seed");
  
  // get the list of movies from our backend
  //const response = await fetch(`http://127.0.0.1:8000/movies?seed=${seed}`);
  //const data = await response.json();

  // Some dummy data because I can't be fucked hooking up the backend right now
  const data = [
    { title : "Kung Fu Panda", year : "2000"}, 
    { title : "Transformers", year : "2000"}, 
    { title : "Blade Runner", year : "2000",}, 
    { title : "The Batman", year : "2000" }
  ];
  
  // debug 
  console.log(seed);

  return NextResponse.json(data, { status: 200 })
}

/*
  this is how you get body data from request object
  DOESNT work for GET method in next which is weird

  const data = await request.json();
  console.log(data);
  console.log("Hey");
  return NextResponse.json({status: 200})

*/