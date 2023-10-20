import { useParams } from "react-router-dom";


async function GetMovie(id: string) {
    const url = "http://127.0.0.1:8080/api/movie/";
    const response = await fetch(url + id)
        .then(r => {
            return r
        })
    return response;
}


export default function PrintableCardView() {
    const params = useParams();
    const id_movie: string | undefined = params["id_movie"];
    if (id_movie) {
        console.clear();
        GetMovie(id_movie)
            .then(response => {
                console.log(response);
            })
            .then(res => {
                console.log(res);
            })
    }

    return (
        <>
            <h1>Hello World!</h1>
            <p>This page come from <code>/src/views/printable_card_view.tsx</code></p>
            <p>id_movie= {id_movie}</p>
        </>
    );
}

