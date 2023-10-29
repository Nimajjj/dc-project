import { useEffect, useState } from 'react';
import { useParams } from "react-router-dom";
import "../styles/print.css"

const undefined_img: string = "https://media.istockphoto.com/vectors/no-image-available-sign-vector-id1138179183?k=6&m=1138179183&s=612x612&w=0&h=prMYPP9mLRNpTp3XIykjeJJ8oCZRhb2iez6vKs8a8eE="

interface Movie {
    id_movie: number,
    imdb_id: string,
    visa: string, 
    minimum_age: string,
    awards: string,
    title: string,
    original_title: string,
    duration: string, 
    overview: string,
    thumbnail: string,
    release_date: string,
    language: string,
    distributor: string,
    actors: string,
    directors: string,
    writers: string,
    countries: string,
    genres: string,
}


function arrayToFString(arr: any[], separator: string = ", ") : string {
    let fString = "";

    arr.forEach((e: string, i: number) => {
        if (i !== 0) fString += separator;
        fString += e;
    });
    
    return fString;
}

function formatDate(dateString: string) {
    const date = new Date(dateString);

    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0'); 
    const year = date.getFullYear().toString();

    return `${day}-${month}-${year}`;
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
        const url = `http://127.0.0.1:8080/api/movie/${id}/details`;
        const response = await fetch(url, {mode: "cors"})
        const data = await response.json()
            .catch(error => console.log(error));
        
        if (!data.movie) {
            return null;
        }

        let poster = data.movie.poster;
        if (poster[0] === "/") {
            poster = "https://image.tmdb.org/t/p/original" + poster;
        }

        const durationHour = Math.floor(data.movie.duration_min / 60);
        const durationMinutes = data.movie.duration_min % 60;
        const fDuration: string = `${durationHour}h${durationMinutes}`;

        cachedMovie = {
            id_movie: Number(id),
            imdb_id: data.movie.imdb_id,
            visa: data.movie.visa_number,
            minimum_age: data.movie.minimum_age,
            awards: data.movie.awards,
            distributor: data.movie.distributor_name,
            title: data.movie.title,
            original_title: data.movie.original_title,
            duration: fDuration,
            overview: data.movie.overview,
            thumbnail: poster, 
            release_date: formatDate(data.movie.release_date),
            language: data.movie.original_language,
            actors: arrayToFString(data.movie.actors, " - "),
            directors:  arrayToFString(data.movie.directors),
            countries:  arrayToFString(data.movie.countries),
            writers:  arrayToFString(data.movie.writers),
            genres: arrayToFString(data.movie.genres, " - "),
        };
    }

    return cachedMovie;
}

function PrintButton() {
    function printPage() {
        const bt: Element|null  = document.querySelector("#printButton");
        if (!bt) return;

        bt.classList.add("noPrint");
        window.print();
        bt.classList.remove("noPrint");
    }

    return (
        <>
            <button id="printButton" onClick={printPage}>Print</button>
        </>
    )
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
            console.log(m);
            setMovie(m);
            setLoading(false);
        })
    }, [id_movie]);


    // Conditionals
    if (!id_movie) return <p>No movie id has been provided...</p>;

    if (loading) return <p>Loading ...</p>;

    if (!movie) return <p>Movie {id_movie} not found...</p>;

    console.log(movie.release_date)

    // Render movie details
    console.log(movie);
    return (
        <section>
            <div id="header">
                <PrintButton/>
                <h1 id="title" >{movie.title}</h1>
                <p id="duration">(durée: {movie.duration})</p>
            </div>

            <div id="details">
                <img id="thumbnail" src={movie.thumbnail ? movie.thumbnail : undefined_img} alt="movie thumbnail"/>
                <table>
                    <tr>
                        <td>Date de sortie</td>
                        <td>{movie.release_date}</td>
                    </tr>
                    <tr>
                        <td>Realisateur</td>
                        <td>{movie.directors}</td>
                    </tr>
                    <tr>
                        <td>Origine</td>
                        <td>{movie.countries}</td>
                    </tr>
                    <tr>
                        <td>Acteurs</td>
                        <td>{movie.actors}</td>
                    </tr>
                    <tr>
                        <td>Genres</td>
                        <td>{movie.genres}</td>
                    </tr>
                    <tr>
                        <td>Distributeur</td>
                        <td>{movie.distributor}</td>
                    </tr>
                    <tr>
                        <td>Visa</td>
                        <td>{movie.visa}</td>
                    </tr>
                </table>
            </div>

            <h3>Synopsis</h3>
            <p>{movie.overview}</p>
        </section>
    );
}


