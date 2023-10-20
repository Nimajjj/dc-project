import { useEffect, useState } from 'react';
import { useParams } from "react-router-dom";

const undefined_img: string = "https://media.istockphoto.com/vectors/no-image-available-sign-vector-id1138179183?k=6&m=1138179183&s=612x612&w=0&h=prMYPP9mLRNpTp3XIykjeJJ8oCZRhb2iez6vKs8a8eE="

interface Movie {
    id_movie: number,
    imdb_id: string,
    visa: string, 
    minimum_age: string,
    awards: string,
    distributor: string,
    title: string,
    original_title: string,
    duration: string, 
    overview: string,
    thumbnail: string,
    release_date: string,
    language: string,
}


// todo(nmj): move this function to API dedicated service
let cachedMovie: Movie|null;
async function GetMovie(id: string|undefined): Promise<Movie|null> {
    if (!id) {
        return null;
    }
    if (cachedMovie) {
        if (cachedMovie.id_movie !== Number(id)) {
            cachedMovie = null;
        }
    }
    
    if (!cachedMovie) {
        const url = "http://127.0.0.1:8080/api/movie/";
        const response = await fetch(url + id, {mode: "cors"})
        const data = await response.json();
        
        if (!data.movie) {
            return null;
        }

        console.log(data);

        cachedMovie = {
            id_movie: Number(id),
            imdb_id: data.movie.imdb_id,
            visa: data.movie.visa_number,
            minimum_age: data.movie.minimum_age,
            awards: data.movie.awards,
            distributor: data.movie.id_distributor,
            title: data.movie.title,
            original_title: data.movie.original_title,
            duration: data.movie.duration_min,
            overview: data.movie.overview,
            thumbnail: data.movie.thumnail,
            release_date: data.movie.release_date,
            language: data.movie.original_language
        };
    }

    return cachedMovie;
}


export default function PrintableCardView() {
    console.clear();

    // Get movie id from params
    const id_movie: string|undefined = useParams()["id_movie"];

    // State
    const [loading, setLoading] = useState(true); 
    const [movie, setMovie] = useState<Movie|null>(null);

    // Fetch movie
    useEffect(() => {
        GetMovie(id_movie).then(m => {
            setMovie(m);
            setLoading(false);
        })
    }, [id_movie]);


    // Conditionals
    if (!id_movie) return <p>No movie id has been provided...</p>;

    if (loading) return <p>Loading ...</p>;

    if (!movie) return <p>Movie {id_movie} not found...</p>;

    // Render movie details
    console.log(movie);
    return (
        <>
            <p>{movie.id_movie}</p>

            <div id="title-container">
                <img id="thumbnail" src={movie.thumbnail ? movie.thumbnail : undefined_img} />
                <h1 id="title" >{movie.title}</h1>
            </div>

            <p>Durée: {movie.duration}</p>
            <p>Synopsis: {movie.overview}</p>
            <p>Visa: {movie.visa}</p>
        </>
    );
}


