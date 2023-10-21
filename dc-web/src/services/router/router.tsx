import * as React from "react";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import HomeView from "../../views/home_view"
import PrintableCardView from "../../views/printable_card_view"


const router = createBrowserRouter([
    {
        path: "/",
        element: <HomeView />,
    },
    {
        path: "/printable_card/:id_movie",
        element: <PrintableCardView />,
    },
]);


export default function Router() {
    return (
        <RouterProvider router={router} />
    );
}
